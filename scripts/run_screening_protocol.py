"""Protocol T3: the identical 82-run screening every candidate model goes through.

Full rationale, model ladders and budget: docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md

What this is for
----------------
Two questions, one protocol:

  - Open models (local GPU): which candidate is the SMALLEST that is still a competent
    participant, so the definitive comparison measures adversarial robustness instead of basic
    incompetence? Read from `utility_rate` in the tool-using environments.
  - Paid models (OpenAI Platform): does the extra capability of a more expensive tier actually
    change the safety/utility picture, or would we be paying 20x for the same conclusion? Read
    from the ASR/utility/robustness deltas between price tiers, against measured USD.

Those two questions only compose into one table if every model runs EXACTLY the same protocol on
EXACTLY the same cases. That is the whole point of this script: the design is a constant in the
source (PROTOCOL below), not a set of flags, so no candidate can accidentally get an easier or
harder screening. What the operator chooses is the model, the backend and the output directory.

The five blocks (82 runs per model)
-----------------------------------
  L   breadth      40  4 environments x 10 cases, stratified over the distinct Target agents
  A   repetition    8  travel_planning, case 0, 8 repeats -- run-to-run variability
  B1  benign par.  10  travel_planning, case 0, 5 benign-task paraphrases x 2 repeats
  B2  adversarial  16  travel_planning, cases 0 and 3, 4 adversarial-goal paraphrases each x 2
  F   factorial     8  travel_planning, case 0, Defense{off,on} x Perturbation{none,weather_first}, 2 reps

Sizing note (T3 supersedes T2's 45 runs). The binding constraint is NOT money: at 82 runs the four
paid models cost US$ 3.44 expected and US$ 9.59 in the deliberately inflated projection, against a
US$ 10 ceiling. What actually caps the design is GPU time on a SHARED machine -- the open ladder at
82 runs is an estimated 6 to 14 hours, of which the 70B alone is 3 to 7. Raising the count further
buys tighter intervals in dollars nobody misses and GPU-hours somebody does.

Blocks A/B1/B2/F reuse scripts/run_robustness_experiments.py and block L reuses
scripts/run_screening.py, so the run_label contract and every existing analyzer keep working
unchanged. Each block writes its own manifest under the model's output directory.

Block A is not read on its own. Four blocks put a run in the SAME reference condition
(travel_planning, case 0, defense off, no perturbation, original task, original goal): block A's 8
repeats, block B1's `base` variant x2, block B2's `base` variant of case 0 x2, and block F's
(off, none) cell with 2 reps. That is 14 observations of one identical condition, and
analyze_screening_protocol.py pools them for the repeatability read instead of looking only at
block A. Block L gets the largest share because it carries the paired cross-model comparison: it
is the block that answers "is the expensive model worth it", via exact McNemar over 40 paired
cases (T2 had 20, which only separated very large differences).

Usage
-----
    # 1. always look before you spend
    python scripts/run_screening_protocol.py --tag gpt5nano \\
      --model-client gpt-5-nano --model-provider openai --dry-run

    # 2. run it. A reasoning model needs its effort pinned, or the reasoning tokens (billed as
    #    output) drift run to run and the cost comparison stops meaning anything.
    python scripts/run_screening_protocol.py --tag gpt5nano \\
      --model-client gpt-5-nano --model-provider openai --budget-usd 0.30 \\
      --model-extra-args '{"reasoning_effort": "minimal"}'

Analyze with scripts/analyze_screening_protocol.py (all models at once).
"""

from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_cost import DEFAULT_PRICES  # noqa: E402
from sweep_resume import completed_keys  # noqa: E402

PROTOCOL_VERSION = "T3"

# The screening design. Changing any number here changes it for EVERY model, which is the only
# way the cross-model table stays comparable. If you change it, bump PROTOCOL_VERSION and re-run
# every model -- a mixed-version table is not a comparison.
PROTOCOL = {
    "seed": 12345,
    "environments": [
        "travel_planning",
        "financial_article_writing",
        "code_generation",
        "multi_agent_debate",
    ],
    "deep_environment": "travel_planning",
    "deep_adversarial_agent": "PLANNER_AGENT",
    # Block L: breadth. Defense OFF, which is the standard BAD-ACTS condition, so the ASR column
    # is comparable with the published benchmark. Competence is read from utility_rate here; when
    # a candidate fails the floor, block F's defense-ON cells tell you whether it was incompetence
    # or the attack derailing an otherwise capable model.
    "L": {"cases_per_environment": 10, "repeats": 1, "safe": False, "case_selection": "stratified"},
    "A": {"case_id": 0, "repeats": 8, "safe": False},
    "B1": {"case_id": 0, "repeats": 2},   # 5 variants in the CSV (base + 4 paraphrases)
    "B2": {"repeats": 2},                 # 2 cases x 4 variants, ids carried by the CSV
    "F": {"case_id": 0, "repeats": 2, "perturbations": ["none", "weather_first"]},
}

BLOCK_RUNS = {"L": 40, "A": 8, "B1": 10, "B2": 16, "F": 8}
# Runs expected in EACH manifest. Block F is executed as two sweeps (defense off / on) writing two
# manifests, so each holds half of the block. Used by --resume to tell a finished block from one
# that was interrupted partway.
MANIFEST_RUNS = {
    "L": BLOCK_RUNS["L"],
    "A": BLOCK_RUNS["A"],
    "B1": BLOCK_RUNS["B1"],
    "B2": BLOCK_RUNS["B2"],
    "F/def0_nosafe": BLOCK_RUNS["F"] // 2,
    "F/def1_safe": BLOCK_RUNS["F"] // 2,
}
TOTAL_RUNS = sum(BLOCK_RUNS.values())  # 82

ALL_BLOCKS = ["L", "A", "B1", "B2", "F"]

# Token profile measured on the 163-episode gpt-4o-mini pilot (travel_planning), used ONLY to
# project cost before spending. See scripts/analyze_cost.py for the accounting. Real cost is
# always re-measured from the result files after each block.
PILOT_INPUT_TOKENS = 11930
PILOT_OUTPUT_TOKENS = 1333
# The pilot only covers travel_planning with a small non-reasoning model, so the projection is
# inflated twice before it is used for planning:
#   - every model gets a 2x factor, for other environments and for larger models producing longer
#     trajectories;
#   - a reasoning model gets a further 2x on OUTPUT only, because its reasoning tokens are billed
#     as output and do not exist in the pilot profile at all. Pinning --model-extra-args
#     '{"reasoning_effort": "minimal"}' is what keeps that factor from being much larger.
PROJECTION_SAFETY_FACTOR = 2.0
REASONING_OUTPUT_FACTOR = 2.0

# Model families that spend reasoning tokens. Prefix match, so gpt-5-nano/-mini/full and the
# o-series are all covered. Used only for the cost FORECAST; the measured cost never guesses.
REASONING_MODEL_PREFIXES = ("gpt-5", "o1", "o3", "o4")


def is_reasoning_model(model):
    name = (model or "").lower().strip()
    return name.startswith(REASONING_MODEL_PREFIXES)


def project_cost(model, runs=TOTAL_RUNS, prices=None):
    """Projected USD for `runs` episodes: (expected, conservative). None for unpriced models."""
    prices = prices or DEFAULT_PRICES
    price = prices.get(model)
    if price is None:
        return None, None
    input_cost = PILOT_INPUT_TOKENS / 1e6 * price["input"]
    output_cost = PILOT_OUTPUT_TOKENS / 1e6 * price["output"]
    expected = (input_cost + output_cost) * runs

    output_factor = PROJECTION_SAFETY_FACTOR * (
        REASONING_OUTPUT_FACTOR if is_reasoning_model(model) else 1.0
    )
    conservative = (
        input_cost * PROJECTION_SAFETY_FACTOR + output_cost * output_factor
    ) * runs
    return expected, conservative


def model_flags(args):
    """Backend flags forwarded verbatim to every sub-runner."""
    flags = ["--model-client", args.model_client, "--model-provider", args.model_provider]
    if getattr(args, "results_dir", None):
        flags += ["--results-dir", args.results_dir]
    if args.model_base_url:
        flags += ["--model-base-url", args.model_base_url]
    if args.model_api_key:
        flags += ["--model-api-key", args.model_api_key]
    if args.model_family:
        flags += ["--model-family", args.model_family]
    if args.model_no_function_calling:
        flags.append("--model-no-function-calling")
    if args.model_extra_args:
        flags += ["--model-extra-args", args.model_extra_args]
    return flags


def robustness_command(args, method, manifest, extra):
    return (
        [sys.executable, "scripts/run_robustness_experiments.py", "--method", method]
        + model_flags(args)
        + [
            "--environment", PROTOCOL["deep_environment"],
            "--adversarial-agent", PROTOCOL["deep_adversarial_agent"],
            "--seed", str(args.seed),
            "--manifest-path", str(manifest),
        ]
        + extra
    )


def build_block_commands(args, out_dir):
    """Return [(block, manifest_path, command), ...] in execution order."""
    blocks = []

    # ---- L: breadth over the four environments -------------------------------------------
    manifest = out_dir / "manifest_L_breadth.jsonl"
    cmd = (
        [sys.executable, "scripts/run_screening.py", "--models", args.model_client]
        + ["--model-provider", args.model_provider]
        + (["--model-base-url", args.model_base_url] if args.model_base_url else [])
        + (["--model-api-key", args.model_api_key] if args.model_api_key else [])
        + (["--model-family", args.model_family] if args.model_family else [])
        + (["--model-no-function-calling"] if args.model_no_function_calling else [])
        + (["--model-extra-args", args.model_extra_args] if args.model_extra_args else [])
        + (["--results-dir", args.results_dir] if args.results_dir else [])
        + [
            "--environments", ",".join(PROTOCOL["environments"]),
            "--cases", str(PROTOCOL["L"]["cases_per_environment"]),
            "--repeats", str(PROTOCOL["L"]["repeats"]),
            "--case-selection", PROTOCOL["L"]["case_selection"],
            "--no-safe",
            "--seed", str(args.seed),
            "--manifest-path", str(manifest),
        ]
    )
    blocks.append(("L", manifest, cmd))

    # ---- A: repetition -------------------------------------------------------------------
    manifest = out_dir / "manifest_A_repetition.jsonl"
    blocks.append((
        "A", manifest,
        robustness_command(args, "A", manifest, [
            "--id", str(PROTOCOL["A"]["case_id"]),
            "--repeats", str(PROTOCOL["A"]["repeats"]),
        ]),
    ))

    # ---- B1: benign-task paraphrase ------------------------------------------------------
    manifest = out_dir / "manifest_B1_benign_paraphrase.jsonl"
    blocks.append((
        "B1", manifest,
        robustness_command(args, "B1", manifest, [
            "--id", str(PROTOCOL["B1"]["case_id"]),
            "--repeats", str(PROTOCOL["B1"]["repeats"]),
        ]),
    ))

    # ---- B2: adversarial-goal paraphrase (ids come from the variants CSV) ----------------
    manifest = out_dir / "manifest_B2_adversarial_paraphrase.jsonl"
    blocks.append((
        "B2", manifest,
        robustness_command(args, "B2", manifest, [
            "--repeats", str(PROTOCOL["B2"]["repeats"]),
        ]),
    ))

    # ---- F: 2^2 factorial, Defense x Perturbation ----------------------------------------
    # Two sweeps because --safe is a flag of the runner, not a swept factor. The factorial
    # analyzer crosses them by reading the `safe` field saved inside each datapoint.
    for defense_on in (False, True):
        suffix = "def1_safe" if defense_on else "def0_nosafe"
        manifest = out_dir / f"manifest_F_factorial_{suffix}.jsonl"
        extra = [
            "--id", str(PROTOCOL["F"]["case_id"]),
            "--repeats", str(PROTOCOL["F"]["repeats"]),
            "--trajectory-perturbations", *PROTOCOL["F"]["perturbations"],
        ]
        if defense_on:
            extra.append("--safe")
        blocks.append((f"F/{suffix}", manifest, robustness_command(args, "C", manifest, extra)))

    return blocks


def measured_cost(manifests, prices_json=None):
    """Re-measure spend from the result files listed in `manifests`. Returns USD or None."""
    existing = [str(m) for m in manifests if Path(m).exists()]
    if not existing:
        return 0.0

    cmd = [sys.executable, "scripts/analyze_cost.py"]
    for manifest in existing:
        cmd += ["--manifest-path", manifest]
    if prices_json:
        cmd += ["--prices-json", prices_json]

    completed = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in completed.stdout.splitlines():
        if line.startswith("TOTAL MEASURED: US$"):
            try:
                return float(line.split("US$", 1)[1].strip())
            except ValueError:
                return None
    return None


def main():
    parser = ArgumentParser(description=f"Screening protocol {PROTOCOL_VERSION}: {TOTAL_RUNS} runs per model.")
    parser.add_argument("--tag", required=True, help="Short directory-safe name for this model (e.g. gpt5nano, qwen3-32b).")
    parser.add_argument("--model-client", required=True, help="Model name as the backend knows it.")
    parser.add_argument(
        "--model-provider",
        required=True,
        choices=["openai", "ollama", "vllm", "openai_compatible", "auto"],
    )
    parser.add_argument("--model-base-url", default=None, help="Endpoint for vllm/openai_compatible.")
    parser.add_argument("--model-api-key", default=None)
    parser.add_argument("--model-family", default=None, help="model_info family for vllm/openai_compatible (qwen, llama, ...).")
    parser.add_argument("--model-no-function-calling", action="store_true")
    parser.add_argument(
        "--model-extra-args",
        default=None,
        help=(
            'JSON create-args forwarded to every run, e.g. \'{"reasoning_effort": "minimal"}\'. '
            "Required in practice for a reasoning model: its reasoning tokens are billed as output, "
            "so leaving the effort at the provider default makes the cost both larger and variable."
        ),
    )
    parser.add_argument("--seed", type=int, default=PROTOCOL["seed"])
    parser.add_argument(
        "--results-dir",
        default=None,
        help="Directory the episode JSONs are written to, forwarded to every sub-runner. Keeps "
             "sweeps apart instead of piling every episode into results/. Convention: "
             "results/triagem/abertos, results/triagem/pagos, results/definitivo/<model>.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Default: evaluation_results/screening/<tag>. One directory per model, one manifest per block.",
    )
    parser.add_argument(
        "--blocks",
        default=",".join(ALL_BLOCKS),
        help=f"Comma-separated subset of {ALL_BLOCKS}. Only for resuming after a failure; a partial protocol is not comparable.",
    )
    parser.add_argument(
        "--budget-usd",
        type=float,
        default=None,
        help="Abort as soon as the MEASURED spend for this model passes the cap. Paid models only.",
    )
    parser.add_argument("--prices-json", default=None, help="Price override forwarded to analyze_cost.py.")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip blocks whose manifest already exists (after an interrupted sweep).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the plan and the cost projection; run nothing.")
    args = parser.parse_args()

    # Sub-runners write straight to the terminal; line-buffer ours so the block headers do not
    # end up shuffled behind their own output when the sweep is piped to a log file.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except AttributeError:
        pass

    requested = [b.strip() for b in args.blocks.split(",") if b.strip()]
    unknown = [b for b in requested if b not in ALL_BLOCKS]
    if unknown:
        parser.error(f"Unknown block(s): {unknown}. Valid: {ALL_BLOCKS}")

    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "evaluation_results" / "screening" / args.tag
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    if args.dry_run:
        out_dir = out_dir / "dryrun"
    out_dir.mkdir(parents=True, exist_ok=True)

    blocks = [b for b in build_block_commands(args, out_dir) if b[0].split("/")[0] in requested]
    planned_runs = sum(BLOCK_RUNS[name.split("/")[0]] for name, _, _ in blocks)
    # Block F is two sweeps of 4 runs; BLOCK_RUNS counts the whole block, so halve it.
    planned_runs -= sum(BLOCK_RUNS["F"] // 2 for name, _, _ in blocks if name.startswith("F/"))

    expected, conservative = project_cost(args.model_client, planned_runs, None)

    print("=" * 108)
    print(f"SCREENING PROTOCOL {PROTOCOL_VERSION}  |  model={args.model_client}  provider={args.model_provider}  tag={args.tag}")
    print("=" * 108)
    print(f"Blocks:        {', '.join(name for name, _, _ in blocks)}")
    print(f"Runs:          {planned_runs} (full protocol = {TOTAL_RUNS})")
    print(f"Seed:          {args.seed}")
    print(f"Output dir:    {out_dir}")
    if expected is None:
        print("Cost:          not priced (local model). The scarce resource is GPU time; see s/run after the sweep.")
    else:
        factors = f"{PROJECTION_SAFETY_FACTOR:g}x"
        if is_reasoning_model(args.model_client):
            factors += f" in / {PROJECTION_SAFETY_FACTOR * REASONING_OUTPUT_FACTOR:g}x out, reasoning model"
        print(
            f"Cost forecast: US$ {expected:.2f} expected, US$ {conservative:.2f} conservative "
            f"({factors}), from the pilot profile of "
            f"{PILOT_INPUT_TOKENS} in / {PILOT_OUTPUT_TOKENS} out tokens per episode."
        )
    if args.budget_usd is not None:
        print(f"Budget cap:    US$ {args.budget_usd:.2f} (measured after every block; the sweep aborts if passed)")
    if args.model_extra_args:
        print(f"Extra args:    {args.model_extra_args}")
    elif is_reasoning_model(args.model_client):
        print(
            f"WARNING: '{args.model_client}' is a reasoning model and no --model-extra-args was given. "
            "It will run at the provider's default reasoning effort, which costs more and varies "
            'between runs. Consider --model-extra-args \'{"reasoning_effort": "minimal"}\'.'
        )
    print()

    started_at = datetime.now()
    manifests = []
    executed = []

    for name, manifest, cmd in blocks:
        print("=" * 108)
        print(f"BLOCK {name}")
        print(" ".join(str(c) for c in cmd))

        if args.resume and not args.dry_run:
            # Resume is RUN-level, not block-level. Skipping a block just because its manifest
            # file exists is wrong: the manifest is appended after every run, so a block
            # interrupted after 1 of 40 runs would be treated as finished and the remaining 39
            # silently dropped into the comparison table. Count what actually completed instead,
            # and hand --resume to the sub-runner so it skips only the runs that are really done.
            done = len(completed_keys(manifest))
            expected = MANIFEST_RUNS.get(name)
            if expected is not None and done >= expected:
                print(f"RESUME: block already complete ({done}/{expected} runs), skipped -> {manifest}")
                manifests.append(manifest)
                continue
            if done:
                print(f"RESUME: block partially done ({done}/{expected} runs), continuing where it stopped.")
            cmd = cmd + ["--resume"]

        if args.dry_run:
            subprocess.run(cmd + ["--dry-run"], cwd=ROOT)
            continue

        completed = subprocess.run(cmd, cwd=ROOT)
        manifests.append(manifest)
        executed.append((name, completed.returncode))
        if completed.returncode != 0:
            print(f"Warning: block {name} exited with code {completed.returncode}.", file=sys.stderr)

        if args.budget_usd is not None:
            spent = measured_cost(manifests, args.prices_json)
            if spent is None:
                print("Budget check: could not measure spend (unpriced model?). Continuing.")
            else:
                print(f"Budget check: US$ {spent:.4f} measured so far of US$ {args.budget_usd:.2f}.")
                if spent > args.budget_usd:
                    print(
                        f"BUDGET EXCEEDED after block {name}: US$ {spent:.4f} > US$ {args.budget_usd:.2f}. "
                        "Stopping. The protocol is INCOMPLETE for this model and must not be put in the "
                        "comparison table as if it were.",
                        file=sys.stderr,
                    )
                    sys.exit(3)

    print("=" * 108)
    if args.dry_run:
        print("Dry run finished. Nothing was executed; the throwaway manifests are under the dryrun/ subfolder.")
        return

    summary = {
        "protocol_version": PROTOCOL_VERSION,
        "tag": args.tag,
        "model_client": args.model_client,
        "model_provider": args.model_provider,
        "model_base_url": args.model_base_url,
        "model_extra_args": args.model_extra_args,
        "seed": args.seed,
        "blocks": [name for name, _, _ in blocks],
        "planned_runs": planned_runs,
        "started_at": started_at.isoformat(timespec="seconds"),
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "elapsed_seconds": round((datetime.now() - started_at).total_seconds(), 1),
        "block_return_codes": dict(executed),
        "manifests": [str(m) for m in manifests],
    }
    summary_path = out_dir / "protocol_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    spent = measured_cost(manifests, args.prices_json)
    print(f"Protocol finished in {summary['elapsed_seconds'] / 60:.1f} min. Summary: {summary_path}")
    if spent:
        print(f"Measured spend for {args.model_client}: US$ {spent:.4f}")
    print("Next: python scripts/analyze_screening_protocol.py --screening-dir evaluation_results/screening")


if __name__ == "__main__":
    main()
