from __future__ import annotations

import hashlib
import json

from macrofair.repository import get_metadata
from macrofair.service import MacroFairService


def _hash_payload(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def test_zerve_submission_package_is_deterministic() -> None:
    service = MacroFairService()

    first = service.get_zerve_submission_package()
    second = service.get_zerve_submission_package()

    assert first == second
    assert _hash_payload(first) == _hash_payload(second)


def test_zerve_submission_package_has_expected_shape() -> None:
    service = MacroFairService()
    metadata = get_metadata()

    package = service.get_zerve_submission_package()

    assert package["package_name"] == "macrofair-zerve-submission-package"
    assert package["generated_at"] == metadata["last_refresh"]
    assert package["mode"] == "demo"
    assert package["findings"]["flagship"]["top_market_id"] == "poly-cpi-jun-2026-over-3"
    assert package["ranked_snapshot_summary"]["count"] >= 5
    assert isinstance(package["payload_hash"], str)
    assert len(package["payload_hash"]) == 64
