# Methodology

## Pipeline

1. Read deterministic fixture data for Polymarket, Kalshi, and FRED-linked context.
2. Normalize contracts into a canonical schema and category taxonomy.
3. Build deterministic feature rows (market state, spread, liquidity, macro signal, momentum, event horizon).
4. Estimate fair value using a baseline + fundamentals blend and deterministic calibration.
5. Score dislocation, confidence, and actionability.
6. Generate explanation payloads and findings artifacts.

## Findings Evidence Layer

MacroFair now separates findings into three deterministic evidence blocks:

1. Flagship snapshot finding (`artifacts/evaluation/flagship_finding.json`).
2. Flagship persistence over a committed snapshot window (`artifacts/evaluation/flagship_persistence.json`).
3. Secondary platform asymmetry finding (`artifacts/evaluation/secondary_finding.json`).

## Determinism

- Default mode is deterministic demo mode.
- Longitudinal snapshots are fixture-backed in `data/fixtures/snapshot_window.json`.
- Repeat-run equality is tested for persistence and secondary payloads.

## Limits

- Snapshot window is intentionally short and synthetic for reproducibility.
- Findings are calibration-oriented research signals, not execution guidance.
