from __future__ import annotations

import os
from dataclasses import dataclass, field


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_float(value: str | None, default: float) -> float:
    if value is None:
        return default
    try:
        parsed = float(value)
    except ValueError:
        return default
    return parsed if parsed > 0 else default


@dataclass(frozen=True)
class ZerveSettings:
    enabled: bool
    base_url: str
    project_id: str
    timeout_seconds: float
    api_key_configured: bool
    missing_required: list[str]
    api_key: str = field(repr=False, default="")

    @property
    def configured(self) -> bool:
        return self.enabled and len(self.missing_required) == 0


DEFAULT_ZERVE_BASE_URL = "https://api.zerve.ai"


def load_zerve_settings() -> ZerveSettings:
    enabled = _parse_bool(os.getenv("ZERVE_ENABLED"), default=False)
    base_url = (os.getenv("ZERVE_BASE_URL") or DEFAULT_ZERVE_BASE_URL).strip().rstrip("/")
    project_id = (os.getenv("ZERVE_PROJECT_ID") or "").strip()
    api_key = (os.getenv("ZERVE_API_KEY") or "").strip()
    timeout_seconds = _parse_float(os.getenv("ZERVE_TIMEOUT_SECONDS"), default=4.0)

    missing_required: list[str] = []
    if enabled:
        if not base_url:
            missing_required.append("ZERVE_BASE_URL")
        if not project_id:
            missing_required.append("ZERVE_PROJECT_ID")
        if not api_key:
            missing_required.append("ZERVE_API_KEY")

    return ZerveSettings(
        enabled=enabled,
        base_url=base_url,
        project_id=project_id,
        timeout_seconds=timeout_seconds,
        api_key=api_key,
        api_key_configured=bool(api_key),
        missing_required=missing_required,
    )
