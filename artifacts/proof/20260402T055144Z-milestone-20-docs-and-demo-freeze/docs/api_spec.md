# API Spec

## API design goals

- stable, typed, judge-friendly
- read-only in V1
- deterministic fixture mode
- small enough to finish during the hackathon

## Base path

`/api/v1`

## Endpoints

### GET `/health`
Returns service health and current mode.

Response:
```json
{
  "status": "ok",
  "mode": "demo",
  "version": "0.1.0"
}
```

### GET `/metadata`
Returns source versions, last refresh time, supported categories, and model version.

### GET `/markets`
List live scored markets.

Query params:
- `platform`
- `category`
- `limit`
- `sort_by`
- `min_confidence`

Response fields:
- `market_id`
- `platform`
- `title`
- `category`
- `market_probability`
- `fair_probability`
- `gap`
- `confidence`
- `liquidity_score`
- `resolution_time`
- `updated_at`

### GET `/markets/{market_id}`
Return full detail for one market.

Includes:
- static metadata
- latest market stats
- fair-value estimate
- explanation factors
- linked macro series
- recent history

### GET `/markets/{market_id}/history`
Return normalized history series for charts.

### GET `/markets/{market_id}/explain`
Return explanation payload only.

Fields:
- `top_factors`
- `factor_contributions`
- `model_notes`
- `confidence_notes`

### GET `/findings/flagship`
Return the deterministic headline finding payload used for homepage storytelling and demo narration.

Fields include:

- `headline_finding`
- `question`
- `method`
- `result`
- `interpretation`
- `limitations`
- `top_market_id`
- `top_market_title`
- `top_absolute_gap`
- `top_share_of_total_gap`
- `top_to_second_ratio`
- `herfindahl_index`
- `contributions`

### GET `/findings/flagship/persistence`
Return longitudinal concentration evidence computed across committed deterministic snapshots.

Fields include:

- `window_name`
- `window_size`
- `dominant_top_market_id`
- `persistence_rate`
- `average_top_share`
- `snapshots[]` with `top_share_of_total_gap`, `top_to_second_ratio`, and `herfindahl_index`

### GET `/findings/secondary`
Return the complementary deterministic finding payload.

Current secondary finding type:

- platform gap asymmetry (`polymarket_mean_gap - kalshi_mean_gap`)

Fields include:

- `window_name`
- `window_size`
- `average_asymmetry_gap`
- `positive_window_share`
- `one_sentence`
- `snapshots[]`

### GET `/findings/third`
Return the third deterministic finding payload focused on category-share drift.

Fields include:

- `window_name`
- `window_size`
- `dominant_drift_category`
- `dominant_drift_points`
- `one_sentence`
- `category_drift[]`
- `snapshots[]` (with `category_shares[]`)

### GET `/findings`
Return a compact findings index with deterministic headlines and payload hash.

Fields include:

- `generated_at`
- `mode`
- `window_name`
- `window_size`
- `headlines` (`flagship`, `flagship_persistence`, `secondary`, `third`)
- `payload_hash`

### GET `/findings/report`
Return the full typed consolidated findings report payload.

Fields include:

- report metadata (`report_name`, `report_version`, `generated_at`, `mode`)
- model/schema metadata
- `findings` bundle (`flagship`, `flagship_persistence`, `secondary`, `third`)
- `ranked_snapshot_summary`
- deterministic `payload_hash`

### GET `/reports/submission`
Return a submission-ready wrapper around findings report plus Zerve integration status.

Fields include:

- `report_name`
- `findings_report`
- `zerve_integration`
- deterministic `payload_hash`

### GET `/integrations/zerve/status`
Return server-side integration status without exposing secrets.

Fields include:

- `enabled`
- `configured`
- `api_key_configured` (boolean only)
- `missing_required`
- `mode`
- `remote_check_attempted`
- `remote_connected`

### GET `/integrations/zerve/package`
Return deterministic submission package payload plus current integration status.

Package includes:

- flagship finding
- persistence finding
- secondary finding
- third finding
- ranked snapshot summary
- findings report hash
- deterministic `payload_hash`

### POST `/integrations/zerve/sync`
Optional sync endpoint for sending submission package to Zerve-compatible API.

Request body:

- `dry_run` (boolean, default `true`)

Behavior:

- Disabled/unconfigured mode: returns safe non-sync fallback.
- Dry run mode: validates package and returns no-network result.
- Live sync only when explicitly requested and configured.

### GET `/snapshots/latest`
Return current ranked snapshot and metadata.

### GET `/compare`
Compare matching or near-matching contracts across platforms where supported.

## Error format

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Market not found"
  }
}
```

## Performance targets

- `/health`: < 100 ms
- `/markets`: < 500 ms in demo mode
- detail endpoints: < 800 ms in demo mode

## OpenAPI

FastAPI should auto-generate OpenAPI docs and keep response models fully typed.

## Future endpoints

Not for V1:
- watchlists
- alerts
- export CSV
- paper-trading simulation
