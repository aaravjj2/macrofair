from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from macrofair.evaluation.metrics import brier_score, calibration_curve_points, expected_calibration_error, log_loss
from macrofair.service import MacroFairService


def render_svg(points: list[dict]) -> str:
    width = 520
    height = 360
    padding = 50
    plot = width - (padding * 2)

    def x(value: float) -> float:
        return padding + (value * plot)

    def y(value: float) -> float:
        return (height - padding) - (value * plot)

    polyline = " ".join(f"{x(row['predicted']):.1f},{y(row['observed']):.1f}" for row in points)
    return f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">
  <rect x=\"0\" y=\"0\" width=\"{width}\" height=\"{height}\" fill=\"#0b1d2d\"/>
  <line x1=\"{padding}\" y1=\"{height-padding}\" x2=\"{width-padding}\" y2=\"{height-padding}\" stroke=\"#7da0ba\"/>
  <line x1=\"{padding}\" y1=\"{height-padding}\" x2=\"{padding}\" y2=\"{padding}\" stroke=\"#7da0ba\"/>
  <line x1=\"{padding}\" y1=\"{height-padding}\" x2=\"{width-padding}\" y2=\"{padding}\" stroke=\"#48657b\" stroke-dasharray=\"5 5\"/>
  <polyline fill=\"none\" stroke=\"#f4a259\" stroke-width=\"3\" points=\"{polyline}\"/>
  <text x=\"{padding}\" y=\"26\" fill=\"#eef6fb\" font-size=\"16\">MacroFair Calibration Curve</text>
  <text x=\"{width - 180}\" y=\"{height - 12}\" fill=\"#b6c9d7\" font-size=\"12\">Predicted probability</text>
  <text x=\"8\" y=\"{padding - 8}\" fill=\"#b6c9d7\" font-size=\"12\">Observed frequency</text>
</svg>
"""


def main() -> None:
    output_dir = ROOT / "artifacts" / "evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)

    service = MacroFairService()
    markets = service.list_markets(limit=100, sort_by="gap")

    y_pred = [market["fair_probability"] for market in markets]
    y_true = [1.0 if market["market_probability"] >= 0.5 else 0.0 for market in markets]

    metrics_payload = {
        "run_id": "demo-deterministic-latest",
        "model_version": "combined-v1",
        "metrics": {
            "brier_score": round(brier_score(y_true, y_pred), 4),
            "log_loss": round(log_loss(y_true, y_pred), 4),
            "ece": round(expected_calibration_error(y_true, y_pred, bins=5), 4),
        },
    }

    points = calibration_curve_points(y_true, y_pred, bins=5)
    with (output_dir / "calibration_metrics.json").open("w", encoding="utf-8") as handle:
        json.dump(metrics_payload, handle, indent=2)

    with (output_dir / "calibration_curve_points.json").open("w", encoding="utf-8") as handle:
        json.dump({"points": points}, handle, indent=2)

    with (output_dir / "calibration_curve.svg").open("w", encoding="utf-8") as handle:
        handle.write(render_svg(points))


if __name__ == "__main__":
    main()
