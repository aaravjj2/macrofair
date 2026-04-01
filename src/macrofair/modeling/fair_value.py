from __future__ import annotations


def _clamp(value: float, low: float = 0.01, high: float = 0.99) -> float:
    return max(low, min(value, high))


class FairValueBaselineModel:
    """Simple deterministic baseline blending market and macro signals."""

    model_version = "baseline-v1"

    def predict(self, feature_row: dict) -> tuple[float, float]:
        market_probability = feature_row["market_probability"]
        macro_signal = feature_row["macro_signal"]
        momentum = feature_row["momentum_24h"]
        event_urgency = feature_row["event_urgency"]
        liquidity_score = feature_row["liquidity_score"]
        spread = feature_row["spread"]
        mapping_confidence = feature_row["mapping_confidence"]

        fair_probability = _clamp(
            (0.58 * market_probability)
            + (0.32 * macro_signal)
            + (0.10 * (0.5 + momentum))
            - (0.05 * event_urgency)
            + 0.025
        )

        confidence = _clamp(
            0.35
            + (0.35 * liquidity_score)
            + (0.2 * mapping_confidence)
            + (0.1 * (1.0 - min(spread * 10.0, 1.0))),
            low=0.05,
            high=0.99
        )

        return round(fair_probability, 4), round(confidence, 4)


class FundamentalsOnlyModel:
    """Simple macro-only model used as a complementary signal."""

    model_version = "fundamentals-v1"

    def predict(self, feature_row: dict) -> float:
        macro_signal = feature_row["macro_signal"]
        event_urgency = feature_row["event_urgency"]
        momentum = feature_row["momentum_24h"]
        return round(_clamp((0.82 * macro_signal) + (0.08 * (0.5 + momentum)) - (0.05 * event_urgency) + 0.04), 4)


class ProbabilityCalibrator:
    """Deterministic calibration layer that dampens noisy edge regions."""

    calibration_version = "piecewise-v1"

    def calibrate(self, probability: float, spread: float, liquidity_score: float) -> float:
        centered = probability - 0.5
        edge_penalty = min(max(spread * 2.5, 0.0), 0.08)
        liquidity_boost = max(liquidity_score - 0.5, 0.0) * 0.03
        calibrated = 0.5 + (centered * 0.94) - edge_penalty + liquidity_boost
        return round(_clamp(calibrated), 4)


class CombinedFairValueModel:
    """Combined model blending market-aware and fundamentals-only views then calibrating."""

    model_version = "combined-v1"

    def __init__(self) -> None:
        self.baseline = FairValueBaselineModel()
        self.fundamentals = FundamentalsOnlyModel()
        self.calibrator = ProbabilityCalibrator()

    def predict(self, feature_row: dict) -> tuple[float, float]:
        baseline_fair, baseline_confidence = self.baseline.predict(feature_row)
        fundamentals_fair = self.fundamentals.predict(feature_row)

        blended_fair = _clamp((0.7 * baseline_fair) + (0.3 * fundamentals_fair))
        calibrated_fair = self.calibrator.calibrate(
            probability=blended_fair,
            spread=feature_row["spread"],
            liquidity_score=feature_row["liquidity_score"],
        )

        model_agreement = 1.0 - min(abs(baseline_fair - fundamentals_fair) * 2.5, 1.0)
        confidence = _clamp((0.78 * baseline_confidence) + (0.22 * model_agreement), low=0.05, high=0.99)
        return round(calibrated_fair, 4), round(confidence, 4)
