from __future__ import annotations

import time
from typing import Callable

from app.broker.schemas.contracts import (
    BrokerAnalyticalResponse,
    BrokerContext,
    BrokerNarrationTelemetry,
    BrokerReasoningPlan,
)
from app.broker.services.formatter import AIResponseFormatter, response_formatter
from app.core.observability import metrics


class BrokerNarrationResult:
    def __init__(self, *, response: BrokerAnalyticalResponse, telemetry: BrokerNarrationTelemetry) -> None:
        self.response = response
        self.telemetry = telemetry


class DeterministicBrokerNarrationRuntime:
    """Compatibility runtime for the transitional broker API.

    Phase 5.5C.6 model narration is owned exclusively by the Copilot
    Orchestrator pipeline. The legacy broker API remains deterministic.
    """

    def __init__(self, *, formatter: AIResponseFormatter) -> None:
        self.formatter = formatter

    def generate(
        self,
        *,
        context: BrokerContext,
        plan: BrokerReasoningPlan,
        on_chunk: Callable[[str, dict], None] | None = None,
    ) -> BrokerNarrationResult:
        self._emit_safe_progress_chunks(context=context, plan=plan, on_chunk=on_chunk)
        start = time.perf_counter()
        response = self.formatter.format(context)
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        telemetry = BrokerNarrationTelemetry(
            provider="deterministic_formatter",
            used_llm=False,
            latency_ms=latency_ms,
            fallback_reason="legacy_broker_llm_runtime_retired",
        )
        metrics.observe("broker.narration_latency_ms", latency_ms, {"provider": telemetry.provider})
        metrics.increment("broker.narration_generation", {"provider": telemetry.provider, "used_llm": False})
        return BrokerNarrationResult(response=response, telemetry=telemetry)

    @staticmethod
    def _emit_safe_progress_chunks(
        *,
        context: BrokerContext,
        plan: BrokerReasoningPlan,
        on_chunk: Callable[[str, dict], None] | None,
    ) -> None:
        if on_chunk is None:
            return
        chunks = [
            (
                "Deterministic evidence context is locked for broker narration. ",
                {"phase": "context_locked", "evidence_count": len(context.evidence)},
            ),
            (
                "Narration is constrained to authoritative valuation, comparable, district, and confidence fields. ",
                {"phase": "governance_constraints", "checks": plan.governance_checks},
            ),
        ]
        for text, payload in chunks:
            on_chunk(text, payload)


deterministic_narration_runtime = DeterministicBrokerNarrationRuntime(formatter=response_formatter)
