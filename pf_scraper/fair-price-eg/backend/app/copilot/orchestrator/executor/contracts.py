from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from app.copilot.orchestrator.intents import Intent
from app.copilot.orchestrator.planner import ExecutionStrategy, PlannedToolCall


class ExecutionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILED = "FAILED"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"


@dataclass(frozen=True)
class ToolOrderingMetadata:
    order_index: int
    parallel_group_index: int | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "order_index": self.order_index,
            "parallel_group_index": self.parallel_group_index,
        }


@dataclass(frozen=True)
class ToolExecutionResult:
    planned_tool: PlannedToolCall
    tool_name: str
    payload: dict[str, Any]
    execution_time_ms: float
    ordering_metadata: ToolOrderingMetadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "planned_tool": self.planned_tool.value,
            "tool_name": self.tool_name,
            "payload": self.payload,
            "execution_time_ms": self.execution_time_ms,
            "ordering_metadata": self.ordering_metadata.to_dict(),
        }


@dataclass(frozen=True)
class ToolExecutionFailure:
    planned_tool: PlannedToolCall
    tool_name: str
    error_type: str
    error_message: str
    execution_time_ms: float
    ordering_metadata: ToolOrderingMetadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "planned_tool": self.planned_tool.value,
            "tool_name": self.tool_name,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "execution_time_ms": self.execution_time_ms,
            "ordering_metadata": self.ordering_metadata.to_dict(),
        }


@dataclass(frozen=True)
class ExecutionAuditMetadata:
    executed_tools: tuple[PlannedToolCall, ...]
    successful_tools: tuple[PlannedToolCall, ...]
    failed_tools: tuple[PlannedToolCall, ...]
    execution_strategy: ExecutionStrategy
    timeout_seconds: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "executed_tools": [tool.value for tool in self.executed_tools],
            "successful_tools": [tool.value for tool in self.successful_tools],
            "failed_tools": [tool.value for tool in self.failed_tools],
            "execution_strategy": self.execution_strategy.value,
            "timeout_seconds": self.timeout_seconds,
        }


@dataclass(frozen=True)
class ExecutionResult:
    execution_id: str
    plan_id: str
    primary_intent: Intent
    secondary_intents: tuple[Intent, ...]
    status: ExecutionStatus
    tool_results: tuple[ToolExecutionResult, ...]
    failed_tools: tuple[ToolExecutionFailure, ...]
    execution_time_ms: float
    partial_success: bool
    audit_metadata: ExecutionAuditMetadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "plan_id": self.plan_id,
            "primary_intent": self.primary_intent.value,
            "secondary_intents": [intent.value for intent in self.secondary_intents],
            "status": self.status.value,
            "tool_results": [result.to_dict() for result in self.tool_results],
            "failed_tools": [failure.to_dict() for failure in self.failed_tools],
            "execution_time_ms": self.execution_time_ms,
            "partial_success": self.partial_success,
            "audit_metadata": self.audit_metadata.to_dict(),
        }
