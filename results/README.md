# IEEE IoT-J R1 GitHub CSV evidence package

All recovered CSV artifacts are separated by experiment protocol. Upload folders to `results/revision_r1/` (or preserve the folder structure). The original multiclass study, the strict multiclass split attempt, binary host-disjoint task, threshold selection, and feature ablation are DIFFERENT protocols and must not be pooled.

- `01_multiclass_calibration/`: original revision multi-class five-seed comparisons, teacher perturbations, label smoothing, geometry, paired tests, protocol gates.
- `02_multiclass_host_shift/`: first exploratory source-host shift results and capture audits.
- `03_strict_multiclass_host_split/`: audit of unsuccessful locked 15-class split. Empty result files are NOT successful experiments.
- `04_binary_host_shift/`: successful locked binary split, five-seed evaluations and host assignments.
- `05_binary_thresholds/`: validation-selected thresholds, uses the SAME binary split; duplicated files retained intentionally for independent run provenance.
- `06_all_in_one_ablation/`: full versus reduced predictor experiments, host geometry, audits, computational proxy latency.
- `07_external_validity/`: cross-dataset and predictor-compatibility audits, not a successful cross-dataset transfer experiment.
- `08_cpu_reference_latency/`: separate local CPU architecture measurements, NOT a physical gateway benchmark.
- `09_reference_audit/`: publication and manuscript audit records; optional for public code repository.

Large `locked_binary_row_assignments.csv`, `host_by_attack_counts.csv` and `binary_host_contingency.csv` are helpful for provenance but not strictly required for a lightweight public GitHub repository. Keep them archived if GitHub file limits or privacy review requires omitting them. Review raw IP/host identifiers before publishing!

Use `FILE_MANIFEST.csv` to verify source, row estimates, and SHA256 checksums. No experiment results have been modified; files are copied from the supplied archives. Do not claim cross-dataset, temporal or real edge-hardware evaluation was completed.
