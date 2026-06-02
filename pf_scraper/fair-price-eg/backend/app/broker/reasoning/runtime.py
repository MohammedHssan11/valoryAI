from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Callable, TypeVar

from app.broker.schemas.contracts import BrokerStage
from app.broker.telemetry.tracing import BrokerTrace
from app.core.config import settings
from app.core.observability import get_request_telemetry, metrics

logger = logging.getLogger(__name__)
T = TypeVar("T")


@dataclass(frozen=True)
class StageExecutionPolicy:
    timeout_ms: float = settings.BROKER_REASONING_STAGE_TIMEOUT_MS
    retries: int = 0


class ReasoningStageError(RuntimeError):
    def __init__(self, *, stage: BrokerStage, code: str, message: str) -> None:
        super().__init__(message)
        self.stage = stage
        self.code = code


class ReasoningStageRuntime:
    def execute(
        self,
        *,
        trace: BrokerTrace,
        stage: BrokerStage,
        message: str,
        operation: Callable[[], T],
        policy: StageExecutionPolicy | None = None,
    ) -> T:
        policy = policy or StageExecutionPolicy()
        trace.add_event(stage=stage, event_type="stage_started", message=message)
        start = time.perf_counter()
        attempts = 0
        last_error: Exception | None = None

        while attempts <= policy.retries:
            attempts += 1
            try:
                trace.add_event(
                    stage=stage,
                    event_type="stage_progress",
                    message=f"{stage.value} executing",
                    payload={"attempt": attempts, "timeout_ms": policy.timeout_ms},
                )
                result = operation()
                duration_ms = (time.perf_counter() - start) * 1000
                self._record_success(trace, stage, duration_ms, attempts, policy)
                return result
            except Exception as exc:
                last_error = exc
                if attempts <= policy.retries:
                    trace.add_event(
                        stage=stage,
                        event_type="reasoning_event",
                        message=f"{stage.value} retry scheduled",
                        payload={"attempt": attempts, "error": str(exc)},
                    )

        duration_ms = (time.perf_counter() - start) * 1000
        self._record_failure(trace, stage, duration_ms, attempts, last_error)
        raise ReasoningStageError(
            stage=stage,
            code="REASONING_STAGE_FAILED",
            message=str(last_error) if last_error else f"{stage.value} failed",
        )

    def _record_success(
        self,
        trace: BrokerTrace,
        stage: BrokerStage,
        duration_ms: float,
        attempts: int,
        policy: StageExecutionPolicy,
    ) -> None:
        timeout_exceeded = duration_ms > policy.timeout_ms
        telemetry = get_request_telemetry()
        if telemetry is not None:
            telemetry.add_timing(f"broker.reasoning.{stage.value}_ms", duration_ms)
            telemetry.set_attribute("broker_session_id", trace.session_id)
        metrics.observe("broker.reasoning_stage_duration_ms", duration_ms, {"stage": stage.value})
        metrics.increment(
            "broker.reasoning_stage_completed",
            {"stage": stage.value, "timeout_exceeded": timeout_exceeded},
        )
        if timeout_exceeded:
            logger.warning(
                "broker_reasoning_stage_timeout_budget_exceeded",
                extra={"stage": stage.value, "duration_ms": round(duration_ms, 2), "budget_ms": policy.timeout_ms},
            )
            trace.add_event(
                stage=stage,
                event_type="reasoning_event",
                message=f"{stage.value} exceeded soft timeout budget",
                elapsed_ms=duration_ms,
                payload={"timeout_ms": policy.timeout_ms},
            )
        trace.add_event(
            stage=stage,
            event_type="stage_completed",
            message=f"{stage.value} completed",
            elapsed_ms=duration_ms,
            payload={"attempts": attempts, "timeout_exceeded": timeout_exceeded},
        )

    def _record_failure(
        self,
        trace: BrokerTrace,
        stage: BrokerStage,
        duration_ms: float,
        attempts: int,
        error: Exception | None,
    ) -> None:
        metrics.observe("broker.reasoning_stage_duration_ms", duration_ms, {"stage": stage.value})
        metrics.increment("broker.reasoning_stage_failed", {"stage": stage.value})
        trace.add_event(
            stage=stage,
            event_type="stage_failed",
            message=f"{stage.value} failed",
            elapsed_ms=duration_ms,
            payload={"attempts": attempts, "error": str(error) if error else None},
        )


reasoning_stage_runtime = ReasoningStageRuntime()
