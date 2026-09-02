"""Measured token accounting and USD cost for BAD-ACTS episodes.

Why this exists
---------------
The 8-model screening (docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md) runs four paid OpenAI models under a
hard budget cap. Budgeting from guessed token counts is how budgets get blown, so this module
reads the token counts that are ALREADY inside every result file and turns them into dollars.

Where the tokens live
---------------------
`run_experiments.py` saves `team.save_state()` under `team_states`. Inside it,
`agent_states.SelectorGroupChatManager.message_thread` is the ordered thread of the episode, and
every message produced by a model call carries `models_usage = {prompt_tokens, completion_tokens}`.
Summing that thread is the complete, non-duplicated billing record of the episode: one entry per
model call, tool-execution events (which cost nothing) carry no usage.

  IMPORTANT -- do NOT also sum `agent_states.<AGENT>.message_buffer`. Those buffers hold COPIES of
  thread messages that were still queued for delivery when the state was saved, so adding them
  double-counts. On the 163-episode pilot the thread sums to 12.1k input / 1.3k output tokens per
  episode, while thread+buffers sums to 37.2k / 3.7k -- roughly 3x too high. The earlier estimate
  quoted in docs/05-apresentacoes/reuniao-02/apresentacao.html (slide 16b) used the inflated figure; this module is
  the corrected accounting.

Prices are USD per 1M tokens and are only a table: CONFIRM them on the provider's pricing page
before spending, and override with --prices-json when they move. Local models (ollama / vllm)
have no token price; for them the scarce resource is GPU seconds, reported from the manifest.

Usage
-----
    python scripts/analyze_cost.py --manifest-path evaluation_results/screening/gpt5nano/*.jsonl
    python scripts/analyze_cost.py --results 'results/*.json' --budget-usd 6.00

Exit codes: 0 = fine, 3 = the measured cost exceeded --budget-usd (so a runner can abort).
"""

from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

# USD per 1M tokens (input, output). Table checked against the OpenAI pricing page in May 2026 and
# reproduced from docs/05-apresentacoes/reuniao-02/apresentacao.html. Verify before spending; override with
# --prices-json '{"model": {"input": 0.1, "output": 0.4}}'.
DEFAULT_PRICES = {
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1": {"input": 2.00, "output": 8.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "o4-mini": {"input": 1.10, "output": 4.40},
    "gpt-5-nano": {"input": 0.05, "output": 0.40},
    "gpt-5-mini": {"input": 0.25, "output": 2.00},
    "gpt-5": {"input": 1.25, "output": 10.00},
}

# Providers whose usage costs no money. GPU seconds are the scarce resource instead.
FREE_PROVIDERS = {"ollama", "vllm", "openai_compatible"}


def episode_usage(datapoint):
    """Return (input_tokens, output_tokens, model_calls, thread_length) for one episode.

    Reads only the group-chat manager's `message_thread`; see the module docstring for why the
    per-agent `message_buffer` copies must not be added on top.
    """
    team_states = datapoint.get("team_states") or {}
    agent_states = team_states.get("agent_states") or {}
    manager = agent_states.get("SelectorGroupChatManager") or {}
    thread = manager.get("message_thread") or []

    input_tokens = 0
    output_tokens = 0
    model_calls = 0
    for message in thread:
        usage = message.get("models_usage")
        if not usage:
            continue
        input_tokens += int(usage.get("prompt_tokens") or 0)
        output_tokens += int(usage.get("completion_tokens") or 0)
        model_calls += 1

    return input_tokens, output_tokens, model_calls, len(thread)


def usd_cost(model, input_tokens, output_tokens, prices):
    """USD for one episode, or None when the model has no price entry (local models included)."""
    price = prices.get(model)
    if price is None:
        return None
    return input_tokens / 1e6 * price["input"] + output_tokens / 1e6 * price["output"]


def load_result_file(path):
    with Path(path).open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = [data]
    return data


def read_manifest_records(manifest_path):
    manifest_path = Path(manifest_path)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    records = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


def expand_paths(patterns):
    """Expand file paths / globs / directories relative to the repo root."""
    files = []
    for raw in patterns:
        path = Path(raw)
        if not path.is_absolute():
            path = ROOT / path
        if any(ch in str(path) for ch in "*?["):
            files.extend(sorted(ROOT.glob(str(path.relative_to(ROOT)))))
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.json")))
        else:
            files.append(path)

    unique = []
    seen = set()
    for path in files:
        resolved = path.resolve()
        if resolved in seen or not resolved.is_file():
            continue
        seen.add(resolved)
        unique.append(resolved)
    return unique


def collect(manifest_paths, result_patterns, prices):
    """Aggregate cost per (model, provider, environment).

    Manifests are the preferred input: they also carry wall-clock duration and the return code,
    so crashed runs are visible instead of silently missing.
    """
    cells = defaultdict(lambda: {
        "episodes": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "model_calls": 0,
        "thread_length": 0,
        "usd": 0.0,
        "priced": True,
        "durations": [],
        "runs_planned": 0,
        "runs_crashed": 0,
    })

    def account(path, provider_hint=None, duration=None, environment_hint=None):
        for datapoint in load_result_file(path):
            model = datapoint.get("model_client")
            provider = datapoint.get("model_provider") or provider_hint
            environment = datapoint.get("environment") or environment_hint
            cell = cells[(model, provider, environment)]

            input_tokens, output_tokens, model_calls, thread_length = episode_usage(datapoint)
            cell["episodes"] += 1
            cell["input_tokens"] += input_tokens
            cell["output_tokens"] += output_tokens
            cell["model_calls"] += model_calls
            cell["thread_length"] += thread_length

            cost = usd_cost(model, input_tokens, output_tokens, prices)
            if cost is None:
                cell["priced"] = provider in FREE_PROVIDERS
                if provider in FREE_PROVIDERS:
                    cell["usd"] = 0.0
            else:
                cell["usd"] += cost
            if duration is not None:
                cell["durations"].append(duration)

    seen_outputs = set()

    for manifest_path in manifest_paths:
        for record in read_manifest_records(manifest_path):
            model = record.get("model_client")
            provider = record.get("model_provider")
            environment = record.get("environment")
            key = (model, provider, environment)
            cells[key]["runs_planned"] += 1

            output_path = record.get("output_path")
            if record.get("return_code") != 0 or not output_path:
                cells[key]["runs_crashed"] += 1
                continue

            path = Path(output_path)
            if not path.is_absolute():
                path = ROOT / path
            if not path.exists():
                cells[key]["runs_crashed"] += 1
                continue
            if path.resolve() in seen_outputs:
                continue
            seen_outputs.add(path.resolve())
            account(path, provider, record.get("duration_seconds"), environment)

    for path in expand_paths(result_patterns):
        if path in seen_outputs:
            continue
        seen_outputs.add(path)
        account(path)

    return cells


def summarize(cells):
    rows = []
    for (model, provider, environment), cell in sorted(
        cells.items(), key=lambda item: tuple(str(part) for part in item[0])
    ):
        episodes = cell["episodes"]
        rows.append({
            "model_client": model,
            "model_provider": provider,
            "environment": environment,
            "runs_planned": cell["runs_planned"] or episodes,
            "runs_crashed": cell["runs_crashed"],
            "episodes": episodes,
            "mean_input_tokens": round(cell["input_tokens"] / episodes) if episodes else 0,
            "mean_output_tokens": round(cell["output_tokens"] / episodes) if episodes else 0,
            "mean_model_calls": round(cell["model_calls"] / episodes, 1) if episodes else 0,
            "mean_thread_length": round(cell["thread_length"] / episodes, 1) if episodes else 0,
            "total_input_tokens": cell["input_tokens"],
            "total_output_tokens": cell["output_tokens"],
            "usd_total": round(cell["usd"], 4) if cell["priced"] else None,
            "usd_per_episode": round(cell["usd"] / episodes, 5) if cell["priced"] and episodes else None,
            "mean_seconds_per_run": (
                round(sum(cell["durations"]) / len(cell["durations"]), 1) if cell["durations"] else None
            ),
        })
    return rows


def main():
    parser = ArgumentParser(description="Measured token usage and USD cost per model.")
    parser.add_argument(
        "--manifest-path",
        action="append",
        default=[],
        help="Manifest JSONL produced by a runner (repeatable). Preferred input.",
    )
    parser.add_argument(
        "--results",
        action="append",
        default=[],
        help="Result JSON path, glob or directory (repeatable). Use when there is no manifest.",
    )
    parser.add_argument(
        "--prices-json",
        default=None,
        help='Override prices, as inline JSON or a path: {"gpt-4.1": {"input": 2.0, "output": 8.0}}.',
    )
    parser.add_argument(
        "--budget-usd",
        type=float,
        default=None,
        help="Fail with exit code 3 when the measured total exceeds this. Use it to guard a sweep.",
    )
    parser.add_argument("--by-environment", action="store_true", help="Break the table down per environment.")
    parser.add_argument("--out-json", default=None)
    parser.add_argument("--out-csv", default=None)
    args = parser.parse_args()

    if not args.manifest_path and not args.results:
        parser.error("Pass at least one --manifest-path or --results.")

    prices = dict(DEFAULT_PRICES)
    if args.prices_json:
        raw = args.prices_json
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = ROOT / raw
        text = candidate.read_text(encoding="utf-8") if candidate.exists() else raw
        prices.update(json.loads(text))

    cells = collect(args.manifest_path, args.results, prices)
    rows = summarize(cells)

    if not rows:
        print("No episodes found.")
        return

    if not args.by_environment:
        merged = defaultdict(lambda: defaultdict(float))
        for row in rows:
            key = (row["model_client"], row["model_provider"])
            bucket = merged[key]
            for field in ("runs_planned", "runs_crashed", "episodes", "total_input_tokens", "total_output_tokens"):
                bucket[field] += row[field]
            if row["usd_total"] is not None:
                bucket["usd_total"] += row["usd_total"]
            else:
                bucket["unpriced"] = 1
            if row["mean_seconds_per_run"] is not None:
                bucket["seconds_total"] += row["mean_seconds_per_run"] * row["episodes"]
                bucket["seconds_episodes"] += row["episodes"]

        rows = []
        for (model, provider), bucket in sorted(merged.items(), key=lambda i: (str(i[0][0]), str(i[0][1]))):
            episodes = int(bucket["episodes"])
            rows.append({
                "model_client": model,
                "model_provider": provider,
                "environment": "ALL",
                "runs_planned": int(bucket["runs_planned"]),
                "runs_crashed": int(bucket["runs_crashed"]),
                "episodes": episodes,
                "mean_input_tokens": round(bucket["total_input_tokens"] / episodes) if episodes else 0,
                "mean_output_tokens": round(bucket["total_output_tokens"] / episodes) if episodes else 0,
                "mean_model_calls": None,
                "mean_thread_length": None,
                "total_input_tokens": int(bucket["total_input_tokens"]),
                "total_output_tokens": int(bucket["total_output_tokens"]),
                "usd_total": None if bucket.get("unpriced") else round(bucket["usd_total"], 4),
                "usd_per_episode": (
                    None if bucket.get("unpriced") or not episodes
                    else round(bucket["usd_total"] / episodes, 5)
                ),
                "mean_seconds_per_run": (
                    round(bucket["seconds_total"] / bucket["seconds_episodes"], 1)
                    if bucket.get("seconds_episodes") else None
                ),
            })

    print("=" * 108)
    print("MEASURED COST -- tokens read from team_states.agent_states.SelectorGroupChatManager.message_thread")
    print("=" * 108)
    header = (
        f"{'model':<22}{'prov':<10}{'env':<26}{'eps':>5}{'in/ep':>9}{'out/ep':>8}"
        f"{'US$ total':>11}{'US$/ep':>10}{'s/run':>8}"
    )
    print(header)
    print("-" * len(header))
    total_usd = 0.0
    unpriced = []
    for row in rows:
        usd_total = row["usd_total"]
        if usd_total is None:
            unpriced.append(row["model_client"])
            usd_cell, usd_ep = "n/a", "n/a"
        else:
            total_usd += usd_total
            usd_cell, usd_ep = f"{usd_total:.4f}", f"{row['usd_per_episode']:.5f}"
        seconds = "-" if row["mean_seconds_per_run"] is None else f"{row['mean_seconds_per_run']:.0f}"
        print(
            f"{str(row['model_client']):<22}{str(row['model_provider']):<10}{str(row['environment']):<26}"
            f"{row['episodes']:>5}{row['mean_input_tokens']:>9}{row['mean_output_tokens']:>8}"
            f"{usd_cell:>11}{usd_ep:>10}{seconds:>8}"
        )
        if row["runs_crashed"]:
            print(f"{'':<22}{'':<10}  ^ crashed/missing runs: {row['runs_crashed']} of {row['runs_planned']}")

    print("-" * len(header))
    print(f"TOTAL MEASURED: US$ {total_usd:.4f}")
    if unpriced:
        print(
            "Not priced (no token price -- local model, or a name missing from the price table): "
            + ", ".join(sorted({str(m) for m in unpriced}))
        )
    print("Prices are a table, not an invoice. Confirm against the provider's billing page.")

    if args.out_csv:
        import csv
        out_csv = Path(args.out_csv)
        if not out_csv.is_absolute():
            out_csv = ROOT / out_csv
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        with out_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"CSV saved to: {out_csv}")

    if args.out_json:
        out_json = Path(args.out_json)
        if not out_json.is_absolute():
            out_json = ROOT / out_json
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(
            json.dumps({"total_usd": round(total_usd, 4), "rows": rows}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"JSON saved to: {out_json}")

    if args.budget_usd is not None and total_usd > args.budget_usd:
        print(
            f"\nBUDGET EXCEEDED: measured US$ {total_usd:.4f} > cap US$ {args.budget_usd:.2f}",
            file=sys.stderr,
        )
        sys.exit(3)


if __name__ == "__main__":
    main()
