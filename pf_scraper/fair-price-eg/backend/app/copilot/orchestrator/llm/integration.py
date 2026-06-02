from __future__ import annotations

from copy import deepcopy
import hashlib
import time
from typing import Any, Iterable

from app.copilot.orchestrator.composer import ComposedResponse
from app.copilot.orchestrator.intents import Intent
from app.copilot.orchestrator.llm.contracts import (
    GroundingDecision,
    NarrationAdmissionState,
    NarrationResult,
    NarrationScope,
    NarrationStatus,
)
from app.copilot.orchestrator.llm.gate import NarrationAdmissionGate
from app.copilot.orchestrator.llm.grounding import DeterministicGroundingLayer, grounding_layer
from app.copilot.orchestrator.llm.parser import CandidateParser, CandidateParserError
from app.copilot.orchestrator.llm.prompts import PromptAssembler, PromptAssemblyError
from app.copilot.orchestrator.llm.provider import (
    GeminiStatelessProviderAdapter,
    NarrationProvider,
    ProviderTransportError,
)
from app.copilot.orchestrator.memory import MemoryContext
from app.core.config import settings


class CopilotOrchestratorLLMV1:
    """Single authorized Phase 5.5C.6 narration pipeline."""

    def __init__(
        self,
        *,
        provider: NarrationProvider | None,
        enabled_intents: Iterable[Intent],
        admission_gate: NarrationAdmissionGate | None = None,
        prompt_assembler: PromptAssembler | None = None,
        candidate_parser: CandidateParser | None = None,
        grounding: DeterministicGroundingLayer | None = None,
    ) -> None:
        self.provider = provider
        self.admission_gate = admission_gate or NarrationAdmissionGate(enabled_intents=enabled_intents)
        self.prompt_assembler = prompt_assembler or PromptAssembler()
        self.candidate_parser = candidate_parser or CandidateParser()
        self.grounding = grounding or grounding_layer

    def narrate(
        self,
        *,
        scope: NarrationScope,
        user_message: str,
        composed_response: ComposedResponse,
        memory_context: MemoryContext,
    ) -> NarrationResult:
        start = time.perf_counter()
        admission = self.admission_gate.evaluate(
            scope=scope,
            composed_response=composed_response,
            memory_context=memory_context,
            user_message=user_message,
        )
        if admission.state != NarrationAdmissionState.ADMIT_NARRATION or admission.envelope is None:
            return self._fallback(
                composed_response=composed_response,
                status=NarrationStatus(admission.state.value),
                reason_codes=admission.reason_codes,
                start=start,
                extra={"admission_state": admission.state.value, "provider_called": False},
            )
        envelope = admission.envelope
        if self.provider is None:
            return self._fallback(
                composed_response=composed_response,
                status=NarrationStatus.DETERMINISTIC_ONLY,
                reason_codes=("PROVIDER_NOT_CONFIGURED",),
                start=start,
                extra={"admission_state": admission.state.value, "provider_called": False},
            )

        try:
            prompt = self.prompt_assembler.build(envelope)
        except PromptAssemblyError as exc:
            return self._fallback(
                composed_response=composed_response,
                status=NarrationStatus.REJECT_NARRATION,
                reason_codes=(str(exc),),
                start=start,
                extra={"admission_state": admission.state.value, "provider_called": False},
            )

        try:
            provider_response = self.provider.generate(prompt)
        except ProviderTransportError as exc:
            return self._fallback(
                composed_response=composed_response,
                status=NarrationStatus.REJECT_NARRATION,
                reason_codes=(str(exc),),
                start=start,
                extra=self._transport_metadata(prompt=prompt, provider_called=True),
            )
        except Exception as exc:
            return self._fallback(
                composed_response=composed_response,
                status=NarrationStatus.REJECT_NARRATION,
                reason_codes=(f"PROVIDER_TRANSPORT_FAILURE:{type(exc).__name__}",),
                start=start,
                extra=self._transport_metadata(prompt=prompt, provider_called=True),
            )

        try:
            candidate = self.candidate_parser.parse(provider_response)
        except CandidateParserError as exc:
            return self._fallback(
                composed_response=composed_response,
                status=NarrationStatus.REJECT_NARRATION,
                reason_codes=(str(exc),),
                start=start,
                extra={
                    **self._transport_metadata(prompt=prompt, provider_called=True),
                    "provider": provider_response.provider,
                    "model": provider_response.model,
                    "provider_latency_ms": provider_response.latency_ms,
                    "provider_response_bytes": provider_response.response_bytes,
                },
            )

        grounding = self.grounding.validate(
            candidate=candidate,
            envelope=envelope,
            assembly_metadata=prompt.metadata,
        )
        telemetry = {
            **self._transport_metadata(prompt=prompt, provider_called=True),
            "provider": provider_response.provider,
            "model": provider_response.model,
            "provider_latency_ms": provider_response.latency_ms,
            "provider_response_bytes": provider_response.response_bytes,
            "token_usage": deepcopy(provider_response.token_usage),
            "grounding_decision": grounding.decision.value,
            "grounding_reason_codes": list(grounding.reason_codes),
            "checked_policy_versions": deepcopy(grounding.checked_policy_versions),
            "checked_citation_count": grounding.checked_citation_count,
            "latency_ms": round((time.perf_counter() - start) * 1000, 3),
        }
        if grounding.decision == GroundingDecision.ACCEPT_NARRATION:
            return NarrationResult(
                response_id=self._response_id(composed_response.response_id, envelope.binding_attestation),
                status=NarrationStatus.ACCEPT_NARRATION,
                narrated_text=candidate.narration_text,
                deterministic_fallback_payload=None,
                citation_package=deepcopy(composed_response.citation_package),
                telemetry=telemetry,
            )
        return self._fallback(
            composed_response=composed_response,
            status=NarrationStatus(grounding.decision.value),
            reason_codes=grounding.reason_codes,
            start=start,
            extra=telemetry,
        )

    @staticmethod
    def _response_id(composed_response_id: str, binding_attestation: str) -> str:
        digest = hashlib.sha256(f"{composed_response_id}:{binding_attestation}".encode("utf-8")).hexdigest()
        return f"narration_{digest}"

    @staticmethod
    def _transport_metadata(*, prompt, provider_called: bool) -> dict[str, Any]:
        return {
            "provider_called": provider_called,
            "request_token_estimate": prompt.token_count_estimate,
            "max_output_tokens": prompt.max_output_tokens,
            "assembly_policy_version": prompt.metadata.assembly_policy_version,
            "serializer_version": prompt.metadata.serializer_version,
            "tokenizer_version": prompt.metadata.tokenizer_version,
            "provider_profile_id": prompt.metadata.provider_profile_id,
            "included_segment_count": len(prompt.metadata.included_segment_ids),
            "evicted_optional_segment_count": len(prompt.metadata.evicted_optional_segment_ids),
        }

    @staticmethod
    def _fallback(
        *,
        composed_response: ComposedResponse,
        status: NarrationStatus,
        reason_codes: tuple[str, ...],
        start: float,
        extra: dict[str, Any],
    ) -> NarrationResult:
        access_denied = status == NarrationStatus.ACCESS_DENIED
        telemetry = {
            **deepcopy(extra),
            "reason_codes": list(reason_codes),
            "latency_ms": round((time.perf_counter() - start) * 1000, 3),
        }
        return NarrationResult(
            response_id=f"narration_{composed_response.response_id}",
            status=status,
            narrated_text=None,
            deterministic_fallback_payload=None if access_denied else deepcopy(composed_response.frontend_payload),
            citation_package=None if access_denied else deepcopy(composed_response.citation_package),
            telemetry=telemetry,
        )


def build_copilot_orchestrator_llm_v1() -> CopilotOrchestratorLLMV1:
    enabled_intents = tuple(Intent(value) for value in settings.COPILOT_NARRATION_INTENTS)
    provider = None
    if settings.COPILOT_NARRATION_ENABLED:
        provider = GeminiStatelessProviderAdapter(api_key=settings.COPILOT_GEMINI_API_KEY or "")
    return CopilotOrchestratorLLMV1(provider=provider, enabled_intents=enabled_intents)
