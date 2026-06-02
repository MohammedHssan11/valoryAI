from __future__ import annotations

import contextvars
from collections import deque
import asyncio
import json
import logging
import sys
import time
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.observability import (
    correlation_id_var,
    get_correlation_id,
    metrics,
    reset_request_telemetry,
    start_request_telemetry,
    telemetry_snapshot,
)

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


def get_request_id() -> str:
    return request_id_var.get()


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        record.correlation_id = get_correlation_id()
        record.environment = settings.ENV
        return True


class JsonFormatter(logging.Formatter):
    _reserved = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__)

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
            "correlation_id": getattr(record, "correlation_id", "-"),
            "environment": getattr(record, "environment", settings.ENV),
        }
        excluded = {"request_id", "correlation_id", "environment"}
        for key, value in record.__dict__.items():
            if key not in self._reserved and key not in payload and key not in excluded:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=False)


def setup_logging():
    level = getattr(logging, settings.LOG_LEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(RequestIdFilter())
    if settings.use_json_logs:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | request_id=%(request_id)s | correlation_id=%(correlation_id)s | %(name)s | %(message)s"
            )
        )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else level)

    # reduce noisy libs
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


class InMemoryRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = {}

    def allow(self, key: str) -> tuple[bool, int]:
        now = time.monotonic()
        window_start = now - self.window_seconds
        hits = self._hits.setdefault(key, deque())

        while hits and hits[0] < window_start:
            hits.popleft()

        if len(hits) >= self.max_requests:
            retry_after = max(1, int(self.window_seconds - (now - hits[0])))
            return False, retry_after

        hits.append(now)
        if len(self._hits) > 10000:
            empty_keys = [item_key for item_key, item_hits in self._hits.items() if not item_hits]
            for item_key in empty_keys[:1000]:
                self._hits.pop(item_key, None)
        return True, 0


rate_limiter = InMemoryRateLimiter(settings.RATE_LIMIT_PER_MINUTE)


def _client_identity(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()
    return request.client.host if request.client else "unknown"


def _rate_limited_path(path: str) -> bool:
    for prefix in settings.RATE_LIMIT_PATHS:
        clean_prefix = prefix.rstrip("/")
        if path == clean_prefix or path.startswith(f"{clean_prefix}/"):
            return True
    return False


def _error_response(status_code: int, code: str, message: str, headers: dict[str, str] | None = None) -> JSONResponse:
    meta = {"request_id": get_request_id()}
    content = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": [],
        },
        "meta": meta,
    }
    response = JSONResponse(status_code=status_code, content=content)
    for key, value in (headers or {}).items():
        response.headers[key] = value
    return response


def _apply_platform_headers(response, request_id: str, correlation_id: str) -> None:
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")


def add_request_logging_middleware(app: FastAPI) -> None:
    logger = logging.getLogger("app.request")

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        correlation_id = request.headers.get("X-Correlation-ID") or request_id
        token = request_id_var.set(request_id)
        correlation_token = correlation_id_var.set(correlation_id)
        telemetry_token = start_request_telemetry()
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id
        start = time.perf_counter()
        try:
            content_length = request.headers.get("content-length")
            try:
                body_bytes = int(content_length) if content_length else 0
            except ValueError:
                body_bytes = settings.MAX_REQUEST_BODY_BYTES + 1

            if body_bytes > settings.MAX_REQUEST_BODY_BYTES:
                response = _error_response(413, "REQUEST_TOO_LARGE", "Request body exceeds the configured size limit")
                metrics.increment("api.request_rejected", {"reason": "request_too_large", "path": request.url.path})
            elif settings.RATE_LIMIT_ENABLED and _rate_limited_path(request.url.path):
                client_key = _client_identity(request)
                limiter_key = f"{client_key}:{request.method}:{request.url.path}"
                allowed, retry_after = rate_limiter.allow(limiter_key)
                if not allowed:
                    response = _error_response(
                        429,
                        "RATE_LIMIT_EXCEEDED",
                        "Too many requests. Please retry shortly.",
                        {"Retry-After": str(retry_after)},
                    )
                    metrics.increment("api.request_rejected", {"reason": "rate_limit", "path": request.url.path})
                    logger.warning(
                        "rate_limit_exceeded",
                        extra={
                            "endpoint": request.url.path,
                            "method": request.method,
                            "client": client_key,
                            "retry_after_seconds": retry_after,
                        },
                    )
                else:
                    response = await asyncio.wait_for(call_next(request), timeout=settings.API_REQUEST_TIMEOUT_SECONDS)
            else:
                response = await asyncio.wait_for(call_next(request), timeout=settings.API_REQUEST_TIMEOUT_SECONDS)

            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            telemetry = telemetry_snapshot()
            _apply_platform_headers(response, request_id, correlation_id)
            for span_name, span_duration_ms in telemetry.get("timings_ms", {}).items():
                metrics.observe(
                    "request.span_timing_ms",
                    float(span_duration_ms),
                    {
                        "path": request.url.path,
                        "span": span_name,
                    },
                )
            metrics.observe(
                "api.endpoint_latency_ms",
                duration_ms,
                {
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                },
            )
            event_fields = {
                "endpoint": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "request_id": request_id,
                "correlation_id": correlation_id,
            }
            metrics.record_event("request", event_fields)
            if duration_ms >= settings.SLOW_REQUEST_MS:
                metrics.increment("api.slow_request", {"path": request.url.path, "method": request.method})
                metrics.record_event("slow_request", {**event_fields, "threshold_ms": settings.SLOW_REQUEST_MS})
                logger.warning(
                    "slow_request",
                    extra={
                        "endpoint": request.url.path,
                        "method": request.method,
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                        "threshold_ms": settings.SLOW_REQUEST_MS,
                    },
                )
            logger.info(
                "request_completed",
                extra={
                    "endpoint": request.url.path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "telemetry": telemetry,
                },
            )
            return response
        except asyncio.TimeoutError:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            response = _error_response(504, "REQUEST_TIMEOUT", "Request processing exceeded the configured timeout")
            _apply_platform_headers(response, request_id, correlation_id)
            metrics.increment("api.request_rejected", {"reason": "timeout", "path": request.url.path})
            metrics.record_event(
                "slow_request",
                {
                    "endpoint": request.url.path,
                    "method": request.method,
                    "status_code": 504,
                    "duration_ms": duration_ms,
                    "threshold_ms": settings.API_REQUEST_TIMEOUT_SECONDS * 1000,
                    "request_id": request_id,
                    "correlation_id": correlation_id,
                },
            )
            metrics.observe(
                "api.endpoint_latency_ms",
                duration_ms,
                {
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 504,
                },
            )
            logger.warning(
                "request_timeout",
                extra={
                    "endpoint": request.url.path,
                    "method": request.method,
                    "duration_ms": duration_ms,
                    "timeout_seconds": settings.API_REQUEST_TIMEOUT_SECONDS,
                },
            )
            return response
        except Exception:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            metrics.increment("api.request_failed", {"path": request.url.path, "method": request.method})
            logger.exception(
                "request_failed",
                extra={
                    "endpoint": request.url.path,
                    "method": request.method,
                    "duration_ms": duration_ms,
                },
            )
            raise
        finally:
            request_id_var.reset(token)
            correlation_id_var.reset(correlation_token)
            reset_request_telemetry(telemetry_token)
