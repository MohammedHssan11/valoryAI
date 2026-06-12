from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class MemoryStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILED = "FAILED"
    EMPTY_CONTEXT = "EMPTY_CONTEXT"
    ACCESS_DENIED = "ACCESS_DENIED"


@dataclass(frozen=True)
class MemoryContext:
    memory_id: str
    status: MemoryStatus
    workspace_context: dict[str, Any]
    scenario_context: dict[str, Any] | None
    broker_session_context: dict[str, Any] | None
    recent_tool_history: tuple[dict[str, Any], ...]
    recent_decisions: tuple[dict[str, Any], ...]
    recent_valuations: tuple[dict[str, Any], ...]
    active_assumptions: tuple[dict[str, Any], ...]
    active_comparison_context: dict[str, Any] | None
    recent_conversation_metadata: tuple[dict[str, Any], ...]
    citation_package: dict[str, Any]
    memory_metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "status": self.status.value,
            "workspace_context": self.workspace_context,
            "scenario_context": self.scenario_context,
            "broker_session_context": self.broker_session_context,
            "recent_tool_history": list(self.recent_tool_history),
            "recent_decisions": list(self.recent_decisions),
            "recent_valuations": list(self.recent_valuations),
            "active_assumptions": list(self.active_assumptions),
            "active_comparison_context": self.active_comparison_context,
            "recent_conversation_metadata": list(self.recent_conversation_metadata),
            "citation_package": self.citation_package,
            "memory_metadata": self.memory_metadata,
        }
