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
isolated to this sweep. Case selection is deterministic (no RNG), so every candidate model is
screened on exactly the SAME cases: by default it round-robins over the distinct `Target` agents
of the environment (`--case-selection stratified`), skipping cases whose `Target` is the
adversarial agent (those are skipped by run_experiments.py and would waste a run).

Runs default to --safe (defense prompts ON): a competence read with as little attack pressure as
possible. Pass --no-safe to screen under attack instead, which is the standard BAD-ACTS condition
and the one the 8-model screening protocol uses for its breadth block (see
scripts/run_screening_protocol.py and docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md).

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


def select_case_ids(environment, adversarial_agent, n_cases, explicit_ids=None,
                    selection="stratified"):
    """Return positional --id values for the environment slice.

    `--id` is a positional index into the per-environment slice of BAD-ACTS.csv, not the raw
    pandas index. Cases whose Target equals the adversarial agent are skipped by
    run_experiments.py (the adversary would be attacking itself), so they are filtered out here.

    Two selection modes, both deterministic (no RNG), so every candidate model is screened on
    exactly the SAME cases -- that pairing is what makes the cross-model comparison valid:

      - "first":      the first N usable positions. Cheap, but in BAD-ACTS the dataset is sorted
                      by Target, so the first N cases usually all attack the SAME agent. That
                      reads competence through a single channel.
      - "stratified": round-robin over the distinct Target values (ordered by first appearance),
                      taking one case per Target per pass. With N >= number of targets this
                      covers every attack channel of the environment. Default.
    """
    dataset = pd.read_csv(DATASET_PATH)
    env_slice = dataset[dataset["Environment"] == environment].reset_index(drop=True)

    if explicit_ids:
        return [int(i) for i in explicit_ids]

    by_target = {}
    order = []
    for position, row in env_slice.iterrows():
        target = str(row["Target"]).strip()
        if target == str(adversarial_agent).strip():
            continue
        if target not in by_target:
            by_target[target] = []
            order.append(target)
        by_target[target].append(int(position))

    if selection == "first":
        flat = sorted(position for positions in by_target.values() for position in positions)
        return flat[:n_cases]

    selected = []
    depth = 0
    while len(selected) < n_cases:
        added = False
        for target in order:
            positions = by_target[target]
            if depth < len(positions):
                selected.append(positions[depth])
                added = True
                if len(selected) >= n_cases:
                    break
        if not added:
            break
        depth += 1
    return sorted(selected)


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
    if args.model_extra_args:
        cmd.extend(["--model-extra-args", args.model_extra_args])
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
        "--model-extra-args",
        default=None,
        help='JSON create-args forwarded to run_experiments.py, e.g. \'{"reasoning_effort": "minimal"}\'.',
    )
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
        "--case-selection",
        default="stratified",
        choices=["stratified", "first"],
        help=(
            "How to pick the cases of each environment. 'stratified' (default) round-robins over "
            "the distinct Target agents so the screening covers every attack channel; 'first' "
            "takes the first N usable positions (legacy, biased towards one Target)."
        ),
    )
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
            case_ids = select_case_ids(
                environment, adversarial_agent, args.cases, explicit_ids, args.case_selection
            )
            for case_id in case_ids:
                for repeat_index in range(1, args.repeats + 1):
                    plan.append((model, environment, adversarial_agent, case_id, repeat_index))

    print(f"Root: {ROOT}")
    print(f"Candidates: {models}")
    print(f"Environments: {environments}")
    print(f"Defense prompts (--safe): {args.safe}")
    print(f"Case selection: {args.case_selection}")
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
            "model_extra_args": args.model_extra_args,
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
