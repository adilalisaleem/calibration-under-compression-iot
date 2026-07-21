#!/usr/bin/env python3
"""
Reproduce the headline numbers of the manuscript directly from the released
per-run results, with no model retraining required.

Usage:
    python scripts/reproduce_paper_numbers.py

Reads:
    results/all_runs_raw.csv     (one row per dataset x seed x regime)
    results/stats_tests.csv      (paired-per-seed statistics, as released)
    results/aurc.csv             (area under risk-coverage curve)
    results/latency.csv          (CPU latency and parameter counts)

Prints the abstract/Results quantities so a reader can confirm every figure
in the paper is traceable to the released logits-derived metrics.
"""

import os
import sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")


def load(name):
    path = os.path.join(RES, name)
    if not os.path.exists(path):
        sys.exit(f"Missing {path}. Run from the repository root.")
    return pd.read_csv(path)


def mean_of(df, dataset, regime, metric):
    sub = df[(df["dataset"] == dataset) & (df["regime"] == regime)]
    if sub.empty:
        return None
    return float(sub[metric].mean())


def main():
    runs = load("all_runs_raw.csv")
    stats = load("stats_tests.csv")
    aurc = load("aurc.csv")
    lat = load("latency.csv")

    print("=" * 68)
    print("HEADLINE NUMBERS REPRODUCED FROM RELEASED PER-SEED RESULTS")
    print("=" * 68)

    print("\n[Calibration transfer: scratch -> KD-FT student ECE]")
    for ds, label in [("ciciot2023", "CICIoT2023"), ("edgeiiot", "Edge-IIoTset")]:
        s = mean_of(runs, ds, "student_scratch", "ece")
        k = mean_of(runs, ds, "student_kd_ft", "ece")
        print(f"  {label:12s}: scratch ECE {s:.3f} -> KD-FT ECE {k:.3f}")

    print("\n[Paired statistics as released (Cohen's d_z, Holm p)]")
    key = stats[stats["comparison"].str.contains("KD transfers calibration \\(ECE\\)")]
    for _, r in key.iterrows():
        print(f"  {r['dataset']:11s} d_z={r['cohens_dz']:+.2f}  Holm p={r['p_holm']:.3f}")

    print("\n[Teachers: accuracy / macro-F1 / ECE]")
    for ds, label in [("ciciot2023", "CICIoT2023"), ("edgeiiot", "Edge-IIoTset")]:
        for reg, name in [("teacher_ft", "FT-Transformer"),
                          ("xgboost", "XGBoost"),
                          ("teacher_llm", "Serialized-flow LM")]:
            a = mean_of(runs, ds, reg, "accuracy")
            f = mean_of(runs, ds, reg, "macro_f1")
            e = mean_of(runs, ds, reg, "ece")
            print(f"  {label:12s} {name:20s} {a:.3f} / {f:.3f} / {e:.3f}")

    print("\n[Counterfactual arms: teacher ECE -> student ECE]")
    for ds, label in [("ciciot2023", "CICIoT2023"), ("edgeiiot", "Edge-IIoTset")]:
        for treg, sreg, arm in [
            ("teacher_ft_sharp", "student_kd_ft_sharp", "sharpen"),
            ("teacher_ft_jitter", "student_kd_ft_jitter", "jitter"),
            ("teacher_ft_selsharp", "student_kd_ft_selsharp", "selective"),
        ]:
            te = mean_of(runs, ds, treg, "ece")
            se = mean_of(runs, ds, sreg, "ece")
            print(f"  {label:12s} {arm:10s}: teacher {te:.3f} -> student {se:.3f}")

    print("\n[AURC (lower is better): key regimes]")
    for ds, label in [("ciciot2023", "CICIoT2023"), ("edgeiiot", "Edge-IIoTset")]:
        for reg in ["student_kd_ft", "student_mid_kd_ft", "student_scratch"]:
            row = aurc[(aurc["dataset"] == ds) & (aurc["regime"] == reg)]
            if not row.empty:
                print(f"  {label:12s} {reg:20s} AURC={row['mean'].iloc[0]:.4f}")

    print("\n[Latency and parameter counts]")
    print(lat.to_string(index=False))

    print("\n" + "=" * 68)
    print("If these match the manuscript, every reported quantity is traceable.")
    print("=" * 68)


if __name__ == "__main__":
    main()
