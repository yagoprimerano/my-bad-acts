"""Backfill `failure_kind` for manifests written before the runners classified their failures.

Why this exists
---------------
Until 25/09/2026 a manifest line only said `return_code: 1`. Whether that was the machine (retry it,
it is missing data) or the model (a result, do not retry, see `classify_failure` in
scripts/sweep_exec.py) was only in the per-model log, next to the traceback. This script reads the
log, finds each failed run by its unique `--run-tag`, classifies the traceback that follows it, and
writes the answer to a sidecar, `failure_kinds.jsonl`, in the model's manifest directory.

A sidecar and not an in-place edit of the manifest, because the manifests are copied from the lab
box with rsync: an edited manifest would be silently overwritten on the next copy. The sidecar is
derived data and is rebuilt from scratch on every run of this script.

A failed run whose command is not in the log is recorded as `unknown` with `evidence: "log
ausente"`. That happens because the batch wrappers used `tee` without `-a` until 25/09, so the
second invocation of a sweep erased the tracebacks of the first. Nothing is inferred for those; the
analyzer decides how to treat them (`--unknown-failures`) and says how many there were.

    python scripts/classify_failures.py --screening-dir evaluation_results/screening
"""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sweep_exec import OUTCOME_UNKNOWN, classify_failure  # noqa: E402
from sweep_resume import FAILURE_SIDECAR, _read_jsonl  # noqa: E402

RUN_TAG_IN_COMMAND = re.compile(r"--run-tag (\S+)")


def model_dirs(root):
    return sorted(
        path for path in root.rglob("*")
        if path.is_dir() and path.name != "dryrun" and any(path.glob("manifest_*.jsonl"))
    )


def log_segments(log_text):
    """`{run_tag: text}`: from each printed command to the next one, i.e. that run's own output."""
    matches = list(RUN_TAG_IN_COMMAND.finditer(log_text))
    segments = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(log_text)
        segments[match.group(1)] = log_text[match.start():end]
    return segments


def classify_model_dir(model_dir, logs_dir):
    log_path = logs_dir / f"{model_dir.name}.log"
    segments = log_segments(log_path.read_text(encoding="utf-8", errors="replace")) if log_path.exists() else {}

    rows = []
    for manifest in sorted(model_dir.glob("manifest_*.jsonl")):
        for record in _read_jsonl(manifest):
            if record.get("return_code") in (0, 2, None) or record.get("timed_out"):
                continue
            if record.get("failure_kind"):
                continue  # written by the runner itself, nothing to backfill
            run_tag = record.get("run_tag")
            segment = segments.get(run_tag)
            if segment is None:
                kind, detail, evidence = OUTCOME_UNKNOWN, None, "log ausente"
            else:
                kind, detail = classify_failure(record.get("return_code"), segment, False)
                evidence = "log"
            rows.append({
                "run_tag": run_tag,
                "manifest": manifest.name,
                "environment": record.get("environment"),
                "run_label": record.get("run_label"),
                "id": record.get("id"),
                "safe": record.get("safe"),
                "return_code": record.get("return_code"),
                "failure_kind": kind,
                "failure_detail": detail,
                "evidence": evidence,
            })
    return rows, log_path.exists()


def main():
    parser = ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--screening-dir", default="evaluation_results/screening")
    parser.add_argument("--logs-dir", default="evaluation_results/screening/logs")
    parser.add_argument("--dry-run", action="store_true", help="Print the classification, write nothing.")
    args = parser.parse_args()

    root = Path(args.screening_dir)
    root = root if root.is_absolute() else ROOT / root
    logs_dir = Path(args.logs_dir)
    logs_dir = logs_dir if logs_dir.is_absolute() else ROOT / logs_dir

    for model_dir in model_dirs(root):
        rows, has_log = classify_model_dir(model_dir, logs_dir)
        sidecar = model_dir / FAILURE_SIDECAR
        if not rows:
            if sidecar.exists() and not args.dry_run:
                sidecar.unlink()
            continue

        counts = Counter((r["failure_kind"], r["evidence"]) for r in rows)
        summary = ", ".join(f"{kind} ({evidence}) = {n}" for (kind, evidence), n in sorted(counts.items()))
        print(f"{model_dir.relative_to(root)}: {len(rows)} quebra(s) sem classificacao -> {summary}"
              + ("" if has_log else "  [sem log]"))
        for detail, n in Counter(r["failure_detail"] for r in rows if r["failure_detail"]).most_common(5):
            print(f"    {n:>3}x {detail[:150]}")

        if not args.dry_run:
            sidecar.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

    if args.dry_run:
        print("\nDRY RUN: nenhum arquivo escrito.")


if __name__ == "__main__":
    main()
