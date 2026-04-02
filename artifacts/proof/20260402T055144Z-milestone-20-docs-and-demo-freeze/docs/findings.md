# Findings

## 1) Flagship snapshot finding

In the latest deterministic demo snapshot, the CPI inflation contract (`poly-cpi-jun-2026-over-3`) contributes **69.82%** of total absolute dislocation mass and is **3.146x** larger than the second-ranked gap.

Evidence artifacts:

- JSON: `artifacts/evaluation/flagship_finding.json`
- Contributions table: `artifacts/evaluation/flagship_dislocation_contributions.csv`
- Category table: `artifacts/evaluation/flagship_category_breakdown.csv`
- Chart: `artifacts/evaluation/flagship_dislocation_concentration.svg`

## 2) Flagship persistence result (longitudinal window)

Question: is the flagship concentration signal a one-off artifact or persistent across deterministic snapshots?

Result across the committed snapshot window (`flagship-persistence-window-v2`):

- Top market persisted in **11/12 snapshots** (**91.67% persistence**).
- Average top-share across window: **54.55%**.
- Top-share range: **40.81%** to **69.82%**.

Evidence artifacts:

- JSON: `artifacts/evaluation/flagship_persistence.json`
- Table: `artifacts/evaluation/flagship_persistence.csv`
- Chart: `artifacts/evaluation/flagship_persistence.svg`

## 3) Secondary deterministic finding

Chosen angle: **platform gap asymmetry**.

One-sentence finding:

Across the deterministic window, Polymarket contracts are consistently priced further above fair value than Kalshi contracts on average.

Measured result:

- Average asymmetry (Polymarket mean gap minus Kalshi mean gap): **7.67 pts**.
- Positive asymmetry windows: **12/12 snapshots** (**100.0%**).

Evidence artifacts:

- JSON: `artifacts/evaluation/secondary_finding.json`
- Table: `artifacts/evaluation/secondary_finding.csv`
- Chart: `artifacts/evaluation/secondary_finding.svg`

## 4) Third deterministic finding

Chosen angle: **category dislocation-share drift**.

One-sentence finding:

Inflation is the largest drifting category, increased by 30.66 pts from the first to last deterministic snapshot.

Measured result:

- Dominant drift category: **inflation**.
- Drift magnitude (first to last share): **+30.66 pts**.

Evidence artifacts:

- JSON: `artifacts/evaluation/third_finding.json`
- Table: `artifacts/evaluation/third_finding.csv`
- Snapshot-category table: `artifacts/evaluation/third_finding_snapshot_category_shares.csv`
- Chart: `artifacts/evaluation/third_finding.svg`

## 5) Consolidated findings and submission reports

Deterministic reports now export a typed report/index/submission bundle for integration and judging workflows.

Artifacts:

- Findings index: `artifacts/evaluation/findings_index.json`
- Findings report: `artifacts/evaluation/findings_report.json`
- Submission report: `artifacts/evaluation/submission_report.json`
- Zerve submission package: `artifacts/evaluation/zerve_submission_package.json`

## Method notes

- All findings run in default deterministic demo mode.
- Snapshot inputs are committed fixtures: `data/fixtures/snapshot_window.json`.
- Repeated runs produce identical payloads and hashes in tests.
