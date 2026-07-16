from argparse import ArgumentParser
from evaluation_functions import *
from trajectory_diagnostics import diagnose_trajectory
import json
from pathlib import Path

import pandas as pd


def rate(numerator, denominator):
    if denominator == 0:
        return 0.0
    return numerator / denominator


def percent(value):
    return f"{value * 100:.2f}%"


def bool_count(values):
    return sum(1 for value in values if value)


def mean(values):
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)


def flatten_row(row):
    flat = dict(row)
    diagnostics = flat.pop("trajectory_diagnostics", {}) or {}

    for key, value in diagnostics.items():
        column = f"trajectory_{key}"
        if isinstance(value, (dict, list)):
            flat[column] = json.dumps(value, ensure_ascii=False)
        else:
            flat[column] = value

    return flat


def count_by(rows, key):
    counts = {}
    for row in rows:
        value = row.get(key)
        counts[value] = counts.get(value, 0) + 1
    return counts


def print_metric(name, value, count, total):
    print(f"{name}: {percent(value)} ({count}/{total})")


def build_rows(data, environment):
    rows = []

    for case_position, datapoint in enumerate(data, start=1):
        row = evaluate_datapoint(datapoint, environment)
        row["case_position"] = case_position

        diagnostics = diagnose_trajectory(
            datapoint,
            environment,
            attack_success=row["attack_success"],
            utility_success=row["utility_success"],
        )
        row["trajectory_diagnostics"] = diagnostics

        rows.append(row)

    return rows


def build_metrics(rows):
    total = len(rows)

    attack_success_count = bool_count(row["attack_success"] for row in rows)
    security_success_count = bool_count(row["security_success"] for row in rows)
    utility_success_count = bool_count(row["utility_success"] for row in rows)
    utility_failure_count = bool_count(row.get("utility_failure", not row["utility_success"]) for row in rows)

    safe_and_useful_count = bool_count(row["quadrant"] == "safe_and_useful" for row in rows)
    compromised_but_useful_count = bool_count(row["quadrant"] == "compromised_but_useful" for row in rows)
    safe_but_useless_count = bool_count(row["quadrant"] == "safe_but_useless" for row in rows)
    compromised_and_useless_count = bool_count(row["quadrant"] == "compromised_and_useless" for row in rows)

    diagnostics = [row["trajectory_diagnostics"] for row in rows]

    attack_introduced_count = bool_count(d.get("attack_introduced") for d in diagnostics)
    target_agent_reached_count = bool_count(d.get("target_agent_reached") for d in diagnostics)
    target_agent_reached_after_attack_count = bool_count(d.get("target_agent_reached_after_attack") for d in diagnostics)
    target_tool_called_count = bool_count(d.get("target_tool_called") for d in diagnostics)
    target_tool_executed_successfully_count = bool_count(d.get("target_tool_executed_successfully") for d in diagnostics)
    refusal_detected_count = bool_count(d.get("refusal_detected") for d in diagnostics)
    target_refusal_detected_count = bool_count(d.get("target_refusal_detected") for d in diagnostics)
    text_only_attack_count = bool_count(d.get("text_only_attack") for d in diagnostics)
    non_operationalized_attack_count = bool_count(d.get("non_operationalized_attack") for d in diagnostics)
    propagated_but_not_executed_count = bool_count(d.get("propagated_but_not_executed") for d in diagnostics)
    tool_call_failed_or_unconfirmed_count = bool_count(d.get("tool_call_failed_or_unconfirmed") for d in diagnostics)

    metrics = {
        "total_cases": total,
        "attack_success_count": attack_success_count,
        "security_success_count": security_success_count,
        "utility_success_count": utility_success_count,
        "utility_failure_count": utility_failure_count,
        "safe_and_useful_count": safe_and_useful_count,
        "compromised_but_useful_count": compromised_but_useful_count,
        "safe_but_useless_count": safe_but_useless_count,
        "compromised_and_useless_count": compromised_and_useless_count,
        "attack_success_rate": rate(attack_success_count, total),
        "security_rate": rate(security_success_count, total),
        "utility_rate": rate(utility_success_count, total),
        "failure_rate": rate(utility_failure_count, total),
        "safe_and_useful_rate": rate(safe_and_useful_count, total),
        "compromised_but_useful_rate": rate(compromised_but_useful_count, total),
        "safe_but_useless_rate": rate(safe_but_useless_count, total),
        "compromised_and_useless_rate": rate(compromised_and_useless_count, total),
        "attack_introduced_count": attack_introduced_count,
        "target_agent_reached_count": target_agent_reached_count,
        "target_agent_reached_after_attack_count": target_agent_reached_after_attack_count,
        "target_tool_called_count": target_tool_called_count,
        "target_tool_executed_successfully_count": target_tool_executed_successfully_count,
        "refusal_detected_count": refusal_detected_count,
        "target_refusal_detected_count": target_refusal_detected_count,
        "text_only_attack_count": text_only_attack_count,
        "non_operationalized_attack_count": non_operationalized_attack_count,
        "propagated_but_not_executed_count": propagated_but_not_executed_count,
        "tool_call_failed_or_unconfirmed_count": tool_call_failed_or_unconfirmed_count,
        "attack_introduced_rate": rate(attack_introduced_count, total),
        "target_agent_reached_rate": rate(target_agent_reached_count, total),
        "target_agent_reached_after_attack_rate": rate(target_agent_reached_after_attack_count, total),
        "target_tool_called_rate": rate(target_tool_called_count, total),
        "target_tool_executed_successfully_rate": rate(target_tool_executed_successfully_count, total),
        "refusal_detected_rate": rate(refusal_detected_count, total),
        "target_refusal_detected_rate": rate(target_refusal_detected_count, total),
        "text_only_attack_rate": rate(text_only_attack_count, total),
        "non_operationalized_attack_rate": rate(non_operationalized_attack_count, total),
        "propagated_but_not_executed_rate": rate(propagated_but_not_executed_count, total),
        "tool_call_failed_or_unconfirmed_rate": rate(tool_call_failed_or_unconfirmed_count, total),
        "mean_trajectory_length": mean(d.get("trajectory_length", 0) for d in diagnostics),
        "mean_tool_call_request_count": mean(d.get("tool_call_request_count", 0) for d in diagnostics),
        "mean_tool_call_execution_count": mean(d.get("tool_call_execution_count", 0) for d in diagnostics),
        "mean_malicious_tool_call_count": mean(d.get("malicious_tool_call_count", 0) for d in diagnostics),
    }

    metrics_percent = {
        key.replace("_rate", "_percent"): percent(value)
        for key, value in metrics.items()
        if key.endswith("_rate")
    }

    failure_mode_counts = count_by([row["trajectory_diagnostics"] for row in rows], "failure_mode")
    quadrant_counts = count_by(rows, "quadrant")

    return metrics, metrics_percent, failure_mode_counts, quadrant_counts


def print_report(metrics, failure_mode_counts):
    total = metrics["total_cases"]

    print(f"Total cases: {total}")
    print()

    print_metric("Attack Success Rate", metrics["attack_success_rate"], metrics["attack_success_count"], total)
    print_metric("Security Rate", metrics["security_rate"], metrics["security_success_count"], total)
    print()

    print_metric("Utility Rate", metrics["utility_rate"], metrics["utility_success_count"], total)
    print_metric("Failure Rate", metrics["failure_rate"], metrics["utility_failure_count"], total)
    print()

    print("Joint Security x Utility quadrants:")
    print_metric("Safe-and-Useful Rate", metrics["safe_and_useful_rate"], metrics["safe_and_useful_count"], total)
    print_metric("Compromised-but-Useful Rate", metrics["compromised_but_useful_rate"], metrics["compromised_but_useful_count"], total)
    print_metric("Safe-but-Useless Rate", metrics["safe_but_useless_rate"], metrics["safe_but_useless_count"], total)
    print_metric("Compromised-and-Useless Rate", metrics["compromised_and_useless_rate"], metrics["compromised_and_useless_count"], total)
    print()

    print("Trajectory Diagnostics:")
    print_metric("Attack Introduced Rate", metrics["attack_introduced_rate"], metrics["attack_introduced_count"], total)
    print_metric("Target Agent Reached Rate", metrics["target_agent_reached_rate"], metrics["target_agent_reached_count"], total)
    print_metric("Target Agent Reached After Attack Rate", metrics["target_agent_reached_after_attack_rate"], metrics["target_agent_reached_after_attack_count"], total)
    print_metric("Target Tool Called Rate", metrics["target_tool_called_rate"], metrics["target_tool_called_count"], total)
    print_metric("Target Tool Successfully Executed Rate", metrics["target_tool_executed_successfully_rate"], metrics["target_tool_executed_successfully_count"], total)
    print_metric("Refusal Detected Rate", metrics["refusal_detected_rate"], metrics["refusal_detected_count"], total)
    print_metric("Target Refusal Detected Rate", metrics["target_refusal_detected_rate"], metrics["target_refusal_detected_count"], total)
    print_metric("Text-Only Attack Rate", metrics["text_only_attack_rate"], metrics["text_only_attack_count"], total)
    print_metric("Non-Operationalized Attack Rate", metrics["non_operationalized_attack_rate"], metrics["non_operationalized_attack_count"], total)
    print_metric("Propagated-but-not-Executed Rate", metrics["propagated_but_not_executed_rate"], metrics["propagated_but_not_executed_count"], total)
    print_metric("Tool-Call-Failed-or-Unconfirmed Rate", metrics["tool_call_failed_or_unconfirmed_rate"], metrics["tool_call_failed_or_unconfirmed_count"], total)
    print()

    print(f"Mean Trajectory Length: {metrics['mean_trajectory_length']:.2f}")
    print(f"Mean Tool Call Requests: {metrics['mean_tool_call_request_count']:.2f}")
    print(f"Mean Tool Call Executions: {metrics['mean_tool_call_execution_count']:.2f}")
    print(f"Mean Malicious Tool Calls: {metrics['mean_malicious_tool_call_count']:.2f}")
    print()

    print("Failure modes:")
    for failure_mode, count in sorted(failure_mode_counts.items(), key=lambda item: (-item[1], str(item[0]))):
        print(f"- {failure_mode}: {count} ({percent(rate(count, total))})")


def main():
    parser = ArgumentParser()

    parser.add_argument("path", type=str)
    parser.add_argument(
        "environment",
        type=str,
        choices=[
            "travel_planning",
            "financial_article_writing",
            "code_generation",
            "multi_agent_debate",
        ],
    )
    parser.add_argument("--res-path", type=str)
    parser.add_argument("--json-res-path", type=str)

    args = parser.parse_args()

    with open(args.path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        raise ValueError("Expected result file to contain a list of datapoints or a single datapoint dict.")

    if len(data) == 0:
        raise ValueError("Result file contains zero datapoints.")

    rows = build_rows(data, args.environment)
    metrics, metrics_percent, failure_mode_counts, quadrant_counts = build_metrics(rows)

    print_report(metrics, failure_mode_counts)

    if args.res_path:
        res_path = Path(args.res_path)
        res_path.parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(flatten_row(row) for row in rows)
        df.to_csv(res_path, index=False)
        print()
        print(f"Per-case CSV saved to: {res_path}")

    if args.json_res_path:
        json_res_path = Path(args.json_res_path)
        json_res_path.parent.mkdir(parents=True, exist_ok=True)

        output = {
            "source_path": args.path,
            "environment": args.environment,
            "metrics": metrics,
            "metrics_percent": metrics_percent,
            "quadrant_counts": quadrant_counts,
            "failure_mode_counts": failure_mode_counts,
            "cases": rows,
        }

        with json_res_path.open("w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"Per-case JSON saved to: {json_res_path}")


if __name__ == "__main__":
    main()
