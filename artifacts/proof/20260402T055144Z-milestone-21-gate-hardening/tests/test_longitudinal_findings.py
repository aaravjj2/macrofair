from __future__ import annotations

import hashlib
import json

from macrofair.evaluation.longitudinal_findings import (
    build_scored_snapshot_series,
    compute_flagship_persistence,
    compute_secondary_finding,
    compute_third_finding,
)


def _payload_hash(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def test_scored_snapshot_series_has_expected_shape() -> None:
    series = build_scored_snapshot_series()

    assert series["series_name"] == "flagship-persistence-window-v2"
    assert len(series["snapshots"]) == 12
    assert all(len(snapshot["markets"]) == 5 for snapshot in series["snapshots"])
    assert all("feature_snapshot_hash" in snapshot for snapshot in series["snapshots"])


def test_flagship_persistence_is_deterministic() -> None:
    first = compute_flagship_persistence()
    second = compute_flagship_persistence()

    assert first == second
    assert _payload_hash(first) == _payload_hash(second)
    assert first["window_size"] == 12
    assert first["dominant_top_market_id"] == "poly-cpi-jun-2026-over-3"
    assert first["persistence_rate"] >= 0.75


def test_secondary_finding_is_deterministic() -> None:
    first = compute_secondary_finding()
    second = compute_secondary_finding()

    assert first == second
    assert _payload_hash(first) == _payload_hash(second)
    assert first["window_size"] == 12
    assert first["average_asymmetry_gap"] > 0
    assert first["positive_window_share"] >= 0.75


def test_third_finding_is_deterministic() -> None:
    first = compute_third_finding()
    second = compute_third_finding()

    assert first == second
    assert _payload_hash(first) == _payload_hash(second)
    assert first["window_size"] == 12
    assert first["dominant_drift_category"] == "inflation"
    assert first["dominant_drift_points"] > 0
