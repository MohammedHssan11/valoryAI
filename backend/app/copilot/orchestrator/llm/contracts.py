from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from app.copilot.orchestrator.intents import Intent


class NarrationAdmissionState(str, Enum):
    ADMIT_NARRATION = "ADMIT_NARRATION"
    DETERMINISTIC_ONLY = "DETERMINISTIC_ONLY"
    REJECT_NARRATION = "REJECT_NARRATION"
    ACCESS_DENIED = "ACCESS_DENIED"


class GroundingDecision(str, Enum):
    ACCEPT_NARRATION = "ACCEPT_NARRATION"
    REJECT_NARRATION = "REJECT_NARRATION"
    ACCESS_DENIED = "ACCESS_DENIED"


class NarrationStatus(str, Enum):
    ACCEPT_NARRATION = "ACCEPT_NARRATION"
    DETERMINISTIC_ONLY = "DETERMINISTIC_ONLY"
    REJECT_NARRATION = "REJECT_NARRATION"
    ACCESS_DENIED = "ACCESS_DENIED"


@dataclass(frozen=True)
class NarrationScope:
    user_id: int
    workspace_id: int
    scenario_id: int | None = None
    broker_session_id: str | None = None


@dataclass(frozen=True)
class ProjectionFact:
    fact_id: str
    value: Any
    segment_id: str
    required_citations: tuple[str, ...]


@dataclass(frozen=True)
class ProjectionSegment:
    segment_id: str
    segment_class: str
    protected: bool
    content: dict[str, Any]


@dataclass(frozen=True)
class GroundingManifest:
    binding_attestation: str
    contract_id: str
    contract_version: str
    prohibited_claims_policy_version: str
    facts: tuple[ProjectionFact, ...]
    citation_tokens: dict[str, tuple[str, ...]]
    required_disclosure_fact_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ScopedNarrationEnvelope:
    admission_state: NarrationAdmissionState
    intent: Intent
    binding_attestation: str
    provider_safe_projection: tuple[ProjectionSegment, ...]
    grounding_manifest: GroundingManifest


@dataclass(frozen=True)
class AdmissionResult:
    state: NarrationAdmissionState
    reason_codes: tuple[str, ...]
    envelope: ScopedNarrationEnvelope | None = None


@dataclass(frozen=True)
class PromptAssemblyMetadata:
    assembly_policy_version: str
    serializer_version: str
    tokenizer_version: str
    provider_profile_id: str
    binding_attestation: str
    included_segment_ids: tuple[str, ...]
    evicted_optional_segment_ids: tuple[str, ...]
    request_token_estimate: int
    response_reserve_tokens: int


@dataclass(frozen=True)
class PromptBundle:
    instructions: str
    input_text: str
    token_count_estimate: int
    max_output_tokens: int
    metadata: PromptAssemblyMetadata


@dataclass(frozen=True)
class ProviderTransportResponse:
    provider: str
    model: str
    original_response_body: str
    latency_ms: float
    response_bytes: int
    token_usage: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ParsedNarrationCandidate:
    narration_text: str
    citation_references: tuple[str, ...]
    original_candidate_json: str
    original_response_sha256: str


@dataclass(frozen=True)
class GroundingResult:
    decision: GroundingDecision
    reason_codes: tuple[str, ...]
    checked_policy_versions: dict[str, str]
    checked_citation_count: int


@dataclass(frozen=True)
class NarrationResult:
    response_id: str
    status: NarrationStatus
    narrated_text: str | None
    deterministic_fallback_payload: dict[str, Any] | None
    citation_package: dict[str, Any] | None
    telemetry: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "response_id": self.response_id,
            "status": self.status.value,
            "narrated_text": self.narrated_text,
            "deterministic_fallback_payload": self.deterministic_fallback_payload,
            "citation_package": self.citation_package,
            "telemetry": self.telemetry,
        }
