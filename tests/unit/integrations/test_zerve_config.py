from __future__ import annotations

from macrofair.integrations.zerve.config import load_zerve_settings


def test_zerve_settings_default_to_disabled(monkeypatch) -> None:
    monkeypatch.delenv("ZERVE_ENABLED", raising=False)
    monkeypatch.delenv("ZERVE_BASE_URL", raising=False)
    monkeypatch.delenv("ZERVE_PROJECT_ID", raising=False)
    monkeypatch.delenv("ZERVE_API_KEY", raising=False)

    settings = load_zerve_settings()

    assert settings.enabled is False
    assert settings.configured is False
    assert settings.api_key_configured is False
    assert settings.missing_required == []


def test_zerve_settings_enabled_and_configured(monkeypatch) -> None:
    monkeypatch.setenv("ZERVE_ENABLED", "true")
    monkeypatch.setenv("ZERVE_BASE_URL", "https://example.zerve.test")
    monkeypatch.setenv("ZERVE_PROJECT_ID", "project-123")
    monkeypatch.setenv("ZERVE_API_KEY", "unit-test-key")

    settings = load_zerve_settings()

    assert settings.enabled is True
    assert settings.configured is True
    assert settings.base_url == "https://example.zerve.test"
    assert settings.project_id == "project-123"
    assert settings.api_key_configured is True
    assert settings.missing_required == []


def test_zerve_settings_enabled_missing_values(monkeypatch) -> None:
    monkeypatch.setenv("ZERVE_ENABLED", "1")
    monkeypatch.delenv("ZERVE_PROJECT_ID", raising=False)
    monkeypatch.delenv("ZERVE_API_KEY", raising=False)

    settings = load_zerve_settings()

    assert settings.enabled is True
    assert settings.configured is False
    assert "ZERVE_PROJECT_ID" in settings.missing_required
    assert "ZERVE_API_KEY" in settings.missing_required
