from __future__ import annotations

import hashlib
import json
from typing import Any

from macrofair.explain.generator import build_explanation
from macrofair.evaluation.flagship_finding import compute_flagship_finding
from macrofair.evaluation.longitudinal_findings import (
    compute_flagship_persistence,
    compute_secondary_finding,
)
from macrofair.features.pipeline import build_feature_row
from macrofair.ingestion.fred import FREDAdapter
from macrofair.integrations.zerve import ZerveClient, ZerveSettings, load_zerve_settings
from macrofair.ingestion.kalshi import KalshiAdapter
from macrofair.ingestion.polymarket import PolymarketAdapter
from macrofair.modeling.fair_value import CombinedFairValueModel
from macrofair.normalization.canonical import normalize_markets
from macrofair.repository import get_history, get_metadata
from macrofair.scoring.dislocation import rank_markets, score_market
from macrofair.settings import app_mode, app_version


class MacroFairService:
    def __init__(
        self,
        zerve_settings: ZerveSettings | None = None,
        zerve_client: ZerveClient | None = None,
    ) -> None:
        self.polymarket = PolymarketAdapter()
        self.kalshi = KalshiAdapter()
        self.fred = FREDAdapter()
        self.model = CombinedFairValueModel()
        self.zerve_settings = zerve_settings or load_zerve_settings()
        self.zerve_client = zerve_client or ZerveClient(self.zerve_settings)

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

    @staticmethod
    def _payload_hash(payload: dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def get_zerve_status(self, verify_remote: bool = False) -> dict[str, Any]:
        settings = self.zerve_settings
        status: dict[str, Any] = {
            "integration": "zerve",
            "enabled": settings.enabled,
            "configured": settings.configured,
            "mode": app_mode(),
            "base_url": settings.base_url if settings.enabled else "",
            "project_id": settings.project_id if settings.enabled else "",
            "api_key_configured": settings.api_key_configured,
            "missing_required": settings.missing_required,
            "remote_check_attempted": False,
            "remote_connected": False,
            "remote_status_code": None,
            "last_error": None,
            "note": "Zerve integration disabled. Demo mode remains default.",
        }

        if settings.enabled and not settings.configured:
            status["note"] = "Zerve integration enabled but missing required server-side env vars."
        elif settings.configured:
            status["note"] = "Zerve integration configured and ready."

        if verify_remote and settings.configured:
            remote = self.zerve_client.check_project_status()
            status["remote_check_attempted"] = True
            status["remote_connected"] = bool(remote.get("ok"))
            status["remote_status_code"] = remote.get("status_code")
            status["last_error"] = remote.get("error")
            if remote.get("ok"):
                status["note"] = "Zerve configuration verified via remote status check."
            else:
                status["note"] = "Zerve configured but remote status check failed."

        return status

    def get_zerve_submission_package(self) -> dict[str, Any]:
        metadata = get_metadata()
        ranked = self.list_markets(limit=10, sort_by="gap")

        package: dict[str, Any] = {
            "package_name": "macrofair-zerve-submission-package",
            "package_version": "1.0.0",
            "generated_at": metadata["last_refresh"],
            "mode": app_mode(),
            "app_version": app_version(),
            "model_version": metadata["model_version"],
            "schema_version": metadata["schema_version"],
            "metadata": {
                "supported_categories": metadata["supported_categories"],
                "sources": metadata["sources"],
                "snapshot_as_of": metadata["last_refresh"],
            },
            "findings": {
                "flagship": self.get_flagship_finding(),
                "flagship_persistence": self.get_flagship_persistence(),
                "secondary": self.get_secondary_finding(),
            },
            "ranked_snapshot_summary": {
                "count": len(ranked),
                "markets": [
                    {
                        "rank": row["rank"],
                        "market_id": row["market_id"],
                        "title": row["title"],
                        "platform": row["platform"],
                        "category": row["category"],
                        "market_probability": row["market_probability"],
                        "fair_probability": row["fair_probability"],
                        "gap": row["gap"],
                        "confidence": row["confidence"],
                    }
                    for row in ranked
                ],
            },
        }
        package["payload_hash"] = self._payload_hash(package)
        return package

    def get_zerve_package_payload(self) -> dict[str, Any]:
        return {
            "status": self.get_zerve_status(verify_remote=False),
            "package": self.get_zerve_submission_package(),
        }

    def sync_zerve_submission_package(self, dry_run: bool = True) -> dict[str, Any]:
        status = self.get_zerve_status(verify_remote=False)
        package = self.get_zerve_submission_package()
        package_hash = package["payload_hash"]

        if not status["configured"]:
            return {
                "attempted": False,
                "dry_run": dry_run,
                "synced": False,
                "status_code": None,
                "message": "Zerve is disabled or missing required configuration.",
                "remote_error": None,
                "package_hash": package_hash,
                "status": status,
            }

        if dry_run:
            return {
                "attempted": False,
                "dry_run": True,
                "synced": False,
                "status_code": None,
                "message": "Dry run only. Package was not sent to Zerve.",
                "remote_error": None,
                "package_hash": package_hash,
                "status": status,
            }

        remote = self.zerve_client.sync_submission_package(package)
        payload = remote.get("payload")
        remote_reference = payload.get("id") if isinstance(payload, dict) else None
        return {
            "attempted": True,
            "dry_run": False,
            "synced": bool(remote.get("ok")),
            "status_code": remote.get("status_code"),
            "message": "Zerve sync completed." if remote.get("ok") else "Zerve sync failed.",
            "remote_error": remote.get("error"),
            "remote_reference": remote_reference,
            "package_hash": package_hash,
            "status": status,
        }
