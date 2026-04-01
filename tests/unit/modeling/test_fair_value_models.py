from __future__ import annotations

from macrofair.features.pipeline import build_feature_row
from macrofair.modeling.fair_value import CombinedFairValueModel, FairValueBaselineModel, FundamentalsOnlyModel, ProbabilityCalibrator
from macrofair.repository import get_markets, get_metadata


def _sample_feature_row() -> dict:
    return build_feature_row(get_markets()[0], as_of=get_metadata()["last_refresh"])


def test_baseline_model_outputs_probability_and_confidence() -> None:
    fair, confidence = FairValueBaselineModel().predict(_sample_feature_row())
    assert 0.0 < fair < 1.0
    assert 0.0 < confidence <= 1.0


def test_fundamentals_model_outputs_probability() -> None:
    fair = FundamentalsOnlyModel().predict(_sample_feature_row())
    assert 0.0 < fair < 1.0


def test_calibrator_keeps_range() -> None:
    calibrated = ProbabilityCalibrator().calibrate(probability=0.71, spread=0.03, liquidity_score=0.7)
    assert 0.0 < calibrated < 1.0


def test_combined_model_outputs_probability_and_confidence() -> None:
    fair, confidence = CombinedFairValueModel().predict(_sample_feature_row())
    assert 0.0 < fair < 1.0
    assert 0.0 < confidence <= 1.0
