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
