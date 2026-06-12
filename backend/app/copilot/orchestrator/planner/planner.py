from __future__ import annotations

import hashlib
import json

from app.copilot.orchestrator.intents import ConfidenceLevel, Intent, IntentResult
from app.copilot.orchestrator.planner.contracts import (
    ExecutionPlan,
    ExecutionStrategy,
    PlannedToolCall,
)


_INTENT_SOURCE = "INTENT_ENGINE_V1"
_APPROVED_TOOL_MAP_SOURCE = "APPROVED_TOOL_MAP"
_PROPERTY_COMPARISON_SOURCE = "APPROVED_PROPERTY_COMPARISON_PATTERN"
_CLARIFICATION_SOURCE = "CLARIFICATION_POLICY"

_DIRECT_TOOL_MAP = {
    Intent.PROPERTY_EVALUATION: (
        PlannedToolCall.VALUATION_TOOL,
        PlannedToolCall.COMPARABLES_TOOL,
        PlannedToolCall.MARKET_INSIGHT_TOOL,
    ),
    Intent.INVESTMENT_ANALYSIS: (PlannedToolCall.INVESTMENT_TOOL,),
    Intent.RISK_ANALYSIS: (
        PlannedToolCall.INVESTMENT_TOOL,
        PlannedToolCall.MARKET_INSIGHT_TOOL,
    ),
    Intent.MARKET_COMPARISON: (
        PlannedToolCall.COMPARABLES_TOOL,
        PlannedToolCall.MARKET_INSIGHT_TOOL,
    ),
    Intent.NEGOTIATION_SUPPORT: (PlannedToolCall.NEGOTIATION_TOOL,),
    Intent.VALUATION: (PlannedToolCall.VALUATION_TOOL,),
    Intent.EXPLAINABILITY: (PlannedToolCall.EXPLAINABILITY_TOOL,),
    Intent.COMPARABLES: (PlannedToolCall.COMPARABLES_TOOL,),
    Intent.FAIRNESS: (PlannedToolCall.FAIRNESS_TOOL,),
    Intent.WHAT_IF: (PlannedToolCall.WHAT_IF_TOOL,),
    Intent.NEGOTIATION: (PlannedToolCall.NEGOTIATION_TOOL,),
    Intent.INVESTMENT: (PlannedToolCall.INVESTMENT_TOOL,),
    Intent.MARKET_INSIGHT: (PlannedToolCall.MARKET_INSIGHT_TOOL,),
}
_PROPERTY_COMPARISON_TOOLS = (
    PlannedToolCall.VALUATION_TOOL_PROPERTY_A,
    PlannedToolCall.VALUATION_TOOL_PROPERTY_B,
)


def _stable_plan_id(intent_result: IntentResult) -> str:
    serialized = json.dumps(
        intent_result.to_dict(),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]
    return f"plan_{digest}"


def _unique_intents(intent_result: IntentResult) -> tuple[Intent, ...]:
    return tuple(dict.fromkeys((intent_result.intent, *intent_result.secondary_intents)))


def _selection_source(intents: tuple[Intent, ...]) -> str:
    if Intent.PROPERTY_COMPARISON in intents:
        return f"{_APPROVED_TOOL_MAP_SOURCE}+{_PROPERTY_COMPARISON_SOURCE}"
    return _APPROVED_TOOL_MAP_SOURCE


class DeterministicToolPlanner:
    def plan(self, intent_result: IntentResult) -> ExecutionPlan:
        if not isinstance(intent_result, IntentResult):
            raise TypeError("intent_result must be an IntentResult")

        plan_id = _stable_plan_id(intent_result)
        intents = _unique_intents(intent_result)

        if intent_result.requires_clarification or intent_result.confidence == ConfidenceLevel.LOW:
            return self._clarification_plan(
                plan_id=plan_id,
                intent_result=intent_result,
                reason="Intent confidence is too low or clarification was requested; no Tools were selected.",
            )

        if Intent.GENERAL_QUESTION in intents:
            return self._clarification_plan(
                plan_id=plan_id,
                intent_result=intent_result,
                reason="GENERAL_QUESTION has no approved Tool mapping; clarification is required before execution.",
            )

        tools = self._select_tools(intents)
        if len(tools) == 1:
            strategy = ExecutionStrategy.SEQUENTIAL
            parallel_groups: tuple[tuple[PlannedToolCall, ...], ...] = ()
        else:
            strategy = ExecutionStrategy.PARALLEL
            parallel_groups = (tools,)

        return ExecutionPlan(
            plan_id=plan_id,
            primary_intent=intent_result.intent,
            secondary_intents=intent_result.secondary_intents,
            tools=tools,
            parallel_groups=parallel_groups,
            execution_strategy=strategy,
            requires_clarification=False,
            reason=self._reason(intents=intents, tools=tools),
            selected_tools=tools,
            selection_source=_selection_source(intents),
            intent_source=_INTENT_SOURCE,
        )

    @staticmethod
    def _select_tools(intents: tuple[Intent, ...]) -> tuple[PlannedToolCall, ...]:
        selected: list[PlannedToolCall] = []
        for intent in intents:
            mapped_tools = (
                _PROPERTY_COMPARISON_TOOLS
                if intent == Intent.PROPERTY_COMPARISON
                else _DIRECT_TOOL_MAP[intent]
            )
            for tool in mapped_tools:
                if tool not in selected:
                    selected.append(tool)
        return tuple(selected)

    @staticmethod
    def _reason(*, intents: tuple[Intent, ...], tools: tuple[PlannedToolCall, ...]) -> str:
        if intents == (Intent.PROPERTY_COMPARISON,):
            return (
                "Property comparison uses two parallel VALUATION_TOOL invocations for PROPERTY_A and PROPERTY_B; "
                "comparison remains a later Response Composer responsibility."
            )
        if intents == (Intent.NEGOTIATION,):
            return "NEGOTIATION_TOOL already orchestrates the required evidence."
        if intents == (Intent.INVESTMENT,):
            return "INVESTMENT_TOOL already orchestrates the required evidence chain."
        if len(tools) > 1:
            return (
                "Independent intents map to top-level Tool calls that can be executed in parallel: "
                f"{', '.join(tool.value for tool in tools)}."
            )
        return f"{intents[0].value} maps directly to {tools[0].value}."

    @staticmethod
    def _clarification_plan(
        *,
        plan_id: str,
        intent_result: IntentResult,
        reason: str,
    ) -> ExecutionPlan:
        return ExecutionPlan(
            plan_id=plan_id,
            primary_intent=intent_result.intent,
            secondary_intents=intent_result.secondary_intents,
            tools=(),
            parallel_groups=(),
            execution_strategy=ExecutionStrategy.CLARIFICATION_REQUIRED,
            requires_clarification=True,
            reason=reason,
            selected_tools=(),
            selection_source=_CLARIFICATION_SOURCE,
            intent_source=_INTENT_SOURCE,
        )


tool_planner = DeterministicToolPlanner()
