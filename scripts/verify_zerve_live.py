from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib import error, request


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from macrofair.integrations.zerve import ZerveSettings
from macrofair.service import MacroFairService


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_key() -> str:
    # Read from environment first; fallback to local ignored key file.
    key = (os.getenv("ZERVE_API_KEY") or "").strip()
    if key:
        return key

    key_file = ROOT / "ZERVE_API_KEY"
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()
    return ""


def _request_json(url: str, api_key: str) -> dict[str, object]:
    headers = {
        "Accept": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = request.Request(url=url, headers=headers, method="GET")

    try:
        with request.urlopen(req, timeout=10) as response:
            _ = response.read()
            return {
                "ok": True,
                "status_code": int(response.status),
                "error": None,
                "response_body_logged": False,
            }
    except error.HTTPError as exc:
        _ = exc.read()
        return {
            "ok": False,
            "status_code": int(exc.code),
            "error": f"http_{exc.code}",
            "response_body_logged": False,
        }
    except error.URLError as exc:
        reason = str(getattr(exc, "reason", exc))
        return {
            "ok": False,
            "status_code": None,
            "error": f"url_error:{reason}",
            "response_body_logged": False,
        }
    except TimeoutError:
        return {
            "ok": False,
            "status_code": None,
            "error": "timeout",
            "response_body_logged": False,
        }


def main() -> None:
    output_dir = ROOT / "artifacts" / "evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)

    base_url = (os.getenv("ZERVE_BASE_URL") or "https://api.zerve.cloud").strip().rstrip("/")
    project_id = (os.getenv("ZERVE_PROJECT_ID") or "").strip()
    api_key = _load_key()

    probes: dict[str, object] = {
        "base_root": _request_json(f"{base_url}/", api_key),
        "projects_list": _request_json(f"{base_url}/v1/projects", api_key),
    }
    if project_id:
        probes["project_status"] = _request_json(f"{base_url}/v1/projects/{project_id}/status", api_key)

    service_probe: dict[str, object]
    if project_id and api_key:
        settings = ZerveSettings(
            enabled=True,
            base_url=base_url,
            project_id=project_id,
            timeout_seconds=10.0,
            api_key=api_key,
            api_key_configured=True,
            missing_required=[],
        )
        service = MacroFairService(zerve_settings=settings)
        service_probe = service.get_zerve_status(verify_remote=True)
    else:
        service_probe = {
            "integration": "zerve",
            "enabled": False,
            "configured": False,
            "note": "Skipped verify_remote because ZERVE_PROJECT_ID is not set in environment.",
        }

    payload = {
        "checked_at": _utc_now(),
        "base_url": base_url,
        "project_id_present": bool(project_id),
        "api_key_present": bool(api_key),
        "probes": probes,
        "service_verify_remote": service_probe,
        "security": {
            "api_key_logged": False,
            "raw_api_key_in_payload": False,
        },
    }

    output_file = output_dir / "zerve_live_verification.json"
    output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
