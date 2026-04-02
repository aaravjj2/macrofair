# MacroFair

MacroFair is a macro prediction-market mispricing detector. It compares market-implied probability with a deterministic fundamentals-aware fair value, ranks the largest dislocations, and explains why they occur.

## Evidence-backed findings layer

MacroFair now ships a three-part deterministic findings package:

1. Flagship snapshot finding: CPI June 2026 contributes 69.82% of dislocation mass (3.146x #2).
2. Longitudinal persistence: dominant top dislocation persists in 11/12 committed snapshots.
3. Secondary finding (platform asymmetry): Polymarket mean gaps remain above Kalshi in 12/12 snapshots.
4. Third finding (category drift): inflation share rises by 30.66 points from first to last snapshot.

Evidence:

- `docs/findings.md`
- `artifacts/evaluation/flagship_finding.json`
- `artifacts/evaluation/flagship_persistence.json`
- `artifacts/evaluation/secondary_finding.json`
- `artifacts/evaluation/third_finding.json`
- `artifacts/evaluation/findings_report.json`

## Why this matters

Prediction markets are useful but noisy. MacroFair helps judges and researchers rapidly see where crowd odds and a deterministic fair value disagree most, and then verify whether that signal persists across snapshots and platforms.

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

## Optional Zerve integration

- Zerve integration is feature-flagged and server-side only.
- Default remains `ZERVE_ENABLED=false`.
- If no key is present, MacroFair still runs fully in deterministic demo mode.
- Frontend never receives raw key material.

Key env vars:

- `ZERVE_ENABLED=false`
- `ZERVE_API_KEY`
- `ZERVE_BASE_URL`
- `ZERVE_PROJECT_ID`

Use `.env.example` as a template and keep real values in local `.env` only.

Integration docs: `docs/zerve_integration.md`

## API surface

- `GET /api/v1/health`
- `GET /api/v1/metadata`
- `GET /api/v1/markets`
- `GET /api/v1/markets/{market_id}`
- `GET /api/v1/markets/{market_id}/history`
- `GET /api/v1/markets/{market_id}/explain`
- `GET /api/v1/findings/flagship`
- `GET /api/v1/findings/flagship/persistence`
- `GET /api/v1/findings/secondary`
- `GET /api/v1/findings/third`
- `GET /api/v1/findings`
- `GET /api/v1/findings/report`
- `GET /api/v1/reports/submission`
- `GET /api/v1/snapshots/latest`
- `GET /api/v1/compare`
- `GET /api/v1/integrations/zerve/status`
- `GET /api/v1/integrations/zerve/package`
- `POST /api/v1/integrations/zerve/sync`

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

Latest rerun proof pack:

- `artifacts/proof/20260402T025336Z-milestone-10-flagship-story-rerun/`

Latest milestone-11 proof pack:

- `artifacts/proof/20260402T031728Z-milestone-11-longitudinal-findings/`

Latest milestone-12 proof pack:

- `artifacts/proof/20260402T033334Z-milestone-12-zerve-integration/`
