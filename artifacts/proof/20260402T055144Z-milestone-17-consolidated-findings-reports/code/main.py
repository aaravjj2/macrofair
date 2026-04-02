from __future__ import annotations

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from macrofair.repository import get_metadata
from macrofair.schemas import (
    ExplanationPayload,
    FindingsIndexPayload,
    FindingsReportPayload,
    FlagshipFindingPayload,
    FlagshipPersistencePayload,
    HealthResponse,
    HistoryPoint,
    MarketDetail,
    MarketListItem,
    MetadataResponse,
    SecondaryFindingPayload,
    SubmissionReportPayload,
    ThirdFindingPayload,
    ZervePackagePayload,
    ZerveStatusPayload,
    ZerveSyncPayload,
    ZerveSyncRequest,
)
from macrofair.service import MacroFairService
from macrofair.settings import app_mode, app_version


app = FastAPI(title="MacroFair API", version=app_version())
service = MacroFairService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", mode=app_mode(), version=app_version())


@app.get("/api/v1/metadata", response_model=MetadataResponse)
def metadata() -> MetadataResponse:
    return MetadataResponse(**get_metadata())


@app.get("/api/v1/markets", response_model=list[MarketListItem])
def list_markets(
    platform: str | None = Query(default=None),
    category: str | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=100),
    sort_by: str = Query(default="gap", pattern="^(gap|confidence|time)$"),
    min_confidence: float = Query(default=0.0, ge=0.0, le=1.0),
) -> list[MarketListItem]:
    rows = service.list_markets(
        platform=platform,
        category=category,
        limit=limit,
        sort_by=sort_by,
        min_confidence=min_confidence,
    )
    return [MarketListItem(**row) for row in rows]


@app.get("/api/v1/markets/{market_id}", response_model=MarketDetail)
def get_market(market_id: str) -> MarketDetail:
    row = service.get_market(market_id)
    if row is None:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND", "message": "Market not found"}})
    return MarketDetail(**row)


@app.get("/api/v1/markets/{market_id}/history", response_model=list[HistoryPoint])
def get_market_history(market_id: str) -> list[HistoryPoint]:
    history = service.get_history(market_id)
    if not history:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND", "message": "Market history not found"}})
    return [HistoryPoint(**point) for point in history]


@app.get("/api/v1/markets/{market_id}/explain", response_model=ExplanationPayload)
def get_market_explain(market_id: str) -> ExplanationPayload:
    explain = service.get_explain(market_id)
    if explain is None:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND", "message": "Market not found"}})
    return ExplanationPayload(**explain)


@app.get("/api/v1/snapshots/latest")
def latest_snapshot() -> dict:
    metadata_payload = get_metadata()
    markets = service.list_markets(limit=50, sort_by="gap")
    return {
        "metadata": metadata_payload,
        "markets": markets,
        "count": len(markets),
    }


@app.get("/api/v1/compare")
def compare_markets(category: str | None = Query(default=None)) -> dict:
    markets = service.list_markets(limit=100, sort_by="gap", category=category)
    grouped: dict[str, list[dict]] = {}
    for market in markets:
        grouped.setdefault(market["category"], []).append(market)

    comparisons: list[dict] = []
    for group_category, rows in grouped.items():
        by_platform: dict[str, dict] = {row["platform"]: row for row in rows}
        if "Polymarket" in by_platform and "Kalshi" in by_platform:
            poly = by_platform["Polymarket"]
            kalshi = by_platform["Kalshi"]
            comparisons.append(
                {
                    "category": group_category,
                    "polymarket_market_id": poly["market_id"],
                    "kalshi_market_id": kalshi["market_id"],
                    "market_probability_diff": round(poly["market_probability"] - kalshi["market_probability"], 4),
                    "fair_probability_diff": round(poly["fair_probability"] - kalshi["fair_probability"], 4),
                }
            )

    return {"comparisons": comparisons, "count": len(comparisons)}


@app.get("/api/v1/findings/flagship", response_model=FlagshipFindingPayload)
def flagship_finding() -> FlagshipFindingPayload:
    finding = service.get_flagship_finding()
    return FlagshipFindingPayload(**finding)


@app.get("/api/v1/findings/flagship/persistence", response_model=FlagshipPersistencePayload)
def flagship_persistence() -> FlagshipPersistencePayload:
    persistence = service.get_flagship_persistence()
    return FlagshipPersistencePayload(**persistence)


@app.get("/api/v1/findings/secondary", response_model=SecondaryFindingPayload)
def secondary_finding() -> SecondaryFindingPayload:
    finding = service.get_secondary_finding()
    return SecondaryFindingPayload(**finding)


@app.get("/api/v1/findings/third", response_model=ThirdFindingPayload)
def third_finding() -> ThirdFindingPayload:
    finding = service.get_third_finding()
    return ThirdFindingPayload(**finding)


@app.get("/api/v1/findings", response_model=FindingsIndexPayload)
def findings_index() -> FindingsIndexPayload:
    payload = service.get_findings_index_payload()
    return FindingsIndexPayload(**payload)


@app.get("/api/v1/findings/report", response_model=FindingsReportPayload)
def findings_report() -> FindingsReportPayload:
    payload = service.get_findings_report_payload()
    return FindingsReportPayload(**payload)


@app.get("/api/v1/reports/submission", response_model=SubmissionReportPayload)
def submission_report() -> SubmissionReportPayload:
    payload = service.get_submission_report_payload()
    return SubmissionReportPayload(**payload)


@app.get("/api/v1/integrations/zerve/status", response_model=ZerveStatusPayload)
def zerve_status(verify_remote: bool = Query(default=False)) -> ZerveStatusPayload:
    status = service.get_zerve_status(verify_remote=verify_remote)
    return ZerveStatusPayload(**status)


@app.get("/api/v1/integrations/zerve/package", response_model=ZervePackagePayload)
def zerve_package() -> ZervePackagePayload:
    payload = service.get_zerve_package_payload()
    return ZervePackagePayload(**payload)


@app.post("/api/v1/integrations/zerve/sync", response_model=ZerveSyncPayload)
def zerve_sync(request_payload: ZerveSyncRequest = Body(default_factory=ZerveSyncRequest)) -> ZerveSyncPayload:
    result = service.sync_zerve_submission_package(dry_run=request_payload.dry_run)
    return ZerveSyncPayload(**result)
