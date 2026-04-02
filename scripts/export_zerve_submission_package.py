from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from macrofair.service import MacroFairService


def main() -> None:
    output_dir = ROOT / "artifacts" / "evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)

    service = MacroFairService()
    payload = service.get_zerve_submission_package()

    output_file = output_dir / "zerve_submission_package.json"
    with output_file.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


if __name__ == "__main__":
    main()
