from argparse import ArgumentParser
from pathlib import Path
import json
import re
import statistics
import sys
from collections import Counter, defaultdict

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
EVALUATION_DIR = ROOT / "evaluation"
sys.path.insert(0, str(EVALUATION_DIR))

from evaluation_functions import evaluate_datapoint  # noqa: E402
from trajectory_diagnostics import diagnose_trajectory  # noqa: E402


def percent(value):
    return f"{value * 100:.2f}%"


def rate(numerator, denominator):
    if denominator == 0:
        return 0.0
    return numerator / denominator


def bool_count(values):
    return sum(1 for value in values if value)


def mean(values):
    values = [v for v in values if v is not None]
    if not values:
        return 0.0
    return sum(values) / len(values)


def stdev(values):
    values = [v for v in values if v is not None]
    if len(values) < 2:
        return 0.0
    return statistics.stdev(values)


def coefficient_of_variation(values):
    values = [v for v in values if v is not None]
    m = mean(values)
    if not values or m == 0:
        return 0.0
    return stdev(values) / m


def parse_run_label(run_label):
    run_label = str(run_label or "")
    match = re.match(r"^robust_([ABC])_(.+)_r(\d+)$", run_label)
    if not match:
        return {
            "robust_method": None,
            "robust_condition": None,
            "robust_repeat": None,
        }
    return {
        "robust_method": match.group(1),
        "robust_condition": match.group(2),
        "robust_repeat": int(match.group(3)),
    }


def read_manifest_paths(manifest_path):
    """Read a robustness manifest JSONL and return only the output paths of successful runs.

    Using the manifest guarantees isolated analysis of exactly the files produced by one
    robustness sweep, instead of accidentally scanning the whole results/ directory.
    """
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


def resolve_input_files(paths):
    files = []
    for raw_path in paths:
        path = Path(raw_path)
        if not path.is_absolute():
            path = ROOT / path

        if path.is_dir():
            print(
                f"Warning: analyzing all JSON files under directory {path}. "
                f"Use --manifest-path for isolated robustness analysis.",
                file=sys.stderr,
            )
            files.extend(sorted(path.rglob("*.json")))
        elif any(ch in str(path) for ch in "*?[]"):
            files.extend(sorted(Path().glob(str(path))))
        else:
            files.append(path)

    unique = []
    seen = set()
    for file_path in files:
        file_path = file_path.resolve()
        if file_path in seen:
            continue
        seen.add(file_path)
        if file_path.exists() and file_path.is_file():
            unique.append(file_path)
    return unique


def load_result_file(path):
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise ValueError(f"Expected list or dict in {path}")
    return data


def case_key(datapoint):
    if datapoint.get("dataset_index") is not None:
        return str(datapoint.get("dataset_index"))
    if datapoint.get("id") is not None:
        return str(datapoint.get("id"))
    return str(datapoint.get("target_action"))


def evaluate_file(path, environment):
    records = []
    data = load_result_file(path)

    for case_position, datapoint in enumerate(data, start=1):
        evaluation = evaluate_datapoint(datapoint, environment)
        diagnostics = diagnose_trajectory(
            datapoint,
            environment,
            attack_success=evaluation["attack_success"],
            utility_success=evaluation["utility_success"],
        )

        run_label = datapoint.get("run_label")
        label_info = parse_run_label(run_label)

        record = {
            "source_file": str(path),
            "case_position_in_file": case_position,
            "case_key": case_key(datapoint),
            "id": datapoint.get("id"),
            "dataset_index": datapoint.get("dataset_index"),
            "model_client": datapoint.get("model_client"),
            "environment": datapoint.get("environment", environment),
            "safe": datapoint.get("safe"),
            "guardian": datapoint.get("guardian"),
            "run_label": run_label,
            "robust_method": label_info["robust_method"],
            "robust_condition": label_info["robust_condition"],
            "robust_repeat": label_info["robust_repeat"],
            "benign_task": datapoint.get("benign_task"),
            "trajectory_perturbation": datapoint.get("trajectory_perturbation", "none"),
            "target_agent": datapoint.get("target_agent"),
            "adversarial_agent": datapoint.get("adversarial_agent"),
            "target_action": datapoint.get("target_action"),
            "keywords": datapoint.get("keywords"),
            "attack_success": evaluation["attack_success"],
            "security_success": evaluation["security_success"],
            "utility_success": evaluation["utility_success"],
            "quadrant": evaluation["quadrant"],
            "trajectory_length": diagnostics.get("trajectory_length"),
            "tool_call_request_count": diagnostics.get("tool_call_request_count"),
            "tool_call_execution_count": diagnostics.get("tool_call_execution_count"),
            "malicious_tool_call_count": diagnostics.get("malicious_tool_call_count"),
            "failure_mode": diagnostics.get("failure_mode"),
            "attack_introduced": diagnostics.get("attack_introduced"),
            "target_agent_reached_after_attack": diagnostics.get("target_agent_reached_after_attack"),
            "target_tool_called": diagnostics.get("target_tool_called"),
            "target_tool_executed_successfully": diagnostics.get("target_tool_executed_successfully"),
            "refusal_detected": diagnostics.get("refusal_detected"),
            "target_refusal_detected": diagnostics.get("target_refusal_detected"),
            "text_only_attack": diagnostics.get("text_only_attack"),
            "non_operationalized_attack": diagnostics.get("non_operationalized_attack"),
            "propagated_but_not_executed": diagnostics.get("propagated_but_not_executed"),
        }
        records.append(record)

    return records


def summarize_observations(records):
    total = len(records)
    attack_success_count = bool_count(r["attack_success"] for r in records)
    utility_success_count = bool_count(r["utility_success"] for r in records)
    security_success_count = bool_count(r["security_success"] for r in records)

    quadrant_counts = Counter(r["quadrant"] for r in records)
    failure_mode_counts = Counter(r["failure_mode"] for r in records)

    return {
        "total_observations": total,
        "unique_cases": len(set(r["case_key"] for r in records)),
        "attack_success_count": attack_success_count,
        "security_success_count": security_success_count,
        "utility_success_count": utility_success_count,
        "attack_success_rate": rate(attack_success_count, total),
        "security_rate": rate(security_success_count, total),
        "utility_rate": rate(utility_success_count, total),
        "quadrant_counts": dict(quadrant_counts),
        "failure_mode_counts": dict(failure_mode_counts),
        "mean_trajectory_length": mean(r["trajectory_length"] for r in records),
        "mean_tool_call_request_count": mean(r["tool_call_request_count"] for r in records),
        "mean_tool_call_execution_count": mean(r["tool_call_execution_count"] for r in records),
        "mean_malicious_tool_call_count": mean(r["malicious_tool_call_count"] for r in records),
    }


def summarize_stability(records):
    by_case = defaultdict(list)
    for record in records:
        by_case[record["case_key"]].append(record)

    case_rows = []
    for key, rows in sorted(by_case.items(), key=lambda item: str(item[0])):
        attack_values = {bool(r["attack_success"]) for r in rows}
        utility_values = {bool(r["utility_success"]) for r in rows}
        quadrant_values = {r["quadrant"] for r in rows}
        failure_modes = {r["failure_mode"] for r in rows}
        lengths = [r["trajectory_length"] for r in rows if r["trajectory_length"] is not None]
        tool_requests = [r["tool_call_request_count"] for r in rows if r["tool_call_request_count"] is not None]
        malicious_tool_calls = [r["malicious_tool_call_count"] for r in rows if r["malicious_tool_call_count"] is not None]

        case_rows.append({
            "case_key": key,
            "observations": len(rows),
            "target_agent": rows[0].get("target_agent"),
            "adversarial_agent": rows[0].get("adversarial_agent"),
            "target_action": rows[0].get("target_action"),
            "attack_flip": len(attack_values) > 1,
            "utility_flip": len(utility_values) > 1,
            "quadrant_stable": len(quadrant_values) == 1,
            "failure_mode_stable": len(failure_modes) == 1,
            "attack_success_values": "/".join(str(v) for v in sorted(attack_values)),
            "utility_success_values": "/".join(str(v) for v in sorted(utility_values)),
            "quadrant_values": "/".join(sorted(str(v) for v in quadrant_values)),
            "failure_mode_values": "/".join(sorted(str(v) for v in failure_modes)),
            "mean_trajectory_length": mean(lengths),
            "trajectory_length_stdev": stdev(lengths),
            "trajectory_length_cv": coefficient_of_variation(lengths),
            "mean_tool_call_request_count": mean(tool_requests),
            "tool_call_request_stdev": stdev(tool_requests),
            "mean_malicious_tool_call_count": mean(malicious_tool_calls),
        })

    total_cases = len(case_rows)
    attack_flip_count = bool_count(row["attack_flip"] for row in case_rows)
    utility_flip_count = bool_count(row["utility_flip"] for row in case_rows)
    quadrant_stable_count = bool_count(row["quadrant_stable"] for row in case_rows)
    failure_mode_stable_count = bool_count(row["failure_mode_stable"] for row in case_rows)

    metrics = {
        "unique_cases": total_cases,
        "attack_flip_count": attack_flip_count,
        "utility_flip_count": utility_flip_count,
        "quadrant_stable_count": quadrant_stable_count,
        "failure_mode_stable_count": failure_mode_stable_count,
        "attack_flip_rate": rate(attack_flip_count, total_cases),
        "utility_flip_rate": rate(utility_flip_count, total_cases),
        "quadrant_stability_rate": rate(quadrant_stable_count, total_cases),
        "failure_mode_stability_rate": rate(failure_mode_stable_count, total_cases),
        "mean_trajectory_length_stdev": mean(row["trajectory_length_stdev"] for row in case_rows),
        "mean_trajectory_length_cv": mean(row["trajectory_length_cv"] for row in case_rows),
        "mean_tool_call_request_stdev": mean(row["tool_call_request_stdev"] for row in case_rows),
    }

    return metrics, case_rows


def summarize_by_condition(records):
    by_condition = defaultdict(list)
    for record in records:
        condition_key = (
            record.get("robust_method") or "unknown",
            record.get("robust_condition") or "unknown",
            record.get("trajectory_perturbation") or "none",
        )
        by_condition[condition_key].append(record)

    condition_rows = []
    for (method, condition, trajectory_perturbation), rows in sorted(by_condition.items()):
        total = len(rows)
        attack_success_count = bool_count(r["attack_success"] for r in rows)
        utility_success_count = bool_count(r["utility_success"] for r in rows)
        quadrant_counts = Counter(r["quadrant"] for r in rows)

        condition_rows.append({
            "robust_method": method,
            "robust_condition": condition,
            "trajectory_perturbation": trajectory_perturbation,
            "observations": total,
            "unique_cases": len(set(r["case_key"] for r in rows)),
            "attack_success_rate": rate(attack_success_count, total),
            "utility_rate": rate(utility_success_count, total),
            "safe_and_useful_rate": rate(quadrant_counts.get("safe_and_useful", 0), total),
            "compromised_but_useful_rate": rate(quadrant_counts.get("compromised_but_useful", 0), total),
            "safe_but_useless_rate": rate(quadrant_counts.get("safe_but_useless", 0), total),
            "compromised_and_useless_rate": rate(quadrant_counts.get("compromised_and_useless", 0), total),
            "mean_trajectory_length": mean(r["trajectory_length"] for r in rows),
            "mean_malicious_tool_call_count": mean(r["malicious_tool_call_count"] for r in rows),
        })

    return condition_rows


def _select_baseline(method, rows):
    """Select the baseline observation for a case under a given method.

    Returns (baseline_row_or_None, non_baseline_rows, rule_string).
    Baseline selection is method-specific and always recorded in the output so the
    comparison is auditable.
    """
    def min_repeat(candidates):
        with_repeat = [r for r in candidates if r.get("robust_repeat") is not None]
        if with_repeat:
            return min(with_repeat, key=lambda r: r["robust_repeat"])
        return candidates[0] if candidates else None

    if method == "A":
        rule = "method_A: earliest repeat (min robust_repeat) of the single condition"
        baseline = min_repeat(rows)
        non_baseline = [r for r in rows if r is not baseline]
        return baseline, non_baseline, rule

    if method == "C":
        rule = "method_C: perturbation 'none' (earliest repeat); other perturbations compared against it"
        none_rows = [
            r for r in rows
            if (r.get("trajectory_perturbation") or "none") == "none" or str(r.get("robust_condition")) == "none"
        ]
        baseline = min_repeat(none_rows)
        non_baseline = [
            r for r in rows
            if (r.get("trajectory_perturbation") or "none") != "none" and str(r.get("robust_condition")) != "none"
        ]
        return baseline, non_baseline, rule

    if method == "B":
        base_rows = [r for r in rows if str(r.get("robust_condition")) == "base"]
        if base_rows:
            rule = "method_B: variant 'base' (earliest repeat); other variants compared against it"
            baseline = min_repeat(base_rows)
        else:
            rule = "method_B: no 'base' variant present, fallback to first observed condition"
            baseline = min_repeat(rows)
        non_baseline = [r for r in rows if r is not baseline]
        return baseline, non_baseline, rule

    rule = "unknown_method: first observed observation used as baseline"
    baseline = min_repeat(rows)
    non_baseline = [r for r in rows if r is not baseline]
    return baseline, non_baseline, rule


def summarize_baseline_disagreement(records):
    """For each method, compare non-baseline observations against a per-case baseline.

    Answers: "If I had run only once (the baseline), how many conclusions would change
    across repetitions / perturbations / paraphrases?"
    """
    by_method_case = defaultdict(lambda: defaultdict(list))
    for record in records:
        method = record.get("robust_method") or "unknown"
        by_method_case[method][record["case_key"]].append(record)

    result = {}
    for method, cases in sorted(by_method_case.items()):
        compared = 0
        attack_disagree = 0
        utility_disagree = 0
        quadrant_disagree = 0
        failure_disagree = 0
        abs_deltas = []
        rel_deltas = []
        rule_used = None
        cases_with_baseline = 0

        for _, rows in cases.items():
            baseline, non_baseline, rule = _select_baseline(method, rows)
            rule_used = rule
            if baseline is None or not non_baseline:
                continue
            cases_with_baseline += 1

            base_len = baseline.get("trajectory_length")
            for obs in non_baseline:
                compared += 1
                if bool(obs.get("attack_success")) != bool(baseline.get("attack_success")):
                    attack_disagree += 1
                if bool(obs.get("utility_success")) != bool(baseline.get("utility_success")):
                    utility_disagree += 1
                if obs.get("quadrant") != baseline.get("quadrant"):
                    quadrant_disagree += 1
                if obs.get("failure_mode") != baseline.get("failure_mode"):
                    failure_disagree += 1

                obs_len = obs.get("trajectory_length")
                if base_len is not None and obs_len is not None:
                    delta = abs(obs_len - base_len)
                    abs_deltas.append(delta)
                    if base_len != 0:
                        rel_deltas.append(delta / base_len)

        result[method] = {
            "baseline_selection_rule": rule_used,
            "cases_with_baseline": cases_with_baseline,
            "comparisons": compared,
            "baseline_attack_disagreement_rate": rate(attack_disagree, compared),
            "baseline_utility_disagreement_rate": rate(utility_disagree, compared),
            "baseline_quadrant_disagreement_rate": rate(quadrant_disagree, compared),
            "baseline_failure_mode_disagreement_rate": rate(failure_disagree, compared),
            "mean_baseline_trajectory_length_absolute_delta": mean(abs_deltas),
            "mean_baseline_trajectory_length_relative_delta": mean(rel_deltas),
        }

    return result


def print_report(observation_metrics, stability_metrics, condition_rows, baseline_disagreement=None):
    print("Robustness Evaluation")
    print("=" * 100)
    print(f"Total observations: {observation_metrics['total_observations']}")
    print(f"Unique cases: {observation_metrics['unique_cases']}")
    print()
    print(f"Attack Success Rate: {percent(observation_metrics['attack_success_rate'])} ({observation_metrics['attack_success_count']}/{observation_metrics['total_observations']})")
    print(f"Security Rate: {percent(observation_metrics['security_rate'])} ({observation_metrics['security_success_count']}/{observation_metrics['total_observations']})")
    print(f"Utility Rate: {percent(observation_metrics['utility_rate'])} ({observation_metrics['utility_success_count']}/{observation_metrics['total_observations']})")
    print()
    print("Stability across repeated/perturbed observations:")
    print(f"Attack Flip Rate: {percent(stability_metrics['attack_flip_rate'])} ({stability_metrics['attack_flip_count']}/{stability_metrics['unique_cases']})")
    print(f"Utility Flip Rate: {percent(stability_metrics['utility_flip_rate'])} ({stability_metrics['utility_flip_count']}/{stability_metrics['unique_cases']})")
    print(f"Quadrant Stability Rate: {percent(stability_metrics['quadrant_stability_rate'])} ({stability_metrics['quadrant_stable_count']}/{stability_metrics['unique_cases']})")
    print(f"Failure-Mode Stability Rate: {percent(stability_metrics['failure_mode_stability_rate'])} ({stability_metrics['failure_mode_stable_count']}/{stability_metrics['unique_cases']})")
    print(f"Mean Trajectory-Length StdDev: {stability_metrics['mean_trajectory_length_stdev']:.2f}")
    print(f"Mean Trajectory-Length CV: {stability_metrics['mean_trajectory_length_cv']:.2f}")
    print()
    print("Condition-level summary:")
    for row in condition_rows:
        print(
            f"- method={row['robust_method']} condition={row['robust_condition']} "
            f"perturbation={row['trajectory_perturbation']} | "
            f"ASR={percent(row['attack_success_rate'])} | "
            f"Utility={percent(row['utility_rate'])} | "
            f"Safe+Useful={percent(row['safe_and_useful_rate'])} | "
            f"n={row['observations']}"
        )

    if baseline_disagreement:
        print()
        print("Baseline disagreement (single-run vs repeated/perturbed):")
        for method, m in sorted(baseline_disagreement.items()):
            if not m.get("comparisons"):
                continue
            print(f"- method={method} | rule: {m['baseline_selection_rule']}")
            print(
                f"    comparisons={m['comparisons']} "
                f"attack={percent(m['baseline_attack_disagreement_rate'])} "
                f"utility={percent(m['baseline_utility_disagreement_rate'])} "
                f"quadrant={percent(m['baseline_quadrant_disagreement_rate'])} "
                f"failure_mode={percent(m['baseline_failure_mode_disagreement_rate'])}"
            )
            print(
                f"    traj-length delta: abs={m['mean_baseline_trajectory_length_absolute_delta']:.2f} "
                f"rel={m['mean_baseline_trajectory_length_relative_delta']:.2f}"
            )


def main():
    parser = ArgumentParser(
        description=(
            "Analyze robustness results from BAD-ACTS repeated/perturbed runs. "
            "Prefer --manifest-path to analyze exactly the files produced by one sweep."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help=(
            "Result JSON files, globs or directories. Directories are searched recursively for *.json "
            "(with a warning). Optional when --manifest-path is given."
        ),
    )
    parser.add_argument(
        "--manifest-path",
        type=str,
        default=None,
        help="Robustness manifest JSONL. Only successful runs (return_code == 0) are analyzed.",
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
    # Defaults are resolved after parsing: when --manifest-path is given and an output is not
    # explicitly set, the manifest stem is appended so different methods don't overwrite each
    # other (e.g. robustness_observations_manifest_A_id1.csv).
    parser.add_argument("--out-csv", type=str, default=None)
    parser.add_argument("--case-csv", type=str, default=None)
    parser.add_argument("--condition-csv", type=str, default=None)
    parser.add_argument("--out-json", type=str, default=None)

    args = parser.parse_args()

    manifest_suffix = f"_{Path(args.manifest_path).stem}" if args.manifest_path else ""
    if args.out_csv is None:
        args.out_csv = f"evaluation_results/robustness_observations{manifest_suffix}.csv"
    if args.case_csv is None:
        args.case_csv = f"evaluation_results/robustness_case_stability{manifest_suffix}.csv"
    if args.condition_csv is None:
        args.condition_csv = f"evaluation_results/robustness_condition_summary{manifest_suffix}.csv"
    if args.out_json is None:
        args.out_json = f"evaluation_results/robustness_summary{manifest_suffix}.json"

    input_paths = list(args.paths)
    if args.manifest_path:
        manifest_paths = read_manifest_paths(args.manifest_path)
        if not manifest_paths:
            raise FileNotFoundError(
                f"No successful runs (return_code == 0 with an output_path) found in manifest: {args.manifest_path}"
            )
        input_paths.extend(manifest_paths)

    if not input_paths:
        raise ValueError("No inputs given. Provide result paths and/or --manifest-path.")

    files = resolve_input_files(input_paths)
    if not files:
        raise FileNotFoundError("No result JSON files found.")

    records = []
    for path in files:
        records.extend(evaluate_file(path, args.environment))

    if not records:
        raise ValueError("No datapoints found in input files.")

    observation_metrics = summarize_observations(records)
    stability_metrics, case_rows = summarize_stability(records)
    condition_rows = summarize_by_condition(records)
    baseline_disagreement = summarize_baseline_disagreement(records)

    print_report(observation_metrics, stability_metrics, condition_rows, baseline_disagreement)

    # Small-n exploratory warnings.
    if observation_metrics["unique_cases"] == 1:
        print(
            "Warning: only one unique case was analyzed. Flip rates are binary and should be "
            "interpreted as exploratory, not statistically meaningful.",
            file=sys.stderr,
        )
    max_obs_per_case = max((row["observations"] for row in case_rows), default=0)
    if max_obs_per_case < 2:
        print(
            "Warning: at most one observation per case. Stability/flip metrics cannot be computed "
            "meaningfully; increase --repeats or the number of conditions.",
            file=sys.stderr,
        )

    out_csv = Path(args.out_csv)
    if not out_csv.is_absolute():
        out_csv = ROOT / out_csv
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(out_csv, index=False)
    print()
    print(f"Observation CSV saved to: {out_csv}")

    case_csv = Path(args.case_csv)
    if not case_csv.is_absolute():
        case_csv = ROOT / case_csv
    case_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(case_rows).to_csv(case_csv, index=False)
    print(f"Case-stability CSV saved to: {case_csv}")

    condition_csv = Path(args.condition_csv)
    if not condition_csv.is_absolute():
        condition_csv = ROOT / condition_csv
    condition_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(condition_rows).to_csv(condition_csv, index=False)
    print(f"Condition-summary CSV saved to: {condition_csv}")

    out_json = Path(args.out_json)
    if not out_json.is_absolute():
        out_json = ROOT / out_json
    out_json.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "input_files": [str(path) for path in files],
        "manifest_path": args.manifest_path,
        "environment": args.environment,
        "observation_metrics": observation_metrics,
        "stability_metrics": stability_metrics,
        "baseline_disagreement": baseline_disagreement,
        "condition_rows": condition_rows,
        "case_rows": case_rows,
    }
    with out_json.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"JSON summary saved to: {out_json}")


if __name__ == "__main__":
    main()
