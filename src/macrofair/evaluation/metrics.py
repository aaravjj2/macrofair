from __future__ import annotations

import math


def brier_score(y_true: list[float], y_pred: list[float]) -> float:
    if not y_true or not y_pred or len(y_true) != len(y_pred):
        return 0.0
    return sum((target - pred) ** 2 for target, pred in zip(y_true, y_pred, strict=True)) / len(y_true)


def log_loss(y_true: list[float], y_pred: list[float]) -> float:
    if not y_true or not y_pred or len(y_true) != len(y_pred):
        return 0.0
    eps = 1e-9
    total = 0.0
    for target, pred in zip(y_true, y_pred, strict=True):
        p = min(max(pred, eps), 1.0 - eps)
        total += target * math.log(p) + (1.0 - target) * math.log(1.0 - p)
    return -total / len(y_true)


def expected_calibration_error(y_true: list[float], y_pred: list[float], bins: int = 5) -> float:
    if not y_true or not y_pred or len(y_true) != len(y_pred):
        return 0.0
    bin_size = 1.0 / bins
    total = 0.0

    for idx in range(bins):
        low = idx * bin_size
        high = 1.0 if idx == bins - 1 else (idx + 1) * bin_size
        bucket = [
            (target, pred)
            for target, pred in zip(y_true, y_pred, strict=True)
            if low <= pred < high or (idx == bins - 1 and pred == 1.0)
        ]
        if not bucket:
            continue
        avg_target = sum(item[0] for item in bucket) / len(bucket)
        avg_pred = sum(item[1] for item in bucket) / len(bucket)
        total += (len(bucket) / len(y_true)) * abs(avg_target - avg_pred)

    return total


def calibration_curve_points(y_true: list[float], y_pred: list[float], bins: int = 5) -> list[dict]:
    if not y_true or not y_pred or len(y_true) != len(y_pred):
        return []
    bin_size = 1.0 / bins
    rows: list[dict] = []
    for idx in range(bins):
        low = idx * bin_size
        high = 1.0 if idx == bins - 1 else (idx + 1) * bin_size
        bucket = [
            (target, pred)
            for target, pred in zip(y_true, y_pred, strict=True)
            if low <= pred < high or (idx == bins - 1 and pred == 1.0)
        ]
        if not bucket:
            continue
        rows.append(
            {
                "bucket": idx + 1,
                "predicted": round(sum(item[1] for item in bucket) / len(bucket), 4),
                "observed": round(sum(item[0] for item in bucket) / len(bucket), 4),
                "count": len(bucket),
            }
        )
    return rows