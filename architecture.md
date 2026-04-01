# Architecture

## System overview

MacroFair has four layers:

1. **Ingestion**
   - Polymarket market data
   - Kalshi market data
   - FRED macro series
   - optional release calendar metadata

2. **Normalization**
   - canonical market schema
   - contract taxonomy
   - market-to-macro mapping
   - derived feature generation

3. **Scoring**
   - fair-value model
   - calibration layer
   - dislocation scoring
   - explainability layer

4. **Serving**
   - FastAPI backend
   - Next.js frontend
   - static artifacts / proof packs
   - scheduled refresh jobs

## Recommended repo structure

```text
macrofair/
├── apps/
│   ├── api/
│   └── web/
├── packages/
│   ├── schemas/
│   └── ui/
├── src/
│   ├── ingestion/
│   ├── normalization/
│   ├── features/
│   ├── models/
│   ├── scoring/
│   ├── evaluation/
│   └── exports/
├── notebooks/
├── data/
│   ├── raw/
│   ├── processed/
│   └── fixtures/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── artifacts/
│   └── proof/
├── docs/
└── scripts/
```

## Mode separation

### DEMO mode (default)
- no trading keys
- no order submission
- network calls optional, but app works from fixtures/snapshots
- reproducible outputs
- suitable for judging and tests

### LOCAL mode (optional)
- real API credentials allowed
- cached responses required
- provenance recorded
- tests never depend on LOCAL mode

## Data flow

1. fetch raw market lists and price snapshots
2. fetch historical price series where available
3. fetch FRED series and release metadata
4. map contracts to taxonomy
5. build feature rows
6. run fair-value model
7. compute dislocation metrics
8. write snapshot tables / JSON
9. serve through API and frontend

## Service boundaries

### Python core
Owns:
- API clients
- mapping logic
- model features
- scoring and evaluation
- export artifacts

### FastAPI
Owns:
- HTTP endpoints
- response schemas
- health and metadata
- cache reads

### Next.js
Owns:
- user interface
- client-side filtering and sorting
- route-level loading/error handling

## Storage choices

- DuckDB for analysis and repeatable queries
- Parquet for snapshots and feature tables
- JSON for exported app payloads
- no heavyweight database required for V1

## Caching strategy

- raw response cache with timestamp and source metadata
- processed snapshot cache keyed by run id
- deterministic fixture snapshots for tests

## Observability

- structured logs
- run manifest for each refresh
- artifact export after model/scoring run
- explicit version string for schema + model

## Security and secrets

- `.env` only for LOCAL mode
- no secrets committed
- no live trading permissions in V1
- read-only market data by default
