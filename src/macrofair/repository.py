from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT_DIR / "data" / "fixtures"


@lru_cache
def _read_json(file_name: str) -> Any:
    with (FIXTURE_DIR / file_name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_metadata() -> dict[str, Any]:
    return _read_json("metadata.json")


def get_markets() -> list[dict[str, Any]]:
    return _read_json("markets.json")


def get_histories() -> dict[str, list[dict[str, Any]]]:
    return _read_json("histories.json")


def get_history(market_id: str) -> list[dict[str, Any]]:
    return get_histories().get(market_id, [])


def get_fred_series() -> dict[str, list[dict[str, Any]]]:
    return _read_json("fred_series.json")


def get_snapshot_window() -> dict[str, Any]:
    return _read_json("snapshot_window.json")
