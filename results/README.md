# Results data dictionary

All metrics are computed from saved model logits over five fixed seeds
(13, 42, 77, 2024, 31337) on CICIoT2023 and Edge-IIoTset.

## all_runs_raw.csv
One row per `(dataset, seed, regime)`. Columns:
- `dataset` — `ciciot2023` or `edgeiiot`
- `seed` — one of the five fixed seeds
- `regime` — training regime (see the mapping table in the top-level README)
- `accuracy`, `macro_f1` — discrimination metrics
- `ece`, `adaptive_ece`, `classwise_ece` — calibration error (15 bins;
  adaptive = equal-mass; classwise = mean one-vs-rest, imbalance-sensitive)
- `brier`, `nll` — strictly proper scoring rules
- `conf_on_errors` — mean top-1 confidence on misclassified flows
- `gate_p` — internal stability-gate flag (teacher retrain trigger); not used
  in the paper's analysis
- per-class F1 columns (e.g. `F1_Spoofing`, `F1_Malware`, `F1_Web`) where present

## summary_ciciot2023.csv, summary_edgeiiot.csv
Per-regime aggregates. **These files have a two-row header** (metric name in
row 1, `mean`/`std` in row 2), as exported by pandas. Read with:
```python
import pandas as pd
df = pd.read_csv("summary_ciciot2023.csv", header=[0, 1], index_col=0)
```

## stats_tests.csv
Pre-specified paired-per-seed comparisons (pairs = seeds, n = 5). Columns:
`dataset, comparison, A, B, metric, n_pairs, mean_diff, sd_diff, cohens_dz,
p_ttest, p_wilcoxon, p_holm`. Holm correction is applied within each dataset's
family of comparisons. At n = 5 the exact Wilcoxon two-sided floor is 0.0625;
interpretation leans on effect sizes and cross-dataset replication.

## aurc.csv
Area under the risk-coverage curve per `(dataset, regime)`: `mean`, `std`.
Lower is better.

## latency.csv
CPU latency and parameter counts per model: single-flow (batch 1) and batched
(batch 256), measured on a single CPU core in PyTorch eager mode.

## replication_view.csv
A convenience side-by-side of key metrics (ECE, cwECE, macro-F1) across the two
datasets for every regime.
