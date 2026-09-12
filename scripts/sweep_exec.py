"""Bounded execution of one episode, shared by the sweep runners.

Why this exists
---------------
A screening sweep is 72 runs per model, and on the open ladder that is 15 to 22 hours of wall
clock. Calling `subprocess.run` with no timeout means a single episode that never finishes stalls
the entire sweep FOREVER, and silently: the runner sits inside the call, the manifest stops
growing, and nothing in the log says why.

This is not hypothetical. Measured on the lab box (c4ai, 11/09/2026): `qwen3:14b` on
`travel_planning` case 0 ran for 1h48 with GPU 0 pinned at 98% while the saved trajectory was still
on its FIRST agent turn. Ollama does not bound generation length -- when the context window fills
it shifts context and keeps going -- so a model that falls into a loop generates without end.

Why a timeout is the right experimental call
--------------------------------------------
Counting a runaway episode as a FAILED run is not a workaround, it is the correct treatment: a
candidate that cannot finish an episode inside a generous bound has failed the competence floor
that block L exists to measure. Failing to finish is a result, not missing data.

What is deliberately NOT done here is capping `num_predict` or turning off the Qwen3 thinking mode.
Either would bound the runtime too, but both change how the model generates, and therefore change
what is being measured -- breaking comparability with the other candidates and with the runs
already on record.

A timed-out run is recorded like any other failure: non-zero return code and no output path. Every
analyzer keeps only records with `return_code == 0` AND an `output_path`, so it contributes nothing
to the tallies, and `--resume` retries it on the next pass.

Caveat worth knowing: killing the episode kills the CLIENT. Ollama cancels generation when the
HTTP connection drops, so the GPU is released, but if you ever see the next run queue behind a
still-busy server, `ollama stop <model>` clears it.
"""

import subprocess

# Generous by design. The slowest episode measured on the open ladder is the 70B on
# multi_agent_debate at 16m46s, so 20 minutes bounds a runaway episode while still leaving room for
# a legitimately slow one. Raise it with --run-timeout on a slower machine or a larger model.
DEFAULT_RUN_TIMEOUT_SECONDS = 1200

# Same convention as timeout(1), so a timed-out run is recognisable when grepping a manifest.
TIMEOUT_RETURN_CODE = 124


def run_episode(cmd, cwd, timeout_seconds=DEFAULT_RUN_TIMEOUT_SECONDS):
    """Run one episode under a wall-clock bound.

    Returns `(returncode, stdout, timed_out)`. On timeout the output captured so far is kept and a
    marker line is appended, because where the episode got stuck is the diagnostic that matters.
    Pass `timeout_seconds=0` (or None) to disable the bound.
    """
    limit = timeout_seconds if timeout_seconds and timeout_seconds > 0 else None
    try:
        completed = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=limit,
        )
        return completed.returncode, completed.stdout, False
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout or ""
        if isinstance(partial, bytes):
            partial = partial.decode("utf-8", errors="replace")
        partial += (
            f"\n\nRUN TIMED OUT after {limit}s and was killed. Counted as a failed run "
            f"(return code {TIMEOUT_RETURN_CODE}); see scripts/sweep_exec.py for why.\n"
        )
        return TIMEOUT_RETURN_CODE, partial, True
