# Milestone Status

Status values:

- ACCEPTED
- REJECTED

## Milestone 0 — Repo bootstrap

Status: ACCEPTED

Evidence:

- Workspace + monorepo structure established.
- Python project config and dependency management in place.
- Lint/type/test scripts and CI workflow added.
- Docs and contribution guide available.

## Milestone 1 — Data ingestion

Status: ACCEPTED

Evidence:

- Read-only Polymarket, Kalshi, and FRED adapters implemented.
- Deterministic fixture snapshots with timestamps committed.
- Ingestion tests implemented.

## Milestone 2 — Normalization and taxonomy

Status: ACCEPTED

Evidence:

- Canonical normalization and category taxonomy implemented.
- Market-to-target mapping with mapping confidence included.
- Normalization tests implemented.

## Milestone 3 — Feature pipeline

Status: ACCEPTED

Evidence:

- Market/macro/event feature row generation implemented.
- Repeatable feature snapshot hash implemented.
- Feature determinism tests implemented.

## Milestone 4 — Fair-value model

Status: ACCEPTED

Evidence:

- Baseline model plus combined model implemented.
- Calibration layer implemented.
- Evaluation metrics and calibration chart artifacts exported.
- Model tests implemented.

## Milestone 5 — Scoring and explanation

Status: ACCEPTED

Evidence:

- Dislocation scoring and ranking implemented.
- Explanation payload generation implemented.
- Scoring/explanation tests implemented.

## Milestone 6 — API

Status: ACCEPTED

Evidence:

- FastAPI endpoints implemented and tested.
- OpenAPI export script added.

## Milestone 7 — Frontend

Status: ACCEPTED

Evidence:

- Screener, detail, and methodology pages implemented.
- Required UI states implemented.
- Interactive elements include `data-testid`.
- Frontend unit tests implemented.

## Milestone 8 — E2E and proof

Status: ACCEPTED

Evidence:

- Playwright configuration uses retries=0 and workers=1.
- Video/trace/screenshot capture enabled.
- Proof pack generated under `artifacts/proof/`.

## Milestone 9 — Demo and submission

Status: ACCEPTED

Evidence:

- Demo script created in `docs/demo_script_3min.md`.
- Submission summary created in `docs/submission_summary_300w.md`.
- Public screenshots available in proof packs.
- Public repository linked: `https://github.com/aaravjj2/macrofair`.
- Public app/API URLs verified and captured in:
	- `artifacts/proof/20260401T153759Z-milestone-9-demo-submission/public_urls.json`
	- `artifacts/proof/20260401T153759Z-milestone-9-demo-submission/checks/`

## Milestone 10 — Flagship insight and story polish

Status: ACCEPTED

Evidence:

- Current-state audit documented in `docs/current_state_audit.md`.
- Flagship analytical finding documented in `docs/findings.md`.
- Deterministic finding artifacts exported to `artifacts/evaluation/flagship_*`.
- Story-first UI updates shipped on homepage, detail page, and methodology page.
- Typed flagship finding endpoint added: `GET /api/v1/findings/flagship`.
- Fresh proof pack generated at:
  - `artifacts/proof/20260402T024608Z-milestone-10-flagship-story/`

## Milestone 11 — Longitudinal and secondary findings evidence

Status: ACCEPTED

Evidence:

- Committed deterministic snapshot window fixture: `data/fixtures/snapshot_window.json`.
- Longitudinal flagship persistence artifacts:
	- `artifacts/evaluation/flagship_persistence.json`
	- `artifacts/evaluation/flagship_persistence.csv`
	- `artifacts/evaluation/flagship_persistence.svg`
- Secondary deterministic finding artifacts:
	- `artifacts/evaluation/secondary_finding.json`
	- `artifacts/evaluation/secondary_finding.csv`
	- `artifacts/evaluation/secondary_finding.svg`
- Typed API endpoints added:
	- `GET /api/v1/findings/flagship/persistence`
	- `GET /api/v1/findings/secondary`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T031728Z-milestone-11-longitudinal-findings/`

## Milestone 12 — Optional Zerve integration layer

Status: ACCEPTED

Evidence:

- Optional server-side integration module:
	- `src/macrofair/integrations/zerve/config.py`
	- `src/macrofair/integrations/zerve/client.py`
- Typed integration endpoints:
	- `GET /api/v1/integrations/zerve/status`
	- `GET /api/v1/integrations/zerve/package`
	- `POST /api/v1/integrations/zerve/sync`
- Deterministic submission package export:
	- `artifacts/evaluation/zerve_submission_package.json`
	- `scripts/export_zerve_submission_package.py`
- Integration documentation:
	- `docs/zerve_integration.md`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T033334Z-milestone-12-zerve-integration/`

## Milestone 13 — Live Zerve verification hardening

Status: ACCEPTED

Evidence:

- Added sanitized live verification exporter:
	- `scripts/verify_zerve_live.py`
- Live verification artifact (key-safe):
	- `artifacts/evaluation/zerve_live_verification.json`
- Updated default integration base URL and env template:
	- `src/macrofair/integrations/zerve/config.py`
	- `.env.example`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-13-live-zerve-verification/`

## Milestone 14 — Public URL verification

Status: ACCEPTED

Evidence:

- Public URL declarations and checks:
	- `artifacts/evaluation/public_urls.json`
	- `artifacts/evaluation/public_url_verification.json`
	- `artifacts/evaluation/public_checks/`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-14-public-url-verification/`

## Milestone 15 — Expanded longitudinal window

Status: ACCEPTED

Evidence:

- Added deterministic snapshot-window generator:
	- `scripts/generate_expanded_snapshot_window.py`
- Expanded snapshot fixture to v2 (12 snapshots):
	- `data/fixtures/snapshot_window.json`
- Refreshed persistence artifacts:
	- `artifacts/evaluation/flagship_persistence.json`
	- `artifacts/evaluation/flagship_persistence.csv`
	- `artifacts/evaluation/flagship_persistence.svg`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-15-expanded-snapshot-window/`

## Milestone 16 — Third deterministic finding

Status: ACCEPTED

Evidence:

- Added category-drift third finding computation:
	- `src/macrofair/evaluation/longitudinal_findings.py`
- Third finding artifacts:
	- `artifacts/evaluation/third_finding.json`
	- `artifacts/evaluation/third_finding.csv`
	- `artifacts/evaluation/third_finding.svg`
	- `artifacts/evaluation/third_finding_snapshot_category_shares.csv`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-16-third-deterministic-finding/`

## Milestone 17 — Consolidated findings/report surfaces

Status: ACCEPTED

Evidence:

- Added typed consolidated schemas and service payload builders:
	- `src/macrofair/schemas.py`
	- `src/macrofair/service.py`
- Added API endpoints:
	- `GET /api/v1/findings`
	- `GET /api/v1/findings/report`
	- `GET /api/v1/reports/submission`
	- `GET /api/v1/findings/third`
- Consolidated artifacts:
	- `artifacts/evaluation/findings_index.json`
	- `artifacts/evaluation/findings_report.json`
	- `artifacts/evaluation/submission_report.json`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-17-consolidated-findings-reports/`

## Milestone 18 — Export bundle expansion

Status: ACCEPTED

Evidence:

- Exporters expanded for third finding and consolidated reports:
	- `scripts/export_longitudinal_findings.py`
	- `scripts/export_zerve_submission_package.py`
- Updated package/report artifacts:
	- `artifacts/evaluation/zerve_submission_package.json`
	- `artifacts/evaluation/findings_report.json`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-18-export-bundle-expansion/`

## Milestone 19 — Findings UX expansion

Status: ACCEPTED

Evidence:

- Findings/methodology UI updated for v2 window and third finding:
	- `apps/web/app/findings/page.tsx`
	- `apps/web/app/methodology/page.tsx`
	- `apps/web/lib/findings-data.ts`
	- `apps/web/lib/findings-utils.ts`
- E2E updated to validate third findings panel:
	- `tests/e2e/smoke.spec.ts`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-19-findings-ui-expansion/`

## Milestone 20 — Docs and demo freeze

Status: ACCEPTED

Evidence:

- Findings, API, integration, and submission docs refreshed:
	- `docs/findings.md`
	- `api_spec.md`
	- `docs/zerve_integration.md`
	- `docs/demo_script_3min.md`
	- `docs/submission_summary_300w.md`
	- `README.md`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-20-docs-and-demo-freeze/`

## Milestone 21 — Gate hardening and regression coverage

Status: ACCEPTED

Evidence:

- Updated tests for v2 window, third finding, and report endpoints:
	- `tests/unit/api/test_api.py`
	- `tests/unit/evaluation/test_longitudinal_findings.py`
	- `tests/unit/evaluation/test_zerve_submission_package.py`
	- `apps/web/lib/__tests__/findings-utils.test.ts`
- Final gate summary:
	- `artifacts/evaluation/gate_summary_13_22.json`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-21-gate-hardening/`

## Milestone 22 — Submission readiness

Status: ACCEPTED

Evidence:

- Finalized evaluation/report/public/live verification artifacts:
	- `artifacts/evaluation/findings_index.json`
	- `artifacts/evaluation/findings_report.json`
	- `artifacts/evaluation/submission_report.json`
	- `artifacts/evaluation/public_url_verification.json`
	- `artifacts/evaluation/zerve_live_verification.json`
- Fresh proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-22-submission-readiness/`

## Milestone 13–22 Rollup

Status: ACCEPTED

Evidence:

- Consolidated rollup proof pack generated at:
	- `artifacts/proof/20260402T055144Z-milestone-rollup-13-22/`
