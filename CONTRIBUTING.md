# Contributing

## Setup

1. Install dependencies:
   - `npm install`
   - `python -m pip install -e .[dev]`
2. Use deterministic demo fixtures in `data/fixtures/` for all tests.

## Required quality gates

Run all commands before opening a PR:

- `npm run lint`
- `npm run tsc`
- `npm run vitest`
- `python -m pytest -q`
- `npm run playwright`

## Test policy

- Every interactive element must include `data-testid`.
- Playwright selectors should use `data-testid`.
- No skipped tests in final milestone proof.

## Proof packs

Every milestone must include:

- `artifacts/proof/<timestamp>-<milestone>/MANIFEST.md`
- `manifest.json`
- test outputs and media artifacts

Use `scripts/create_proof_pack.sh <milestone-name>` after running all gates.
