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
