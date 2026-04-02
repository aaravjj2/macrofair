from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from macrofair.service import MacroFairService


def render_svg(contributions: list[dict]) -> str:
    width = 760
    height = 360
    margin_left = 70
    margin_right = 30
    margin_top = 40
    margin_bottom = 70
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    max_value = max((row["absolute_gap"] for row in contributions), default=1.0)
    bar_count = max(len(contributions), 1)
    slot_width = plot_width / bar_count
    bar_width = slot_width * 0.62

    bars = []
    labels = []
    for idx, row in enumerate(contributions):
        value = row["absolute_gap"]
        x = margin_left + (idx * slot_width) + ((slot_width - bar_width) / 2)
        h = 0.0 if max_value == 0 else (value / max_value) * plot_height
        y = margin_top + (plot_height - h)
        color = "#f4a259" if idx == 0 else "#6ed39e"
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{h:.1f}" fill="{color}" rx="6" />'
        )
        labels.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{height - 44}" text-anchor="middle" fill="#b6c9d7" font-size="11">#{idx + 1}</text>'
        )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect x="0" y="0" width="100%" height="100%" fill="#0b1d2d"/>',
            f'<line x1="{margin_left}" y1="{margin_top + plot_height}" x2="{width - margin_right}" y2="{margin_top + plot_height}" stroke="#6f8aa0"/>',
            f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_height}" stroke="#6f8aa0"/>',
            '<text x="70" y="24" fill="#eef6fb" font-size="17">Flagship Finding: Dislocation Concentration</text>',
            '<text x="70" y="44" fill="#b6c9d7" font-size="12">Absolute gap by ranked market (demo snapshot)</text>',
            *bars,
            *labels,
            '</svg>',
        ]
    )


def main() -> None:
    output_dir = ROOT / "artifacts" / "evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)

    service = MacroFairService()
    finding = service.get_flagship_finding()

    json_path = output_dir / "flagship_finding.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(finding, handle, indent=2)

    contributions_csv = output_dir / "flagship_dislocation_contributions.csv"
    with contributions_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "rank",
                "market_id",
                "title",
                "category",
                "platform",
                "gap",
                "absolute_gap",
                "share_of_total_gap",
                "cumulative_share",
                "confidence",
            ],
        )
        writer.writeheader()
        writer.writerows(finding["contributions"])

    category_csv = output_dir / "flagship_category_breakdown.csv"
    with category_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["category", "absolute_gap", "share_of_total_gap"],
        )
        writer.writeheader()
        writer.writerows(finding["category_breakdown"])

    svg_path = output_dir / "flagship_dislocation_concentration.svg"
    with svg_path.open("w", encoding="utf-8") as handle:
        handle.write(render_svg(finding["contributions"]))


if __name__ == "__main__":
    main()
