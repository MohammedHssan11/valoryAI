from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from app.copilot.orchestrator.composer import ComposedResponse, CompositionStatus
from app.copilot.orchestrator.intents import Intent
from app.copilot.orchestrator.llm import (
    CandidateParser,
    CandidateParserError,
    CopilotOrchestratorLLMV1,
    DeterministicGroundingLayer,
    GeminiStatelessProviderAdapter,
    GroundingDecision,
    NarrationAdmissionGate,
    NarrationScope,
    NarrationStatus,
    PromptAssembler,
    ProjectionSegment,
    ProviderTransportResponse,
)
from app.copilot.orchestrator.llm.policy import (
    MAX_RESPONSE_TOKENS,
    PROVIDER_ENDPOINT,
    PROVIDER_MODEL,
)
from app.copilot.orchestrator.memory import MemoryContext, MemoryStatus


VALUATION_ID = "val_fixture_001"
FAIR_PRICE_FACT = "composer.evidence.tool_summaries.0.summary.fair_price"


def _composed(
    *,
    intent: Intent = Intent.VALUATION,
    secondary_intents: tuple[Intent, ...] = (),
    status: CompositionStatus = CompositionStatus.SUCCESS,
    valuation_id: str = VALUATION_ID,
) -> ComposedResponse:
    citations = {
        "valuation_ids": [valuation_id],
        "tool_event_ids": [],
        "comparable_ids": [],
        "unavailable_optional_citation_types": ["tool_event_id", "comparable_id"],
    }
    compressed_context = {
        "schema_version": "1.0",
        "composition_status": status.value,
        "intent": {
            "primary": intent.value,
            "secondary": [item.value for item in secondary_intents],
        },
        "evidence": {
            "tool_summaries": [
                {
                    "planned_tool": "VALUATION_TOOL",
                    "tool_name": "valuation",
                    "status": "SUCCESS",
                    "summary": {
                        "valuation_id": valuation_id,
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
        response_id="response_fixture",
        execution_id="execution_fixture",
        plan_id="plan_fixture",
        primary_intent=intent,
        secondary_intents=secondary_intents,
        status=status,
        evidence_summary={},
        citation_package=citations,
        compressed_context=compressed_context,
        frontend_payload={"composition_status": status.value, "citations": citations},
        composer_metadata={"composer_mode": "DETERMINISTIC_ONLY"},
    )


def _memory(
    *,
    workspace_id: int = 10,
    scenario_id: int = 20,
    status: MemoryStatus = MemoryStatus.SUCCESS,
    valuation_id: str = VALUATION_ID,
) -> MemoryContext:
    citation_package = {
        "workspace_id": workspace_id,
        "scenario_id": scenario_id,
        "valuation_ids": [valuation_id],
        "tool_event_ids": [],
        "comparable_ids": [],
    }
    return MemoryContext(
        memory_id="memory_fixture",
        status=status,
        workspace_context={"workspace_id": workspace_id, "name": "Workspace"},
        scenario_context={
            "current": {"scenario_id": scenario_id, "name": "Scenario"},
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
        citation_package=citation_package,
        memory_metadata={},
    )


def _scope(*, workspace_id: int = 10, scenario_id: int = 20) -> NarrationScope:
    return NarrationScope(user_id=1, workspace_id=workspace_id, scenario_id=scenario_id)


def _candidate_body(
    *,
    narration_text: str | None = None,
    citations: list[str] | None = None,
    extra_candidate_field: bool = False,
) -> str:
    candidate = {
        "narration_text": narration_text
        or f"The approved upstream fact {FAIR_PRICE_FACT} is 1200000 [citation:{VALUATION_ID}].",
        "citation_references": citations if citations is not None else [VALUATION_ID],
    }
    if extra_candidate_field:
        candidate["authoritative_values"] = {"fair_price": 1_200_000}
    return json.dumps(
        {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": json.dumps(candidate, ensure_ascii=True, separators=(",", ":"))}]
                    }
                }
            ],
            "usageMetadata": {"promptTokenCount": 100, "candidatesTokenCount": 30},
        },
        ensure_ascii=True,
        separators=(",", ":"),
    )


class MockProvider:
    name = "mock_gemini"
    model = PROVIDER_MODEL

    def __init__(self, response_body: str | None = None) -> None:
        self.response_body = response_body or _candidate_body()
        self.calls = 0
        self.last_prompt = None

    def generate(self, prompt):
        self.calls += 1
        self.last_prompt = prompt
        return ProviderTransportResponse(
            provider=self.name,
            model=self.model,
            original_response_body=self.response_body,
            latency_ms=1.0,
            response_bytes=len(self.response_body.encode("utf-8")),
            token_usage={"promptTokenCount": 100, "candidatesTokenCount": 30},
        )


class RaisingProvider:
    name = "raising_provider"
    model = PROVIDER_MODEL

    def __init__(self) -> None:
        self.calls = 0

    def generate(self, prompt):
        self.calls += 1
        raise RuntimeError("transport unavailable")


def _runtime(provider) -> CopilotOrchestratorLLMV1:
    return CopilotOrchestratorLLMV1(provider=provider, enabled_intents=(Intent.VALUATION,))


def test_end_to_end_accepts_exact_grounded_candidate():
    provider = MockProvider()
    result = _runtime(provider).narrate(
        scope=_scope(),
        user_message="What is the approved valuation?",
        composed_response=_composed(),
        memory_context=_memory(),
    )

    assert provider.calls == 1
    assert result.status == NarrationStatus.ACCEPT_NARRATION
    assert result.narrated_text == (
        f"The approved upstream fact {FAIR_PRICE_FACT} is 1200000 [citation:{VALUATION_ID}]."
    )
    assert result.deterministic_fallback_payload is None
    assert result.citation_package == _composed().citation_package
    assert result.telemetry["grounding_decision"] == "ACCEPT_NARRATION"


def test_cross_workspace_binding_fails_closed_before_provider_contact():
    provider = MockProvider()
    result = _runtime(provider).narrate(
        scope=_scope(workspace_id=99),
        user_message="Value?",
        composed_response=_composed(),
        memory_context=_memory(workspace_id=10),
    )

    assert provider.calls == 0
    assert result.status == NarrationStatus.ACCESS_DENIED
    assert result.narrated_text is None
    assert result.deterministic_fallback_payload is None
    assert result.citation_package is None


def test_general_question_and_multi_intent_remain_deterministic_only():
    provider = MockProvider()
    general = _runtime(provider).narrate(
        scope=_scope(),
        user_message="Hello",
        composed_response=_composed(intent=Intent.GENERAL_QUESTION),
        memory_context=_memory(),
    )
    multi = _runtime(provider).narrate(
        scope=_scope(),
        user_message="Value and insight?",
        composed_response=_composed(secondary_intents=(Intent.MARKET_INSIGHT,)),
        memory_context=_memory(),
    )

    assert provider.calls == 0
    assert general.status == NarrationStatus.DETERMINISTIC_ONLY
    assert multi.status == NarrationStatus.DETERMINISTIC_ONLY
    assert general.deterministic_fallback_payload is not None


@pytest.mark.parametrize(
    ("body", "reason"),
    [
        (
            _candidate_body(
                narration_text=f"The approved upstream fact {FAIR_PRICE_FACT} is 999999 [citation:{VALUATION_ID}]."
            ),
            "UNGROUNDED_VALUE",
        ),
        (
            _candidate_body(
                narration_text=f"The approved upstream fact {FAIR_PRICE_FACT} is 1200000 [citation:val_fabricated].",
                citations=["val_fabricated"],
            ),
            "CITATION_MISMATCH",
        ),
        (
            _candidate_body(narration_text=f"The property should rise next year [citation:{VALUATION_ID}]."),
            "AMBIGUOUS_VALIDATION",
        ),
    ],
)
def test_grounding_rejects_original_candidate_without_repair(body: str, reason: str):
    provider = MockProvider(body)
    result = _runtime(provider).narrate(
        scope=_scope(),
        user_message="Value?",
        composed_response=_composed(),
        memory_context=_memory(),
    )

    assert provider.calls == 1
    assert result.status == NarrationStatus.REJECT_NARRATION
    assert result.narrated_text is None
    assert result.deterministic_fallback_payload is not None
    assert reason in result.telemetry["reason_codes"]


def test_candidate_parser_rejects_unknown_fields_without_repair():
    parser = CandidateParser()
    body = _candidate_body(extra_candidate_field=True)
    with pytest.raises(CandidateParserError, match="INVALID_CANDIDATE_SCHEMA"):
        parser.parse(
            ProviderTransportResponse(
                provider="mock",
                model=PROVIDER_MODEL,
                original_response_body=body,
                latency_ms=1.0,
                response_bytes=len(body),
            )
        )


def test_provider_failure_is_not_retried():
    provider = RaisingProvider()
    result = _runtime(provider).narrate(
        scope=_scope(),
        user_message="Value?",
        composed_response=_composed(),
        memory_context=_memory(),
    )

    assert provider.calls == 1
    assert result.status == NarrationStatus.REJECT_NARRATION
    assert result.deterministic_fallback_payload is not None
    assert result.telemetry["provider_called"] is True


def test_prompt_assembly_is_deterministic_and_evicts_optional_segments():
    gate = NarrationAdmissionGate(enabled_intents=(Intent.VALUATION,))
    admission = gate.evaluate(
        scope=_scope(),
        composed_response=_composed(),
        memory_context=_memory(),
        user_message="Value?",
    )
    assert admission.envelope is not None
    optional = tuple(
        ProjectionSegment(
            segment_id=f"memory_summary.{index:04d}",
            segment_class="memory_summary",
            protected=False,
            content={"summary": "x" * 20_000},
        )
        for index in range(3)
    )
    envelope = replace(
        admission.envelope,
        provider_safe_projection=(*admission.envelope.provider_safe_projection, *optional),
    )

    first = PromptAssembler().build(envelope)
    second = PromptAssembler().build(envelope)

    assert first == second
    assert first.metadata.evicted_optional_segment_ids
    assert first.metadata.evicted_optional_segment_ids[0] == "memory_summary.0002"
    assert first.token_count_estimate + first.metadata.response_reserve_tokens <= 12_000
    assert "workspace_id" not in first.input_text
    assert "scenario_id" not in first.input_text


def test_grounding_is_deterministic():
    gate = NarrationAdmissionGate(enabled_intents=(Intent.VALUATION,))
    envelope = gate.evaluate(
        scope=_scope(),
        composed_response=_composed(),
        memory_context=_memory(),
        user_message="Value?",
    ).envelope
    assert envelope is not None
    prompt = PromptAssembler().build(envelope)
    candidate = CandidateParser().parse(
        ProviderTransportResponse(
            provider="mock",
            model=PROVIDER_MODEL,
            original_response_body=_candidate_body(),
            latency_ms=1.0,
            response_bytes=1,
        )
    )

    first = DeterministicGroundingLayer().validate(
        candidate=candidate,
        envelope=envelope,
        assembly_metadata=prompt.metadata,
    )
    second = DeterministicGroundingLayer().validate(
        candidate=candidate,
        envelope=envelope,
        assembly_metadata=prompt.metadata,
    )

    assert first == second
    assert first.decision == GroundingDecision.ACCEPT_NARRATION


def test_gemini_adapter_uses_one_stateless_tool_free_request(monkeypatch):
    gate = NarrationAdmissionGate(enabled_intents=(Intent.VALUATION,))
    envelope = gate.evaluate(
        scope=_scope(),
        composed_response=_composed(),
        memory_context=_memory(),
        user_message="Value?",
    ).envelope
    assert envelope is not None
    prompt = PromptAssembler().build(envelope)
    captured = {"calls": 0}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def read(self, limit):
            return _candidate_body().encode("utf-8")

    def fake_urlopen(req, timeout):
        captured["calls"] += 1
        captured["url"] = req.full_url
        captured["timeout"] = timeout
        captured["payload"] = json.loads(req.data.decode("utf-8"))
        return Response()

    monkeypatch.setattr("app.copilot.orchestrator.llm.provider.request.urlopen", fake_urlopen)
    result = GeminiStatelessProviderAdapter(api_key="test-key").generate(prompt)

    assert captured["calls"] == 1
    assert captured["url"] == PROVIDER_ENDPOINT
    assert captured["payload"]["generationConfig"]["maxOutputTokens"] == MAX_RESPONSE_TOKENS
    assert "tools" not in captured["payload"]
    assert "toolConfig" not in captured["payload"]
    assert "cachedContent" not in captured["payload"]
    assert result.model == PROVIDER_MODEL


def test_legacy_and_rejected_provider_paths_are_absent():
    app_root = Path(__file__).resolve().parents[1]
    broker_llm = app_root / "broker" / "llm"
    config_source = (app_root / "core" / "config.py").read_text(encoding="utf-8")
    orchestrator_source = (app_root / "broker" / "orchestrator" / "core.py").read_text(encoding="utf-8")

    assert not list(broker_llm.rglob("*.py"))
    assert "BROKER_LLM_" not in config_source
    assert "app.broker.llm" not in orchestrator_source
