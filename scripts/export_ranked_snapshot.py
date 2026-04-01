from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from macrofair.repository import get_metadata
from macrofair.service import MacroFairService


def main() -> None:
    output_dir = ROOT / "artifacts" / "evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)

    service = MacroFairService()
    metadata = get_metadata()
    ranked = service.list_markets(limit=50, sort_by="gap")

    payload = {
        "as_of": metadata["last_refresh"],
        "mode": metadata["mode"],
        "markets": [
            {
                "rank": row["rank"],
                "market_id": row["market_id"],
                "platform": row["platform"],
                "gap": row["gap"],
                "confidence": row["confidence"],
            }
            for row in ranked
        ],
    }

    with (output_dir / "sample_ranked_snapshot.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


if __name__ == "__main__":
    main()
