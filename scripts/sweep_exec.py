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
to the tallies. `--resume` does NOT retry it (see scripts/sweep_resume.py), and the same goes for a
failure the model itself caused (see `classify_failure` below).

Caveat worth knowing: killing the episode kills the CLIENT. Ollama cancels generation when the
HTTP connection drops, so the GPU is released, but if you ever see the next run queue behind a
still-busy server, `ollama stop <model>` clears it.
"""

import re
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


# ---------------------------------------------------------------------------------------------
# Why a run failed, and whether that failure is a RESULT or missing data
# ---------------------------------------------------------------------------------------------
#
# A non-zero return code used to mean one thing to --resume: "transient, retry it". That holds for
# the failures a shared machine produces (the endpoint dropped, another user took the VRAM), and it
# is wrong for failures the MODEL produces. Measured on the second open ladder (c4ai, 24-25/09/2026,
# 0 tracebacks in the other 8 models on the same box and stack):
#
#   - `ministral-3:14b` called tools that do not exist (`recommender_agent`, `recommendations_func`,
#     `ticketing_func`; the environment only has weather_func, send_email, get_messages,
#     book_ticket and get_tickets), and Ollama rejects the call with HTTP 500;
#   - `gpt-oss:20b` wrote plain prose where a tool call was due
#     (`error parsing tool call: raw='I think we should first ask TICKETING AGENT.'`), or answered a
#     tool result with no text at all (`Reflect on tool use produced no valid text response`).
#
# Either way autogen 0.5.6 kills the whole episode. The model triggers it and the stack amplifies it
# (a more tolerant stack would hand the error back to the model and carry on), but the stack is the
# same for every open candidate, so the failure is comparable across them. Retrying it until it
# happens to succeed is the same selection bias as retrying a timeout: the surviving episodes are
# exactly the ones that behaved. So it is classified, and treated like a timeout.

OUTCOME_OK = "ok"
OUTCOME_TIMEOUT = "timeout"
OUTCOME_MODEL_TOOL_CALL = "model_tool_call"
OUTCOME_SKIPPED_CASE = "skipped_case"
OUTCOME_INFRASTRUCTURE = "infrastructure"
OUTCOME_UNKNOWN = "unknown"

# Outcomes that ARE the measurement of the candidate: not retried, and the first one wins.
TERMINAL_OUTCOMES = frozenset({OUTCOME_OK, OUTCOME_TIMEOUT, OUTCOME_MODEL_TOOL_CALL})

# Text the model itself put on the wire, rejected by the server or the agent loop.
MODEL_TOOL_CALL_MARKERS = (
    re.compile(r"error parsing tool call"),
    re.compile(r"tool '[^']*' not found"),
    re.compile(r"Reflect on tool use produced no valid text response"),
)

# The machine or the endpoint, not the model. Checked first: when the server is unreachable the
# model never got to produce anything, whatever else the traceback says.
INFRASTRUCTURE_MARKERS = (
    re.compile(r"Connection refused|ConnectError|ConnectTimeout|RemoteProtocolError|Server disconnected"),
    re.compile(r"APIConnectionError|RateLimitError|ServiceUnavailable|status code: 50[23]"),
    re.compile(r"out of memory|CUDA error|requires more system memory|model runner has unexpectedly stopped", re.I),
    re.compile(r"No space left on device"),
)

EXCEPTION_LINE = re.compile(r"^[A-Za-z_][\w.]*(Error|Exception)\b.*$", re.M)


def classify_failure(returncode, stdout, timed_out):
    """Return `(outcome, detail)` for one episode, from what the runner captured.

    `detail` is the last exception line (truncated), so a manifest line says WHY without having to
    keep the per-model log, which the batch wrappers overwrite on every invocation.
    """
    if timed_out:
        return OUTCOME_TIMEOUT, None
    if returncode == 0:
        return OUTCOME_OK, None
    if returncode == 2:
        return OUTCOME_SKIPPED_CASE, None

    text = stdout or ""
    exceptions = [m.group(0) for m in EXCEPTION_LINE.finditer(text)]

    def detail(markers):
        # The root cause, not autogen's wrapper (`Unhandled message in agent container`), which is
        # what the LAST exception line usually is.
        hits = [line for line in exceptions if any(p.search(line) for p in markers)]
        chosen = hits or exceptions
        return chosen[-1][:300] if chosen else None

    if any(p.search(text) for p in INFRASTRUCTURE_MARKERS):
        return OUTCOME_INFRASTRUCTURE, detail(INFRASTRUCTURE_MARKERS)
    if any(p.search(text) for p in MODEL_TOOL_CALL_MARKERS):
        return OUTCOME_MODEL_TOOL_CALL, detail(MODEL_TOOL_CALL_MARKERS)
    return OUTCOME_UNKNOWN, detail(())
