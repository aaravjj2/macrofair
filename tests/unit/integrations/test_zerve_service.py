from __future__ import annotations

from macrofair.integrations.zerve.client import ZerveClient
from macrofair.integrations.zerve.config import load_zerve_settings
from macrofair.service import MacroFairService


class FakeZerveClient(ZerveClient):
    def __init__(self, settings):
        super().__init__(settings)
        self.sync_calls = 0

    def check_project_status(self) -> dict:
        return {
            "ok": True,
            "status_code": 200,
            "error": None,
            "payload": {"status": "ready"},
        }

    def sync_submission_package(self, package: dict) -> dict:
        self.sync_calls += 1
        assert "findings" in package
        return {
            "ok": True,
            "status_code": 201,
            "error": None,
            "payload": {"id": "sync-123"},
        }


def test_zerve_disabled_status_and_sync_fallback(monkeypatch) -> None:
    monkeypatch.delenv("ZERVE_ENABLED", raising=False)
    monkeypatch.delenv("ZERVE_BASE_URL", raising=False)
    monkeypatch.delenv("ZERVE_PROJECT_ID", raising=False)
    monkeypatch.delenv("ZERVE_API_KEY", raising=False)

    service = MacroFairService()
    status = service.get_zerve_status()
    sync_result = service.sync_zerve_submission_package(dry_run=False)

    assert status["enabled"] is False
    assert status["configured"] is False
    assert sync_result["attempted"] is False
    assert sync_result["synced"] is False


def test_zerve_dry_run_when_configured(monkeypatch) -> None:
    monkeypatch.setenv("ZERVE_ENABLED", "true")
    monkeypatch.setenv("ZERVE_BASE_URL", "https://example.zerve.test")
    monkeypatch.setenv("ZERVE_PROJECT_ID", "project-123")
    monkeypatch.setenv("ZERVE_API_KEY", "unit-test-key")

    service = MacroFairService()
    status = service.get_zerve_status()
    sync_result = service.sync_zerve_submission_package(dry_run=True)

    assert status["configured"] is True
    assert sync_result["attempted"] is False
    assert sync_result["dry_run"] is True
    assert sync_result["synced"] is False


def test_zerve_sync_uses_client_when_enabled(monkeypatch) -> None:
    monkeypatch.setenv("ZERVE_ENABLED", "true")
    monkeypatch.setenv("ZERVE_BASE_URL", "https://example.zerve.test")
    monkeypatch.setenv("ZERVE_PROJECT_ID", "project-123")
    monkeypatch.setenv("ZERVE_API_KEY", "unit-test-key")

    settings = load_zerve_settings()
    fake_client = FakeZerveClient(settings)
    service = MacroFairService(zerve_settings=settings, zerve_client=fake_client)

    status = service.get_zerve_status(verify_remote=True)
    sync_result = service.sync_zerve_submission_package(dry_run=False)

    assert status["remote_check_attempted"] is True
    assert status["remote_connected"] is True
    assert sync_result["attempted"] is True
    assert sync_result["synced"] is True
    assert sync_result["remote_reference"] == "sync-123"
    assert fake_client.sync_calls == 1
