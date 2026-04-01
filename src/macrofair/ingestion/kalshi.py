from __future__ import annotations

from macrofair.repository import get_markets


class KalshiAdapter:
    """Read-only adapter that exposes deterministic Kalshi fixture rows."""

    def list_markets(self) -> list[dict]:
        return [market for market in get_markets() if market["platform"] == "Kalshi"]
