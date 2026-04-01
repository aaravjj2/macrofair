from __future__ import annotations

import os


def app_mode() -> str:
    return os.getenv("MACROFAIR_MODE", "demo")


def app_version() -> str:
    return "0.1.0"
