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
