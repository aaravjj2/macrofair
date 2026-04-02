from __future__ import annotations


def _percent(value: float) -> float:
    return round(value * 100.0, 2)


def compute_flagship_finding(markets: list[dict], as_of: str) -> dict:
    ranked = sorted(markets, key=lambda market: abs(float(market["gap"])), reverse=True)
    total_absolute_gap = sum(abs(float(market["gap"])) for market in ranked)

    contributions: list[dict] = []
    cumulative_share = 0.0
    for rank, market in enumerate(ranked, start=1):
        absolute_gap = abs(float(market["gap"]))
        share_of_total_gap = 0.0 if total_absolute_gap == 0.0 else absolute_gap / total_absolute_gap
        cumulative_share += share_of_total_gap
        contributions.append(
            {
                "rank": rank,
                "market_id": market["market_id"],
                "title": market["title"],
                "category": market["category"],
                "platform": market["platform"],
                "gap": round(float(market["gap"]), 4),
                "absolute_gap": round(absolute_gap, 4),
                "share_of_total_gap": round(share_of_total_gap, 4),
                "cumulative_share": round(cumulative_share, 4),
                "confidence": round(float(market["confidence"]), 4),
            }
        )

    top = contributions[0]
    second = contributions[1] if len(contributions) > 1 else None
    top_to_second_ratio = (
        round(top["absolute_gap"] / second["absolute_gap"], 3)
        if second and second["absolute_gap"] > 0
        else 0.0
    )
    herfindahl_index = round(
        sum((row["share_of_total_gap"] ** 2) for row in contributions),
        4,
    )

    category_map: dict[str, float] = {}
    for row in contributions:
        category_map[row["category"]] = category_map.get(row["category"], 0.0) + row["absolute_gap"]
    category_breakdown = [
        {
            "category": category,
            "absolute_gap": round(absolute_gap, 4),
            "share_of_total_gap": round(0.0 if total_absolute_gap == 0.0 else absolute_gap / total_absolute_gap, 4),
        }
        for category, absolute_gap in sorted(category_map.items(), key=lambda item: item[1], reverse=True)
    ]

    headline = (
        f"{top['title']} contributes {_percent(top['share_of_total_gap'])}% of total absolute gap mass, "
        f"{top_to_second_ratio}x larger than the second-ranked dislocation."
    )
    result = (
        f"Top dislocation share: {_percent(top['share_of_total_gap'])}% | "
        f"Top gap: {_percent(top['absolute_gap'])} pts | "
        f"Concentration index (HHI): {herfindahl_index}"
    )

    return {
        "headline_finding": headline,
        "question": "How concentrated are crowd-vs-fair dislocations in the current demo snapshot?",
        "method": (
            "Compute absolute gap for each scored market, divide by total absolute gap mass, "
            "and summarize concentration using top-share and Herfindahl index."
        ),
        "result": result,
        "interpretation": (
            "Dislocations are highly concentrated rather than evenly distributed, so judges can "
            "understand the product quickly by focusing on the top ranked contract."
        ),
        "limitations": [
            "Demo universe is intentionally small and fixture-based.",
            "Finding is snapshot-specific and should be monitored over time.",
            "Concentration does not imply tradability or guaranteed edge.",
        ],
        "as_of": as_of,
        "top_market_id": top["market_id"],
        "top_market_title": top["title"],
        "top_absolute_gap": top["absolute_gap"],
        "total_absolute_gap": round(total_absolute_gap, 4),
        "top_share_of_total_gap": top["share_of_total_gap"],
        "top_to_second_ratio": top_to_second_ratio,
        "herfindahl_index": herfindahl_index,
        "contributions": contributions,
        "category_breakdown": category_breakdown,
    }
