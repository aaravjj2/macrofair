# Testing Strategy

## Hard gates

Nothing is done until all of these pass together:
- `tsc` with 0 errors
- `vitest` with 0 failed, 0 skipped
- `pytest` with 0 failed, 0 skipped
- `playwright` with 0 failed, 0 skipped, retries = 0

## Playwright rules

- selectors: `data-testid` only
- `workers = 1`
- `retries = 0`
- `video = on`
- `trace = on`
- `screenshot = on`
- app served via `vite build` + `vite preview` style production mode or equivalent production build path
- never hot reload mode for E2E

## Required proof pack

Each milestone must write:
`/artifacts/proof/<timestamp>-<milestone>/`

Contents:
- `MANIFEST.md`
- `manifest.json`
- `README.md`
- `playwright-report/`
- `test-results/`
- `screenshots/`
- `TOUR.webm` when UX changes

## Determinism

Need at least one of:
- hash comparison
- snapshot comparison
- repeat-run equality test

Demo mode must be deterministic.

## Required fixture coverage

Need fixtures for:
- markets list
- market detail
- FRED series
- scored dislocation snapshot

## Suggested test matrix

### Python unit
- source adapters
- contract mapping
- feature generation
- score computation
- explanation rendering

### Frontend unit
- table rendering
- filters/sorts
- loading/error states
- chart data transforms

### Integration
- API returns typed payloads
- latest snapshot uses fixture data correctly
- frontend pages consume API contract

### E2E
- home page loads
- filters work
- sorting works
- clicking row opens detail page
- methodology page loads
- demo mode banner or metadata visible if used

## Acceptance status language

Only two valid states:
- **ACCEPTED**
- **REJECTED**
