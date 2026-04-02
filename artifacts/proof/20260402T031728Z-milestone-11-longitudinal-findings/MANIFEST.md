# MANIFEST

## Objective

Strengthen MacroFair's claim beyond a single snapshot by proving flagship dislocation persistence across a deterministic snapshot window and adding a complementary deterministic secondary finding.

## Scope

- Added committed deterministic longitudinal snapshot fixture window.
- Added deterministic analytics pipeline for flagship persistence across snapshots.
- Added deterministic secondary finding (platform gap asymmetry).
- Added typed API schema/service/endpoint support for both findings.
- Added frontend findings evidence surfacing (methodology + dedicated findings page).
- Updated docs and evaluation artifacts.
- Re-ran full quality gates and captured fresh proof artifacts.

## Exact Commands Run

- `npm run tsc`
- `npm run vitest`
- `python -m pytest -q`
- `npm run playwright`
- `python scripts/export_longitudinal_findings.py`
- `python scripts/export_openapi.py`
- `./scripts/create_proof_pack.sh milestone-11-longitudinal-findings`

## Exact Results

- TypeScript (`tsc`): passed, 0 errors
- Vitest: 7 passed, 0 failed, 0 skipped
- Pytest: 28 passed, 0 failed, 0 skipped
- Playwright: 1 passed, 0 failed, 0 skipped, retries=0, workers=1

## Root Causes And Fixes

- No gate failures occurred in the final run.

## File Inventory

- `manifest.json`
- `MANIFEST.md`
- `README.md`
- `playwright-report/`
- `test-results/`
- `screenshots/`
- `TOUR.webm`

## Known Limitations

- Longitudinal window is short and synthetic for deterministic reproducibility.
- Secondary finding is descriptive and does not imply causality.
- Demo universe is intentionally small relative to full production-scale market coverage.
