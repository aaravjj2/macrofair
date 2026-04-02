from __future__ import annotations

import json
from typing import Any
from urllib import error, request

from macrofair.integrations.zerve.config import ZerveSettings


class ZerveClient:
    def __init__(self, settings: ZerveSettings) -> None:
        self.settings = settings

    def _request_json(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.settings.configured:
            return {
                "ok": False,
                "status_code": None,
                "error": "zerve_not_configured",
                "payload": {},
            }

        body_bytes = None
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        }
        if payload is not None:
            headers["Content-Type"] = "application/json"
            body_bytes = json.dumps(payload).encode("utf-8")

        url = f"{self.settings.base_url}{path}"
        req = request.Request(url=url, data=body_bytes, method=method, headers=headers)

        try:
            with request.urlopen(req, timeout=self.settings.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw) if raw else {}
                return {
                    "ok": True,
                    "status_code": int(response.status),
                    "error": None,
                    "payload": parsed,
                }
        except error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            parsed: dict[str, Any]
            try:
                parsed = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                parsed = {"raw": raw[:500]}
            return {
                "ok": False,
                "status_code": int(exc.code),
                "error": f"http_{exc.code}",
                "payload": parsed,
            }
        except error.URLError:
            return {
                "ok": False,
                "status_code": None,
                "error": "network_unreachable",
                "payload": {},
            }
        except TimeoutError:
            return {
                "ok": False,
                "status_code": None,
                "error": "timeout",
                "payload": {},
            }

    def check_project_status(self) -> dict[str, Any]:
        path = f"/v1/projects/{self.settings.project_id}/status"
        return self._request_json("GET", path)

    def sync_submission_package(self, package: dict[str, Any]) -> dict[str, Any]:
        path = f"/v1/projects/{self.settings.project_id}/packages/macrofair-findings"
        return self._request_json("POST", path, payload=package)
