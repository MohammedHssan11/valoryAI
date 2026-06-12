from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

from app.copilot.orchestrator.composer import ComposedResponse, CompositionStatus
from app.copilot.orchestrator.intents import Intent
from app.copilot.orchestrator.llm.contracts import (
    AdmissionResult,
    GroundingManifest,
    NarrationAdmissionState,
    NarrationScope,
    ProjectionFact,
    ProjectionSegment,
    ScopedNarrationEnvelope,
)
from app.copilot.orchestrator.llm.policy import (
    APPROVED_INTENTS,
    CITATION_TOKEN_PATTERN,
    CONTRACT_IDS,
    CONTRACT_VERSION,
    FORBIDDEN_PROVIDER_VISIBLE_KEYS,
    MAX_CITATIONS,
    MAX_CURRENT_TURN_CHARACTERS,
    MAX_PROJECTION_FACTS,
    PROHIBITED_CLAIMS_POLICY_VERSION,
)
from app.copilot.orchestrator.memory import MemoryContext, MemoryStatus


_ALLOWED_COMPOSER_CITATION_KEYS = frozenset(
    {
        "valuation_ids",
        "tool_event_ids",
        "comparable_ids",
        "unavailable_optional_citation_types",
    }
)
_CITATION_KEYS = ("valuation_ids", "tool_event_ids", "comparable_ids")


class AdmissionGateError(ValueError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def _unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


class NarrationAdmissionGate:
    """Deterministic no-I/O policy firewall before provider egress."""

    def __init__(self, *, enabled_intents: Iterable[Intent]) -> None:
        self.enabled_intents = frozenset(enabled_intents)
        if not self.enabled_intents.issubset(APPROVED_INTENTS):
            raise ValueError("Narration activation contains an unapproved intent")

    def evaluate(
        self,
        *,
        scope: NarrationScope,
        composed_response: ComposedResponse,
        memory_context: MemoryContext,
        user_message: str,
    ) -> AdmissionResult:
        if not isinstance(scope, NarrationScope) or scope.user_id <= 0 or scope.workspace_id <= 0:
            return self._result(NarrationAdmissionState.ACCESS_DENIED, "INVALID_INTERNAL_SCOPE")
        if not isinstance(composed_response, ComposedResponse) or not isinstance(memory_context, MemoryContext):
            return self._result(NarrationAdmissionState.REJECT_NARRATION, "INVALID_UPSTREAM_ARTIFACT")
        if memory_context.status == MemoryStatus.ACCESS_DENIED:
            return self._result(NarrationAdmissionState.ACCESS_DENIED, "MEMORY_ACCESS_DENIED")
        if memory_context.status == MemoryStatus.FAILED:
            return self._result(NarrationAdmissionState.REJECT_NARRATION, "MEMORY_FAILED")
        binding_error = self._scope_binding_error(scope=scope, memory_context=memory_context)
        if binding_error is not None:
            return self._result(NarrationAdmissionState.ACCESS_DENIED, binding_error)
        if composed_response.status == CompositionStatus.CLARIFICATION_REQUIRED:
            return self._result(NarrationAdmissionState.DETERMINISTIC_ONLY, "CLARIFICATION_REQUIRED")
        if composed_response.status == CompositionStatus.FAILED:
            return self._result(NarrationAdmissionState.REJECT_NARRATION, "COMPOSITION_FAILED")
        if composed_response.primary_intent == Intent.GENERAL_QUESTION:
            return self._result(NarrationAdmissionState.DETERMINISTIC_ONLY, "GENERAL_QUESTION")
        if composed_response.secondary_intents:
            return self._result(NarrationAdmissionState.DETERMINISTIC_ONLY, "MULTI_INTENT_NOT_APPROVED")
        if composed_response.primary_intent not in APPROVED_INTENTS:
            return self._result(NarrationAdmissionState.DETERMINISTIC_ONLY, "UNSUPPORTED_INTENT")
        if composed_response.primary_intent not in self.enabled_intents:
            return self._result(NarrationAdmissionState.DETERMINISTIC_ONLY, "INTENT_NOT_ACTIVATED")
        if not isinstance(user_message, str) or not user_message or len(user_message) > MAX_CURRENT_TURN_CHARACTERS:
            return self._result(NarrationAdmissionState.REJECT_NARRATION, "CURRENT_TURN_OUT_OF_BOUNDS")

        try:
            citation_tokens = self._composer_citations(composed_response.citation_package)
            self._validate_memory_citation_binding(
                memory_context=memory_context,
                citation_tokens=citation_tokens,
            )
            flattened_citations = tuple(token for key in _CITATION_KEYS for token in citation_tokens[key])
            if not flattened_citations:
                raise AdmissionGateError("GROUNDING_CITATIONS_UNAVAILABLE")
            facts = self._composer_facts(
                composed_response=composed_response,
                citation_tokens=citation_tokens,
            )
            if not facts:
                raise AdmissionGateError("GROUNDING_FACTS_UNAVAILABLE")
            required_disclosures = self._required_disclosures(composed_response, facts)
            binding_attestation = self._binding_attestation(
                scope=scope,
                composed_response=composed_response,
                memory_context=memory_context,
                citation_tokens=citation_tokens,
            )
            contract_id = CONTRACT_IDS[composed_response.primary_intent]
            segments = self._segments(
                intent=composed_response.primary_intent,
                contract_id=contract_id,
                user_message=user_message,
                facts=facts,
                required_disclosures=required_disclosures,
                citation_tokens=citation_tokens,
            )
            for segment in segments:
                self._ensure_provider_safe(segment.content)
            manifest = GroundingManifest(
                binding_attestation=binding_attestation,
                contract_id=contract_id,
                contract_version=CONTRACT_VERSION,
                prohibited_claims_policy_version=PROHIBITED_CLAIMS_POLICY_VERSION,
                facts=facts,
                citation_tokens=citation_tokens,
                required_disclosure_fact_ids=required_disclosures,
            )
            envelope = ScopedNarrationEnvelope(
                admission_state=NarrationAdmissionState.ADMIT_NARRATION,
                intent=composed_response.primary_intent,
                binding_attestation=binding_attestation,
                provider_safe_projection=segments,
                grounding_manifest=manifest,
            )
            return AdmissionResult(
                state=NarrationAdmissionState.ADMIT_NARRATION,
                reason_codes=(),
                envelope=envelope,
            )
        except AdmissionGateError as exc:
            return self._result(NarrationAdmissionState.REJECT_NARRATION, str(exc))

    @staticmethod
    def _result(state: NarrationAdmissionState, reason: str) -> AdmissionResult:
        return AdmissionResult(state=state, reason_codes=(reason,))

    @staticmethod
    def _scope_binding_error(*, scope: NarrationScope, memory_context: MemoryContext) -> str | None:
        workspace_id = memory_context.workspace_context.get("workspace_id")
        memory_citation_workspace = memory_context.citation_package.get("workspace_id")
        if workspace_id != scope.workspace_id or memory_citation_workspace != scope.workspace_id:
            return "WORKSPACE_BINDING_MISMATCH"

        scenario_context = memory_context.scenario_context
        memory_citation_scenario = memory_context.citation_package.get("scenario_id")
        if scope.scenario_id is None:
            if scenario_context is not None or memory_citation_scenario is not None:
                return "SCENARIO_BINDING_MISMATCH"
        else:
            current = scenario_context.get("current") if isinstance(scenario_context, dict) else None
            if not isinstance(current, dict) or current.get("scenario_id") != scope.scenario_id:
                return "SCENARIO_BINDING_MISMATCH"
            if memory_citation_scenario != scope.scenario_id:
                return "SCENARIO_CITATION_BINDING_MISMATCH"

        broker_context = memory_context.broker_session_context
        if scope.broker_session_id is not None:
            if not isinstance(broker_context, dict):
                return "BROKER_SESSION_BINDING_MISMATCH"
            if broker_context.get("session_id") != scope.broker_session_id:
                return "BROKER_SESSION_BINDING_MISMATCH"
            if broker_context.get("workspace_id") != scope.workspace_id:
                return "BROKER_SESSION_WORKSPACE_MISMATCH"
            if broker_context.get("scenario_id") != scope.scenario_id:
                return "BROKER_SESSION_SCENARIO_MISMATCH"
        return None

    @staticmethod
    def _composer_citations(package: dict[str, Any]) -> dict[str, tuple[str, ...]]:
        if not isinstance(package, dict) or set(package) - _ALLOWED_COMPOSER_CITATION_KEYS:
            raise AdmissionGateError("UNKNOWN_COMPOSER_CITATION_FIELD")
        citations: dict[str, tuple[str, ...]] = {}
        count = 0
        for key in _CITATION_KEYS:
            values = package.get(key, [])
            if not isinstance(values, list):
                raise AdmissionGateError("INVALID_COMPOSER_CITATION_PACKAGE")
            checked = []
            for token in values:
                if not isinstance(token, str) or not CITATION_TOKEN_PATTERN.fullmatch(token):
                    raise AdmissionGateError("UNSAFE_CITATION_TOKEN")
                checked.append(token)
            unique = _unique(checked)
            if len(unique) != len(checked):
                raise AdmissionGateError("DUPLICATE_CITATION_TOKEN")
            citations[key] = unique
            count += len(unique)
        if count > MAX_CITATIONS:
            raise AdmissionGateError("CITATION_LIMIT_EXCEEDED")
        return citations

    @staticmethod
    def _validate_memory_citation_binding(
        *,
        memory_context: MemoryContext,
        citation_tokens: dict[str, tuple[str, ...]],
    ) -> None:
        for key in _CITATION_KEYS:
            memory_values = memory_context.citation_package.get(key, [])
            if not isinstance(memory_values, list):
                raise AdmissionGateError("INVALID_MEMORY_CITATION_PACKAGE")
            if not set(citation_tokens[key]).issubset(set(memory_values)):
                raise AdmissionGateError("CITATION_PACKAGE_BINDING_MISMATCH")

    def _composer_facts(
        self,
        *,
        composed_response: ComposedResponse,
        citation_tokens: dict[str, tuple[str, ...]],
    ) -> tuple[ProjectionFact, ...]:
        facts: list[ProjectionFact] = []
        self._flatten_facts(
            value=composed_response.compressed_context,
            prefix="composer",
            segment_id="composer_facts",
            citation_tokens=citation_tokens,
            facts=facts,
            intent=composed_response.primary_intent,
        )
        if len(facts) > MAX_PROJECTION_FACTS:
            raise AdmissionGateError("PROJECTION_FACT_LIMIT_EXCEEDED")
        return tuple(facts)

    def _flatten_facts(
        self,
        *,
        value: Any,
        prefix: str,
        segment_id: str,
        citation_tokens: dict[str, tuple[str, ...]],
        facts: list[ProjectionFact],
        intent: Intent,
    ) -> None:
        if isinstance(value, dict):
            for key in sorted(value):
                if str(key).casefold() in FORBIDDEN_PROVIDER_VISIBLE_KEYS:
                    raise AdmissionGateError("FORBIDDEN_PROVIDER_VISIBLE_FIELD")
                self._flatten_facts(
                    value=value[key],
                    prefix=f"{prefix}.{key}",
                    segment_id=segment_id,
                    citation_tokens=citation_tokens,
                    facts=facts,
                    intent=intent,
                )
            return
        if isinstance(value, list):
            for index, item in enumerate(value):
                self._flatten_facts(
                    value=item,
                    prefix=f"{prefix}.{index}",
                    segment_id=segment_id,
                    citation_tokens=citation_tokens,
                    facts=facts,
                    intent=intent,
                )
            return
        if value is None or isinstance(value, str | int | float | bool):
            facts.append(
                ProjectionFact(
                    fact_id=prefix,
                    value=value,
                    segment_id=segment_id,
                    required_citations=self._required_fact_citations(
                        fact_id=prefix,
                        fact_value=value,
                        citation_tokens=citation_tokens,
                        intent=intent,
                    ),
                )
            )
            return
        raise AdmissionGateError("UNSUPPORTED_PROVIDER_VISIBLE_VALUE")

    @staticmethod
    def _required_fact_citations(
        *,
        fact_id: str,
        fact_value: Any,
        citation_tokens: dict[str, tuple[str, ...]],
        intent: Intent,
    ) -> tuple[str, ...]:
        valuations = citation_tokens["valuation_ids"]
        all_tokens = tuple(token for key in _CITATION_KEYS for token in citation_tokens[key])
        if isinstance(fact_value, str) and fact_value in all_tokens:
            return (fact_value,)
        if intent == Intent.PROPERTY_COMPARISON and len(valuations) >= 2:
            if ".property_a." in fact_id:
                return (valuations[0],)
            if ".property_b." in fact_id:
                return (valuations[1],)
            if fact_id.endswith(".price_delta") or fact_id.endswith(".price_percentage_delta"):
                return valuations[:2]
        return valuations[:1] or all_tokens[:1]

    @staticmethod
    def _required_disclosures(
        composed_response: ComposedResponse,
        facts: tuple[ProjectionFact, ...],
    ) -> tuple[str, ...]:
        if composed_response.status not in {
            CompositionStatus.PARTIAL_SUCCESS,
            CompositionStatus.SPARSE_EVIDENCE,
        }:
            return ()
        disclosure_id = "composer.composition_status"
        if not any(fact.fact_id == disclosure_id for fact in facts):
            raise AdmissionGateError("REQUIRED_LIMITATION_DISCLOSURE_MISSING")
        return (disclosure_id,)

    @staticmethod
    def _segments(
        *,
        intent: Intent,
        contract_id: str,
        user_message: str,
        facts: tuple[ProjectionFact, ...],
        required_disclosures: tuple[str, ...],
        citation_tokens: dict[str, tuple[str, ...]],
    ) -> tuple[ProjectionSegment, ...]:
        return (
            ProjectionSegment(
                segment_id="governance",
                segment_class="governance",
                protected=True,
                content={
                    "intent": intent.value,
                    "contract_id": contract_id,
                    "contract_version": CONTRACT_VERSION,
                    "prohibited_claims_policy_version": PROHIBITED_CLAIMS_POLICY_VERSION,
                },
            ),
            ProjectionSegment(
                segment_id="untrusted_current_turn",
                segment_class="untrusted_current_turn",
                protected=True,
                content={"kind": "untrusted_user_data", "text": user_message},
            ),
            ProjectionSegment(
                segment_id="composer_facts",
                segment_class="composer_facts",
                protected=True,
                content={
                    "facts": [
                        {
                            "fact_id": fact.fact_id,
                            "value": fact.value,
                            "required_citations": list(fact.required_citations),
                        }
                        for fact in facts
                    ]
                },
            ),
            ProjectionSegment(
                segment_id="limitations",
                segment_class="limitations",
                protected=True,
                content={"required_disclosure_fact_ids": list(required_disclosures)},
            ),
            ProjectionSegment(
                segment_id="citation_tokens",
                segment_class="citation_tokens",
                protected=True,
                content={key: list(citation_tokens[key]) for key in _CITATION_KEYS},
            ),
        )

    @staticmethod
    def _ensure_provider_safe(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if str(key).casefold() in FORBIDDEN_PROVIDER_VISIBLE_KEYS:
                    raise AdmissionGateError("FORBIDDEN_PROVIDER_VISIBLE_FIELD")
                NarrationAdmissionGate._ensure_provider_safe(child)
        elif isinstance(value, list):
            for child in value:
                NarrationAdmissionGate._ensure_provider_safe(child)
        elif value is not None and not isinstance(value, str | int | float | bool):
            raise AdmissionGateError("UNSUPPORTED_PROVIDER_VISIBLE_VALUE")

    @staticmethod
    def _binding_attestation(
        *,
        scope: NarrationScope,
        composed_response: ComposedResponse,
        memory_context: MemoryContext,
        citation_tokens: dict[str, tuple[str, ...]],
    ) -> str:
        payload = {
            "scope": {
                "user_id": scope.user_id,
                "workspace_id": scope.workspace_id,
                "scenario_id": scope.scenario_id,
                "broker_session_id": scope.broker_session_id,
            },
            "response_id": composed_response.response_id,
            "memory_id": memory_context.memory_id,
            "citations": citation_tokens,
        }
        digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
        return f"binding_{digest}"
