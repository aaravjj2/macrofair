from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any

from macrofair.evaluation.flagship_finding import compute_flagship_finding
from macrofair.features.pipeline import build_feature_rows, feature_snapshot_hash
from macrofair.modeling.fair_value import CombinedFairValueModel
from macrofair.normalization.canonical import normalize_markets
from macrofair.repository import get_markets, get_snapshot_window
from macrofair.scoring.dislocation import rank_markets, score_market


def _percent(value: float) -> float:
    return round(value * 100.0, 2)


def _round(value: float) -> float:
    return round(float(value), 4)


def _apply_snapshot_overrides(base_markets: list[dict], overrides: dict[str, dict], as_of: str) -> list[dict]:
    snapshot_markets: list[dict] = []
    for market in base_markets:
        patched = dict(market)
        patch = overrides.get(market["market_id"], {})
        patched.update(patch)
        patched["updated_at"] = patched.get("updated_at", as_of)
        snapshot_markets.append(patched)
    return snapshot_markets


def _score_snapshot(markets: list[dict], as_of: str) -> tuple[list[dict], str]:
    normalized = normalize_markets(markets)
    features = build_feature_rows(normalized, as_of=as_of)
    snapshot_hash = feature_snapshot_hash(features)
    model = CombinedFairValueModel()

    scored_rows: list[dict] = []
    for market, feature_row in zip(normalized, features):
        fair_probability, confidence = model.predict(feature_row)
        scoring = score_market(
            market_probability=market["market_probability"],
            fair_probability=fair_probability,
            confidence=confidence,
            liquidity_score=market["liquidity_score"],
        )
        scored_rows.append(
            {
                "market_id": market["market_id"],
                "platform": market["platform"],
                "title": market["title"],
                "category": market["category"],
                "market_probability": _round(market["market_probability"]),
                "fair_probability": _round(fair_probability),
                "gap": _round(scoring["gap"]),
                "confidence": _round(confidence),
                "liquidity_score": _round(market["liquidity_score"]),
                "resolution_time": market["resolution_time"],
                "updated_at": market["updated_at"],
                "actionability_score": _round(scoring["actionability_score"]),
                "mapping_confidence": _round(market["mapping_confidence"]),
                "macro_series_id": market["macro_series_id"],
            }
        )

    return rank_markets(scored_rows), snapshot_hash


def _category_share_rows(markets: list[dict]) -> list[dict[str, Any]]:
    totals: dict[str, float] = {}
    total_absolute_gap = 0.0
    for row in markets:
        absolute_gap = abs(float(row["gap"]))
        category = row["category"]
        totals[category] = totals.get(category, 0.0) + absolute_gap
        total_absolute_gap += absolute_gap

    category_rows = [
        {
            "category": category,
            "absolute_gap": _round(absolute_gap),
            "share_of_total_gap": _round(0.0 if total_absolute_gap == 0 else absolute_gap / total_absolute_gap),
        }
        for category, absolute_gap in sorted(totals.items(), key=lambda item: item[1], reverse=True)
    ]
    return category_rows


def build_scored_snapshot_series() -> dict[str, Any]:
    base_markets = get_markets()
    window = get_snapshot_window()

    scored_snapshots: list[dict[str, Any]] = []
    for snapshot in window["snapshots"]:
        as_of = snapshot["as_of"]
        markets = _apply_snapshot_overrides(
            base_markets=base_markets,
            overrides=snapshot.get("overrides", {}),
            as_of=as_of,
        )
        scored, snapshot_hash = _score_snapshot(markets=markets, as_of=as_of)
        scored_snapshots.append(
            {
                "snapshot_id": snapshot["snapshot_id"],
                "label": snapshot["label"],
                "as_of": as_of,
                "feature_snapshot_hash": snapshot_hash,
                "markets": scored,
            }
        )

    return {
        "series_name": window["series_name"],
        "description": window.get("description", ""),
        "snapshots": scored_snapshots,
    }


def compute_flagship_persistence(scored_series: dict[str, Any] | None = None) -> dict[str, Any]:
    series = scored_series or build_scored_snapshot_series()

    snapshot_rows: list[dict[str, Any]] = []
    top_market_titles: dict[str, str] = {}
    top_market_ids: list[str] = []

    for snapshot in series["snapshots"]:
        finding = compute_flagship_finding(markets=snapshot["markets"], as_of=snapshot["as_of"])
        top_market_id = finding["top_market_id"]
        top_market_ids.append(top_market_id)
        top_market_titles[top_market_id] = finding["top_market_title"]

        snapshot_rows.append(
            {
                "snapshot_id": snapshot["snapshot_id"],
                "label": snapshot["label"],
                "as_of": snapshot["as_of"],
                "feature_snapshot_hash": snapshot["feature_snapshot_hash"],
                "top_market_id": top_market_id,
                "top_market_title": finding["top_market_title"],
                "top_share_of_total_gap": _round(finding["top_share_of_total_gap"]),
                "top_to_second_ratio": _round(finding["top_to_second_ratio"]),
                "herfindahl_index": _round(finding["herfindahl_index"]),
            }
        )

    top_counter = Counter(top_market_ids)
    dominant_market_id, dominant_count = top_counter.most_common(1)[0]
    dominant_title = top_market_titles[dominant_market_id]

    persistence_rate = dominant_count / len(snapshot_rows)
    average_top_share = mean(row["top_share_of_total_gap"] for row in snapshot_rows)
    min_top_share = min(row["top_share_of_total_gap"] for row in snapshot_rows)
    max_top_share = max(row["top_share_of_total_gap"] for row in snapshot_rows)

    headline = (
        f"{dominant_title} stays the top dislocation in {dominant_count}/{len(snapshot_rows)} "
        f"deterministic snapshots."
    )
    result = (
        f"Persistence rate: {_percent(persistence_rate)}% | "
        f"Average top-share: {_percent(average_top_share)}% | "
        f"Top-share range: {_percent(min_top_share)}% to {_percent(max_top_share)}%"
    )

    return {
        "headline_finding": headline,
        "question": "Is the flagship dislocation concentration a one-off or persistent across deterministic snapshots?",
        "method": (
            "Replay the same deterministic scoring pipeline across a committed snapshot window and recompute "
            "top-share, top-to-second ratio, and HHI for each timestamp."
        ),
        "result": result,
        "interpretation": (
            "The concentration story is stable across the window, so the flagship insight is not driven by a single "
            "timestamp artifact."
        ),
        "limitations": [
            "Snapshot window is short and synthetic by design for deterministic reproducibility.",
            "Persistence here is structural consistency, not a prediction of future market behavior.",
            "Small universe size can amplify concentration metrics relative to broader production universes.",
        ],
        "window_name": series["series_name"],
        "window_size": len(snapshot_rows),
        "dominant_top_market_id": dominant_market_id,
        "dominant_top_market_title": dominant_title,
        "persistence_rate": _round(persistence_rate),
        "average_top_share": _round(average_top_share),
        "min_top_share": _round(min_top_share),
        "max_top_share": _round(max_top_share),
        "snapshots": snapshot_rows,
    }


def compute_secondary_finding(scored_series: dict[str, Any] | None = None) -> dict[str, Any]:
    series = scored_series or build_scored_snapshot_series()

    snapshot_rows: list[dict[str, Any]] = []
    for snapshot in series["snapshots"]:
        poly_rows = [row for row in snapshot["markets"] if row["platform"] == "Polymarket"]
        kalshi_rows = [row for row in snapshot["markets"] if row["platform"] == "Kalshi"]

        poly_mean_gap = mean(row["gap"] for row in poly_rows)
        kalshi_mean_gap = mean(row["gap"] for row in kalshi_rows)
        asymmetry_gap = poly_mean_gap - kalshi_mean_gap

        snapshot_rows.append(
            {
                "snapshot_id": snapshot["snapshot_id"],
                "label": snapshot["label"],
                "as_of": snapshot["as_of"],
                "feature_snapshot_hash": snapshot["feature_snapshot_hash"],
                "polymarket_mean_gap": _round(poly_mean_gap),
                "kalshi_mean_gap": _round(kalshi_mean_gap),
                "asymmetry_gap": _round(asymmetry_gap),
            }
        )

    average_asymmetry_gap = mean(row["asymmetry_gap"] for row in snapshot_rows)
    positive_windows = sum(1 for row in snapshot_rows if row["asymmetry_gap"] > 0)
    positive_window_share = positive_windows / len(snapshot_rows)

    headline = (
        f"Platform gap asymmetry is positive in {positive_windows}/{len(snapshot_rows)} snapshots: "
        f"Polymarket mean gaps stay above Kalshi."
    )
    result = (
        f"Average asymmetry (Polymarket mean gap - Kalshi mean gap): {_percent(average_asymmetry_gap)} pts | "
        f"Positive-window share: {_percent(positive_window_share)}%"
    )

    return {
        "headline_finding": headline,
        "question": "Do platforms exhibit asymmetric signed mispricing across the deterministic snapshot window?",
        "method": (
            "For each snapshot, compute mean signed gap by platform and measure asymmetry as "
            "Polymarket mean gap minus Kalshi mean gap."
        ),
        "result": result,
        "interpretation": (
            "A consistently positive asymmetry indicates directional pricing differences across platforms, which "
            "complements concentration analysis with a cross-platform structural lens."
        ),
        "one_sentence": (
            "Across the deterministic window, Polymarket contracts are consistently priced further above fair value "
            "than Kalshi contracts on average."
        ),
        "limitations": [
            "Only two platforms are represented in the demo fixture universe.",
            "Mean signed gap can hide within-platform category dispersion.",
            "Asymmetry is descriptive evidence, not a causal claim."
        ],
        "window_name": series["series_name"],
        "window_size": len(snapshot_rows),
        "average_asymmetry_gap": _round(average_asymmetry_gap),
        "positive_window_share": _round(positive_window_share),
        "snapshots": snapshot_rows,
    }


def compute_third_finding(scored_series: dict[str, Any] | None = None) -> dict[str, Any]:
    series = scored_series or build_scored_snapshot_series()

    snapshot_rows: list[dict[str, Any]] = []
    for snapshot in series["snapshots"]:
        category_rows = _category_share_rows(snapshot["markets"])
        snapshot_rows.append(
            {
                "snapshot_id": snapshot["snapshot_id"],
                "label": snapshot["label"],
                "as_of": snapshot["as_of"],
                "feature_snapshot_hash": snapshot["feature_snapshot_hash"],
                "category_shares": category_rows,
            }
        )

    first_snapshot = snapshot_rows[0]
    last_snapshot = snapshot_rows[-1]
    first_map = {row["category"]: float(row["share_of_total_gap"]) for row in first_snapshot["category_shares"]}
    last_map = {row["category"]: float(row["share_of_total_gap"]) for row in last_snapshot["category_shares"]}
    categories = sorted(set(first_map) | set(last_map))

    category_drift_rows: list[dict[str, Any]] = []
    for category in categories:
        first_share = first_map.get(category, 0.0)
        last_share = last_map.get(category, 0.0)
        drift = last_share - first_share
        category_drift_rows.append(
            {
                "category": category,
                "first_share": _round(first_share),
                "last_share": _round(last_share),
                "drift": _round(drift),
            }
        )

    category_drift_rows.sort(key=lambda row: abs(float(row["drift"])), reverse=True)
    dominant = category_drift_rows[0]
    dominant_direction = "increased" if dominant["drift"] >= 0 else "decreased"
    dominant_drift_points = abs(float(dominant["drift"]))

    headline = (
        f"{dominant['category'].capitalize()} dislocation share {dominant_direction} by "
        f"{_percent(dominant_drift_points)} pts across the deterministic window."
    )
    result = (
        f"Largest category-share drift: {dominant['category']} {dominant_direction} by "
        f"{_percent(dominant_drift_points)} pts (first={_percent(dominant['first_share'])}%"
        f", last={_percent(dominant['last_share'])}%)."
    )

    return {
        "headline_finding": headline,
        "question": "Which macro category shows the largest dislocation-share drift across deterministic snapshots?",
        "method": (
            "For each snapshot, compute category share of total absolute dislocation, then compare the first and last "
            "snapshot shares to measure drift by category."
        ),
        "result": result,
        "interpretation": (
            "Category drift complements concentration and platform asymmetry by showing where dislocation mass is "
            "rotating in the fixture-backed macro universe over time."
        ),
        "one_sentence": (
            f"{dominant['category'].capitalize()} is the largest drifting category, {dominant_direction} by "
            f"{_percent(dominant_drift_points)} pts from the first to last deterministic snapshot."
        ),
        "limitations": [
            "Category drift is measured on a small deterministic fixture universe.",
            "Drift compares first and last snapshots; intrawindow oscillations may still occur.",
            "Category share drift is descriptive and not a causal forecast signal.",
        ],
        "window_name": series["series_name"],
        "window_size": len(snapshot_rows),
        "dominant_drift_category": dominant["category"],
        "dominant_drift_points": _round(dominant_drift_points),
        "category_drift": category_drift_rows,
        "snapshots": snapshot_rows,
    }
