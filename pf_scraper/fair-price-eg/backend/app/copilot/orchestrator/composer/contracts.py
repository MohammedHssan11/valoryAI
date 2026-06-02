from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from app.copilot.orchestrator.intents import Intent


class CompositionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILED = "FAILED"
    SPARSE_EVIDENCE = "SPARSE_EVIDENCE"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"


@dataclass(frozen=True)
class ComposedResponse:
    response_id: str
    execution_id: str
    plan_id: str
    primary_intent: Intent
    secondary_intents: tuple[Intent, ...]
    status: CompositionStatus
    evidence_summary: dict[str, Any]
    citation_package: dict[str, Any]
    compressed_context: dict[str, Any]
    frontend_payload: dict[str, Any]
    composer_metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "response_id": self.response_id,
            "execution_id": self.execution_id,
            "plan_id": self.plan_id,
            "primary_intent": self.primary_intent.value,
            "secondary_intents": [intent.value for intent in self.secondary_intents],
            "status": self.status.value,
            "evidence_summary": self.evidence_summary,
            "citation_package": self.citation_package,
            "compressed_context": self.compressed_context,
            "frontend_payload": self.frontend_payload,
            "composer_metadata": self.composer_metadata,
        }
