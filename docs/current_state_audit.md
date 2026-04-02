# Current State Audit

## What Already Exists

- Production-structured monorepo with `apps/api`, `apps/web`, `src/macrofair`, `tests`, `data/fixtures`, and proof-pack conventions.
- Deterministic demo-mode adapters, normalization, feature generation, fair-value modeling, scoring, and explanation layers.
- FastAPI endpoints for health, metadata, market list/detail/history/explain, plus snapshot/compare.
- Next.js screener, market detail, and methodology routes with `data-testid` on existing interactive controls.
- Test stack and CI are wired (`tsc`, `vitest`, `pytest`, `playwright`) with strict Playwright policy settings.
- Prior proof packs and evaluation artifacts already present.

## Weak Or Underdeveloped

- No single analytical result is visibly dominant in the product story.
- Homepage is functional but table-first; judges must infer the main insight.
- Methodology page explains pipeline but is light on practical interpretation guidance.
- API does not expose a typed, reusable flagship finding payload.
- Research docs mention findings, but the centerpiece insight is not explicitly documented as a deterministic computed artifact.

## Missing For Strong Submission

- One headline, defensible, reproducible finding with exported evidence (JSON/CSV/chart).
- Homepage hierarchy that communicates value proposition and top insight in under 10 seconds.
- Stronger detail-page narrative bridge to methodology.
- Dedicated milestone proof for this submission-polish pass.

## Changes In This Pass

- Added deterministic flagship finding computation for dislocation concentration.
- Added typed API endpoint: `GET /api/v1/findings/flagship`.
- Added exporter to write flagship evidence into `artifacts/evaluation/`.
- Updated homepage with hero, featured dislocation card, and flagship finding strip.
- Strengthened market detail context and explicit methodology navigation.
- Expanded methodology content to cover fair value, confidence, demo mode, limitations, and interpretation.
- Added unit + API + E2E checks for new story-first and findings behavior.
