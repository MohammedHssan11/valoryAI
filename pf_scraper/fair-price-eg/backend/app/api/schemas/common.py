from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field

from app.core.logging import get_request_id

TData = TypeVar("TData")


class ErrorDetail(BaseModel):
    code: str = Field(description="Stable machine-readable error code.")
    message: str = Field(description="Safe human-readable error message.")
    field: str | None = Field(default=None, description="Request field associated with the error, when applicable.")


class ApiError(BaseModel):
    code: str = Field(description="Stable top-level error code.")
    message: str = Field(description="Safe top-level error message.")
    details: list[ErrorDetail] = Field(default_factory=list, description="Field-level or contextual error details.")


class ErrorResponse(BaseModel):
    success: Literal[False] = Field(default=False, description="Always false for error envelopes.")
    error: ApiError = Field(description="Structured error payload.")
    meta: dict[str, Any] = Field(default_factory=dict, description="Trace metadata, including request_id.")


class SuccessResponse(BaseModel, Generic[TData]):
    success: Literal[True] = Field(default=True, description="Always true for successful envelopes.")
    data: TData = Field(description="Endpoint-specific response payload.")
    meta: dict[str, Any] = Field(default_factory=dict, description="Trace metadata, including request_id.")


def request_meta(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    request_id = get_request_id()
    meta = {} if request_id == "-" else {"request_id": request_id}
    if extra:
        meta.update(extra)
    return meta


def success_response(data: TData, meta: dict[str, Any] | None = None) -> SuccessResponse[TData]:
    return SuccessResponse(data=data, meta=request_meta(meta))
