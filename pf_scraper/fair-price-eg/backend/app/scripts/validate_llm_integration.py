from __future__ import annotations

import hashlib
import json
from pathlib import Path
import time

from app.copilot.orchestrator.composer import ComposedResponse, CompositionStatus
from app.copilot.orchestrator.intents import Intent
from app.copilot.orchestrator.llm import (
    CopilotOrchestratorLLMV1,
    NarrationAdmissionGate,
    NarrationScope,
    NarrationStatus,
    PromptAssembler,
    ProviderTransportResponse,
)
from app.copilot.orchestrator.llm.policy import PROVIDER_MODEL
from app.copilot.orchestrator.memory import MemoryContext, MemoryStatus


VALUATION_ID = "val_docker_validation_001"
FAIR_PRICE_FACT = "composer.evidence.tool_summaries.0.summary.fair_price"


def _composed() -> ComposedResponse:
    citations = {
        "valuation_ids": [VALUATION_ID],
        "tool_event_ids": [],
        "comparable_ids": [],
        "unavailable_optional_citation_types": ["tool_event_id", "comparable_id"],
    }
    compressed_context = {
        "schema_version": "1.0",
        "composition_status": "SUCCESS",
        "intent": {"primary": "VALUATION", "secondary": []},
        "evidence": {
            "tool_summaries": [
                {
                    "planned_tool": "VALUATION_TOOL",
                    "tool_name": "valuation",
                    "status": "SUCCESS",
                    "summary": {
                        "valuation_id": VALUATION_ID,
                        "fair_price": 1_200_000,
                        "confidence_level": "High",
                        "source": "TruthLayer",
                    },
                }
            ],
            "property_comparison": None,
            "sparse_evidence": [],
            "evidence_conflicts": [],
        },
        "failures": [],
        "compression_disclosures": [],
    }
    return ComposedResponse(
        response_id="response_docker_validation",
        execution_id="execution_docker_validation",
        plan_id="plan_docker_validation",
        primary_intent=Intent.VALUATION,
        secondary_intents=(),
        status=CompositionStatus.SUCCESS,
        evidence_summary={},
        citation_package=citations,
        compressed_context=compressed_context,
        frontend_payload={"composition_status": "SUCCESS", "citations": citations},
        composer_metadata={"composer_mode": "DETERMINISTIC_ONLY"},
    )


def _memory(*, workspace_id: int = 10) -> MemoryContext:
    return MemoryContext(
        memory_id="memory_docker_validation",
        status=MemoryStatus.SUCCESS,
        workspace_context={"workspace_id": workspace_id, "name": "Docker workspace"},
        scenario_context={
            "current": {"scenario_id": 20, "name": "Docker scenario"},
            "lineage": [],
            "lineage_truncated": False,
        },
        broker_session_context=None,
        recent_tool_history=(),
        recent_decisions=(),
        recent_valuations=(),
        active_assumptions=(),
        active_comparison_context=None,
        recent_conversation_metadata=(),
        citation_package={
            "workspace_id": workspace_id,
            "scenario_id": 20,
            "valuation_ids": [VALUATION_ID],
            "tool_event_ids": [],
            "comparable_ids": [],
        },
        memory_metadata={},
    )


def _candidate_body(
    *,
    value: int = 1_200_000,
    citation: str = VALUATION_ID,
    narration_text: str | None = None,
) -> str:
    text = narration_text or f"The approved upstream fact {FAIR_PRICE_FACT} is {value} [citation:{citation}]."
    candidate = {"narration_text": text, "citation_references": [citation]}
    return json.dumps(
        {"candidates": [{"content": {"parts": [{"text": json.dumps(candidate, separators=(",", ":"))}]}}]},
        separators=(",", ":"),
    )


class MockProvider:
    name = "mock_gemini"
    model = PROVIDER_MODEL

    def __init__(self, body: str) -> None:
        self.body = body
        self.calls = 0

    def generate(self, prompt) -> ProviderTransportResponse:
        self.calls += 1
        return ProviderTransportResponse(
            provider=self.name,
            model=self.model,
            original_response_body=self.body,
            latency_ms=0.5,
            response_bytes=len(self.body.encode("utf-8")),
            token_usage={},
        )


class RaisingProvider:
    name = "raising_provider"
    model = PROVIDER_MODEL

    def __init__(self) -> None:
        self.calls = 0

    def generate(self, prompt):
        self.calls += 1
        raise RuntimeError("offline")


def _runtime(provider) -> CopilotOrchestratorLLMV1:
    return CopilotOrchestratorLLMV1(provider=provider, enabled_intents=(Intent.VALUATION,))


def _source_boundary() -> dict[str, object]:
    app_root = Path(__file__).resolve().parents[1]
    modern_root = app_root / "copilot" / "orchestrator" / "llm"
    legacy_root = app_root / "broker" / "llm"
    forbidden_references = []
    for path in sorted(modern_root.glob("*.py")):
        text = path.read_text(encoding="utf-8").casefold()
        for term in ("sqlalchemy", "app.models", "app.services", "app.db", "openairesponsesprovider"):
            if term in text:
                forbidden_references.append(f"{path.name}:{term}")
    return {
        "legacy_python_files": [str(path) for path in legacy_root.rglob("*.py")],
        "forbidden_modern_references": forbidden_references,
    }


def main() -> None:
    composed = _composed()
    memory = _memory()
    scope = NarrationScope(user_id=1, workspace_id=10, scenario_id=20)

    provider = MockProvider(_candidate_body())
    accepted = _runtime(provider).narrate(
        scope=scope,
        user_message="What is the approved valuation?",
        composed_response=composed,
        memory_context=memory,
    )

    denied_provider = MockProvider(_candidate_body())
    denied = _runtime(denied_provider).narrate(
        scope=NarrationScope(user_id=1, workspace_id=99, scenario_id=20),
        user_message="Value?",
        composed_response=composed,
        memory_context=memory,
    )

    citation_provider = MockProvider(_candidate_body(citation="val_fabricated"))
    citation_rejected = _runtime(citation_provider).narrate(
        scope=scope,
        user_message="Value?",
        composed_response=composed,
        memory_context=memory,
    )

    value_provider = MockProvider(_candidate_body(value=999_999))
    value_rejected = _runtime(value_provider).narrate(
        scope=scope,
        user_message="Value?",
        composed_response=composed,
        memory_context=memory,
    )

    prediction_provider = MockProvider(
        _candidate_body(narration_text=f"The property should rise next year [citation:{VALUATION_ID}].")
    )
    prediction_rejected = _runtime(prediction_provider).narrate(
        scope=scope,
        user_message="Value?",
        composed_response=composed,
        memory_context=memory,
    )

    raising_provider = RaisingProvider()
    transport_rejected = _runtime(raising_provider).narrate(
        scope=scope,
        user_message="Value?",
        composed_response=composed,
        memory_context=memory,
    )

    admission = NarrationAdmissionGate(enabled_intents=(Intent.VALUATION,)).evaluate(
        scope=scope,
        composed_response=composed,
        memory_context=memory,
        user_message="Value?",
    )
    assert admission.envelope is not None
    assembler = PromptAssembler()
    started = time.perf_counter()
    bundles = [assembler.build(admission.envelope) for _ in range(1000)]
    average_overhead_ms = ((time.perf_counter() - started) * 1000) / len(bundles)
    fingerprint = hashlib.sha256(
        f"{bundles[0].instructions}:{bundles[0].input_text}".encode("utf-8")
    ).hexdigest()
    source_boundary = _source_boundary()

    result = {
        "authorized_runtime": "COPILOT_ORCHESTRATOR_LLM_V1",
        "target_runtime_count": 1,
        "legacy_python_file_count": len(source_boundary["legacy_python_files"]),
        "forbidden_modern_reference_count": len(source_boundary["forbidden_modern_references"]),
        "accepted_status": accepted.status.value,
        "accepted_provider_calls": provider.calls,
        "citations_verified": accepted.citation_package == composed.citation_package,
        "grounding_status": accepted.telemetry.get("grounding_decision"),
        "tenant_isolation_status": denied.status.value,
        "tenant_isolation_provider_calls": denied_provider.calls,
        "citation_rejection_status": citation_rejected.status.value,
        "citation_rejection_provider_calls": citation_provider.calls,
        "fake_value_rejection_status": value_rejected.status.value,
        "fake_value_rejection_provider_calls": value_provider.calls,
        "fake_prediction_rejection_status": prediction_rejected.status.value,
        "fake_prediction_rejection_provider_calls": prediction_provider.calls,
        "fail_closed_transport_status": transport_rejected.status.value,
        "fail_closed_transport_calls": raising_provider.calls,
        "deterministic_assembly": all(bundle == bundles[0] for bundle in bundles),
        "assembly_fingerprint": fingerprint,
        "prompt_assembly_overhead_ms": round(average_overhead_ms, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    failures = [
        result["target_runtime_count"] != 1,
        result["legacy_python_file_count"] != 0,
        result["forbidden_modern_reference_count"] != 0,
        result["accepted_status"] != "ACCEPT_NARRATION",
        result["accepted_provider_calls"] != 1,
        not result["citations_verified"],
        result["grounding_status"] != "ACCEPT_NARRATION",
        result["tenant_isolation_status"] != "ACCESS_DENIED",
        result["tenant_isolation_provider_calls"] != 0,
        result["citation_rejection_status"] != "REJECT_NARRATION",
        result["citation_rejection_provider_calls"] != 1,
        result["fake_value_rejection_status"] != "REJECT_NARRATION",
        result["fake_value_rejection_provider_calls"] != 1,
        result["fake_prediction_rejection_status"] != "REJECT_NARRATION",
        result["fake_prediction_rejection_provider_calls"] != 1,
        result["fail_closed_transport_status"] != "REJECT_NARRATION",
        result["fail_closed_transport_calls"] != 1,
        not result["deterministic_assembly"],
        average_overhead_ms >= 10.0,
    ]
    if any(failures):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
