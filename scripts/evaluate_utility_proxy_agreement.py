"""Measure agreement between the deterministic utility proxy and manual labels.

Reads a CSV produced by create_utility_labeling_sample.py after a human filled in the
`manual_utility_success` column, and reports accuracy / precision / recall / F1 and a
confusion matrix of proxy vs manual.

Positive class = utility_success is True (task considered accomplished).
Rows with an empty/unparseable `manual_utility_success` are skipped.
"""

from argparse import ArgumentParser
from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

TRUE_TOKENS = {"true", "1", "yes", "y", "t", "sim"}
FALSE_TOKENS = {"false", "0", "no", "n", "f", "nao", "não"}


def parse_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in TRUE_TOKENS:
        return True
    if text in FALSE_TOKENS:
        return False
    return None


def safe_div(numerator, denominator):
    return numerator / denominator if denominator else 0.0


def main():
    parser = ArgumentParser(description="Evaluate utility-proxy agreement against manual labels.")
    parser.add_argument("labeled_csv", type=str, help="CSV with manual_utility_success filled in.")
    parser.add_argument("--proxy-column", type=str, default="utility_success_proxy")
    parser.add_argument("--manual-column", type=str, default="manual_utility_success")
    parser.add_argument("--out-json", type=str, default=None)
    args = parser.parse_args()

    csv_path = Path(args.labeled_csv)
    if not csv_path.is_absolute():
        csv_path = ROOT / csv_path
    df = pd.read_csv(csv_path)

    for column in (args.proxy_column, args.manual_column):
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in {csv_path}. Columns: {list(df.columns)}")

    tp = tn = fp = fn = 0
    skipped = 0
    total_labeled = 0

    for _, row in df.iterrows():
        manual = parse_bool(row[args.manual_column])
        proxy = parse_bool(row[args.proxy_column])
        if manual is None or proxy is None:
            skipped += 1
            continue
        total_labeled += 1
        if proxy and manual:
            tp += 1
        elif not proxy and not manual:
            tn += 1
        elif proxy and not manual:
            fp += 1  # proxy said useful, human said not -> false positive
        else:
            fn += 1  # proxy said not useful, human said useful -> false negative

    accuracy = safe_div(tp + tn, total_labeled)
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)

    report = {
        "labeled_csv": str(csv_path),
        "rows_total": int(len(df)),
        "rows_evaluated": total_labeled,
        "rows_skipped": skipped,
        "confusion_matrix": {
            "true_positive": tp,
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
        },
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }

    print(f"Labeled rows evaluated: {total_labeled} (skipped: {skipped})")
    print()
    print("Confusion matrix (proxy vs manual, positive = useful):")
    print(f"  TP (proxy=useful, manual=useful):       {tp}")
    print(f"  TN (proxy=not useful, manual=not useful): {tn}")
    print(f"  FP (proxy=useful, manual=not useful):    {fp}")
    print(f"  FN (proxy=not useful, manual=useful):    {fn}")
    print()
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1:        {f1:.4f}")

    if args.out_json:
        out_json = Path(args.out_json)
        if not out_json.is_absolute():
            out_json = ROOT / out_json
        out_json.parent.mkdir(parents=True, exist_ok=True)
        with out_json.open("w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print()
        print(f"Report saved to: {out_json}")


if __name__ == "__main__":
    main()
