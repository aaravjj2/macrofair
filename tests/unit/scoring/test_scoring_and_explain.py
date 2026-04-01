from __future__ import annotations

from macrofair.explain.generator import build_explanation
from macrofair.features.pipeline import build_feature_row
from macrofair.repository import get_markets, get_metadata
from macrofair.scoring.dislocation import rank_markets, score_market


def test_score_market_has_required_fields() -> None:
    score = score_market(market_probability=0.58, fair_probability=0.51, confidence=0.81, liquidity_score=0.7)
    assert {"gap", "absolute_gap", "actionability_score", "confidence_score"}.issubset(score.keys())


def test_rank_markets_orders_by_actionability() -> None:
    rows = [
        {"market_id": "a", "actionability_score": 0.15},
        {"market_id": "b", "actionability_score": 0.21},
        {"market_id": "c", "actionability_score": 0.08},
    ]
    ranked = rank_markets(rows)
    assert ranked[0]["market_id"] == "b"
    assert ranked[0]["rank"] == 1


def test_explanation_payload_has_factors() -> None:
    feature_row = build_feature_row(get_markets()[0], as_of=get_metadata()["last_refresh"])
    explain = build_explanation(feature_row=feature_row, fair_probability=0.55, confidence=0.82)
    assert len(explain["top_factors"]) == 3
    assert "narrative_summary" in explain
