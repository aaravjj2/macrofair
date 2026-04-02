# MANIFEST

## Objective

Deliver a memorable, evidence-backed submission pass by adding a deterministic flagship finding, surfacing it clearly in the UI, and proving quality gates with fresh artifacts.

## Scope

- Added deterministic flagship finding computation and exports
- Added typed API endpoint for flagship finding
- Improved homepage hierarchy (hero, featured dislocation, flagship finding strip)
- Improved detail-page context and methodology path
- Expanded methodology page for interpretation clarity
- Updated docs for audit, findings, demo script, and submission narrative

## Exact Commands Run

- `npm run tsc`
- `npm run vitest`
- `/home/aarav/Aarav/macrofair/.venv/bin/python -m pytest -q`
- `npm run playwright`
- `npx playwright test --reporter=line,html`

## Exact Results

- TypeScript (`tsc`): passed, 0 errors
- Vitest: 5 passed, 0 failed, 0 skipped
- Pytest: 23 passed, 0 failed, 0 skipped
- Playwright: 1 passed, 0 failed, 0 skipped, retries=0, workers=1

## Root Causes And Fixes

- No gate failures occurred in the final verification run.

## File Inventory

- `manifest.json`
- `README.md`
- `playwright-report/`
- `test-results/`
- `screenshots/`
- `TOUR.webm`

## Known Limitations

- Flagship finding is computed on a small deterministic fixture universe.
- Concentration finding is snapshot-specific and should be tracked over time.
- Demo-mode evidence is research-oriented and not trading advice.
