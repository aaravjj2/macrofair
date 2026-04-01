from __future__ import annotations


def score_market(market_probability: float, fair_probability: float, confidence: float, liquidity_score: float) -> dict:
    gap = round(market_probability - fair_probability, 4)
    absolute_gap = round(abs(gap), 4)
    actionability_score = round(
        absolute_gap * (0.6 + 0.4 * confidence) * (0.65 + 0.35 * liquidity_score),
        4
    )
    confidence_score = round(confidence * (0.8 + 0.2 * liquidity_score), 4)

    return {
        "gap": gap,
        "absolute_gap": absolute_gap,
        "actionability_score": actionability_score,
        "confidence_score": confidence_score
    }


def rank_markets(rows: list[dict]) -> list[dict]:
    ranked = sorted(rows, key=lambda row: row["actionability_score"], reverse=True)
    for index, row in enumerate(ranked, start=1):
        row["rank"] = index
    return ranked
