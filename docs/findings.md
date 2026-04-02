# Flagship Finding

## Headline Finding

In the deterministic demo snapshot, the CPI inflation contract contributes **69.82%** of total absolute dislocation mass and is **3.146x** larger than the second-ranked gap.

## Question

How concentrated are crowd-vs-fair dislocations in the current deterministic macro market snapshot?

## Method

1. Score all demo markets with the deterministic service pipeline.
2. Compute absolute gap for each market: $|\text{market probability} - \text{fair probability}|$.
3. Rank by absolute gap.
4. Compute each market's share of total absolute gap mass and concentration statistics (top-share and Herfindahl index).

Computation source:

- `scripts/export_flagship_finding.py`
- `artifacts/evaluation/flagship_finding.json`

## Result

- Top contract: `poly-cpi-jun-2026-over-3`
- Top absolute gap: **14.41 pts**
- Total absolute gap mass: **20.64 pts**
- Top-share of total: **69.82%**
- Top-to-second ratio: **3.146x**
- Concentration index (HHI): **0.5398**

Supporting artifacts:

- JSON: `artifacts/evaluation/flagship_finding.json`
- Contributions table: `artifacts/evaluation/flagship_dislocation_contributions.csv`
- Category table: `artifacts/evaluation/flagship_category_breakdown.csv`
- Chart: `artifacts/evaluation/flagship_dislocation_concentration.svg`

## Interpretation

The demo universe is not showing diffuse, small disagreements. It shows one dominant dislocation that drives most of the total divergence. This makes the product narrative clear for judges: MacroFair surfaces where attention should go first.

## Limitations

- The demo universe is intentionally small and fixture-backed.
- This is a snapshot finding; concentration can shift across refresh windows.
- Dislocation concentration is a research signal, not a trading instruction.
