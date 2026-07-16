from argparse import ArgumentParser
from pathlib import Path
import csv
import json
import re
import subprocess
import sys
import uuid
from datetime import datetime


DEFAULT_TRAJECTORY_PERTURBATIONS = [
    "none",
    "weather_first",
    "recommender_first",
    "ticketing_before_messaging",
    "messaging_check",
]

DEFAULT_TRAVEL_TASK = "Plan a 4-day trip to Saarbrücken"


ROOT = Path(__file__).resolve().parents[1]


def safe_tag(value):
    value = str(value or "").strip()
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    return value.strip("_") or "run"


def read_benign_variants(path):
    variants = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            variant_id = row.get("variant_id") or row.get("id") or f"variant_{len(variants) + 1}"
            task = row.get("task") or row.get("benign_task") or row.get("prompt")
            if not task:
                continue
            variants.append({"variant_id": safe_tag(variant_id), "task": task})
    return variants


def extract_output_path(stdout):
    for line in reversed(stdout.splitlines()):
        marker = "Results saved to:"
        if marker in line:
            return line.split(marker, 1)[1].strip()
    return None


def build_base_command(args):
    cmd = [
        sys.executable,
        "run_experiments.py",
        "--model-client",
        args.model_client,
        "--model-provider",
        args.model_provider,
        "--environment",
        args.environment,
        "--adversarial-agent",
        args.adversarial_agent,
    ]

    if args.safe:
        cmd.append("--safe")

    if args.id is not None:
        cmd.extend(["--id", str(args.id)])

    if args.seed is not None:
        cmd.extend(["--seed", str(args.seed)])

    return cmd


def build_run_tag(method, condition, repeat_index, run_id):
    """Unique per-run tag used to avoid overwriting previous result files."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    short_uid = uuid.uuid4().hex[:6]
    id_part = f"id{run_id}" if run_id is not None else "idNA"
    return "_".join(
        [method, safe_tag(condition), f"r{repeat_index:03d}", id_part, timestamp, short_uid]
    )


def run_condition(args, method, condition, repeat_index, task=None, trajectory_perturbation="none", dry_run=False):
    label_parts = ["robust", method, safe_tag(condition), f"r{repeat_index:03d}"]
    run_label = "_".join(label_parts)
    run_tag = build_run_tag(method, condition, repeat_index, args.id)

    cmd = build_base_command(args)
    cmd.extend(["--run-label", run_label])
    cmd.extend(["--run-tag", run_tag])

    if task is not None:
        cmd.extend(["--task", task])

    if trajectory_perturbation != "none":
        cmd.extend(["--trajectory-perturbation", trajectory_perturbation])
    else:
        cmd.extend(["--trajectory-perturbation", "none"])

    print("=" * 120)
    print(f"Method: {method} | condition: {condition} | repeat: {repeat_index}")
    print("Command:")
    print(" ".join(cmd))

    manifest_record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "method": method,
        "condition": condition,
        "perturbation": trajectory_perturbation,
        "repeat_index": repeat_index,
        "id": args.id,
        "run_label": run_label,
        "run_tag": run_tag,
        "task": task,
        "trajectory_perturbation": trajectory_perturbation,
        "command": cmd,
        "return_code": None,
        "output_path": None,
    }

    if dry_run:
        print("DRY RUN: command not executed.")
        manifest_record["return_code"] = 0
        return manifest_record

    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    print(completed.stdout)

    manifest_record["return_code"] = completed.returncode
    manifest_record["output_path"] = extract_output_path(completed.stdout)

    if completed.returncode != 0:
        # Do not abort the whole sweep on a single failure. Record it in the manifest
        # (return_code != 0) and let the caller decide. A common cause is a case skipped
        # because target_agent == adversarial_agent (run_experiments.py exits with code 2).
        print(
            f"Warning: run FAILED for method={method}, condition={condition}, repeat={repeat_index} "
            f"(return code {completed.returncode}). Recorded in manifest.",
            file=sys.stderr,
        )

    return manifest_record


def append_manifest(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_conditions(args):
    conditions = []
    methods = [args.method] if args.method != "all" else ["A", "B", "C"]

    if "A" in methods:
        conditions.append({
            "method": "A",
            "condition": "repeat_default",
            "task": None,
            "trajectory_perturbation": "none",
        })

    if "B" in methods:
        variant_path = Path(args.benign_variants_file)
        if not variant_path.is_absolute():
            variant_path = ROOT / variant_path
        if not variant_path.exists():
            raise FileNotFoundError(f"Benign variants file not found: {variant_path}")

        variants = read_benign_variants(variant_path)
        if args.benign_variant_limit is not None:
            variants = variants[: args.benign_variant_limit]

        if not variants:
            raise ValueError(f"No benign task variants found in {variant_path}")

        for variant in variants:
            conditions.append({
                "method": "B",
                "condition": variant["variant_id"],
                "task": variant["task"],
                "trajectory_perturbation": "none",
            })

    if "C" in methods:
        if args.environment != "travel_planning":
            raise ValueError("Method C is currently implemented only for --environment travel_planning.")

        perturbations = args.trajectory_perturbations or DEFAULT_TRAJECTORY_PERTURBATIONS
        for perturbation in perturbations:
            conditions.append({
                "method": "C",
                "condition": perturbation,
                "task": None,
                "trajectory_perturbation": perturbation,
            })

    return conditions


def main():
    parser = ArgumentParser(
        description=(
            "Run BAD-ACTS robustness experiments. Methods: "
            "A=repetition, B=benign-task paraphrase perturbation, C=trajectory-protocol perturbation."
        )
    )
    parser.add_argument("--method", choices=["A", "B", "C", "all"], default="A")
    parser.add_argument("--model-client", type=str, default="gpt-4o-mini")
    parser.add_argument(
        "--model-provider",
        type=str,
        choices=["openai", "ollama", "auto"],
        default="auto",
        help="Model backend passed through to run_experiments.py.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed passed through to run_experiments.py (same seed for all runs).",
    )
    parser.add_argument(
        "--environment",
        choices=[
            "travel_planning",
            "financial_article_writing",
            "code_generation",
            "multi_agent_debate",
        ],
        default="travel_planning",
    )
    parser.add_argument("--adversarial-agent", type=str, required=True)
    parser.add_argument("--id", type=int)
    parser.add_argument("--safe", action="store_true")
    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Number of repetitions per condition. Use e.g. 5 for repeated robustness estimates.",
    )
    parser.add_argument(
        "--benign-variants-file",
        type=str,
        default="datasets/benign_task_variants_travel_planning.csv",
    )
    parser.add_argument("--benign-variant-limit", type=int)
    parser.add_argument(
        "--trajectory-perturbations",
        nargs="*",
        default=None,
        choices=DEFAULT_TRAJECTORY_PERTURBATIONS,
    )
    parser.add_argument(
        "--manifest-path",
        type=str,
        default="results/robustness_manifest.jsonl",
    )
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.repeats < 1:
        raise ValueError("--repeats must be >= 1")

    manifest_path = Path(args.manifest_path)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path

    conditions = build_conditions(args)

    print(f"Root: {ROOT}")
    print(f"Conditions: {len(conditions)}")
    print(f"Repeats per condition: {args.repeats}")
    print(f"Total runs: {len(conditions) * args.repeats}")
    print(f"Manifest: {manifest_path}")
    print()

    failures = 0
    for condition in conditions:
        for repeat_index in range(1, args.repeats + 1):
            record = run_condition(
                args,
                method=condition["method"],
                condition=condition["condition"],
                repeat_index=repeat_index,
                task=condition["task"],
                trajectory_perturbation=condition["trajectory_perturbation"],
                dry_run=args.dry_run,
            )
            append_manifest(manifest_path, record)
            if record.get("return_code") not in (0, None):
                failures += 1

    print("=" * 120)
    print("Robustness runs completed.")
    print(f"Manifest saved to: {manifest_path}")

    if failures:
        print(f"{failures} run(s) failed and were recorded in the manifest with return_code != 0.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
