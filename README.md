# MacroFair

MacroFair is a prediction-market mispricing screener for macro contracts. It compares market-implied probabilities (Polymarket and Kalshi) against a deterministic fundamentals-aware fair-value baseline, ranks dislocations, and exposes an explanation payload for each contract.

## Repo structure

```text
macrofair/
├── apps/
│   ├── api/                 # FastAPI endpoints
│   └── web/                 # Next.js frontend
├── src/macrofair/           # Pipeline: ingestion, features, model, scoring, explain
├── tests/
│   ├── unit/api/            # pytest API tests
│   └── e2e/                 # Playwright smoke test
├── data/fixtures/           # Deterministic demo snapshots
├── artifacts/
│   ├── evaluation/          # Calibration/backtest/example outputs
│   └── proof/               # Milestone proof packs
├── docs/
└── scripts/
```

## Requirements

- Node.js 20+
- Python 3.11+

## Setup

```bash
npm install
/home/aarav/Aarav/macrofair/.venv/bin/python -m pip install -e .[dev]
```

If you are using this workspace’s configured interpreter, Python commands should use:

```bash
/home/aarav/Aarav/macrofair/.venv/bin/python
```

## Run

Backend:

```bash
/home/aarav/Aarav/macrofair/.venv/bin/python -m uvicorn apps.api.main:app --reload
```

Frontend:

```bash
npm run dev -w apps/web
```

## API endpoints

- `GET /api/v1/health`
- `GET /api/v1/metadata`
- `GET /api/v1/markets`
- `GET /api/v1/markets/{market_id}`
- `GET /api/v1/markets/{market_id}/history`
- `GET /api/v1/markets/{market_id}/explain`

Also implemented from the extended API spec:

- `GET /api/v1/snapshots/latest`
- `GET /api/v1/compare`

## Test gates

```bash
npm run tsc
npm run vitest
/home/aarav/Aarav/macrofair/.venv/bin/python -m pytest -q
npm run playwright
```

Playwright is configured with:

- retries = 0
- workers = 1
- video = on
- trace = on
- screenshot = on

## Deterministic demo mode

- Default mode is `demo`.
- Data is loaded from `data/fixtures/`.
- No secrets are required for end-to-end behavior.

## Milestone proof packs

Proof packs are written to:

```text
artifacts/proof/<timestamp>-<milestone>/
```

Current implementation proof:

- `artifacts/proof/20260401T044654Z-milestone-1-foundation/`
- `artifacts/proof/20260401T152429Z-milestone-all/`

Milestone acceptance matrix is documented in:

- `docs/milestones.md`

Contains:

- `MANIFEST.md`
- `manifest.json`
- `README.md`
- `playwright-report/`
- `test-results/`
- `screenshots/`
- `TOUR.webm`
