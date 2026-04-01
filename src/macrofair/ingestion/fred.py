from __future__ import annotations

from macrofair.repository import get_fred_series


class FREDAdapter:
    """Read-only adapter for deterministic macro time series."""

    def get_series(self, series_id: str) -> list[dict]:
        return get_fred_series().get(series_id, [])
