from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.schemas.common import ApiError, ErrorDetail, ErrorResponse
from app.core.logging import get_request_id

logger = logging.getLogger(__name__)


def _field_from_loc(loc: tuple[Any, ...] | list[Any]) -> str | None:
    parts = [str(part) for part in loc if part != "body"]
    return ".".join(parts) if parts else None


def _validation_code(field: str | None) -> str:
    if field == "property_type":
        return "INVALID_PROPERTY_TYPE"
    if field in {"lat", "lng"}:
        return "INVALID_COORDINATES"
    if field in {"bedrooms", "bathrooms"}:
        return "INVALID_ROOM_COUNT"
    if field == "target_price_egp":
        return "INVALID_TARGET_PRICE"
    if field == "size_sqm":
        return "INVALID_SIZE"
    return "VALIDATION_ERROR"


def error_payload(code: str, message: str, errors: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    payload = ErrorResponse(
        error=ApiError(
            code=code,
            message=message,
            details=[ErrorDetail(**error) for error in errors or []],
        ),
        meta={"request_id": get_request_id()},
    )
    return payload.model_dump()


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for item in exc.errors():
        field = _field_from_loc(item.get("loc", ()))
        errors.append(
            {
                "code": _validation_code(field),
                "message": item.get("msg", "Invalid value"),
                "field": field,
            }
        )

    top_code = errors[0]["code"] if len({error["code"] for error in errors}) == 1 else "VALIDATION_ERROR"
    logger.warning(
        "request_validation_failed",
        extra={
            "endpoint": request.url.path,
            "method": request.method,
            "error_code": top_code,
            "error_count": len(errors),
        },
    )
    return JSONResponse(
        status_code=422,
        content=error_payload(top_code, "Request validation failed", errors),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail
    if isinstance(detail, dict):
        code = str(detail.get("code") or f"HTTP_{exc.status_code}")
        message = str(detail.get("message") or "Request failed")
    else:
        code = f"HTTP_{exc.status_code}"
        message = str(detail or "Request failed")

    logger.warning(
        "http_exception",
        extra={
            "endpoint": request.url.path,
            "method": request.method,
            "status_code": exc.status_code,
            "error_code": code,
        },
    )
    return JSONResponse(status_code=exc.status_code, content=error_payload(code, message))


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "unhandled_exception",
        extra={
            "endpoint": request.url.path,
            "method": request.method,
            "error_code": "INTERNAL_SERVER_ERROR",
        },
    )
    return JSONResponse(
        status_code=500,
        content=error_payload("INTERNAL_SERVER_ERROR", "An unexpected server error occurred"),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
