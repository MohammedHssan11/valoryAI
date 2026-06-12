from __future__ import annotations

import time
import uuid
from contextlib import contextmanager
from typing import Any, Callable, Iterator

from app.broker.schemas.contracts import BrokerStage, BrokerStageEvent, BrokerToolName
from app.core.observability import get_request_telemetry, metrics


class BrokerTrace:
    def __init__(self, session_id: str, event_handler: Callable[[BrokerStageEvent], None] | None = None) -> None:
        self.session_id = session_id
        self.events: list[BrokerStageEvent] = []
        self.event_handler = event_handler

    def add_event(
        self,
        *,
        stage: BrokerStage,
        event_type: str,
        message: str,
        elapsed_ms: float | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        event = BrokerStageEvent(
            event_id=f"evt_{uuid.uuid4().hex[:12]}",
            stage=stage,
            event_type=event_type,
            message=message,
            elapsed_ms=round(elapsed_ms, 2) if elapsed_ms is not None else None,
            payload=payload or {},
        )
        self.events.append(event)
        if self.event_handler is not None:
            try:
                self.event_handler(event)
            except Exception:
                metrics.increment("broker.trace_event_handler_failed", {"stage": stage.value, "event_type": event_type})

    @contextmanager
    def stage(self, stage: BrokerStage, message: str) -> Iterator[None]:
        self.add_event(stage=stage, event_type="stage_started", message=message)
        start = time.perf_counter()
        try:
            yield
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            telemetry = get_request_telemetry()
            if telemetry is not None:
                telemetry.add_timing(f"broker.{stage.value}_ms", duration_ms)
                telemetry.set_attribute("broker_session_id", self.session_id)
            metrics.observe("broker.stage_duration_ms", duration_ms, {"stage": stage.value})
            metrics.increment("broker.stage_completed", {"stage": stage.value})
            self.add_event(
                stage=stage,
                event_type="stage_completed",
                message=f"{stage.value} completed",
                elapsed_ms=duration_ms,
            )

    def record_tool(self, tool_name: BrokerToolName, duration_ms: float, status: str) -> None:
        metrics.observe(
            "broker.tool_duration_ms",
            duration_ms,
            {"tool": tool_name.value, "status": status},
        )
        metrics.increment("broker.tool_execution", {"tool": tool_name.value, "status": status})
