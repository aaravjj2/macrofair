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
4. Optional Zerve submission package (`artifacts/evaluation/zerve_submission_package.json`).

## Determinism

- Default mode is deterministic demo mode.
- Longitudinal snapshots are fixture-backed in `data/fixtures/snapshot_window.json`.
- Repeat-run equality is tested for persistence and secondary payloads.
- Repeat-run equality is tested for the Zerve submission package payload.

## Optional Zerve Layer

- Zerve integration is server-side and feature-flagged.
- Status/package/sync interfaces are exposed under `/api/v1/integrations/zerve/*`.
- If `ZERVE_ENABLED=false` or key/config is absent, the app degrades gracefully and remains fully demo-functional.
- No secret values are returned by API responses.

## Limits

- Snapshot window is intentionally short and synthetic for reproducibility.
- Findings are calibration-oriented research signals, not execution guidance.
