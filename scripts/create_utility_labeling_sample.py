"""Create a manual-labeling sample for validating the deterministic utility proxies.

The utility proxies in evaluation_functions.py are heuristics, not ground truth. Before
using them in a dissertation, their agreement with human judgment should be measured.

This script reads one or more result JSON files (or a robustness manifest) and produces a
CSV/JSON with the proxy verdicts plus empty columns for a human annotator to fill in:
`manual_utility_success` and `manual_notes`.

Then use scripts/evaluate_utility_proxy_agreement.py on the filled CSV.
"""

from argparse import ArgumentParser
from pathlib import Path
import json
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EVALUATION_DIR = ROOT / "evaluation"
sys.path.insert(0, str(EVALUATION_DIR))

from evaluation_functions import evaluate_datapoint  # noqa: E402
from trajectory_diagnostics import diagnose_trajectory, get_message_thread, as_text  # noqa: E402


LABELING_COLUMNS = [
    "source_file",
    "case_position_in_file",
    "case_id",
    "dataset_index",
    "run_label",
    "run_tag",
    "target_agent",
    "adversarial_agent",
    "target_action",
    "keywords",
    "attack_success",
    "utility_success_proxy",
    "quadrant_proxy",
    "trajectory_failure_mode",
    "final_answer_or_summary",
    "sent_messages",
    "tickets",
    "files_summary",
    # To be filled in manually:
    "manual_utility_success",
    "manual_notes",
]


def read_manifest_paths(manifest_path):
    manifest_path = Path(manifest_path)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    paths = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        if row.get("return_code") == 0 and row.get("output_path"):
            paths.append(row["output_path"])
    return paths


def resolve_files(paths):
    files = []
    for raw in paths:
        p = Path(raw)
        if not p.is_absolute():
            p = ROOT / p
        if p.is_dir():
            files.extend(sorted(p.rglob("*.json")))
        else:
            files.append(p)
    return [f for f in files if f.exists() and f.is_file()]


def final_text_message(datapoint):
    for event in reversed(get_message_thread(datapoint)):
        if event.get("type") == "TextMessage" and isinstance(event.get("content"), str):
            return event["content"]
    return ""


def files_summary(datapoint):
    files = datapoint.get("files")
    if not isinstance(files, dict):
        return ""
    return "; ".join(f"{name} ({len(as_text(content))} chars)" for name, content in files.items())


def build_rows(files, environment):
    rows = []
    for path in files:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = [data]

        for position, datapoint in enumerate(data, start=1):
            evaluation = evaluate_datapoint(datapoint, environment)
            diagnostics = diagnose_trajectory(
                datapoint,
                environment,
                attack_success=evaluation["attack_success"],
                utility_success=evaluation["utility_success"],
            )
            summary = final_text_message(datapoint)
            rows.append({
                "source_file": str(path),
                "case_position_in_file": position,
                "case_id": datapoint.get("id"),
                "dataset_index": datapoint.get("dataset_index"),
                "run_label": datapoint.get("run_label"),
                "run_tag": datapoint.get("run_tag"),
                "target_agent": datapoint.get("target_agent"),
                "adversarial_agent": datapoint.get("adversarial_agent"),
                "target_action": datapoint.get("target_action"),
                "keywords": datapoint.get("keywords"),
                "attack_success": evaluation["attack_success"],
                "utility_success_proxy": evaluation["utility_success"],
                "quadrant_proxy": evaluation["quadrant"],
                "trajectory_failure_mode": diagnostics.get("failure_mode"),
                "final_answer_or_summary": summary[:2000],
                "sent_messages": as_text(datapoint.get("sent_messages"))[:2000],
                "tickets": as_text(datapoint.get("tickets"))[:1000],
                "files_summary": files_summary(datapoint),
                "manual_utility_success": "",
                "manual_notes": "",
            })
    return rows


def main():
    parser = ArgumentParser(description="Create a manual-labeling sample for utility-proxy validation.")
    parser.add_argument("paths", nargs="*", help="Result JSON files or directories.")
    parser.add_argument("--manifest-path", type=str, default=None, help="Robustness manifest JSONL (successful runs only).")
    parser.add_argument(
        "--environment",
        choices=["travel_planning", "financial_article_writing", "code_generation", "multi_agent_debate"],
        default="travel_planning",
    )
    parser.add_argument("--out-csv", type=str, default="evaluation_results/utility_labeling_sample.csv")
    parser.add_argument("--out-json", type=str, default=None)
    args = parser.parse_args()

    input_paths = list(args.paths)
    if args.manifest_path:
        input_paths.extend(read_manifest_paths(args.manifest_path))
    if not input_paths:
        raise ValueError("No inputs given. Provide result paths and/or --manifest-path.")

    files = resolve_files(input_paths)
    if not files:
        raise FileNotFoundError("No result JSON files found.")

    rows = build_rows(files, args.environment)
    if not rows:
        raise ValueError("No datapoints found in input files.")

    out_csv = Path(args.out_csv)
    if not out_csv.is_absolute():
        out_csv = ROOT / out_csv
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=LABELING_COLUMNS).to_csv(out_csv, index=False)
    print(f"Wrote {len(rows)} rows to {out_csv}")
    print("Fill in 'manual_utility_success' (true/false) and 'manual_notes', then run "
          "scripts/evaluate_utility_proxy_agreement.py")

    if args.out_json:
        out_json = Path(args.out_json)
        if not out_json.is_absolute():
            out_json = ROOT / out_json
        out_json.parent.mkdir(parents=True, exist_ok=True)
        with out_json.open("w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print(f"Wrote JSON to {out_json}")


if __name__ == "__main__":
    main()
