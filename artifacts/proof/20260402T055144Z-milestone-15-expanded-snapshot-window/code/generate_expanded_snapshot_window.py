from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = ROOT / "data" / "fixtures" / "snapshot_window.json"


def _round(value: float, digits: int = 4) -> float:
    return round(float(value), digits)


def _snapshot_label(timestamp: datetime) -> str:
    return timestamp.strftime("%Y-%m-%d close")


def _snapshot_id(timestamp: datetime) -> str:
    return timestamp.strftime("%Y-%m-%d-close")


def _as_of(timestamp: datetime) -> str:
    return timestamp.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _make_market_state(index: int, total: int) -> dict[str, dict[str, float | str]]:
    # Deterministic progression across the window from earlier to latest snapshot.
    p = index / max(total - 1, 1)

    cpi_prob = _round(0.56 + (0.08 * p), 3)
    fed_prob = _round(0.43 + (0.06 * p), 3)
    unemp_prob = _round(0.46 - (0.04 * p), 3)
    rec_prob = _round(0.27 + (0.04 * p), 3)
    gdp_prob = _round(0.41 + (0.05 * p), 3)

    return {
        "poly-cpi-jun-2026-over-3": {
            "market_probability": cpi_prob,
            "best_bid": _round(cpi_prob - 0.01, 3),
            "best_ask": _round(cpi_prob + 0.02, 3),
            "midpoint": _round(cpi_prob + 0.005, 3),
            "spread": _round(0.036 - (0.006 * p), 3),
            "volume_24h": int(54000 + (74500 * p)),
            "open_interest": int(820000 + (92000 * p)),
            "liquidity_score": _round(0.69 + (0.05 * p), 3),
            "macro_signal": _round(0.562 - (0.022 * p), 3),
            "momentum_24h": _round(-0.004 - (0.011 * p), 4),
        },
        "kalshi-fed-sep-2026-cut": {
            "market_probability": fed_prob,
            "best_bid": _round(fed_prob - 0.01, 3),
            "best_ask": _round(fed_prob + 0.01, 3),
            "midpoint": _round(fed_prob, 3),
            "spread": _round(0.024 - (0.004 * p), 3),
            "volume_24h": int(52000 + (47500 * p)),
            "open_interest": int(565000 + (89100 * p)),
            "liquidity_score": _round(0.66 + (0.03 * p), 3),
            "macro_signal": _round(0.548 + (0.022 * p), 3),
            "momentum_24h": _round(0.012 + (0.009 * p), 4),
        },
        "poly-unemp-dec-2026-over-4_5": {
            "market_probability": unemp_prob,
            "best_bid": _round(unemp_prob - 0.01, 3),
            "best_ask": _round(unemp_prob + 0.01, 3),
            "midpoint": _round(unemp_prob, 3),
            "spread": _round(0.023 - (0.003 * p), 3),
            "volume_24h": int(30500 + (40300 * p)),
            "open_interest": int(302000 + (38200 * p)),
            "liquidity_score": _round(0.58 + (0.04 * p), 3),
            "macro_signal": _round(0.332 + (0.028 * p), 3),
            "momentum_24h": _round(-0.004 - (0.004 * p), 4),
        },
        "kalshi-recession-q4-2026": {
            "market_probability": rec_prob,
            "best_bid": _round(rec_prob - 0.02, 3),
            "best_ask": _round(rec_prob + 0.02, 3),
            "midpoint": _round(rec_prob, 3),
            "spread": _round(0.048 - (0.008 * p), 3),
            "volume_24h": int(28000 + (27200 * p)),
            "open_interest": int(392000 + (38700 * p)),
            "liquidity_score": _round(0.5 + (0.05 * p), 3),
            "macro_signal": _round(0.372 + (0.028 * p), 3),
            "momentum_24h": _round(0.01 + (0.008 * p), 4),
        },
        "poly-gdp-q3-2026-below-1_5": {
            "market_probability": gdp_prob,
            "best_bid": _round(gdp_prob - 0.01, 3),
            "best_ask": _round(gdp_prob + 0.01, 3),
            "midpoint": _round(gdp_prob, 3),
            "spread": _round(0.026 - (0.006 * p), 3),
            "volume_24h": int(21000 + (22700 * p)),
            "open_interest": int(258000 + (40100 * p)),
            "liquidity_score": _round(0.54 + (0.05 * p), 3),
            "macro_signal": _round(0.488 + (0.032 * p), 3),
            "momentum_24h": _round(0.006 + (0.005 * p), 4),
        },
    }


def build_window() -> dict:
    start = datetime(2026, 3, 20, 23, 55, tzinfo=timezone.utc)
    total = 12

    snapshots: list[dict] = []
    for index in range(total):
        timestamp = start + timedelta(days=index)
        as_of = _as_of(timestamp)
        market_state = _make_market_state(index=index, total=total)

        overrides: dict[str, dict[str, float | str]] = {}
        for market_id, state in market_state.items():
            row = dict(state)
            row["updated_at"] = as_of
            overrides[market_id] = row

        snapshots.append(
            {
                "snapshot_id": _snapshot_id(timestamp),
                "label": _snapshot_label(timestamp),
                "as_of": as_of,
                "overrides": overrides,
            }
        )

    return {
        "series_name": "flagship-persistence-window-v2",
        "description": "Expanded deterministic synthetic snapshot window for persistence and complementary findings.",
        "snapshots": snapshots,
    }


def main() -> None:
    payload = build_window()
    SNAPSHOT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
