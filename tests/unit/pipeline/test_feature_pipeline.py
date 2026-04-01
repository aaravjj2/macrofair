from __future__ import annotations

from macrofair.features.pipeline import build_feature_row, build_feature_rows, feature_snapshot_hash
from macrofair.repository import get_markets, get_metadata


def test_feature_row_has_expected_columns() -> None:
    market = get_markets()[0]
    row = build_feature_row(market, as_of=get_metadata()["last_refresh"])
    assert row["market_id"] == market["market_id"]
    assert row["time_to_resolution_hours"] >= 0
    assert 0.0 <= row["event_urgency"] <= 1.0


def test_snapshot_hash_deterministic() -> None:
    markets = get_markets()
    as_of = get_metadata()["last_refresh"]
    rows_a = build_feature_rows(markets, as_of=as_of)
    rows_b = build_feature_rows(markets, as_of=as_of)
    assert feature_snapshot_hash(rows_a) == feature_snapshot_hash(rows_b)
