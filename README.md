# MacroFair

MacroFair is a macro prediction-market mispricing detector. It compares market-implied probability with a deterministic fundamentals-aware fair value, ranks the largest dislocations, and explains why they occur.

## Flagship insight

In the deterministic demo snapshot, one inflation contract (`poly-cpi-jun-2026-over-3`) contributes 69.82% of total absolute dislocation mass and is 3.146x larger than the second-ranked dislocation.

Evidence:

- `docs/findings.md`
- `artifacts/evaluation/flagship_finding.json`
- `artifacts/evaluation/flagship_dislocation_contributions.csv`
- `artifacts/evaluation/flagship_dislocation_concentration.svg`

## Why this matters

Prediction markets are useful but noisy. MacroFair helps judges and researchers rapidly see where crowd odds and a deterministic fair value disagree most, and then inspect factor-level explanations.

## Repository layout

```text
macrofair/
├── apps/
│   ├── api/                 # FastAPI endpoints
│   └── web/                 # Next.js frontend
├── src/macrofair/           # ingestion, normalization, features, modeling, scoring, evaluation
├── tests/                   # pytest + playwright
├── data/fixtures/           # deterministic demo fixtures
├── artifacts/
│   ├── evaluation/          # computed findings and metrics
│   └── proof/               # milestone proof packs
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

## Run locally

Backend:

```bash
PYTHONPATH=src /home/aarav/Aarav/macrofair/.venv/bin/python -m uvicorn apps.api.main:app --reload
```

Frontend dev:

```bash
npm run dev -w apps/web
```

Frontend production mode (used by Playwright):

```bash
npm run build -w apps/web
npm run start -w apps/web
```

## Deterministic demo mode

- Default mode is `demo`.
- Test/demo paths are fixture-driven from `data/fixtures/`.
- No secrets are required for tests or demo execution.

## API surface

- `GET /api/v1/health`
- `GET /api/v1/metadata`
- `GET /api/v1/markets`
- `GET /api/v1/markets/{market_id}`
- `GET /api/v1/markets/{market_id}/history`
- `GET /api/v1/markets/{market_id}/explain`
- `GET /api/v1/findings/flagship`
- `GET /api/v1/snapshots/latest`
- `GET /api/v1/compare`

## Verification commands

```bash
npm run tsc
npm run vitest
/home/aarav/Aarav/macrofair/.venv/bin/python -m pytest -q
npm run playwright
```

Playwright policy:

- retries = 0
- workers = 1
- video = on
- trace = on
- screenshot = on

## Proof packs

Every milestone must produce:

```text
artifacts/proof/<timestamp>-<milestone>/
```

Each pack includes at minimum:

- `MANIFEST.md`
- `manifest.json`
- `README.md`
- `playwright-report/`
- `test-results/`
- `screenshots/`
- `TOUR.webm`

See milestone status in `docs/milestones.md`.

Latest flagship-story proof pack:

- `artifacts/proof/20260402T024608Z-milestone-10-flagship-story/`
