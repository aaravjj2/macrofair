# Tasks

## Milestone 0 — Repo bootstrap
- [x] create new repo `macrofair` (local git init completed in this workspace)
- [x] initialize pnpm workspace or equivalent monorepo
- [x] add Python project config
- [x] add linting, formatting, type-checking
- [x] add CI workflow
- [x] add `docs/`, `artifacts/`, `tests/`, `data/fixtures/`
- [x] add contribution and setup docs

## Milestone 1 — Data ingestion
- [x] implement Polymarket read-only adapter
- [x] implement Kalshi public market-data adapter
- [x] implement FRED adapter
- [x] cache raw responses with timestamps
- [x] create fixture snapshots for demo mode
- [x] add ingestion tests

## Milestone 2 — Normalization and taxonomy
- [x] define canonical schemas
- [x] implement market normalization
- [x] implement contract category taxonomy
- [x] implement mapping from contracts to macro targets
- [x] add mapping confidence field
- [x] add normalization tests

## Milestone 3 — Feature pipeline
- [x] generate market features
- [x] generate macro features
- [x] generate event timing features
- [x] build repeatable feature export
- [x] add snapshot equality check
- [x] add feature tests

## Milestone 4 — Fair-value model
- [x] implement baseline model
- [x] implement combined model
- [x] add calibration layer
- [x] export evaluation metrics
- [x] create calibration charts
- [x] add model tests

## Milestone 5 — Scoring and explanation
- [x] compute dislocation score
- [x] rank live markets
- [x] generate explanation bundle
- [x] add score and explanation tests

## Milestone 6 — API
- [x] bootstrap FastAPI app
- [x] add health endpoint
- [x] add markets list endpoint
- [x] add market detail endpoint
- [x] add explanation endpoint
- [x] generate OpenAPI docs
- [x] add API tests

## Milestone 7 — Frontend
- [x] bootstrap Next.js app
- [x] build screener page
- [x] build market detail page
- [x] build methodology page
- [x] add loading/error/empty states
- [x] add test IDs everywhere
- [x] add frontend tests

## Milestone 8 — E2E and proof
- [x] add Playwright config with zero retries and one worker
- [x] record TOUR.webm
- [x] generate milestone proof pack
- [x] verify all gates pass
- [x] mark acceptance only if all proofs exist

## Milestone 9 — Demo and submission
- [x] create 3-minute demo script
- [x] prepare public screenshots
- [x] write 300-word summary
- [ ] publish Zerve project (REJECTED: requires external account/deployment credentials)
- [ ] verify app/API are publicly accessible (REJECTED: depends on public deployment)
