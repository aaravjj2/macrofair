from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    mode: str
    version: str


class MetadataResponse(BaseModel):
    mode: str
    version: str
    last_refresh: str
    model_version: str
    schema_version: str
    supported_categories: list[str]
    sources: dict[str, str]


class MarketListItem(BaseModel):
    market_id: str
    platform: str
    title: str
    category: str
    market_probability: float
    fair_probability: float
    gap: float
    confidence: float
    liquidity_score: float
    resolution_time: str
    updated_at: str
    actionability_score: float
    rank: int


class HistoryPoint(BaseModel):
    timestamp: str
    probability: float
    volume: float
    spread: float


class ExplanationPayload(BaseModel):
    top_factors: list[str]
    factor_contributions: dict[str, float]
    model_notes: str
    confidence_notes: str
    warning_flags: list[str] = Field(default_factory=list)
    narrative_summary: str


class MarketDetail(BaseModel):
    market_id: str
    platform: str
    title: str
    description: str
    category: str
    sub_category: str
    status: str
    resolution_time: str
    market_probability: float
    fair_probability: float
    gap: float
    confidence: float
    liquidity_score: float
    mapping_confidence: float
    target_variable: str
    macro_series_id: str
    explanation: ExplanationPayload
    history: list[HistoryPoint]
    linked_macro_series: list[dict[str, float | str]]


class FlagshipContribution(BaseModel):
    rank: int
    market_id: str
    title: str
    category: str
    platform: str
    gap: float
    absolute_gap: float
    share_of_total_gap: float
    cumulative_share: float
    confidence: float


class FlagshipCategoryBreakdown(BaseModel):
    category: str
    absolute_gap: float
    share_of_total_gap: float


class FlagshipFindingPayload(BaseModel):
    headline_finding: str
    question: str
    method: str
    result: str
    interpretation: str
    limitations: list[str]
    as_of: str
    top_market_id: str
    top_market_title: str
    top_absolute_gap: float
    total_absolute_gap: float
    top_share_of_total_gap: float
    top_to_second_ratio: float
    herfindahl_index: float
    contributions: list[FlagshipContribution]
    category_breakdown: list[FlagshipCategoryBreakdown]


class FlagshipPersistenceSnapshot(BaseModel):
    snapshot_id: str
    label: str
    as_of: str
    feature_snapshot_hash: str
    top_market_id: str
    top_market_title: str
    top_share_of_total_gap: float
    top_to_second_ratio: float
    herfindahl_index: float


class FlagshipPersistencePayload(BaseModel):
    headline_finding: str
    question: str
    method: str
    result: str
    interpretation: str
    limitations: list[str]
    window_name: str
    window_size: int
    dominant_top_market_id: str
    dominant_top_market_title: str
    persistence_rate: float
    average_top_share: float
    min_top_share: float
    max_top_share: float
    snapshots: list[FlagshipPersistenceSnapshot]


class SecondaryFindingSnapshot(BaseModel):
    snapshot_id: str
    label: str
    as_of: str
    feature_snapshot_hash: str
    polymarket_mean_gap: float
    kalshi_mean_gap: float
    asymmetry_gap: float


class SecondaryFindingPayload(BaseModel):
    headline_finding: str
    question: str
    method: str
    result: str
    interpretation: str
    one_sentence: str
    limitations: list[str]
    window_name: str
    window_size: int
    average_asymmetry_gap: float
    positive_window_share: float
    snapshots: list[SecondaryFindingSnapshot]
