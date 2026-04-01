# Master Prompt

Use this as the main build prompt for a coding agent.

---

You are building **MacroFair**, a hackathon-grade but production-structured prediction-market mispricing detector focused on macro contracts from Polymarket and Kalshi.

## Product objective

Build a live screener and explainability app that compares:
- current market-implied probability
- fundamentals-aware fair-value probability

Then rank the biggest live dislocations and explain the gap.

## Core positioning

This is **not** an arbitrage bot and **not** a generic dashboard.

It is:
- a calibration-first research product
- a live ranked screener
- an explainable API + app
- a polished hackathon submission

## Scope

Focus only on macro contracts in V1:
- inflation / CPI
- Fed decisions
- unemployment
- recession
- GDP / related macro releases

## Required stack

- frontend: Next.js + TypeScript + Tailwind + shadcn/ui
- backend: FastAPI + Python
- storage: DuckDB + Parquet + JSON snapshots
- tests: `tsc`, `vitest`, `pytest`, `playwright`

## Non-negotiable requirements

1. Every interactive UI element must have `data-testid`.
2. Playwright must use:
   - retries = 0
   - workers = 1
   - video = on
   - trace = on
   - screenshot = on
3. Demo mode must work without secrets.
4. No milestone is complete without a proof pack in `/artifacts/proof/<timestamp>-<milestone>/`.
5. Every test layer must end with:
   - failed = 0
   - skipped = 0
   - retries = 0
6. No placeholder claims of completion.

## Output required from you

Build a repo with:

```text
macrofair/
├── apps/api
├── apps/web
├── src
├── tests
├── data/fixtures
├── artifacts/proof
├── docs
└── scripts
```

## Functional requirements

### Backend
- read-only Polymarket adapter
- read-only Kalshi adapter
- FRED adapter
- canonical market schema
- feature pipeline
- fair-value baseline model
- dislocation scorer
- explanation generator
- FastAPI endpoints

### Frontend
- screener page
- market detail page
- methodology page
- deterministic demo data mode
- loading/error/empty/completed states

## API endpoints
- `GET /api/v1/health`
- `GET /api/v1/metadata`
- `GET /api/v1/markets`
- `GET /api/v1/markets/{market_id}`
- `GET /api/v1/markets/{market_id}/history`
- `GET /api/v1/markets/{market_id}/explain`

## UI priorities

Home page must immediately show:
- contract
- platform
- market probability
- fair probability
- gap
- confidence

## Data priorities

Use cached or fixture snapshots in demo mode.
Keep all outputs deterministic.

## Evaluation outputs

Generate:
- calibration metrics
- backtest summary
- explanation examples
- sample ranked snapshot

## Delivery style

Work milestone by milestone.  
After each milestone:
- run the required tests
- generate proof artifacts
- update docs if structure changed

If a milestone does not have proof, mark it REJECTED.

---

End of prompt.
