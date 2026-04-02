# MANIFEST

## Objective

Finalize submission-ready package with updated findings, reports, docs, and verification artifacts.

## Scope

- Regenerated all evaluation exports from final code state.
- Included live/public verification artifacts in submission evidence set.
- Prepared milestone status updates and final rollup proof package.

## Exact Commands Run

- `npm run tsc`
- `npm run vitest`
- `PYTHONPATH=src /home/aarav/Aarav/macrofair/.venv/bin/python -m pytest -q`
- `npm run playwright`
- `PYTHONPATH=src /home/aarav/Aarav/macrofair/.venv/bin/python scripts/export_flagship_finding.py`
- `PYTHONPATH=src /home/aarav/Aarav/macrofair/.venv/bin/python scripts/export_longitudinal_findings.py`
- `PYTHONPATH=src /home/aarav/Aarav/macrofair/.venv/bin/python scripts/export_zerve_submission_package.py`
- `PYTHONPATH=src /home/aarav/Aarav/macrofair/.venv/bin/python scripts/export_openapi.py`
- `PYTHONPATH=src /home/aarav/Aarav/macrofair/.venv/bin/python scripts/verify_zerve_live.py`

## Exact Results

- TypeScript (`tsc`): passed, 0 errors
- Vitest: 10 passed, 0 failed, 0 skipped
- Pytest: 44 passed, 0 failed, 0 skipped
- Playwright: 1 passed, 0 failed, 0 skipped, retries=0, workers=1

## Security And Defaults Statement

- No secrets were hardcoded, logged, committed, or exposed in frontend payloads.
- API responses expose key/config presence only; raw key material is never returned.
- Demo mode remained the default behavior.

## File Inventory

- `README.md`
- `TOUR.webm`
- `docs/submission_checklist.md`
- `evidence/findings_index.json`
- `evidence/findings_report.json`
- `evidence/public_url_verification.json`
- `evidence/submission_report.json`
- `evidence/zerve_live_verification.json`
- `manifest.json`
- `playwright-report/data/2a359567733de3ee1ac486f06c33a518a8468883.png`
- `playwright-report/data/55323f582df0b01eab268ae92de0ac91744c2f35.webm`
- `playwright-report/data/d29f248eaf0ac8c9b8b10fd71e048d8b3b667436.zip`
- `playwright-report/index.html`
- `playwright-report/trace/assets/codeMirrorModule-DS0FLvoc.js`
- `playwright-report/trace/assets/defaultSettingsView-GTWI-W_B.js`
- `playwright-report/trace/codeMirrorModule.DYBRYzYX.css`
- `playwright-report/trace/codicon.DCmgc-ay.ttf`
- `playwright-report/trace/defaultSettingsView.B4dS75f0.css`
- `playwright-report/trace/index.CzXZzn5A.css`
- `playwright-report/trace/index.Dtstcb7U.js`
- `playwright-report/trace/index.html`
- `playwright-report/trace/manifest.webmanifest`
- `playwright-report/trace/playwright-logo.svg`
- `playwright-report/trace/snapshot.html`
- `playwright-report/trace/sw.bundle.js`
- `playwright-report/trace/uiMode.Btcz36p_.css`
- `playwright-report/trace/uiMode.Vipi55dB.js`
- `playwright-report/trace/uiMode.html`
- `playwright-report/trace/xtermModule.DYP7pi_n.css`
- `screenshots/home-detail-methodology.png`
- `test-results/.last-run.json`
- `test-results/smoke-screener-to-detail-and-methodology/test-finished-1.png`
- `test-results/smoke-screener-to-detail-and-methodology/trace.zip`
- `test-results/smoke-screener-to-detail-and-methodology/video.webm`
