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
