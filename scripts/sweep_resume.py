"""Run-level resume for the sweep runners, so a long sweep survives being interrupted.

Why this exists
---------------
The screening and the definitive experiments run for many hours on a SHARED GPU machine. The
machine has to be handed back to other users mid-sweep, and it can also just lose power. Without
per-run bookkeeping, every interruption throws away the whole block that was in flight -- up to 40
episodes of block L, which on the 70B is several hours of GPU time.

The manifest already records every run that was attempted, with its return code and the result file
it produced. That is enough to resume: on a re-run, read the manifest, and skip the runs that
already finished successfully.

What counts as "already done"
-----------------------------
`return_code == 0` AND an `output_path` that still exists on disk, **or** a run that was killed by
`--run-timeout`. Both halves of the first case matter:

  - a run that failed is RETRIED, because on a shared machine the common failure is transient
    (another user took the VRAM, the endpoint blipped). Retrying appends a second manifest line for
    that run, which is harmless: every analyzer keeps only records with return_code 0 AND an
    output_path, so the failed line contributes nothing and cannot double-count.
  - the file has to still be there, so that deleting results/ (or copying only part of it between
    machines) makes the sweep re-run the missing episodes instead of silently reporting a gap.

A timed-out run is the exception, and the reason is experimental, not technical
-------------------------------------------------------------------------------
A run killed by `--run-timeout` is counted as DONE and is NOT retried. A transient failure is
missing data and deserves another attempt; a runaway generation is a RESULT -- the candidate did
not finish the episode inside a generous bound, which is precisely the competence failure block L
exists to detect. Retrying it until it happens to succeed, and keeping only the success, is
selection bias: it makes an unreliable candidate look reliable, and it does so silently, because
the surviving episodes are exactly the ones that behaved.

`--retry-timeouts` restores the old behaviour, and should be used only when there is a concrete
reason to believe the timeout was environmental (the box was swapping, another user took the GPU)
rather than the model looping. `analyze_screening_protocol.py` reports `runs_crashed/runs_planned`
per model, so a timed-out run stays visible in the final table either way.

A failure the model caused is the same kind of result
-----------------------------------------------------
Since 25/09/2026 the runners classify every failure (`failure_kind` in the manifest, see
`classify_failure` in scripts/sweep_exec.py). A `model_tool_call` failure -- the model called a tool
that does not exist, or wrote prose where a tool call was due, and the stack killed the episode -- is
treated like a timeout: counted as DONE and not retried, for the same selection-bias reason.
`--retry-model-failures` is the escape hatch. Only `infrastructure` failures, and legacy records
that were never classified, are retried.

Manifests written before the classification existed have no `failure_kind`. For those,
scripts/classify_failures.py rebuilds it from the per-model log and writes a sidecar,
`failure_kinds.jsonl`, next to the manifests (a sidecar and not an in-place edit, so that an rsync
from the lab box never overwrites it). `record_outcome` reads either source.

The first attempt is the measurement
------------------------------------
Because a failed run used to be retried, one run can have several manifest lines. `measured_attempts`
picks, per run, the FIRST attempt that is a result of the candidate (ok, timeout, model failure),
skipping only the ones that are missing data (infrastructure, result file gone). A later success
after a model failure is a survivor and is discarded, and the analyzers report how many they
discarded.

The identity of a run
---------------------
`run_label` alone is NOT unique. In block B2 the label is built from method, condition and repeat
only, so `robust_B2_base_r001` is generated for BOTH case 0 and case 3 -- resuming on the label
alone would skip half of block B2 while believing it complete. The key below therefore includes the
case id, the environment, the model and the defense flag, all of which both runners already write
into every manifest record.
"""

import json
from pathlib import Path

from sweep_exec import (
    OUTCOME_MODEL_TOOL_CALL,
    OUTCOME_OK,
    OUTCOME_SKIPPED_CASE,
    OUTCOME_TIMEOUT,
    OUTCOME_UNKNOWN,
    TERMINAL_OUTCOMES,
)

ROOT = Path(__file__).resolve().parents[1]

# Backfilled failure classification for manifests older than `failure_kind`, keyed by run_tag.
FAILURE_SIDECAR = "failure_kinds.jsonl"

# A result file that is gone is missing data, like an infrastructure failure: retried, never measured.
OUTCOME_MISSING_FILE = "missing_file"

# Fields that together identify one run. Every runner writes all of them into the manifest.
KEY_FIELDS = ("model_client", "environment", "run_label", "id", "safe")


def resume_key(record):
    """Identity of a run, as a hashable tuple. Values are normalised to str so that a case id
    written as int 0 by one runner and as str "0" by another still match."""
    return tuple(
        "" if record.get(f) is None else str(record.get(f))
        for f in KEY_FIELDS
    )


def _read_jsonl(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # a line truncated by a power cut mid-write; that run is simply redone
    return rows


def _resolve(path):
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def load_failure_sidecar(directory):
    """`{run_tag: row}` from the backfilled `failure_kinds.jsonl` in `directory`, or `{}`."""
    path = _resolve(directory) / FAILURE_SIDECAR
    if not path.exists():
        return {}
    return {row["run_tag"]: row for row in _read_jsonl(path) if row.get("run_tag")}


def record_outcome(record, sidecar=None, require_output=True):
    """What one manifest line says happened: one of the OUTCOME_* constants."""
    if record.get("timed_out"):
        return OUTCOME_TIMEOUT
    return_code = record.get("return_code")
    if return_code == 0:
        output_path = record.get("output_path")
        if require_output and (not output_path or not _resolve(output_path).exists()):
            return OUTCOME_MISSING_FILE
        return OUTCOME_OK
    if return_code == 2:
        return OUTCOME_SKIPPED_CASE
    if record.get("failure_kind"):
        return record["failure_kind"]
    backfilled = (sidecar or {}).get(record.get("run_tag"))
    if backfilled and backfilled.get("failure_kind"):
        return backfilled["failure_kind"]
    return OUTCOME_UNKNOWN


def is_terminal(outcome, retry_timeouts=False, retry_model_failures=False, unknown_is_terminal=False):
    """True when `outcome` is a result of the candidate, i.e. must not be retried or replaced."""
    if outcome == OUTCOME_TIMEOUT:
        return not retry_timeouts
    if outcome == OUTCOME_MODEL_TOOL_CALL:
        return not retry_model_failures
    if outcome == OUTCOME_UNKNOWN:
        return unknown_is_terminal
    return outcome in TERMINAL_OUTCOMES


def measured_attempts(records, sidecar=None, unknown_is_terminal=False):
    """One entry per run: `(record, outcome, discarded)`, in first-seen order.

    `record` is the FIRST attempt whose outcome is a result of the candidate. When no attempt is
    (every one was infrastructure, or the file is gone), it is the last attempt, so the gap stays
    visible instead of vanishing. `discarded` counts the later attempts of that run that finished
    ok and were thrown away: the survivors a retry-until-success would have kept.

    `unknown_is_terminal` decides the unclassified failures (legacy lines whose log was lost):
    False treats them as missing data (the old --resume behaviour), True as a result.
    """
    attempts = {}
    for record in records:
        if record.get("return_code") == 0 and not record.get("output_path"):
            continue  # a --dry-run line, not a run
        attempts.setdefault(resume_key(record), []).append(record)

    out = []
    for rows in attempts.values():
        outcomes = [record_outcome(r, sidecar) for r in rows]
        chosen = next(
            (i for i, o in enumerate(outcomes) if is_terminal(o, unknown_is_terminal=unknown_is_terminal)),
            None,
        )
        if chosen is None:
            out.append((rows[-1], outcomes[-1], 0))
            continue
        discarded = sum(1 for o in outcomes[chosen + 1:] if o == OUTCOME_OK)
        out.append((rows[chosen], outcomes[chosen], discarded))
    return out


def completed_keys(manifest_path, require_output=True, retry_timeouts=False, retry_model_failures=False):
    """Keys of the runs in `manifest_path` that must not be run again.

    That is: runs that finished successfully, plus runs whose failure is a result of the candidate
    -- killed by --run-timeout, or broken by the model's own tool call -- unless the matching
    `retry_*` flag is set (see the module docstring for why those are results, not gaps).
    Infrastructure failures and unclassified legacy failures are retried.

    Returns an empty set when the manifest does not exist yet (a fresh sweep). Malformed lines are
    ignored rather than raising: a manifest truncated by a power cut mid-write must not stop the
    resume, it should just cause that one run to be redone.
    """
    manifest_path = _resolve(manifest_path)
    if not manifest_path.exists():
        return set()

    sidecar = load_failure_sidecar(manifest_path.parent)
    done = set()
    for row in _read_jsonl(manifest_path):
        if row.get("return_code") == 0 and not row.get("output_path"):
            continue  # a --dry-run line
        outcome = record_outcome(row, sidecar, require_output=require_output)
        if is_terminal(outcome, retry_timeouts=retry_timeouts, retry_model_failures=retry_model_failures):
            done.add(resume_key(row))
    return done
