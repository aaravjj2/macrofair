from __future__ import annotations

from macrofair.explain.generator import build_explanation
from macrofair.evaluation.flagship_finding import compute_flagship_finding
from macrofair.evaluation.longitudinal_findings import (
    compute_flagship_persistence,
    compute_secondary_finding,
)
from macrofair.features.pipeline import build_feature_row
from macrofair.ingestion.fred import FREDAdapter
from macrofair.ingestion.kalshi import KalshiAdapter
from macrofair.ingestion.polymarket import PolymarketAdapter
from macrofair.modeling.fair_value import CombinedFairValueModel
from macrofair.normalization.canonical import normalize_markets
from macrofair.repository import get_history, get_metadata
from macrofair.scoring.dislocation import rank_markets, score_market


class MacroFairService:
    def __init__(self) -> None:
        self.polymarket = PolymarketAdapter()
        self.kalshi = KalshiAdapter()
        self.fred = FREDAdapter()
        self.model = CombinedFairValueModel()

    def _all_raw_markets(self) -> list[dict]:
        return normalize_markets([*self.polymarket.list_markets(), *self.kalshi.list_markets()])

    def _scored_markets(self) -> list[dict]:
        metadata = get_metadata()
        as_of = metadata["last_refresh"]
        scored_rows: list[dict] = []

        for market in self._all_raw_markets():
            features = build_feature_row(market, as_of=as_of)
            fair_probability, confidence = self.model.predict(features)
            scoring = score_market(
                market_probability=market["market_probability"],
                fair_probability=fair_probability,
                confidence=confidence,
                liquidity_score=market["liquidity_score"]
            )

            scored_rows.append({
                "market_id": market["market_id"],
                "platform": market["platform"],
                "title": market["title"],
                "category": market["category"],
                "market_probability": market["market_probability"],
                "fair_probability": fair_probability,
                "gap": scoring["gap"],
                "confidence": confidence,
                "liquidity_score": market["liquidity_score"],
                "resolution_time": market["resolution_time"],
                "updated_at": market["updated_at"],
                "actionability_score": scoring["actionability_score"],
                "mapping_confidence": market["mapping_confidence"],
                "macro_series_id": market["macro_series_id"]
            })

        return rank_markets(scored_rows)

    def list_markets(
        self,
        platform: str | None = None,
        category: str | None = None,
        limit: int = 25,
        sort_by: str = "gap",
        min_confidence: float = 0.0
    ) -> list[dict]:
        rows = self._scored_markets()
        if platform:
            rows = [row for row in rows if row["platform"].lower() == platform.lower()]
        if category:
            rows = [row for row in rows if row["category"].lower() == category.lower()]
        if min_confidence > 0:
            rows = [row for row in rows if row["confidence"] >= min_confidence]

        if sort_by == "confidence":
            rows = sorted(rows, key=lambda row: row["confidence"], reverse=True)
        elif sort_by == "time":
            rows = sorted(rows, key=lambda row: row["resolution_time"])
        else:
            rows = sorted(rows, key=lambda row: abs(row["gap"]), reverse=True)

        for idx, row in enumerate(rows, start=1):
            row["rank"] = idx

        return rows[:limit]

    def get_market(self, market_id: str) -> dict | None:
        scored = {row["market_id"]: row for row in self._scored_markets()}
        selected = scored.get(market_id)
        if not selected:
            return None

        raw = next(market for market in self._all_raw_markets() if market["market_id"] == market_id)
        features = build_feature_row(raw, as_of=get_metadata()["last_refresh"])
        explanation = build_explanation(
            feature_row=features,
            fair_probability=selected["fair_probability"],
            confidence=selected["confidence"]
        )

        return {
            "market_id": raw["market_id"],
            "platform": raw["platform"],
            "title": raw["title"],
            "description": raw["description"],
            "category": raw["category"],
            "sub_category": raw["sub_category"],
            "status": raw["status"],
            "resolution_time": raw["resolution_time"],
            "market_probability": selected["market_probability"],
            "fair_probability": selected["fair_probability"],
            "gap": selected["gap"],
            "confidence": selected["confidence"],
            "liquidity_score": raw["liquidity_score"],
            "mapping_confidence": raw["mapping_confidence"],
            "target_variable": raw["target_variable"],
            "macro_series_id": raw["macro_series_id"],
            "explanation": explanation,
            "history": get_history(market_id),
            "linked_macro_series": self.fred.get_series(raw["macro_series_id"])
        }

    def get_history(self, market_id: str) -> list[dict]:
        return get_history(market_id)

    def get_explain(self, market_id: str) -> dict | None:
        market = self.get_market(market_id)
        if not market:
            return None
        return market["explanation"]

    def get_flagship_finding(self) -> dict:
        metadata = get_metadata()
        markets = self.list_markets(limit=100, sort_by="gap")
        return compute_flagship_finding(markets=markets, as_of=metadata["last_refresh"])

    def get_flagship_persistence(self) -> dict:
        return compute_flagship_persistence()

    def get_secondary_finding(self) -> dict:
        return compute_secondary_finding()
