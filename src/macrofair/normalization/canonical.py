from __future__ import annotations

from dataclasses import dataclass


CANONICAL_CATEGORIES = {
    "cpi": "inflation",
    "inflation": "inflation",
    "fed": "fed",
    "rates": "fed",
    "unemployment": "unemployment",
    "labor": "unemployment",
    "recession": "recession",
    "business-cycle": "recession",
    "gdp": "gdp",
    "growth": "gdp",
}


@dataclass(frozen=True)
class MappingRule:
    category: str
    target_variable: str
    mapping_type: str


MAPPING_RULES = {
    "inflation": MappingRule(category="inflation", target_variable="CPI_YOY", mapping_type="threshold"),
    "fed": MappingRule(category="fed", target_variable="FED_FUNDS_PATH", mapping_type="event"),
    "unemployment": MappingRule(category="unemployment", target_variable="UNRATE", mapping_type="threshold"),
    "recession": MappingRule(category="recession", target_variable="RECESSION_RISK", mapping_type="event"),
    "gdp": MappingRule(category="gdp", target_variable="GDP_GROWTH", mapping_type="threshold"),
}


def canonicalize_category(category: str, sub_category: str) -> str:
    category_key = category.strip().lower()
    sub_category_key = sub_category.strip().lower()
    return CANONICAL_CATEGORIES.get(category_key) or CANONICAL_CATEGORIES.get(sub_category_key) or "unknown"


def normalize_market(raw_market: dict) -> dict:
    normalized = dict(raw_market)
    canonical_category = canonicalize_category(
        category=raw_market.get("category", ""),
        sub_category=raw_market.get("sub_category", ""),
    )
    rule = MAPPING_RULES.get(canonical_category)

    normalized["category"] = canonical_category
    normalized["market_probability"] = float(raw_market["market_probability"])
    normalized["best_bid"] = float(raw_market["best_bid"])
    normalized["best_ask"] = float(raw_market["best_ask"])
    normalized["midpoint"] = float(raw_market["midpoint"])
    normalized["spread"] = float(raw_market["spread"])
    normalized["volume_24h"] = float(raw_market["volume_24h"])
    normalized["open_interest"] = float(raw_market["open_interest"])
    normalized["liquidity_score"] = float(raw_market["liquidity_score"])
    normalized["mapping_confidence"] = float(raw_market.get("mapping_confidence", 0.5))

    if rule:
        normalized["mapping_type"] = rule.mapping_type
        normalized["target_variable"] = raw_market.get("target_variable", rule.target_variable)
    else:
        normalized["mapping_type"] = "unknown"
        normalized["target_variable"] = raw_market.get("target_variable", "UNKNOWN")
        normalized["mapping_confidence"] = min(normalized["mapping_confidence"], 0.4)

    return normalized


def normalize_markets(raw_markets: list[dict]) -> list[dict]:
    return [normalize_market(market) for market in raw_markets]
