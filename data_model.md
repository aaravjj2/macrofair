# Data Model

## Canonical entities

### Market
Represents one tradable contract outcome.

Fields:
- `market_id`
- `platform`
- `source_event_id`
- `title`
- `description`
- `category`
- `sub_category`
- `status`
- `resolution_time`
- `created_at`
- `updated_at`

### MarketSnapshot
Latest observed market state.

Fields:
- `market_id`
- `as_of`
- `market_probability`
- `best_bid`
- `best_ask`
- `midpoint`
- `spread`
- `volume_24h`
- `open_interest`
- `liquidity_score`

### MarketHistoryPoint
Normalized history point for charts and features.

Fields:
- `market_id`
- `timestamp`
- `probability`
- `volume`
- `spread`

### MacroSeriesPoint
Macro observation from FRED or derived source.

Fields:
- `series_id`
- `timestamp`
- `value`
- `vintage_date`
- `source`

### ContractMapping
Maps a market to its macro interpretation.

Fields:
- `market_id`
- `mapping_type`
- `target_variable`
- `target_threshold`
- `target_window_start`
- `target_window_end`
- `mapping_confidence`
- `mapping_notes`

### FeatureRow
Model-ready row for fair-value estimation.

Fields:
- `feature_row_id`
- `market_id`
- `as_of`
- `time_to_resolution_hours`
- `market_probability`
- `spread`
- `volume_features...`
- `macro_features...`
- `platform_features...`

### FairValueEstimate
Model output.

Fields:
- `market_id`
- `as_of`
- `fair_probability`
- `model_version`
- `calibration_version`
- `confidence`
- `uncertainty_band_low`
- `uncertainty_band_high`

### DislocationScore
Final ranking output.

Fields:
- `market_id`
- `as_of`
- `gap`
- `absolute_gap`
- `actionability_score`
- `confidence_score`
- `rank`

### Explanation
Human-readable explanation bundle.

Fields:
- `market_id`
- `as_of`
- `top_factors`
- `factor_contributions`
- `warning_flags`
- `narrative_summary`

## File outputs

Recommended outputs:
- `data/processed/markets.parquet`
- `data/processed/snapshots.parquet`
- `data/processed/features.parquet`
- `data/processed/fair_values.parquet`
- `data/processed/dislocations.parquet`
- `data/processed/latest_snapshot.json`

## Versioning

Every processed output must include:
- schema version
- run id
- source timestamp
- model version
