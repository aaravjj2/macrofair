from __future__ import annotations


def build_explanation(feature_row: dict, fair_probability: float, confidence: float) -> dict:
    market_probability = feature_row["market_probability"]
    liquidity = feature_row["liquidity_score"]
    spread = feature_row["spread"]
    event_urgency = feature_row["event_urgency"]
    macro_signal = feature_row["macro_signal"]
    momentum = feature_row["momentum_24h"]

    contributions = {
        "macro_signal_divergence": round((macro_signal - market_probability) * 0.55, 4),
        "market_momentum": round(momentum * 0.35, 4),
        "liquidity_adjustment": round((liquidity - 0.5) * 0.2, 4),
        "horizon_pressure": round((0.5 - event_urgency) * 0.15, 4)
    }

    top_factors = [
        key
        for key, _ in sorted(
            contributions.items(),
            key=lambda item: abs(item[1]),
            reverse=True
        )[:3]
    ]

    direction = "above" if market_probability > fair_probability else "below"
    warning_flags: list[str] = []
    if liquidity < 0.45:
        warning_flags.append("LOW_LIQUIDITY")
    if spread > 0.03:
        warning_flags.append("WIDE_SPREAD")

    return {
        "top_factors": top_factors,
        "factor_contributions": contributions,
        "model_notes": "Baseline blend of market microstructure and mapped macro signals.",
        "confidence_notes": f"Confidence {confidence:.2f} incorporates liquidity, spread, and mapping stability.",
        "warning_flags": warning_flags,
        "narrative_summary": (
            f"Market odds are {direction} model fair value, mainly driven by "
            f"{top_factors[0].replace('_', ' ')} and {top_factors[1].replace('_', ' ')}."
        )
    }
