from __future__ import annotations

from fastapi.testclient import TestClient

from apps.api.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert payload["mode"] == "demo"


def test_markets_endpoint() -> None:
    response = client.get("/api/v1/markets")
    payload = response.json()

    assert response.status_code == 200
    assert len(payload) >= 5
    required_fields = {
        "market_id",
        "platform",
        "title",
        "market_probability",
        "fair_probability",
        "gap",
        "confidence"
    }
    assert required_fields.issubset(payload[0].keys())


def test_markets_filters_work() -> None:
    response = client.get("/api/v1/markets", params={"platform": "Kalshi", "category": "fed"})
    payload = response.json()

    assert response.status_code == 200
    assert len(payload) == 1
    assert payload[0]["market_id"] == "kalshi-fed-sep-2026-cut"


def test_market_detail_endpoint() -> None:
    response = client.get("/api/v1/markets/poly-cpi-jun-2026-over-3")
    payload = response.json()

    assert response.status_code == 200
    assert payload["market_id"] == "poly-cpi-jun-2026-over-3"
    assert len(payload["history"]) > 0
    assert "narrative_summary" in payload["explanation"]


def test_market_explain_endpoint() -> None:
    response = client.get("/api/v1/markets/kalshi-recession-q4-2026/explain")
    payload = response.json()

    assert response.status_code == 200
    assert len(payload["top_factors"]) == 3
    assert isinstance(payload["factor_contributions"], dict)


def test_market_not_found() -> None:
    response = client.get("/api/v1/markets/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"]["error"]["code"] == "NOT_FOUND"


def test_flagship_finding_endpoint() -> None:
    response = client.get("/api/v1/findings/flagship")
    payload = response.json()

    assert response.status_code == 200
    assert payload["top_market_id"] == "poly-cpi-jun-2026-over-3"
    assert payload["top_share_of_total_gap"] > 0.5
    assert len(payload["contributions"]) >= 5


def test_flagship_persistence_endpoint() -> None:
    response = client.get("/api/v1/findings/flagship/persistence")
    payload = response.json()

    assert response.status_code == 200
    assert payload["window_name"] == "flagship-persistence-window-v2"
    assert payload["window_size"] == 12
    assert payload["dominant_top_market_id"] == "poly-cpi-jun-2026-over-3"
    assert len(payload["snapshots"]) == 12


def test_secondary_finding_endpoint() -> None:
    response = client.get("/api/v1/findings/secondary")
    payload = response.json()

    assert response.status_code == 200
    assert payload["window_name"] == "flagship-persistence-window-v2"
    assert payload["window_size"] == 12
    assert payload["average_asymmetry_gap"] > 0
    assert len(payload["snapshots"]) == 12


def test_third_finding_endpoint() -> None:
    response = client.get("/api/v1/findings/third")
    payload = response.json()

    assert response.status_code == 200
    assert payload["window_name"] == "flagship-persistence-window-v2"
    assert payload["window_size"] == 12
    assert payload["dominant_drift_category"] == "inflation"
    assert len(payload["category_drift"]) >= 3


def test_findings_index_endpoint() -> None:
    response = client.get("/api/v1/findings")
    payload = response.json()

    assert response.status_code == 200
    assert payload["window_name"] == "flagship-persistence-window-v2"
    assert payload["window_size"] == 12
    assert payload["headlines"]["flagship"]
    assert payload["headlines"]["third"]
    assert isinstance(payload["payload_hash"], str)


def test_findings_report_endpoint() -> None:
    response = client.get("/api/v1/findings/report")
    payload = response.json()

    assert response.status_code == 200
    assert payload["report_name"] == "macrofair-findings-report"
    assert payload["findings"]["third"]["dominant_drift_category"] == "inflation"
    assert payload["ranked_snapshot_summary"]["count"] >= 5
    assert isinstance(payload["payload_hash"], str)


def test_submission_report_endpoint() -> None:
    response = client.get("/api/v1/reports/submission")
    payload = response.json()

    assert response.status_code == 200
    assert payload["report_name"] == "macrofair-submission-report"
    assert payload["findings_report"]["report_name"] == "macrofair-findings-report"
    assert payload["zerve_integration"]["integration"] == "zerve"
    assert isinstance(payload["payload_hash"], str)


def test_zerve_status_endpoint_safe_defaults() -> None:
    response = client.get("/api/v1/integrations/zerve/status")
    payload = response.json()

    assert response.status_code == 200
    assert payload["integration"] == "zerve"
    assert payload["enabled"] is False
    assert payload["configured"] is False
    assert payload["api_key_configured"] is False
    assert payload["mode"] == "demo"


def test_zerve_package_endpoint_returns_deterministic_payload() -> None:
    response = client.get("/api/v1/integrations/zerve/package")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"]["integration"] == "zerve"
    assert payload["package"]["package_name"] == "macrofair-zerve-submission-package"
    assert payload["package"]["findings"]["flagship"]["top_market_id"] == "poly-cpi-jun-2026-over-3"
    assert payload["package"]["findings"]["third"]["dominant_drift_category"] == "inflation"
    assert isinstance(payload["package"]["findings_report_hash"], str)
    assert "api_key" not in payload


def test_zerve_sync_endpoint_fallback_when_disabled() -> None:
    response = client.post("/api/v1/integrations/zerve/sync", json={"dry_run": True})
    payload = response.json()

    assert response.status_code == 200
    assert payload["attempted"] is False
    assert payload["dry_run"] is True
    assert payload["synced"] is False
    assert payload["status"]["configured"] is False
