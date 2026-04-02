# Zerve Integration

## What this integration does

MacroFair provides an optional, server-side Zerve integration layer that can:

- report integration status (`GET /api/v1/integrations/zerve/status`)
- expose a deterministic findings package for deployment/sync workflows (`GET /api/v1/integrations/zerve/package`)
- optionally sync the package when explicitly requested (`POST /api/v1/integrations/zerve/sync`)

The package includes:

- flagship finding
- flagship persistence finding
- secondary finding
- latest ranked snapshot summary
- metadata and deterministic package hash

## What this integration does not do

- It does not replace default deterministic demo mode.
- It does not require a Zerve account for normal app usage.
- It does not expose secrets to frontend code.
- It does not run live network calls in tests.

## Required env vars

All values are read server-side:

- `ZERVE_ENABLED` (default: `false`)
- `ZERVE_API_KEY`
- `ZERVE_BASE_URL` (default: `https://api.zerve.ai`)
- `ZERVE_PROJECT_ID`
- `ZERVE_TIMEOUT_SECONDS` (default: `4.0`)

Optional:

- `MACROFAIR_API_BASE_URL` (used by the web findings page to query backend status; if absent, frontend uses a safe fallback status)

## API key handling and safety

- API key is only read from server-side environment variables.
- API responses expose only `api_key_configured` as a boolean.
- No endpoint returns the raw key.
- No key material is written to artifacts, logs, or frontend bundles.
- `.env` files are git-ignored; use `.env.example` as template.

## Default behavior (no key present)

When key/config is absent:

- app remains fully functional in deterministic demo mode
- findings APIs and frontend continue to work
- Zerve status endpoint reports disabled/unconfigured state
- sync endpoint returns graceful non-sync fallback response

## Local setup

1. Copy `.env.example` to `.env`.
2. Keep `ZERVE_ENABLED=false` for default deterministic mode.
3. To enable optional integration, set:
   - `ZERVE_ENABLED=true`
   - `ZERVE_API_KEY`
   - `ZERVE_PROJECT_ID`
   - `ZERVE_BASE_URL` (if non-default)
4. Start backend and web app as usual.
5. Check status at `/api/v1/integrations/zerve/status`.

## Limitations

- Sync endpoint assumes a Zerve-compatible API path and may require endpoint adaptation for a specific project.
- Connectivity verification is optional and disabled by default unless explicitly requested.
- This milestone focuses on safe packaging/status/sync primitives rather than full deployment orchestration.
