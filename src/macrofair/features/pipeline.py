from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone


def _parse_iso8601(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def build_feature_row(market: dict, as_of: str) -> dict:
    as_of_dt = _parse_iso8601(as_of)
    resolution_dt = _parse_iso8601(market["resolution_time"])
    time_to_resolution_hours = max((resolution_dt - as_of_dt).total_seconds() / 3600.0, 0.0)

    # Event urgency is 1.0 near resolution and tapers to 0.0 with longer horizons.
    event_urgency = max(0.0, min(1.0, 1.0 - min(time_to_resolution_hours / (24.0 * 180.0), 1.0)))

    return {
        "market_id": market["market_id"],
        "as_of": as_of_dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "time_to_resolution_hours": time_to_resolution_hours,
        "market_probability": float(market["market_probability"]),
        "spread": float(market["spread"]),
        "volume_24h": float(market["volume_24h"]),
        "open_interest": float(market["open_interest"]),
        "liquidity_score": float(market["liquidity_score"]),
        "macro_signal": float(market["macro_signal"]),
        "momentum_24h": float(market["momentum_24h"]),
        "mapping_confidence": float(market["mapping_confidence"]),
        "event_urgency": event_urgency
    }


def build_feature_rows(markets: list[dict], as_of: str) -> list[dict]:
    return [build_feature_row(market, as_of=as_of) for market in markets]


def feature_snapshot_hash(feature_rows: list[dict]) -> str:
    canonical_payload = json.dumps(feature_rows, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
