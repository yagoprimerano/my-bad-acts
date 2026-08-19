"""Competence screening for open-weights candidate models (Plano Experimental, Secao 2.7).

This is the STEP THAT COMES BEFORE the definitive runs. Its only purpose is to find the
smallest open model that is still a competent participant in the multi-agent environments,
so that the model comparison measures adversarial robustness instead of basic incompetence.

Why it exists
-------------
An incompetent model looks "safe" for the wrong reason: it does nothing, neither the attack
nor the benign task, so ASR is low while the 2x2 quadrant is `safe_but_useless`. Screening
reads `utility_success` (the deterministic proxy in evaluation/) and keeps only candidates
that clear a utility floor in the tool-using environments.

What it does
------------
For every (candidate model, environment) pair it runs a few cases of BAD-ACTS.csv and writes
a manifest JSONL, exactly like scripts/run_robustness_experiments.py, so that the analysis is
isolated to this sweep. Case selection is deterministic: the first N positional ids of the
environment slice whose `Target` is not the adversarial agent (those cases are skipped by
run_experiments.py and would waste a run).

Runs default to --safe (defense prompts ON): the point here is to read competence with as
little attack pressure as possible. Pass --no-safe to screen under attack instead.

Analyze with scripts/analyze_screening.py.
"""

from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
import json
import re
import subprocess
import sys
import time
import uuid

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = ROOT / "datasets" / "BAD-ACTS.csv"

ALL_ENVIRONMENTS = [
    "travel_planning",
    "financial_article_writing",
    "code_generation",
    "multi_agent_debate",
]

# Environments that require function/tool calling and full multi-agent coordination. These
# are the ones that define the competence floor; multi_agent_debate is text-only and much easier.
TOOL_ENVIRONMENTS = [
    "travel_planning",
    "financial_article_writing",
    "code_generation",
]

# A representative adversarial role per environment (must be a valid agent name of that env).
DEFAULT_ADVERSARIAL_AGENTS = {
    "travel_planning": "PLANNER_AGENT",
    "financial_article_writing": "CHIEF_EDITOR",
    "code_generation": "CEO",
    "multi_agent_debate": "agent_0",
}


def safe_tag(value):
    value = str(value or "").strip()
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    return value.strip("_") or "run"


def select_case_ids(environment, adversarial_agent, n_cases, explicit_ids=None):
    """Return positional --id values for the environment slice.

    `--id` is a positional index into the per-environment slice of BAD-ACTS.csv, not the raw
    pandas index. Cases whose Target equals the adversarial agent are skipped by
    run_experiments.py (the adversary would be attacking itself), so they are filtered out here.
    """
    dataset = pd.read_csv(DATASET_PATH)
    env_slice = dataset[dataset["Environment"] == environment].reset_index(drop=True)

    if explicit_ids:
        return [int(i) for i in explicit_ids]

    usable = []
    for position, row in env_slice.iterrows():
        if str(row["Target"]).strip() == str(adversarial_agent).strip():
            continue
        usable.append(int(position))
        if len(usable) >= n_cases:
            break
    return usable


def build_command(args, model, environment, adversarial_agent, case_id, run_label, run_tag):
    cmd = [
        sys.executable,
        "run_experiments.py",
        "--model-client", model,
        "--model-provider", args.model_provider,
        "--environment", environment,
        "--adversarial-agent", adversarial_agent,
        "--id", str(case_id),
        "--run-label", run_label,
        "--run-tag", run_tag,
    ]

    if args.safe:
        cmd.append("--safe")
    if args.model_base_url:
        cmd.extend(["--model-base-url", args.model_base_url])
    if args.model_api_key:
        cmd.extend(["--model-api-key", args.model_api_key])
    if args.model_family:
        cmd.extend(["--model-family", args.model_family])
    if args.model_no_function_calling:
        cmd.append("--model-no-function-calling")
    if args.seed is not None:
        cmd.extend(["--seed", str(args.seed)])

    return cmd


def extract_output_path(stdout):
    for line in reversed(stdout.splitlines()):
        marker = "Results saved to:"
        if marker in line:
            return line.split(marker, 1)[1].strip()
    return None


def append_manifest(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = ArgumentParser(description="Competence screening ladder for open-weights candidates.")
    parser.add_argument(
        "--models",
        required=True,
        help="Comma-separated candidate models, smallest first (e.g. 'qwen3:8b,mistral-small:24b,qwen3:32b').",
    )
    parser.add_argument(
        "--model-provider",
        default="ollama",
        choices=["openai", "ollama", "vllm", "openai_compatible", "auto"],
        help="Backend for ALL candidates in this sweep. Default: ollama.",
    )
    parser.add_argument("--model-base-url", default=None, help="Endpoint for vllm/openai_compatible.")
    parser.add_argument("--model-api-key", default=None)
    parser.add_argument("--model-family", default=None, help="model_info family (e.g. qwen, llama).")
    parser.add_argument("--model-no-function-calling", action="store_true")
    parser.add_argument(
        "--environments",
        default=",".join(ALL_ENVIRONMENTS),
        help="Comma-separated environments to screen. Default: all four.",
    )
    parser.add_argument("--cases", type=int, default=3, help="Cases per environment. Default: 3.")
    parser.add_argument(
        "--ids",
        default=None,
        help="Explicit comma-separated case ids, applied to every environment (overrides --cases).",
    )
    parser.add_argument("--repeats", type=int, default=1, help="Repeats per case. Default: 1.")
    parser.add_argument(
        "--adversarial-agent",
        default=None,
        help="Override the per-environment default adversarial role (applies to all environments).",
    )
    parser.add_argument(
        "--safe",
        dest="safe",
        action="store_true",
        default=True,
        help="Run with defense prompts ON (default): a cleaner competence read.",
    )
    parser.add_argument(
        "--no-safe",
        dest="safe",
        action="store_false",
        help="Screen under attack pressure instead.",
    )
    parser.add_argument("--seed", type=int, default=12345)
    parser.add_argument(
        "--manifest-path",
        default="evaluation_results/screening/manifest_screening.jsonl",
        help="JSONL manifest of the runs produced by this sweep.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the commands without executing them. Does NOT touch the manifest.",
    )
    args = parser.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    environments = [e.strip() for e in args.environments.split(",") if e.strip()]
    explicit_ids = [i.strip() for i in args.ids.split(",")] if args.ids else None

    for environment in environments:
        if environment not in ALL_ENVIRONMENTS:
            parser.error(f"Unknown environment: {environment}")

    manifest_path = Path(args.manifest_path)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path

    plan = []
    for model in models:
        for environment in environments:
            adversarial_agent = args.adversarial_agent or DEFAULT_ADVERSARIAL_AGENTS[environment]
            case_ids = select_case_ids(environment, adversarial_agent, args.cases, explicit_ids)
            for case_id in case_ids:
                for repeat_index in range(1, args.repeats + 1):
                    plan.append((model, environment, adversarial_agent, case_id, repeat_index))

    print(f"Root: {ROOT}")
    print(f"Candidates: {models}")
    print(f"Environments: {environments}")
    print(f"Defense prompts (--safe): {args.safe}")
    print(f"Total runs: {len(plan)}")
    print(f"Manifest: {manifest_path}")
    if args.dry_run:
        print("DRY RUN: nothing is executed and the manifest is left untouched.")

    for model, environment, adversarial_agent, case_id, repeat_index in plan:
        model_tag = safe_tag(model)
        run_label = f"screen_{model_tag}_{environment}_id{case_id}_r{repeat_index:03d}"
        run_tag = "_".join([
            "screen",
            model_tag,
            environment,
            f"id{case_id}",
            f"r{repeat_index:03d}",
            datetime.now().strftime("%Y%m%d%H%M%S"),
            uuid.uuid4().hex[:6],
        ])

        cmd = build_command(args, model, environment, adversarial_agent, case_id, run_label, run_tag)

        print("=" * 120)
        print(f"Model: {model} | env: {environment} | adversary: {adversarial_agent} | id: {case_id} | repeat: {repeat_index}")
        print(" ".join(cmd))

        if args.dry_run:
            print("DRY RUN: command not executed.")
            continue

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

        record = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "sweep": "screening",
            "model_client": model,
            "model_provider": args.model_provider,
            "model_base_url": args.model_base_url,
            "environment": environment,
            "adversarial_agent": adversarial_agent,
            "id": case_id,
            "repeat_index": repeat_index,
            "safe": args.safe,
            "seed": args.seed,
            "run_label": run_label,
            "run_tag": run_tag,
            "command": cmd,
            "duration_seconds": round(duration, 2),
            "return_code": completed.returncode,
            "output_path": extract_output_path(completed.stdout),
        }
        append_manifest(manifest_path, record)

        if completed.returncode != 0:
            print(
                f"Warning: run FAILED (model={model}, env={environment}, id={case_id}, "
                f"return code {completed.returncode}). Recorded in manifest.",
                file=sys.stderr,
            )

    print("=" * 120)
    if args.dry_run:
        print("Dry run finished. No runs executed, manifest untouched.")
    else:
        print(f"Screening finished. Manifest: {manifest_path}")
        print("Next: python scripts/analyze_screening.py --manifest-path <manifest>")


if __name__ == "__main__":
    main()
