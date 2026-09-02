from argparse import ArgumentParser
from pathlib import Path
import csv
import json
import re
import subprocess
import sys
import time
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


def read_adversarial_variants(path):
    """Read adversarial-goal paraphrase variants for method B2.

    Expected columns: `id`, `variant_id`, `goal`.
    - `id` is the --id value passed to run_experiments.py (the positional index into the
      per-environment dataset). It selects the case whose keywords/target agent are used to
      evaluate the attack, so every paraphrase of an attack must carry that attack's id.
    - `variant_id` labels the paraphrase (e.g. `base`, `paraphrase_01`). `base` should hold the
      original Harmful_Behavior verbatim and is used as the per-case baseline in the analysis.
    - `goal` is the (paraphrased) malicious instruction injected into the adversarial agent.

    Rows without an id or goal are skipped. The `id` is kept as a string tag here but validated
    as an integer so a malformed row fails loudly instead of silently mis-targeting a case.
    """
    variants = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for line_number, row in enumerate(reader, start=2):
            raw_id = (row.get("id") or row.get("dataset_index") or "").strip()
            goal = row.get("goal") or row.get("adversarial_goal") or row.get("harmful_behavior")
            variant_id = row.get("variant_id") or row.get("variant") or f"variant_{len(variants) + 1}"
            if not raw_id or not goal:
                continue
            try:
                case_id = int(raw_id)
            except ValueError:
                raise ValueError(
                    f"Invalid id {raw_id!r} on line {line_number} of {path}: id must be an integer "
                    f"matching the --id of the target case."
                )
            variants.append({
                "id": case_id,
                "variant_id": safe_tag(variant_id),
                "goal": goal,
            })
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

    # Forward OpenAI-compatible endpoint options (vllm/openai_compatible) to run_experiments.py.
    if args.model_base_url:
        cmd.extend(["--model-base-url", args.model_base_url])
    if args.model_api_key:
        cmd.extend(["--model-api-key", args.model_api_key])
    if args.model_family:
        cmd.extend(["--model-family", args.model_family])
    if args.model_no_function_calling:
        cmd.append("--model-no-function-calling")
    if args.model_extra_args:
        cmd.extend(["--model-extra-args", args.model_extra_args])

    # Note: --id is intentionally NOT added here. It is added per condition in run_condition,
    # because method B2 targets a specific case id per adversarial-goal variant, which can differ
    # from the sweep-wide --id.

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


def run_condition(
    args,
    method,
    condition,
    repeat_index,
    task=None,
    trajectory_perturbation="none",
    adversarial_goal=None,
    case_id=None,
    dry_run=False,
):
    # The effective case id: per-condition case_id (method B2) wins over the sweep-wide --id.
    effective_id = case_id if case_id is not None else args.id

    label_parts = ["robust", method, safe_tag(condition), f"r{repeat_index:03d}"]
    run_label = "_".join(label_parts)
    run_tag = build_run_tag(method, condition, repeat_index, effective_id)

    cmd = build_base_command(args)
    cmd.extend(["--run-label", run_label])
    cmd.extend(["--run-tag", run_tag])

    if effective_id is not None:
        cmd.extend(["--id", str(effective_id)])

    if task is not None:
        cmd.extend(["--task", task])

    if adversarial_goal is not None:
        cmd.extend(["--adversarial-goal", adversarial_goal])

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
        # Model/environment identity is repeated here so a manifest is self-describing: the cost
        # and screening analyzers key their per-model tallies off these fields and would otherwise
        # have to open every result file just to learn which model produced the sweep.
        "model_client": args.model_client,
        "model_provider": args.model_provider,
        "model_base_url": args.model_base_url,
        "model_extra_args": args.model_extra_args,
        "environment": args.environment,
        "adversarial_agent": args.adversarial_agent,
        "safe": args.safe,
        "seed": args.seed,
        "method": method,
        "condition": condition,
        "perturbation": trajectory_perturbation,
        "repeat_index": repeat_index,
        "id": effective_id,
        "run_label": run_label,
        "run_tag": run_tag,
        "task": task,
        "adversarial_goal": adversarial_goal,
        "trajectory_perturbation": trajectory_perturbation,
        "command": cmd,
        "return_code": None,
        "output_path": None,
        "duration_seconds": None,
    }

    if dry_run:
        print("DRY RUN: command not executed.")
        manifest_record["return_code"] = 0
        return manifest_record

    started = time.monotonic()
    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    duration = time.monotonic() - started

    print(completed.stdout)

    manifest_record["return_code"] = completed.returncode
    manifest_record["output_path"] = extract_output_path(completed.stdout)
    # Wall clock per run. On the open-weights side GPU time is the scarce resource, so this is
    # what turns a screening into an estimate of how long the definitive sweep will take.
    manifest_record["duration_seconds"] = round(duration, 2)

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


def normalize_methods(method):
    """Resolve the --method value into the concrete list of methods to run.

    'B' is kept as a backward-compatible alias for 'B1' (benign-task paraphrase), the method's
    original name before the adversarial-goal paraphrase (B2) was added.
    """
    if method == "all":
        return ["A", "B1", "B2", "C"]
    if method == "B":
        return ["B1"]
    return [method]


def build_conditions(args):
    conditions = []
    methods = normalize_methods(args.method)

    if "A" in methods:
        conditions.append({
            "method": "A",
            "condition": "repeat_default",
            "task": None,
            "trajectory_perturbation": "none",
        })

    if "B1" in methods:
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
                "method": "B1",
                "condition": variant["variant_id"],
                "task": variant["task"],
                "trajectory_perturbation": "none",
            })

    if "B2" in methods:
        variant_path = Path(args.adversarial_variants_file)
        if not variant_path.is_absolute():
            variant_path = ROOT / variant_path
        if not variant_path.exists():
            raise FileNotFoundError(f"Adversarial variants file not found: {variant_path}")

        variants = read_adversarial_variants(variant_path)
        if args.adversarial_variant_limit is not None:
            variants = variants[: args.adversarial_variant_limit]

        if not variants:
            raise ValueError(f"No adversarial goal variants found in {variant_path}")

        for variant in variants:
            conditions.append({
                "method": "B2",
                "condition": variant["variant_id"],
                "task": None,
                "trajectory_perturbation": "none",
                "adversarial_goal": variant["goal"],
                "case_id": variant["id"],
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
            "A=repetition, B1=benign-task paraphrase perturbation, B2=adversarial-goal paraphrase "
            "perturbation, C=trajectory-protocol perturbation. 'B' is a deprecated alias for 'B1'."
        )
    )
    parser.add_argument("--method", choices=["A", "B", "B1", "B2", "C", "all"], default="A")
    parser.add_argument("--model-client", type=str, default="gpt-4o-mini")
    parser.add_argument(
        "--model-provider",
        type=str,
        choices=["openai", "ollama", "vllm", "openai_compatible", "auto"],
        default="auto",
        help="Model backend passed through to run_experiments.py.",
    )
    parser.add_argument(
        "--model-base-url",
        type=str,
        default=None,
        help="OpenAI-compatible endpoint URL for vllm/openai_compatible (forwarded to run_experiments.py).",
    )
    parser.add_argument(
        "--model-api-key",
        type=str,
        default=None,
        help="API key for the OpenAI-compatible endpoint (forwarded to run_experiments.py).",
    )
    parser.add_argument(
        "--model-family",
        type=str,
        default="unknown",
        help="model_info family label for vllm/openai_compatible (forwarded to run_experiments.py).",
    )
    parser.add_argument(
        "--model-no-function-calling",
        action="store_true",
        help="Declare function_calling=False for vllm/openai_compatible (forwarded to run_experiments.py).",
    )
    parser.add_argument(
        "--model-extra-args",
        type=str,
        default=None,
        help=(
            'JSON create-args forwarded to run_experiments.py, e.g. \'{"reasoning_effort": "minimal"}\'. '
            "Use it to pin the reasoning effort of a reasoning model, otherwise the reasoning tokens "
            "(billed as output) vary run to run and the cost comparison drifts."
        ),
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
        help="CSV of benign-task paraphrases for method B1 (columns: variant_id, task).",
    )
    parser.add_argument("--benign-variant-limit", type=int)
    parser.add_argument(
        "--adversarial-variants-file",
        type=str,
        default="datasets/adversarial_task_variants_travel_planning.csv",
        help=(
            "CSV of adversarial-goal paraphrases for method B2 (columns: id, variant_id, goal). "
            "Each row's id is the --id of the case whose keywords/target agent evaluate the attack."
        ),
    )
    parser.add_argument("--adversarial-variant-limit", type=int)
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
                adversarial_goal=condition.get("adversarial_goal"),
                case_id=condition.get("case_id"),
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
