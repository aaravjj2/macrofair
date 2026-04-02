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


class ThirdFindingCategoryDrift(BaseModel):
    category: str
    first_share: float
    last_share: float
    drift: float


class ThirdFindingCategoryShare(BaseModel):
    category: str
    absolute_gap: float
    share_of_total_gap: float


class ThirdFindingSnapshot(BaseModel):
    snapshot_id: str
    label: str
    as_of: str
    feature_snapshot_hash: str
    category_shares: list[ThirdFindingCategoryShare]


class ThirdFindingPayload(BaseModel):
    headline_finding: str
    question: str
    method: str
    result: str
    interpretation: str
    one_sentence: str
    limitations: list[str]
    window_name: str
    window_size: int
    dominant_drift_category: str
    dominant_drift_points: float
    category_drift: list[ThirdFindingCategoryDrift]
    snapshots: list[ThirdFindingSnapshot]


class FindingsHeadlinesPayload(BaseModel):
    flagship: str
    flagship_persistence: str
    secondary: str
    third: str


class FindingsIndexPayload(BaseModel):
    generated_at: str
    mode: str
    window_name: str
    window_size: int
    headlines: FindingsHeadlinesPayload
    payload_hash: str


class RankedSnapshotMarketPayload(BaseModel):
    rank: int
    market_id: str
    title: str
    platform: str
    category: str
    market_probability: float
    fair_probability: float
    gap: float
    confidence: float


class RankedSnapshotSummaryPayload(BaseModel):
    count: int
    markets: list[RankedSnapshotMarketPayload]


class FindingsBundlePayload(BaseModel):
    flagship: FlagshipFindingPayload
    flagship_persistence: FlagshipPersistencePayload
    secondary: SecondaryFindingPayload
    third: ThirdFindingPayload


class FindingsReportPayload(BaseModel):
    report_name: str
    report_version: str
    generated_at: str
    mode: str
    app_version: str
    model_version: str
    schema_version: str
    metadata: dict[str, object]
    findings: FindingsBundlePayload
    ranked_snapshot_summary: RankedSnapshotSummaryPayload
    payload_hash: str


class ZerveStatusPayload(BaseModel):
    integration: str
    enabled: bool
    configured: bool
    mode: str
    base_url: str
    project_id: str
    api_key_configured: bool
    missing_required: list[str]
    remote_check_attempted: bool
    remote_connected: bool
    remote_status_code: int | None
    last_error: str | None
    note: str


class ZerveSubmissionPackagePayload(BaseModel):
    package_name: str
    package_version: str
    generated_at: str
    mode: str
    app_version: str
    model_version: str
    schema_version: str
    metadata: dict[str, object]
    findings: FindingsBundlePayload
    ranked_snapshot_summary: RankedSnapshotSummaryPayload
    findings_report_hash: str
    payload_hash: str


class ZervePackagePayload(BaseModel):
    status: ZerveStatusPayload
    package: ZerveSubmissionPackagePayload


class ZerveSyncRequest(BaseModel):
    dry_run: bool = True


class ZerveSyncPayload(BaseModel):
    attempted: bool
    dry_run: bool
    synced: bool
    status_code: int | None
    message: str
    remote_error: str | None
    remote_reference: str | None = None
    package_hash: str
    status: ZerveStatusPayload


class SubmissionReportPayload(BaseModel):
    report_name: str
    report_version: str
    generated_at: str
    mode: str
    app_version: str
    findings_report: FindingsReportPayload
    zerve_integration: ZerveStatusPayload
    payload_hash: str
