from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.schemas.common import SuccessResponse, success_response
from app.core.config import settings
from app.core.observability import metrics
from app.db.session import check_database

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=SuccessResponse[dict[str, str]],
    summary="Liveness check",
    description="Confirms the API process is running. Does not validate downstream dependencies.",
)
def health():
    return success_response({"status": "ok"})


@router.get(
    "/health/ready",
    response_model=SuccessResponse[dict[str, str]],
    summary="Readiness check",
    description="Confirms the API can reach the configured database before receiving traffic.",
    responses={
        503: {
            "description": "Database is unavailable",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "code": "DATABASE_UNAVAILABLE",
                            "message": "Database readiness check failed",
                            "details": [],
                        },
                        "meta": {"request_id": "req_01HREADY"},
                    }
                }
            },
        }
    },
)
def readiness():
    try:
        check_database()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "DATABASE_UNAVAILABLE",
                "message": "Database readiness check failed",
            },
        )
    return success_response({"database": "ok"})


@router.get(
    "/health/metrics",
    response_model=SuccessResponse[dict[str, Any]],
    summary="Lightweight runtime metrics snapshot",
    description="Returns in-process latency, count, tier, and confidence telemetry for operational inspection.",
)
def runtime_metrics():
    return success_response(metrics.snapshot())


@router.get(
    "/health/operational",
    response_model=SuccessResponse[dict[str, Any]],
    summary="Operational health and SLO snapshot",
    description=(
        "Returns lightweight staging health: latency SLO checks, valuation confidence and tier "
        "distributions, recent valuation events, and slow request/query summaries."
    ),
)
def operational_health():
    return success_response(
        metrics.operational_summary(
            api_latency_slo_ms=settings.API_LATENCY_SLO_MS,
            valuation_latency_slo_ms=settings.VALUATION_LATENCY_SLO_MS,
        )
    )
