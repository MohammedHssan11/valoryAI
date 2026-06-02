from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from app.copilot.orchestrator.intents import Intent


class ExecutionStrategy(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"


class PlannedToolCall(str, Enum):
    VALUATION_TOOL = "VALUATION_TOOL"
    EXPLAINABILITY_TOOL = "EXPLAINABILITY_TOOL"
    COMPARABLES_TOOL = "COMPARABLES_TOOL"
    FAIRNESS_TOOL = "FAIRNESS_TOOL"
    WHAT_IF_TOOL = "WHAT_IF_TOOL"
    NEGOTIATION_TOOL = "NEGOTIATION_TOOL"
    INVESTMENT_TOOL = "INVESTMENT_TOOL"
    MARKET_INSIGHT_TOOL = "MARKET_INSIGHT_TOOL"
    VALUATION_TOOL_PROPERTY_A = "VALUATION_TOOL:PROPERTY_A"
    VALUATION_TOOL_PROPERTY_B = "VALUATION_TOOL:PROPERTY_B"


@dataclass(frozen=True)
class ExecutionPlan:
    plan_id: str
    primary_intent: Intent
    secondary_intents: tuple[Intent, ...]
    tools: tuple[PlannedToolCall, ...]
    parallel_groups: tuple[tuple[PlannedToolCall, ...], ...]
    execution_strategy: ExecutionStrategy
    requires_clarification: bool
    reason: str
    selected_tools: tuple[PlannedToolCall, ...]
    selection_source: str
    intent_source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "primary_intent": self.primary_intent.value,
            "secondary_intents": [intent.value for intent in self.secondary_intents],
            "tools": [tool.value for tool in self.tools],
            "parallel_groups": [
                [tool.value for tool in group]
                for group in self.parallel_groups
            ],
            "execution_strategy": self.execution_strategy.value,
            "requires_clarification": self.requires_clarification,
            "reason": self.reason,
            "selected_tools": [tool.value for tool in self.selected_tools],
            "selection_source": self.selection_source,
            "intent_source": self.intent_source,
        }
