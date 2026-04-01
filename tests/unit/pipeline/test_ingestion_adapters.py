from __future__ import annotations

from macrofair.ingestion.fred import FREDAdapter
from macrofair.ingestion.kalshi import KalshiAdapter
from macrofair.ingestion.polymarket import PolymarketAdapter


def test_polymarket_adapter_returns_fixture_markets() -> None:
    rows = PolymarketAdapter().list_markets()
    assert rows
    assert all(row["platform"] == "Polymarket" for row in rows)


def test_kalshi_adapter_returns_fixture_markets() -> None:
    rows = KalshiAdapter().list_markets()
    assert rows
    assert all(row["platform"] == "Kalshi" for row in rows)


def test_fred_adapter_reads_series() -> None:
    series = FREDAdapter().get_series("CPIAUCSL")
    assert len(series) >= 2
    assert all("value" in point for point in series)
