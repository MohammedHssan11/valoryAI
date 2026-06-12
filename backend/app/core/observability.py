from __future__ import annotations

import contextvars
import threading
import time
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterator


correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id", default="-")
_telemetry_var: contextvars.ContextVar["RequestTelemetry | None"] = contextvars.ContextVar("request_telemetry", default=None)


def get_correlation_id() -> str:
    return correlation_id_var.get()


@dataclass
class RequestTelemetry:
    timings_ms: dict[str, float] = field(default_factory=dict)
    counters: dict[str, int] = field(default_factory=dict)
    attributes: dict[str, Any] = field(default_factory=dict)

    def add_timing(self, name: str, duration_ms: float) -> None:
        self.timings_ms[name] = round(self.timings_ms.get(name, 0.0) + duration_ms, 2)

    def increment(self, name: str, amount: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + amount

    def set_attribute(self, name: str, value: Any) -> None:
        if value is not None:
            self.attributes[name] = value

    def snapshot(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.timings_ms:
            payload["timings_ms"] = dict(self.timings_ms)
        if self.counters:
            payload["counters"] = dict(self.counters)
        if self.attributes:
            payload["attributes"] = dict(self.attributes)
        return payload


def start_request_telemetry() -> contextvars.Token[RequestTelemetry | None]:
    return _telemetry_var.set(RequestTelemetry())


def reset_request_telemetry(token: contextvars.Token[RequestTelemetry | None]) -> None:
    _telemetry_var.reset(token)


def get_request_telemetry() -> RequestTelemetry | None:
    return _telemetry_var.get()


@contextmanager
def timed_span(name: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        telemetry = get_request_telemetry()
        if telemetry is not None:
            telemetry.add_timing(name, (time.perf_counter() - start) * 1000)


def telemetry_snapshot() -> dict[str, Any]:
    telemetry = get_request_telemetry()
    return telemetry.snapshot() if telemetry is not None else {}


def _labels_key(labels: dict[str, Any] | None) -> tuple[tuple[str, str], ...]:
    if not labels:
        return ()
    return tuple(sorted((str(key), str(value)) for key, value in labels.items()))


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: dict[tuple[str, tuple[tuple[str, str], ...]], int] = {}
        self._histograms: dict[tuple[str, tuple[tuple[str, str], ...]], list[float]] = {}
        self._events: deque[dict[str, Any]] = deque(maxlen=250)

    def increment(self, name: str, labels: dict[str, Any] | None = None, amount: int = 1) -> None:
        key = (name, _labels_key(labels))
        with self._lock:
            self._counters[key] = self._counters.get(key, 0) + amount

    def observe(self, name: str, value: float, labels: dict[str, Any] | None = None) -> None:
        key = (name, _labels_key(labels))
        with self._lock:
            values = self._histograms.setdefault(key, [])
            values.append(float(value))
            if len(values) > 1000:
                del values[: len(values) - 1000]

    def record_event(self, name: str, fields: dict[str, Any] | None = None) -> None:
        event = {
            "name": name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **(fields or {}),
        }
        with self._lock:
            self._events.append(event)

    def _counter_snapshot(self) -> list[dict[str, Any]]:
        return [
            {
                "name": name,
                "labels": dict(labels),
                "value": value,
            }
            for (name, labels), value in sorted(self._counters.items())
        ]

    def _histogram_snapshot(self) -> list[dict[str, Any]]:
        histograms = []
        for (name, labels), values in sorted(self._histograms.items()):
            if not values:
                continue
            ordered = sorted(values)
            count = len(ordered)
            histograms.append(
                {
                    "name": name,
                    "labels": dict(labels),
                    "count": count,
                    "avg": round(sum(ordered) / count, 2),
                    "min": round(ordered[0], 2),
                    "max": round(ordered[-1], 2),
                    "p50": round(ordered[int((count - 1) * 0.50)], 2),
                    "p95": round(ordered[int((count - 1) * 0.95)], 2),
                    "p99": round(ordered[int((count - 1) * 0.99)], 2),
                }
            )
        return histograms

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            counters = self._counter_snapshot()
            histograms = self._histogram_snapshot()
            recent_events = list(self._events)

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "counters": counters,
            "histograms": histograms,
            "recent_events": recent_events[-25:],
        }

    def operational_summary(self, api_latency_slo_ms: float, valuation_latency_slo_ms: float) -> dict[str, Any]:
        with self._lock:
            counters = self._counter_snapshot()
            histograms = self._histogram_snapshot()
            events = list(self._events)

        def counter_map(metric_name: str, label_name: str) -> dict[str, int]:
            out: dict[str, int] = {}
            for item in counters:
                if item["name"] == metric_name:
                    label = item["labels"].get(label_name, "unknown")
                    out[label] = int(item["value"])
            return out

        def histograms_for(metric_name: str) -> list[dict[str, Any]]:
            return [item for item in histograms if item["name"] == metric_name]

        def worst_p95(metric_name: str) -> float | None:
            values = [float(item["p95"]) for item in histograms_for(metric_name)]
            return max(values) if values else None

        slow_requests = [event for event in events if event["name"] == "slow_request"][-10:]
        recent_valuations = [event for event in events if event["name"] == "valuation"][-10:]
        valuation_p95 = worst_p95("valuation.duration_ms")
        api_p95 = worst_p95("api.endpoint_latency_ms")

        checks = [
            {
                "name": "api_latency_p95",
                "status": "unknown" if api_p95 is None else ("ok" if api_p95 <= api_latency_slo_ms else "degraded"),
                "observed_ms": api_p95,
                "threshold_ms": api_latency_slo_ms,
            },
            {
                "name": "valuation_latency_p95",
                "status": "unknown" if valuation_p95 is None else ("ok" if valuation_p95 <= valuation_latency_slo_ms else "degraded"),
                "observed_ms": valuation_p95,
                "threshold_ms": valuation_latency_slo_ms,
            },
            {
                "name": "slow_requests",
                "status": "ok" if not slow_requests else "degraded",
                "count_recent": len(slow_requests),
            },
        ]
        status = "degraded" if any(check["status"] == "degraded" for check in checks) else "ok"

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "checks": checks,
            "latency": {
                "api_endpoint": histograms_for("api.endpoint_latency_ms"),
                "spans": histograms_for("request.span_timing_ms"),
                "valuation": histograms_for("valuation.duration_ms"),
                "broker_stage": histograms_for("broker.stage_duration_ms"),
                "broker_reasoning_stage": histograms_for("broker.reasoning_stage_duration_ms"),
                "broker_tool": histograms_for("broker.tool_duration_ms"),
                "broker_narration": histograms_for("broker.narration_latency_ms"),
                "db_query": histograms_for("db.query_latency_ms"),
                "comparable_count": histograms_for("valuation.comparable_count"),
                "confidence_score": histograms_for("valuation.confidence_score"),
            },
            "distributions": {
                "confidence_labels": counter_map("valuation.confidence_label", "label"),
                "tiers": counter_map("valuation.tier_usage", "tier"),
                "flags": counter_map("valuation.flag", "flag"),
                "broker_requests": counter_map("broker.request", "intent"),
                "broker_reasoning_requests": counter_map("broker.reasoning_request", "intent"),
                "broker_intents": counter_map("broker.intent_classification", "intent"),
                "broker_grounding": counter_map("broker.grounding_validation", "status"),
                "broker_governance": counter_map("broker.response_governance", "status"),
                "request_rejections": counter_map("api.request_rejected", "reason"),
            },
            "recent": {
                "valuations": recent_valuations,
                "broker_orchestrations": [event for event in events if event["name"] == "broker_orchestration"][-10:],
                "broker_intents": [event for event in events if event["name"] == "broker_intent_classified"][-10:],
                "broker_governance": [event for event in events if event["name"] == "broker_response_governance"][-10:],
                "slow_requests": slow_requests,
                "slow_queries": [event for event in events if event["name"] == "slow_query"][-10:],
            },
        }


metrics = MetricsRegistry()
