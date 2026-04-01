from __future__ import annotations

from macrofair.normalization.canonical import canonicalize_category, normalize_market
from macrofair.repository import get_markets


def test_category_canonicalization() -> None:
    assert canonicalize_category("cpi", "inflation") == "inflation"
    assert canonicalize_category("rates", "fed") == "fed"
    assert canonicalize_category("unknown", "unknown") == "unknown"


def test_normalize_market_includes_mapping_fields() -> None:
    raw = get_markets()[0]
    normalized = normalize_market(raw)
    assert normalized["category"] in {"inflation", "fed", "unemployment", "recession", "gdp"}
    assert "mapping_type" in normalized
    assert "target_variable" in normalized
    assert 0.0 <= normalized["mapping_confidence"] <= 1.0
