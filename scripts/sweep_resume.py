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
`return_code == 0` AND an `output_path` that still exists on disk. Both halves matter:

  - a run that failed is RETRIED, because on a shared machine the common failure is transient
    (another user took the VRAM, the endpoint blipped). Retrying appends a second manifest line for
    that run, which is harmless: every analyzer keeps only records with return_code 0 AND an
    output_path, so the failed line contributes nothing and cannot double-count.
  - the file has to still be there, so that deleting results/ (or copying only part of it between
    machines) makes the sweep re-run the missing episodes instead of silently reporting a gap.

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

ROOT = Path(__file__).resolve().parents[1]

# Fields that together identify one run. Every runner writes all of them into the manifest.
KEY_FIELDS = ("model_client", "environment", "run_label", "id", "safe")


def resume_key(record):
    """Identity of a run, as a hashable tuple. Values are normalised to str so that a case id
    written as int 0 by one runner and as str "0" by another still match."""
    return tuple(
        "" if record.get(f) is None else str(record.get(f))
        for f in KEY_FIELDS
    )


def completed_keys(manifest_path, require_output=True):
    """Keys of the runs in `manifest_path` that finished successfully.

    Returns an empty set when the manifest does not exist yet (a fresh sweep). Malformed lines are
    ignored rather than raising: a manifest truncated by a power cut mid-write must not stop the
    resume, it should just cause that one run to be redone.
    """
    manifest_path = Path(manifest_path)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    if not manifest_path.exists():
        return set()

    done = set()
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("return_code") != 0:
            continue
        output_path = row.get("output_path")
        if require_output:
            if not output_path:
                continue
            resolved = Path(output_path)
            if not resolved.is_absolute():
                resolved = ROOT / resolved
            if not resolved.exists():
                continue
        done.add(resume_key(row))
    return done
