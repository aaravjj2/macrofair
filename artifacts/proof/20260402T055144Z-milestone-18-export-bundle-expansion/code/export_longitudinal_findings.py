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


def _line_points(values: list[float], width: int, left: int, right: int, top: int, bottom: int, vmin: float, vmax: float) -> str:
    if not values:
        return ""

    plot_width = width - left - right
    plot_height = bottom - top
    slot = plot_width / max(len(values) - 1, 1)

    points: list[str] = []
    for idx, value in enumerate(values):
        x = left + (idx * slot)
        if vmax == vmin:
            y = top + (plot_height / 2)
        else:
            norm = (value - vmin) / (vmax - vmin)
            y = bottom - (norm * plot_height)
        points.append(f"{x:.1f},{y:.1f}")
    return " ".join(points)


def render_flagship_persistence_svg(rows: list[dict]) -> str:
    width = 860
    height = 380
    left = 70
    right = 30
    top = 44
    bottom = 310

    top_shares = [float(row["top_share_of_total_gap"]) for row in rows]
    hhi_values = [float(row["herfindahl_index"]) for row in rows]
    values = top_shares + hhi_values
    vmax = max(values) if values else 1.0
    vmin = min(values) if values else 0.0

    top_share_points = _line_points(top_shares, width, left, right, top, bottom, vmin, vmax)
    hhi_points = _line_points(hhi_values, width, left, right, top, bottom, vmin, vmax)

    labels: list[str] = []
    if rows:
        step = (width - left - right) / max(len(rows) - 1, 1)
        for idx, row in enumerate(rows):
            x = left + (idx * step)
            labels.append(
                f'<text x="{x:.1f}" y="334" text-anchor="middle" fill="#b6c9d7" font-size="11">{row["label"]}</text>'
            )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect x="0" y="0" width="100%" height="100%" fill="#0b1d2d"/>',
            f'<line x1="{left}" y1="{bottom}" x2="{width - right}" y2="{bottom}" stroke="#6f8aa0"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#6f8aa0"/>',
            '<text x="70" y="24" fill="#eef6fb" font-size="17">Flagship Persistence Across Deterministic Snapshots</text>',
            '<text x="70" y="42" fill="#b6c9d7" font-size="12">Orange = top-share, Green = HHI</text>',
            f'<polyline fill="none" stroke="#f4a259" stroke-width="3" points="{top_share_points}"/>',
            f'<polyline fill="none" stroke="#6ed39e" stroke-width="3" points="{hhi_points}"/>',
            '<rect x="620" y="20" width="12" height="12" fill="#f4a259" rx="2"/>',
            '<text x="638" y="30" fill="#d6e5ef" font-size="11">Top share of total gap</text>',
            '<rect x="620" y="38" width="12" height="12" fill="#6ed39e" rx="2"/>',
            '<text x="638" y="48" fill="#d6e5ef" font-size="11">Herfindahl index (HHI)</text>',
            *labels,
            '</svg>',
        ]
    )


def render_secondary_finding_svg(rows: list[dict]) -> str:
    width = 860
    height = 380
    left = 70
    right = 30
    top = 44
    bottom = 310

    asymmetry = [float(row["asymmetry_gap"]) for row in rows]
    vmax = max(asymmetry) if asymmetry else 1.0
    vmin = min(asymmetry) if asymmetry else -1.0
    if vmin > 0:
        vmin = 0.0
    if vmax < 0:
        vmax = 0.0

    asymmetry_points = _line_points(asymmetry, width, left, right, top, bottom, vmin, vmax)
    zero_points = _line_points([0.0, 0.0], width, left, right, top, bottom, vmin, vmax)

    labels: list[str] = []
    if rows:
        step = (width - left - right) / max(len(rows) - 1, 1)
        for idx, row in enumerate(rows):
            x = left + (idx * step)
            labels.append(
                f'<text x="{x:.1f}" y="334" text-anchor="middle" fill="#b6c9d7" font-size="11">{row["label"]}</text>'
            )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect x="0" y="0" width="100%" height="100%" fill="#0b1d2d"/>',
            f'<line x1="{left}" y1="{bottom}" x2="{width - right}" y2="{bottom}" stroke="#6f8aa0"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#6f8aa0"/>',
            f'<polyline fill="none" stroke="#6f8aa0" stroke-dasharray="4 3" stroke-width="1.5" points="{zero_points}"/>',
            '<text x="70" y="24" fill="#eef6fb" font-size="17">Secondary Finding: Platform Gap Asymmetry</text>',
            '<text x="70" y="42" fill="#b6c9d7" font-size="12">Asymmetry = Polymarket mean gap - Kalshi mean gap</text>',
            f'<polyline fill="none" stroke="#f4a259" stroke-width="3" points="{asymmetry_points}"/>',
            *labels,
            '</svg>',
        ]
    )


def render_third_finding_svg(rows: list[dict], category_drift: list[dict]) -> str:
    width = 860
    height = 380
    left = 70
    right = 30
    top = 44
    bottom = 310

    selected_categories = [row["category"] for row in category_drift[:3]]
    if not selected_categories and rows:
        selected_categories = [entry["category"] for entry in rows[0].get("category_shares", [])[:3]]

    category_series: dict[str, list[float]] = {category: [] for category in selected_categories}
    for snapshot in rows:
        share_map = {entry["category"]: float(entry["share_of_total_gap"]) for entry in snapshot["category_shares"]}
        for category in selected_categories:
            category_series[category].append(share_map.get(category, 0.0))

    values = [value for series in category_series.values() for value in series]
    vmin = min(values) if values else 0.0
    vmax = max(values) if values else 1.0
    if vmin > 0:
        vmin = 0.0

    colors = ["#f4a259", "#6ed39e", "#5ba4ff"]
    lines: list[str] = []
    legend: list[str] = []
    for idx, category in enumerate(selected_categories):
        color = colors[idx % len(colors)]
        points = _line_points(category_series[category], width, left, right, top, bottom, vmin, vmax)
        lines.append(f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{points}"/>')
        legend_y = 30 + (idx * 18)
        legend.append(f'<rect x="620" y="{legend_y - 10}" width="12" height="12" fill="{color}" rx="2"/>')
        legend.append(
            f'<text x="638" y="{legend_y}" fill="#d6e5ef" font-size="11">{category.capitalize()} share of total gap</text>'
        )

    labels: list[str] = []
    if rows:
        step = (width - left - right) / max(len(rows) - 1, 1)
        for idx, row in enumerate(rows):
            if len(rows) > 8 and idx % 2 == 1 and idx != len(rows) - 1:
                continue
            x = left + (idx * step)
            labels.append(
                f'<text x="{x:.1f}" y="334" text-anchor="middle" fill="#b6c9d7" font-size="11">{row["label"]}</text>'
            )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect x="0" y="0" width="100%" height="100%" fill="#0b1d2d"/>',
            f'<line x1="{left}" y1="{bottom}" x2="{width - right}" y2="{bottom}" stroke="#6f8aa0"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#6f8aa0"/>',
            '<text x="70" y="24" fill="#eef6fb" font-size="17">Third Finding: Category Drift Across Snapshots</text>',
            '<text x="70" y="42" fill="#b6c9d7" font-size="12">Top drifting category shares from first to last deterministic snapshot</text>',
            *lines,
            *legend,
            *labels,
            '</svg>',
        ]
    )


def _flatten_third_snapshot_rows(rows: list[dict]) -> list[dict]:
    flattened: list[dict] = []
    for snapshot in rows:
        for category_share in snapshot["category_shares"]:
            flattened.append(
                {
                    "snapshot_id": snapshot["snapshot_id"],
                    "label": snapshot["label"],
                    "as_of": snapshot["as_of"],
                    "feature_snapshot_hash": snapshot["feature_snapshot_hash"],
                    "category": category_share["category"],
                    "absolute_gap": category_share["absolute_gap"],
                    "share_of_total_gap": category_share["share_of_total_gap"],
                }
            )
    return flattened


def main() -> None:
    output_dir = ROOT / "artifacts" / "evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)

    service = MacroFairService()
    persistence = service.get_flagship_persistence()
    secondary = service.get_secondary_finding()
    third = service.get_third_finding()

    with (output_dir / "flagship_persistence.json").open("w", encoding="utf-8") as handle:
        json.dump(persistence, handle, indent=2)

    with (output_dir / "secondary_finding.json").open("w", encoding="utf-8") as handle:
        json.dump(secondary, handle, indent=2)

    with (output_dir / "third_finding.json").open("w", encoding="utf-8") as handle:
        json.dump(third, handle, indent=2)

    with (output_dir / "flagship_persistence.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "snapshot_id",
                "label",
                "as_of",
                "feature_snapshot_hash",
                "top_market_id",
                "top_market_title",
                "top_share_of_total_gap",
                "top_to_second_ratio",
                "herfindahl_index",
            ],
        )
        writer.writeheader()
        writer.writerows(persistence["snapshots"])

    with (output_dir / "secondary_finding.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "snapshot_id",
                "label",
                "as_of",
                "feature_snapshot_hash",
                "polymarket_mean_gap",
                "kalshi_mean_gap",
                "asymmetry_gap",
            ],
        )
        writer.writeheader()
        writer.writerows(secondary["snapshots"])

    with (output_dir / "third_finding.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "category",
                "first_share",
                "last_share",
                "drift",
            ],
        )
        writer.writeheader()
        writer.writerows(third["category_drift"])

    with (output_dir / "third_finding_snapshot_category_shares.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "snapshot_id",
                "label",
                "as_of",
                "feature_snapshot_hash",
                "category",
                "absolute_gap",
                "share_of_total_gap",
            ],
        )
        writer.writeheader()
        writer.writerows(_flatten_third_snapshot_rows(third["snapshots"]))

    with (output_dir / "flagship_persistence.svg").open("w", encoding="utf-8") as handle:
        handle.write(render_flagship_persistence_svg(persistence["snapshots"]))

    with (output_dir / "secondary_finding.svg").open("w", encoding="utf-8") as handle:
        handle.write(render_secondary_finding_svg(secondary["snapshots"]))

    with (output_dir / "third_finding.svg").open("w", encoding="utf-8") as handle:
        handle.write(render_third_finding_svg(third["snapshots"], third["category_drift"]))


if __name__ == "__main__":
    main()
