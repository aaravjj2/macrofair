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
    findings_index = service.get_findings_index_payload()
    findings_report = service.get_findings_report_payload()
    submission_report = service.get_submission_report_payload()
    zerve_package = service.get_zerve_submission_package()

    with (output_dir / "findings_index.json").open("w", encoding="utf-8") as handle:
        json.dump(findings_index, handle, indent=2)

    with (output_dir / "findings_report.json").open("w", encoding="utf-8") as handle:
        json.dump(findings_report, handle, indent=2)

    with (output_dir / "submission_report.json").open("w", encoding="utf-8") as handle:
        json.dump(submission_report, handle, indent=2)

    with (output_dir / "zerve_submission_package.json").open("w", encoding="utf-8") as handle:
        json.dump(zerve_package, handle, indent=2)


if __name__ == "__main__":
    main()
