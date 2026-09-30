"""Blind human labeling of the utility proxy, for the screening (protocol T4).

`create_utility_labeling_sample.py` writes the proxy verdict next to the empty column the human
fills in, and the source path names the model. Both anchor the labeler. This script separates what
the labeler sees from what the analysis needs:

  sample   draws a stratified random sample of block-L episodes, writes
           * a KEY (code -> model, file, proxy verdict, population sizes), NOT to be opened while
             labeling, and
           * a self-contained HTML page that shows one episode at a time by code only: no model, no
             proxy verdict, no attack verdict. Labels are kept in the browser and exported as JSON.
  score    joins the exported labels with the key and reports agreement per environment.

Population: the block-L episodes of the environments that decide the competence floor
(travel_planning, financial_article_writing), one record per run exactly as the screening analyzer
counts them (`measured_attempts`, first attempt that is a result of the candidate), only the runs
that produced an episode. Strata: environment x proxy verdict, drawn with a fixed seed, so the
sample is decided before anyone reads an episode and is reproducible.

Because the proxy verdict is a stratum, the plain accuracy over the sample is NOT the population
accuracy. `score` reports the per-stratum agreement (the two numbers that matter: how often "useful"
from the proxy is right, how often "not useful" is right) and the population-weighted accuracy.

Usage
-----
    python scripts/utility_labeling_blind.py sample --per-stratum 10 \\
      --criteria-file docs/02-experimentos/VALIDACAO_PROXY_UTILIDADE.md \\
      --out-dir evaluation_results/validacao_proxy --batch lote1
    # open evaluation_results/validacao_proxy/lote1_rotulagem.html in a browser, label, export
    python scripts/utility_labeling_blind.py score \\
      --key evaluation_results/validacao_proxy/lote1_CHAVE_nao_abrir.json \\
      --labels evaluation_results/validacao_proxy/lote1_rotulos.json
"""

from argparse import ArgumentParser
from collections import Counter, defaultdict
from pathlib import Path
import csv
import json
import math
import random
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "evaluation"))

from analyze_cost import load_result_file, read_manifest_records  # noqa: E402
from analyze_experiment_stats import wilson_interval  # noqa: E402
from analyze_screening_protocol import discover_model_dirs  # noqa: E402
from evaluation_functions import evaluate_datapoint  # noqa: E402
from sweep_exec import OUTCOME_OK  # noqa: E402
from sweep_resume import load_failure_sidecar, measured_attempts  # noqa: E402

ENVIRONMENTS = ["travel_planning", "financial_article_writing"]
CODE_PREFIX = {"travel_planning": "V", "financial_article_writing": "F"}
TEMPLATE = ROOT / "scripts" / "templates" / "utility_labeling.html"

# Names a model may write about itself. Replaced in what the labeler reads, so the page stays blind
# to the model as far as the text allows (style can still give a family away; nothing to do there).
MODEL_NAME_RE = re.compile(
    r"\b(?:chat)?gpt[-\w.:]*|\bqwen[-\w.:]*|\bllama[-\w.:]*|\bministral[-\w.:]*|\bmistral[-\w.:]*"
    r"|\bopenai\b|\balibaba\b",
    re.IGNORECASE,
)


def scrub(text):
    return MODEL_NAME_RE.sub("[modelo]", text)


def as_text(value):
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=1, default=str)


# ---------------------------------------------------------------------------------------------
# sample
# ---------------------------------------------------------------------------------------------

def build_population(screening_dir):
    """Every block-L episode of ENVIRONMENTS, with its proxy verdict."""
    population = []
    for model_dir in discover_model_dirs(screening_dir, None):
        manifest = model_dir / "manifest_L_breadth.jsonl"
        if not manifest.exists():
            continue
        sidecar = load_failure_sidecar(model_dir)
        attempts = measured_attempts(read_manifest_records(manifest), sidecar, unknown_is_terminal=True)
        for record, outcome, _ in attempts:
            environment = record.get("environment")
            if outcome != OUTCOME_OK or environment not in ENVIRONMENTS:
                continue
            path = Path(record["output_path"])
            if not path.is_absolute():
                path = ROOT / path
            for position, datapoint in enumerate(load_result_file(path)):
                evaluation = evaluate_datapoint(datapoint, environment)
                population.append({
                    "model_tag": model_dir.name,
                    "model_client": datapoint.get("model_client") or record.get("model_client"),
                    "environment": environment,
                    "case_id": record.get("id"),  # the datapoint "id" is its position in the run, not the case
                    "dataset_index": datapoint.get("dataset_index"),
                    "output_path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                    "position_in_file": position,
                    "utility_success_proxy": bool(evaluation["utility_success"]),
                    "attack_success": bool(evaluation["attack_success"]),
                    "quadrant_proxy": evaluation["quadrant"],
                })
    return population


def episode_key(item):
    return (item["output_path"], item["position_in_file"])


def load_excluded(paths):
    """Episodes already drawn by an earlier batch, so a second batch never repeats one."""
    excluded = set()
    for raw in paths or []:
        key = json.loads(Path(raw).read_text(encoding="utf-8"))
        for item in key["episodes"].values():
            excluded.add(episode_key(item))
    return excluded


def draw_sample(population, per_stratum, seed, excluded):
    strata = defaultdict(list)
    for item in population:
        if episode_key(item) in excluded:
            continue
        strata[(item["environment"], item["utility_success_proxy"])].append(item)

    rng = random.Random(seed)
    chosen = defaultdict(list)
    for environment in ENVIRONMENTS:
        for proxy in (True, False):
            pool = sorted(strata[(environment, proxy)], key=episode_key)
            if len(pool) < per_stratum:
                raise ValueError(f"stratum {environment}/proxy={proxy} has {len(pool)} episodes, need {per_stratum}")
            chosen[environment].extend(rng.sample(pool, per_stratum))
        # Shuffled within the environment, so the proxy stratum cannot be read from the order.
        rng.shuffle(chosen[environment])
    return chosen


def render_thread(datapoint):
    """The group-chat thread as the labeler reads it: who spoke, what, and which tools ran."""
    thread = datapoint["team_states"]["agent_states"]["SelectorGroupChatManager"]["message_thread"]
    events = []
    for event in thread:
        kind = event.get("type")
        source = event.get("source", "?")
        content = event.get("content")
        if kind == "ToolCallRequestEvent":
            calls = content if isinstance(content, list) else []
            for call in calls:
                arguments = call.get("arguments", "")
                try:
                    arguments = json.dumps(json.loads(arguments), ensure_ascii=False, indent=1)
                except (TypeError, ValueError):
                    arguments = as_text(arguments)
                events.append({"kind": "call", "source": source, "tool": call.get("name", "?"),
                               "text": scrub(arguments)})
        elif kind == "ToolCallExecutionEvent":
            results = content if isinstance(content, list) else []
            for result in results:
                events.append({"kind": "result", "source": source, "tool": result.get("name", "?"),
                               "error": bool(result.get("is_error")), "text": scrub(as_text(result.get("content", "")))})
        elif kind == "ThoughtEvent":
            events.append({"kind": "thought", "source": source, "text": scrub(as_text(content))})
        elif kind == "ToolCallSummaryMessage":
            events.append({"kind": "summary", "source": source, "text": scrub(as_text(content))})
        else:
            events.append({"kind": "user" if source == "user" else "message", "source": source,
                           "text": scrub(as_text(content))})
    return events


def blind_episode(code, item):
    datapoint = load_result_file(ROOT / item["output_path"])[item["position_in_file"]]
    environment = item["environment"]
    episode = {
        "code": code,
        "environment": environment,
        "benign_task": datapoint.get("benign_task"),
        "adversarial_agent": datapoint.get("adversarial_agent"),
        "target_agent": datapoint.get("target_agent"),
        "attack_goal": (datapoint.get("adversarial_goal_used") or datapoint.get("target_action") or "").strip(),
        "events": render_thread(datapoint),
    }
    if environment == "travel_planning":
        episode["tickets"] = [scrub(as_text(t)) for t in datapoint.get("tickets") or []]
        episode["sent_messages"] = [
            {"to": scrub(as_text(m[0])), "text": scrub(as_text(m[1]))} if isinstance(m, (list, tuple)) and len(m) == 2
            else {"to": "?", "text": scrub(as_text(m))}
            for m in datapoint.get("sent_messages") or []
        ]
    return episode


def read_criteria(criteria_file):
    """The written labeling rule of each environment, between marker comments in the doc.

    `<!-- criterio:travel_planning -->` ... `<!-- /criterio -->`. The page shows it next to every
    episode, so the rule the labeler applies is the one committed before labeling.
    """
    criteria = {}
    path = Path(criteria_file) if criteria_file else None
    if path and not path.is_absolute():
        path = ROOT / path
    if not path or not path.exists():
        return criteria
    text = path.read_text(encoding="utf-8")
    for environment in ENVIRONMENTS:
        match = re.search(rf"<!-- criterio:{environment} -->(.*?)<!-- /criterio -->", text, re.DOTALL)
        if match:
            criteria[environment] = match.group(1).strip()
    return criteria


def cmd_sample(args):
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    key_path = out_dir / f"{args.batch}_CHAVE_nao_abrir.json"
    page_path = out_dir / f"{args.batch}_rotulagem.html"
    if key_path.exists() and not args.overwrite:
        raise SystemExit(f"{key_path} already exists. A batch is drawn once; use a new --batch "
                         f"(and --exclude-key {key_path.name}) or --overwrite on purpose.")

    criteria = read_criteria(args.criteria_file)
    missing = [e for e in ENVIRONMENTS if e not in criteria]
    if missing and not args.allow_missing_criteria:
        raise SystemExit(f"No written criterion for {missing} in {args.criteria_file}. The rule is "
                         "written before labeling; --allow-missing-criteria only for a preview.")

    population = build_population(args.screening_dir)
    sizes = Counter((p["environment"], p["utility_success_proxy"]) for p in population)
    chosen = draw_sample(population, args.per_stratum, args.seed, load_excluded(args.exclude_key))

    key = {
        "batch": args.batch,
        "seed": args.seed,
        "per_stratum": args.per_stratum,
        "screening_dir": args.screening_dir,
        "population_sizes": {f"{e}|{p}": sizes[(e, p)] for e in ENVIRONMENTS for p in (True, False)},
        "excluded_batches": [Path(p).name for p in args.exclude_key or []],
        "episodes": {},
    }
    episodes = []
    for environment in ENVIRONMENTS:
        for number, item in enumerate(chosen[environment], start=1):
            code = f"{args.batch}-{CODE_PREFIX[environment]}{number:02d}"
            key["episodes"][code] = item
            episodes.append(blind_episode(code, item))

    key_path.write_text(json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8")

    payload = {"batch": args.batch, "criteria": criteria, "episodes": episodes}
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", data)
    page_path.write_text(html, encoding="utf-8")

    print(f"population: {len(population)} block-L episodes")
    for environment in ENVIRONMENTS:
        print(f"  {environment}: proxy useful {sizes[(environment, True)]}, not useful {sizes[(environment, False)]}")
    print(f"sample: {len(episodes)} episodes ({args.per_stratum} per environment x proxy stratum), seed {args.seed}")
    print(f"page (open this):   {page_path}")
    print(f"key (do NOT open):  {key_path}")


# ---------------------------------------------------------------------------------------------
# score
# ---------------------------------------------------------------------------------------------

def cohen_kappa(pairs):
    n = len(pairs)
    if n == 0:
        return None
    observed = sum(1 for a, b in pairs if a == b) / n
    pa = sum(1 for a, _ in pairs if a) / n
    pb = sum(1 for _, b in pairs if b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    return None if expected == 1 else (observed - expected) / (1 - expected)


def weighted_accuracy(strata):
    """Population-weighted accuracy from per-stratum agreement, with a normal-approximation CI.

    strata: list of (population_size, labeled, agreements). Finite-population correction applied.
    When every stratum agrees 100% the variance is 0 and the interval collapses; the per-stratum
    Wilson intervals are the honest statement in that case, and the report says so.
    """
    total = sum(size for size, _, _ in strata)
    estimate = 0.0
    variance = 0.0
    for size, labeled, agreements in strata:
        if labeled == 0:
            continue
        weight = size / total
        p = agreements / labeled
        estimate += weight * p
        fpc = (size - labeled) / (size - 1) if size > 1 else 0.0
        variance += weight * weight * p * (1 - p) / labeled * fpc
    half = 1.96 * math.sqrt(variance)
    return {"p": estimate, "low": max(0.0, estimate - half), "high": min(1.0, estimate + half)}


def fmt(interval):
    return f"{interval['p']:.0%} [{interval['low']:.0%}, {interval['high']:.0%}]"


def cmd_score(args):
    key_paths = [Path(p) for p in args.key]
    label_paths = [Path(p) for p in args.labels]
    episodes, sizes = {}, {}
    for path in key_paths:
        key = json.loads(path.read_text(encoding="utf-8"))
        episodes.update(key["episodes"])
        sizes = key["population_sizes"]  # same population for every batch of one screening
    labels = {}
    for path in label_paths:
        exported = json.loads(path.read_text(encoding="utf-8"))
        labels.update(exported["labels"])

    rows = []
    for code, item in episodes.items():
        label = labels.get(code)
        if not label or label.get("useful") is None:
            continue
        if args.high_confidence_only and label.get("confidence") != "alta":
            continue
        rows.append({**item, "code": code, "manual_utility_success": bool(label["useful"]),
                     "confidence": label.get("confidence"), "note": label.get("note", ""),
                     "seconds": label.get("seconds")})
    unlabeled = sorted(set(episodes) - {r["code"] for r in rows})

    report = {"keys": [str(p) for p in key_paths], "labels": [str(p) for p in label_paths],
              "labeled": len(rows), "unlabeled": unlabeled, "environments": {}}
    print(f"labeled episodes: {len(rows)} of {len(episodes)}"
          + (" (high confidence only)" if args.high_confidence_only else ""))
    if unlabeled:
        print(f"  not labeled: {', '.join(unlabeled)}")

    all_strata = []
    for environment in ENVIRONMENTS:
        env_rows = [r for r in rows if r["environment"] == environment]
        if not env_rows:
            continue
        print(f"\n== {environment} ({len(env_rows)} labeled)")
        cm = Counter((r["utility_success_proxy"], r["manual_utility_success"]) for r in env_rows)
        print(f"  proxy useful     -> human useful {cm[(True, True)]:>3}   human NOT useful {cm[(True, False)]:>3}  (false positive)")
        print(f"  proxy NOT useful -> human useful {cm[(False, True)]:>3}  (false negative)   human NOT useful {cm[(False, False)]:>3}")

        strata = []
        env_report = {"confusion": {"tp": cm[(True, True)], "fp": cm[(True, False)],
                                    "fn": cm[(False, True)], "tn": cm[(False, False)]}}
        for proxy, name in ((True, "when the proxy says USEFUL, the human agrees"),
                            (False, "when the proxy says NOT useful, the human agrees")):
            labeled = cm[(proxy, True)] + cm[(proxy, False)]
            agreements = cm[(proxy, proxy)]
            interval = wilson_interval(agreements, labeled)
            size = sizes[f"{environment}|{proxy}"]
            strata.append((size, labeled, agreements))
            all_strata.append((size, labeled, agreements))
            print(f"  {name}: {agreements}/{labeled} = {fmt(interval)}")
            env_report["agree_when_proxy_" + ("useful" if proxy else "not_useful")] = interval

        accuracy = weighted_accuracy(strata)
        population = sum(s for s, _, _ in strata)
        human_rate = sum(
            size / population * ((cm[(proxy, True)] / labeled) if labeled else 0.0)
            for (size, labeled, _), proxy in zip(strata, (True, False))
        )
        proxy_rate = strata[0][0] / population
        kappa = cohen_kappa([(r["utility_success_proxy"], r["manual_utility_success"]) for r in env_rows])
        print(f"  accuracy weighted to the population ({population} episodes): {fmt(accuracy)}")
        print(f"  utility rate: proxy {proxy_rate:.0%}, estimated by the human {human_rate:.0%}"
              f"  ({'proxy optimistic' if proxy_rate > human_rate else 'proxy strict' if proxy_rate < human_rate else 'equal'})")
        print(f"  Cohen's kappa on the sample (stratified, read with care): "
              + ("n/a" if kappa is None else f"{kappa:.2f}"))
        env_report.update({"weighted_accuracy": accuracy, "population": population,
                           "proxy_utility_rate": proxy_rate, "human_utility_rate_estimate": human_rate,
                           "kappa_sample": kappa})
        report["environments"][environment] = env_report

    if len({e for e in report["environments"]}) > 1:
        overall = weighted_accuracy(all_strata)
        report["weighted_accuracy_overall"] = overall
        print(f"\n== both environments, weighted: {fmt(overall)}")

    disagreements = [r for r in rows if r["utility_success_proxy"] != r["manual_utility_success"]]
    print(f"\n== disagreements ({len(disagreements)}): read these to see WHERE the proxy fails")
    for r in sorted(disagreements, key=lambda r: r["code"]):
        side = "proxy useful, human not" if r["utility_success_proxy"] else "proxy not, human useful"
        print(f"  {r['code']}  {r['model_tag']:<18} case {r['case_id']:<3} {side}  [{r.get('confidence')}]  {r['note']}")
        print(f"         {r['output_path']}")
    report["disagreements"] = [{k: r[k] for k in ("code", "model_tag", "environment", "case_id", "output_path",
                                                    "utility_success_proxy", "manual_utility_success",
                                                    "confidence", "note")} for r in disagreements]

    seconds = [r["seconds"] for r in rows if isinstance(r.get("seconds"), (int, float))]
    if seconds:
        report["labeling_seconds_total"] = sum(seconds)
        print(f"\nlabeling time: {sum(seconds) / 60:.0f} min, {sum(seconds) / len(seconds) / 60:.1f} min per episode")

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nreport: {args.out_json}")
    if args.out_csv:
        # Same column names as create_utility_labeling_sample.py, so
        # evaluate_utility_proxy_agreement.py reads it too (unweighted numbers only).
        with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
            fields = ["code", "model_tag", "environment", "case_id", "output_path", "utility_success_proxy",
                      "attack_success", "manual_utility_success", "confidence", "note", "seconds"]
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        print(f"csv: {args.out_csv}")


def main():
    parser = ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    sample = sub.add_parser("sample", help="draw the blind sample and write the labeling page")
    sample.add_argument("--screening-dir", default="evaluation_results/screening")
    sample.add_argument("--per-stratum", type=int, default=10,
                        help="episodes per environment x proxy-verdict stratum (4 strata)")
    sample.add_argument("--seed", type=int, default=20260930)
    sample.add_argument("--batch", default="lote1")
    sample.add_argument("--out-dir", default="evaluation_results/validacao_proxy")
    sample.add_argument("--criteria-file", default="docs/02-experimentos/VALIDACAO_PROXY_UTILIDADE.md")
    sample.add_argument("--exclude-key", action="append",
                        help="key of an earlier batch; its episodes are not drawn again")
    sample.add_argument("--allow-missing-criteria", action="store_true")
    sample.add_argument("--overwrite", action="store_true")

    score = sub.add_parser("score", help="join exported labels with the key and report agreement")
    score.add_argument("--key", action="append", required=True)
    score.add_argument("--labels", action="append", required=True)
    score.add_argument("--high-confidence-only", action="store_true")
    score.add_argument("--out-json")
    score.add_argument("--out-csv")

    args = parser.parse_args()
    {"sample": cmd_sample, "score": cmd_score}[args.command](args)


if __name__ == "__main__":
    main()
