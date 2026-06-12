import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.common import SuccessResponse, success_response
from app.api.schemas.pricing import RentFairPriceRequest, RentFairPriceResponse
from app.db.session import get_db
from app.services.router_service import price_listing_router
from fastapi import BackgroundTasks
import uuid

router = APIRouter(tags=["pricing"])
logger = logging.getLogger(__name__)


@router.post(
    "/v1/valuation/fair-price",
    response_model=SuccessResponse[RentFairPriceResponse],
    summary="Estimate governed category valuation",
    description=(
        "Runs ValorAI's deterministic category-aware valuation pipeline using governed property contracts, "
        "comparable retrieval, amenity intelligence, confidence scoring, and structured explainability traces."
    ),
)
@router.post(
    "/v1/rent/fair-price",
    response_model=SuccessResponse[RentFairPriceResponse],
    summary="Estimate fair residential rent",
    description=(
        "Runs ValorAI's deterministic CMT/CMA valuation pipeline using comparable retrieval, "
        "hard guardrails, MAD outlier filtering, weighted median pricing, confidence scoring, "
        "and structured explainability traces."
    ),
    responses={
        200: {
            "description": "Successful fair-rent valuation envelope",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": RentFairPriceResponse.model_config["json_schema_extra"]["examples"][0],
                        "meta": {"request_id": "req_01HVVALUATION"},
                    }
                }
            },
        },
        422: {
            "description": "Request validation failed",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "code": "INVALID_SIZE",
                            "message": "Request validation failed",
                            "details": [
                                {
                                    "code": "INVALID_SIZE",
                                    "message": "Input should be greater than 0",
                                    "field": "size_sqm",
                                }
                            ],
                        },
                        "meta": {"request_id": "req_01HINVALID"},
                    }
                }
            },
        },
        429: {
            "description": "Rate limit exceeded",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": "Too many requests. Please retry shortly.",
                            "details": [],
                        },
                        "meta": {"request_id": "req_01HRATE"},
                    }
                }
            },
        },
    },
)
def rent_fair_price(req: RentFairPriceRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    ctx = {"stage": "contract_resolution", "comps_count": None, "tier_used": None}
    request_id = f"req_{uuid.uuid4().hex[:12]}"
    try:
        response = price_listing_router(req, db, ctx, background_tasks, request_id)
        return success_response(response)
    except Exception as e:
        if not isinstance(e, HTTPException):
            logger.exception(
                "HTTP 500 INTERNAL_SERVER_ERROR in valuation pipeline",
                extra={
                    "category": req.property_category,
                    "property_type": req.property_type,
                    "request_payload": req.model_dump(),
                    "stage": ctx["stage"],
                    "comps_count": ctx["comps_count"],
                    "tier_used": ctx["tier_used"],
                }
            )
        raise
