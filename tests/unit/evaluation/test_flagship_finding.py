from __future__ import annotations

from macrofair.evaluation.flagship_finding import compute_flagship_finding
from macrofair.service import MacroFairService


def test_flagship_finding_is_deterministic() -> None:
    service = MacroFairService()
    markets = service.list_markets(limit=100, sort_by="gap")

    first = compute_flagship_finding(markets=markets, as_of="2026-03-31T23:55:00Z")
    second = compute_flagship_finding(markets=markets, as_of="2026-03-31T23:55:00Z")

    assert first == second


def test_flagship_finding_has_expected_shape() -> None:
    service = MacroFairService()
    finding = service.get_flagship_finding()

    assert finding["top_market_id"] == "poly-cpi-jun-2026-over-3"
    assert finding["top_share_of_total_gap"] > 0.5
    assert finding["top_to_second_ratio"] > 2.0
    assert len(finding["contributions"]) >= 5