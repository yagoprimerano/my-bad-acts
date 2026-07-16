"""Montgomery-style statistics for the robustness experiments.

Turns robustness manifests into the analyses expected by DOE (Design and Analysis of
Experiments) and SQC (Introduction to Statistical Quality Control):

  mode=spc        Experiment 1 -- process stability / repeatability.
                  Per case: ASR with Wilson 95% CI, a p-chart (fraction nonconforming =
                  attack success) with 3-sigma limits, and an I-MR chart for
                  trajectory_length. Answers "is single-run evaluation in control?".

  mode=factorial  Experiment 2 -- 2^2 factorial: Defense (safe) x Perturbation.
                  Cell ASR/utility with CIs, main effects and interaction, plus an
                  approximate two-proportion test for each main effect.

  mode=noise      Experiment 3 -- benign-task paraphrase as a noise factor, blocked by
                  case. ASR/utility per variant with CIs and disagreement vs the 'base'
                  variant (sensitivity of the conclusion to rephrasing).

These are best-effort exploratory statistics: sample sizes are modest, so treat intervals
as indicative. The official attack verdict remains the final-effect evaluator.
"""

from argparse import ArgumentParser
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_robustness_results import read_manifest_paths, resolve_input_files, evaluate_file  # noqa: E402


Z95 = 1.959963984540054
D2_N2 = 1.128   # unbiasing constant d2 for moving range of size 2
D4_N2 = 3.267   # D4 for moving range chart, n=2
E2_N2 = 2.66    # 3/d2 for individuals chart, n=2


# ======================================================================================
# Statistics helpers
# ======================================================================================

def wilson_interval(successes, n, z=Z95):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return {"p": 0.0, "low": 0.0, "high": 0.0, "successes": 0, "n": 0}
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return {
        "p": p,
        "low": max(0.0, center - half),
        "high": min(1.0, center + half),
        "successes": int(successes),
        "n": int(n),
    }


def _phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def two_proportion_test(k1, n1, k2, n2):
    """Approximate two-proportion z-test (group1 - group2). Normal approximation."""
    if n1 == 0 or n2 == 0:
        return None
    p1, p2 = k1 / n1, k2 / n2
    diff = p1 - p2
    pooled = (k1 + k2) / (n1 + n2)
    se_pooled = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2)) if 0 < pooled < 1 else 0.0
    z = diff / se_pooled if se_pooled > 0 else 0.0
    p_value = 2 * (1 - _phi(abs(z)))
    se_unpooled = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return {
        "p1": p1, "p2": p2, "diff": diff,
        "z": z, "p_value": p_value,
        "ci_low": diff - Z95 * se_unpooled,
        "ci_high": diff + Z95 * se_unpooled,
    }


def fmt_pct(x):
    return f"{x * 100:.1f}%"


def order_key(record):
    rep = record.get("robust_repeat")
    rep = rep if isinstance(rep, int) else 0
    return (rep, str(record.get("source_file")))


# ======================================================================================
# Loading
# ======================================================================================

def load_records(manifests, paths, environment):
    input_paths = list(paths)
    for manifest in manifests:
        found = read_manifest_paths(manifest)
        if not found:
            print(f"Warning: no successful runs in manifest {manifest}", file=sys.stderr)
        input_paths.extend(found)
    if not input_paths:
        raise ValueError("No inputs. Provide --manifest-path and/or result paths.")

    files = resolve_input_files(input_paths)
    if not files:
        raise FileNotFoundError("No result JSON files found.")

    records = []
    for path in files:
        records.extend(evaluate_file(path, environment))
    if not records:
        raise ValueError("No datapoints found.")
    return records


# ======================================================================================
# Mode: SPC (Experiment 1)
# ======================================================================================

def p_chart(values, subgroup_size):
    """values: list of 0/1 in run order. Returns center line, subgroups, limits, signals."""
    n = len(values)
    total = sum(values)
    pbar = total / n if n else 0.0

    subgroups = []
    for start in range(0, n, subgroup_size):
        chunk = values[start:start + subgroup_size]
        m = len(chunk)
        phat = sum(chunk) / m
        sigma = math.sqrt(pbar * (1 - pbar) / m) if 0 <= pbar <= 1 else 0.0
        ucl = min(1.0, pbar + 3 * sigma)
        lcl = max(0.0, pbar - 3 * sigma)
        subgroups.append({
            "index": len(subgroups) + 1,
            "size": m,
            "p": phat,
            "ucl": ucl,
            "lcl": lcl,
            "out_of_control": phat > ucl + 1e-9 or phat < lcl - 1e-9,
        })

    return {"center_line": pbar, "subgroup_size": subgroup_size, "subgroups": subgroups}


def imr_chart(values):
    """Individuals & Moving-Range chart for a continuous series (run order)."""
    xs = [v for v in values if v is not None]
    n = len(xs)
    if n < 2:
        return None
    xbar = sum(xs) / n
    mrs = [abs(xs[i] - xs[i - 1]) for i in range(1, n)]
    mrbar = sum(mrs) / len(mrs)
    sigma_hat = mrbar / D2_N2 if mrbar > 0 else 0.0
    i_ucl = xbar + E2_N2 * mrbar
    i_lcl = xbar - E2_N2 * mrbar
    i_out = [i + 1 for i, x in enumerate(xs) if x > i_ucl + 1e-9 or x < i_lcl - 1e-9]
    mr_ucl = D4_N2 * mrbar
    mr_out = [i + 2 for i, m in enumerate(mrs) if m > mr_ucl + 1e-9]
    return {
        "n": n,
        "mean": xbar,
        "mr_bar": mrbar,
        "sigma_hat": sigma_hat,
        "i_ucl": i_ucl,
        "i_lcl": i_lcl,
        "i_out_of_control_points": i_out,
        "mr_ucl": mr_ucl,
        "mr_out_of_control_points": mr_out,
        "individuals": xs,
        "moving_ranges": mrs,
    }


def run_spc(records, subgroup_size):
    by_case = {}
    for r in records:
        by_case.setdefault(r["case_key"], []).append(r)

    cases = {}
    for case_key, rows in sorted(by_case.items(), key=lambda kv: str(kv[0])):
        rows = sorted(rows, key=order_key)
        attack = [1 if r["attack_success"] else 0 for r in rows]
        utility = [1 if r["utility_success"] else 0 for r in rows]
        lengths = [r["trajectory_length"] for r in rows]

        asr_ci = wilson_interval(sum(attack), len(attack))
        util_ci = wilson_interval(sum(utility), len(utility))
        flips = sum(1 for i in range(1, len(attack)) if attack[i] != attack[i - 1])

        cases[str(case_key)] = {
            "target_agent": rows[0].get("target_agent"),
            "n": len(rows),
            "asr": asr_ci,
            "utility": util_ci,
            "attack_success_series": attack,
            "attack_transitions": flips,
            "p_chart_attack": p_chart(attack, subgroup_size),
            "imr_trajectory_length": imr_chart(lengths),
        }

    print("=" * 90)
    print("EXPERIMENT 1 -- Process stability / repeatability (SQC)")
    print("=" * 90)
    for case_key, c in cases.items():
        print(f"\nCase {case_key} (target={c['target_agent']}, n={c['n']})")
        a = c["asr"]
        u = c["utility"]
        print(f"  ASR      = {fmt_pct(a['p'])}  95% CI [{fmt_pct(a['low'])}, {fmt_pct(a['high'])}]  ({a['successes']}/{a['n']})")
        print(f"  Utility  = {fmt_pct(u['p'])}  95% CI [{fmt_pct(u['low'])}, {fmt_pct(u['high'])}]  ({u['successes']}/{u['n']})")
        print(f"  Attack outcome transitions across runs: {c['attack_transitions']}")
        pc = c["p_chart_attack"]
        n_out = sum(1 for s in pc["subgroups"] if s["out_of_control"])
        print(f"  p-chart (attack, subgroups of {pc['subgroup_size']}): center={fmt_pct(pc['center_line'])}, "
              f"{len(pc['subgroups'])} subgroups, {n_out} out-of-control")
        imr = c["imr_trajectory_length"]
        if imr:
            print(f"  I-MR trajectory_length: mean={imr['mean']:.2f}, sigma_hat={imr['sigma_hat']:.2f}, "
                  f"I-limits [{imr['i_lcl']:.2f}, {imr['i_ucl']:.2f}], "
                  f"out-of-control individuals={imr['i_out_of_control_points']}")
    print()
    print("Reading: if ASR CI is wide or attack transitions > 0, single-run evaluation is")
    print("not in statistical control -> repetition is required (empirical R10 evidence).")
    return {"mode": "spc", "cases": cases}


# ======================================================================================
# Mode: factorial (Experiment 2)
# ======================================================================================

def _cell_stats(rows):
    k_attack = sum(1 for r in rows if r["attack_success"])
    k_util = sum(1 for r in rows if r["utility_success"])
    n = len(rows)
    return {
        "n": n,
        "asr": wilson_interval(k_attack, n),
        "utility": wilson_interval(k_util, n),
        "attack_successes": k_attack,
        "utility_successes": k_util,
    }


def run_factorial(records, defense_names=("off", "on"), pert_low="none"):
    def defense_level(r):
        return bool(r.get("safe"))

    def pert_level(r):
        return r.get("trajectory_perturbation") or "none"

    defense_levels = sorted({defense_level(r) for r in records})           # [False, True]
    pert_levels = sorted({pert_level(r) for r in records}, key=lambda p: (p != pert_low, p))

    cells = {}
    for d in defense_levels:
        for p in pert_levels:
            rows = [r for r in records if defense_level(r) == d and pert_level(r) == p]
            if rows:
                cells[(d, p)] = _cell_stats(rows)

    print("=" * 90)
    print("EXPERIMENT 2 -- 2^k factorial: Defense (safe) x Perturbation (DOE)")
    print("=" * 90)
    print(f"\n{'Defense':>8} | {'Perturbation':>22} | {'n':>3} | {'ASR [95% CI]':>26} | {'Utility [95% CI]':>26}")
    print("-" * 100)
    for d in defense_levels:
        for p in pert_levels:
            c = cells.get((d, p))
            if not c:
                continue
            dname = defense_names[1] if d else defense_names[0]
            a, u = c["asr"], c["utility"]
            asr_s = f"{fmt_pct(a['p'])} [{fmt_pct(a['low'])},{fmt_pct(a['high'])}]"
            util_s = f"{fmt_pct(u['p'])} [{fmt_pct(u['low'])},{fmt_pct(u['high'])}]"
            print(f"{dname:>8} | {p:>22} | {c['n']:>3} | {asr_s:>26} | {util_s:>26}")

    result = {"mode": "factorial", "cells": {f"{d}|{p}": v for (d, p), v in cells.items()}}

    # Closed-form 2^2 effects when exactly 2x2.
    if len(defense_levels) == 2 and len(pert_levels) == 2:
        a_lo, a_hi = defense_levels          # False, True
        b_lo, b_hi = pert_levels             # none, other
        def asr(d, p):
            return cells[(d, p)]["asr"]["p"] if (d, p) in cells else None
        def util(d, p):
            return cells[(d, p)]["utility"]["p"] if (d, p) in cells else None

        def effects(fn):
            y1, ya, yb, yab = fn(a_lo, b_lo), fn(a_hi, b_lo), fn(a_lo, b_hi), fn(a_hi, b_hi)
            if None in (y1, ya, yb, yab):
                return None
            return {
                "main_effect_defense": ((ya + yab) - (y1 + yb)) / 2,
                "main_effect_perturbation": ((yb + yab) - (y1 + ya)) / 2,
                "interaction": ((yab + y1) - (ya + yb)) / 2,
            }

        eff_asr = effects(asr)
        eff_util = effects(util)
        result["effects_asr"] = eff_asr
        result["effects_utility"] = eff_util

        # Main-effect two-proportion tests (collapsing the other factor).
        def collapse(fn_level, level):
            rows = [r for r in records if fn_level(r) == level]
            return sum(1 for r in rows if r["attack_success"]), len(rows)

        k_don, n_don = collapse(defense_level, a_hi)
        k_doff, n_doff = collapse(defense_level, a_lo)
        k_ph, n_ph = collapse(pert_level, b_hi)
        k_pl, n_pl = collapse(pert_level, b_lo)
        test_defense = two_proportion_test(k_don, n_don, k_doff, n_doff)
        test_pert = two_proportion_test(k_ph, n_ph, k_pl, n_pl)
        result["main_effect_test_defense_on_minus_off"] = test_defense
        result["main_effect_test_perturbation_high_minus_none"] = test_pert

        print("\n2^2 effects on ASR (proportion scale):")
        if eff_asr:
            print(f"  Main effect Defense (on-off)     : {eff_asr['main_effect_defense']:+.3f}")
            print(f"  Main effect Perturbation (x-none): {eff_asr['main_effect_perturbation']:+.3f}")
            print(f"  Interaction Defense x Perturbation: {eff_asr['interaction']:+.3f}")
        print("2^2 effects on Utility (proportion scale):")
        if eff_util:
            print(f"  Main effect Defense (on-off)     : {eff_util['main_effect_defense']:+.3f}")
            print(f"  Main effect Perturbation (x-none): {eff_util['main_effect_perturbation']:+.3f}")
            print(f"  Interaction Defense x Perturbation: {eff_util['interaction']:+.3f}")
        if test_defense:
            print(f"\n  Defense main effect on ASR: diff={test_defense['diff']:+.3f} "
                  f"95% CI [{test_defense['ci_low']:+.3f},{test_defense['ci_high']:+.3f}] "
                  f"z={test_defense['z']:.2f} p={test_defense['p_value']:.3f}")
        if test_pert:
            print(f"  Perturbation main effect on ASR: diff={test_pert['diff']:+.3f} "
                  f"95% CI [{test_pert['ci_low']:+.3f},{test_pert['ci_high']:+.3f}] "
                  f"z={test_pert['z']:.2f} p={test_pert['p_value']:.3f}")
        print("\nNote: two-proportion tests are normal approximations; with modest n treat")
        print("p-values as indicative. Interaction != 0 means the effect of one factor")
        print("depends on the level of the other.")
    else:
        print("\n(Closed-form 2^2 effects require exactly two defense and two perturbation")
        print(" levels; cell table above still holds for the general design.)")
    return result


# ======================================================================================
# Mode: noise (Experiment 3)
# ======================================================================================

def run_noise(records, baseline_variant="base"):
    by_case = {}
    for r in records:
        by_case.setdefault(r["case_key"], []).append(r)

    blocks = {}
    agg_variants = {}
    for case_key, rows in sorted(by_case.items(), key=lambda kv: str(kv[0])):
        by_variant = {}
        for r in rows:
            by_variant.setdefault(r.get("robust_condition") or "unknown", []).append(r)

        variant_stats = {}
        for variant, vrows in by_variant.items():
            k = sum(1 for r in vrows if r["attack_success"])
            ku = sum(1 for r in vrows if r["utility_success"])
            variant_stats[variant] = {
                "n": len(vrows),
                "asr": wilson_interval(k, len(vrows)),
                "utility": wilson_interval(ku, len(vrows)),
            }
            agg_variants.setdefault(variant, {"k": 0, "n": 0, "ku": 0})
            agg_variants[variant]["k"] += k
            agg_variants[variant]["n"] += len(vrows)
            agg_variants[variant]["ku"] += ku

        asrs = [vs["asr"]["p"] for vs in variant_stats.values()]
        utils = [vs["utility"]["p"] for vs in variant_stats.values()]
        blocks[str(case_key)] = {
            "target_agent": rows[0].get("target_agent"),
            "variants": variant_stats,
            "asr_range": (max(asrs) - min(asrs)) if asrs else 0.0,
            "utility_range": (max(utils) - min(utils)) if utils else 0.0,
        }

    print("=" * 90)
    print("EXPERIMENT 3 -- Benign-task paraphrase as a noise factor (DOE / Robust Design)")
    print("=" * 90)
    for case_key, b in blocks.items():
        print(f"\nBlock: case {case_key} (target={b['target_agent']})")
        base = b["variants"].get(baseline_variant)
        for variant, vs in sorted(b["variants"].items()):
            a = vs["asr"]
            u = vs["utility"]
            tag = " (baseline)" if variant == baseline_variant else ""
            print(f"  {variant:>14}{tag}: n={vs['n']:>2} | ASR={fmt_pct(a['p'])} [{fmt_pct(a['low'])},{fmt_pct(a['high'])}] "
                  f"| Utility={fmt_pct(u['p'])}")
        print(f"  Sensitivity to paraphrase -> ASR range={fmt_pct(b['asr_range'])}, "
              f"Utility range={fmt_pct(b['utility_range'])}")

    print("\nPooled across blocks (per variant):")
    for variant, agg in sorted(agg_variants.items()):
        ci = wilson_interval(agg["k"], agg["n"])
        print(f"  {variant:>14}: ASR={fmt_pct(ci['p'])} [{fmt_pct(ci['low'])},{fmt_pct(ci['high'])}] "
              f"({ci['successes']}/{ci['n']})")
    print("\nReading: small ASR/Utility range across paraphrases => the safety conclusion is")
    print("robust to semantically-equivalent rephrasings (a good robust-design outcome).")
    return {"mode": "noise", "blocks": blocks,
            "pooled_variants": {v: wilson_interval(a["k"], a["n"]) for v, a in agg_variants.items()}}


# ======================================================================================
# CLI
# ======================================================================================

def main():
    parser = ArgumentParser(description="Montgomery-style stats (SPC/factorial/noise) for robustness experiments.")
    parser.add_argument("mode", choices=["spc", "factorial", "noise"])
    parser.add_argument("--manifest-path", action="append", default=[],
                        help="Robustness manifest JSONL (repeatable, e.g. one per defense level).")
    parser.add_argument("paths", nargs="*", help="Optional extra result JSON files/dirs.")
    parser.add_argument(
        "--environment",
        choices=["travel_planning", "financial_article_writing", "code_generation", "multi_agent_debate"],
        default="travel_planning",
    )
    parser.add_argument("--subgroup-size", type=int, default=5, help="p-chart subgroup size (spc mode).")
    parser.add_argument("--baseline-variant", type=str, default="base", help="Baseline variant for noise mode.")
    parser.add_argument("--out-json", type=str, default=None)
    args = parser.parse_args()

    records = load_records(args.manifest_path, args.paths, args.environment)

    if args.mode == "spc":
        result = run_spc(records, args.subgroup_size)
    elif args.mode == "factorial":
        result = run_factorial(records)
    else:
        result = run_noise(records, args.baseline_variant)

    result["environment"] = args.environment
    result["total_observations"] = len(records)

    if args.out_json:
        out = Path(args.out_json)
        if not out.is_absolute():
            out = ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nJSON saved to: {out}")


if __name__ == "__main__":
    main()
