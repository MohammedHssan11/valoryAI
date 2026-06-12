from __future__ import annotations

import ast
import json
from pathlib import Path
import time

import pytest

from app.copilot.orchestrator.intents import ConfidenceLevel, Intent, IntentResult, intent_engine
from app.copilot.orchestrator.planner import ExecutionStrategy, PlannedToolCall, tool_planner


@pytest.mark.parametrize(
    ("message", "expected_intent", "expected_tool"),
    [
        ("What is the fair price for this property?", Intent.VALUATION, PlannedToolCall.VALUATION_TOOL),
        ("Explain the valuation.", Intent.EXPLAINABILITY, PlannedToolCall.EXPLAINABILITY_TOOL),
        ("Show me nearby comparable properties.", Intent.COMPARABLES, PlannedToolCall.COMPARABLES_TOOL),
        ("Is the asking price fair?", Intent.FAIRNESS, PlannedToolCall.FAIRNESS_TOOL),
        ("What if I add a gym?", Intent.WHAT_IF, PlannedToolCall.WHAT_IF_TOOL),
        ("Should I negotiate?", Intent.NEGOTIATION, PlannedToolCall.NEGOTIATION_TOOL),
        ("Is this a good investment?", Intent.INVESTMENT, PlannedToolCall.INVESTMENT_TOOL),
        ("What is happening in Mivida?", Intent.MARKET_INSIGHT, PlannedToolCall.MARKET_INSIGHT_TOOL),
    ],
)
def test_maps_each_direct_intent_to_its_approved_tool(message, expected_intent, expected_tool):
    plan = tool_planner.plan(intent_engine.classify(message))

    assert plan.primary_intent == expected_intent
    assert plan.tools == (expected_tool,)
    assert plan.selected_tools == plan.tools
    assert plan.parallel_groups == ()
    assert plan.execution_strategy == ExecutionStrategy.SEQUENTIAL
    assert plan.requires_clarification is False
    assert plan.selection_source == "APPROVED_TOOL_MAP"
    assert plan.intent_source == "INTENT_ENGINE_V1"


def test_negotiation_selects_only_tool_six_because_it_orchestrates_required_evidence():
    plan = tool_planner.plan(intent_engine.classify("Should I negotiate?"))

    assert plan.tools == (PlannedToolCall.NEGOTIATION_TOOL,)
    assert plan.reason == "NEGOTIATION_TOOL already orchestrates the required evidence."


@pytest.mark.parametrize(
    ("message", "expected_intent", "expected_tools"),
    [
        (
            "Evaluate this property",
            Intent.PROPERTY_EVALUATION,
            (
                PlannedToolCall.VALUATION_TOOL,
                PlannedToolCall.COMPARABLES_TOOL,
                PlannedToolCall.MARKET_INSIGHT_TOOL,
            ),
        ),
        ("Generate investment analysis", Intent.INVESTMENT_ANALYSIS, (PlannedToolCall.INVESTMENT_TOOL,)),
        (
            "Show risk factors",
            Intent.RISK_ANALYSIS,
            (PlannedToolCall.INVESTMENT_TOOL, PlannedToolCall.MARKET_INSIGHT_TOOL),
        ),
        (
            "Compare with market",
            Intent.MARKET_COMPARISON,
            (PlannedToolCall.COMPARABLES_TOOL, PlannedToolCall.MARKET_INSIGHT_TOOL),
        ),
        ("What's a fair offer?", Intent.NEGOTIATION_SUPPORT, (PlannedToolCall.NEGOTIATION_TOOL,)),
    ],
)
def test_v2_property_aware_intents_map_to_existing_tools(message, expected_intent, expected_tools):
    plan = tool_planner.plan(intent_engine.classify(message))

    assert plan.primary_intent == expected_intent
    assert plan.tools == expected_tools
    assert plan.selected_tools == expected_tools
    assert plan.requires_clarification is False


def test_property_comparison_plans_two_parallel_tool_one_invocations_without_tool_nine():
    plan = tool_planner.plan(intent_engine.classify("Compare these two properties."))

    expected_tools = (
        PlannedToolCall.VALUATION_TOOL_PROPERTY_A,
        PlannedToolCall.VALUATION_TOOL_PROPERTY_B,
    )
    assert plan.primary_intent == Intent.PROPERTY_COMPARISON
    assert plan.tools == expected_tools
    assert plan.selected_tools == expected_tools
    assert plan.parallel_groups == (expected_tools,)
    assert plan.execution_strategy == ExecutionStrategy.PARALLEL
    assert plan.requires_clarification is False
    assert plan.selection_source == "APPROVED_TOOL_MAP+APPROVED_PROPERTY_COMPARISON_PATTERN"
    assert "Response Composer" in plan.reason
    assert all("TOOL_9" not in tool.value for tool in plan.tools)


def test_multi_intent_plan_groups_independent_tools_for_parallel_execution():
    plan = tool_planner.plan(
        intent_engine.classify("What is happening in Mivida and should I negotiate?")
    )

    expected_tools = (
        PlannedToolCall.MARKET_INSIGHT_TOOL,
        PlannedToolCall.NEGOTIATION_TOOL,
    )
    assert plan.primary_intent == Intent.MARKET_INSIGHT
    assert plan.secondary_intents == (Intent.NEGOTIATION,)
    assert plan.tools == expected_tools
    assert plan.parallel_groups == (expected_tools,)
    assert plan.execution_strategy == ExecutionStrategy.PARALLEL


def test_intent_engine_clarification_result_produces_no_tool_plan():
    plan = tool_planner.plan(intent_engine.classify("Tell me more"))

    assert plan.primary_intent == Intent.GENERAL_QUESTION
    assert plan.tools == ()
    assert plan.selected_tools == ()
    assert plan.parallel_groups == ()
    assert plan.execution_strategy == ExecutionStrategy.CLARIFICATION_REQUIRED
    assert plan.requires_clarification is True
    assert plan.selection_source == "CLARIFICATION_POLICY"


def test_low_confidence_input_cannot_select_tools_even_when_intent_is_mapped():
    low_confidence_result = IntentResult(
        intent=Intent.VALUATION,
        confidence=ConfidenceLevel.LOW,
        matched_rules=("valuation.keyword",),
        matched_keywords=("valuation",),
        requires_clarification=False,
        reason="Synthetic contract edge case for planner boundary validation.",
    )

    plan = tool_planner.plan(low_confidence_result)

    assert plan.tools == ()
    assert plan.execution_strategy == ExecutionStrategy.CLARIFICATION_REQUIRED
    assert plan.requires_clarification is True


def test_general_question_without_flag_still_requires_clarification():
    general_question = IntentResult(
        intent=Intent.GENERAL_QUESTION,
        confidence=ConfidenceLevel.MEDIUM,
        matched_rules=("general.synthetic",),
        matched_keywords=("general",),
        requires_clarification=False,
        reason="Synthetic contract edge case for planner boundary validation.",
    )

    plan = tool_planner.plan(general_question)

    assert plan.tools == ()
    assert plan.execution_strategy == ExecutionStrategy.CLARIFICATION_REQUIRED
    assert plan.requires_clarification is True


def test_execution_plan_serializes_required_contract_and_audit_fields():
    plan = tool_planner.plan(
        intent_engine.classify("What is happening in Mivida and should I negotiate?")
    ).to_dict()

    assert plan == {
        "plan_id": plan["plan_id"],
        "primary_intent": "MARKET_INSIGHT",
        "secondary_intents": ["NEGOTIATION"],
        "tools": ["MARKET_INSIGHT_TOOL", "NEGOTIATION_TOOL"],
        "parallel_groups": [["MARKET_INSIGHT_TOOL", "NEGOTIATION_TOOL"]],
        "execution_strategy": "PARALLEL",
        "requires_clarification": False,
        "reason": (
            "Independent intents map to top-level Tool calls that can be executed in parallel: "
            "MARKET_INSIGHT_TOOL, NEGOTIATION_TOOL."
        ),
        "selected_tools": ["MARKET_INSIGHT_TOOL", "NEGOTIATION_TOOL"],
        "selection_source": "APPROVED_TOOL_MAP",
        "intent_source": "INTENT_ENGINE_V1",
    }
    assert plan["plan_id"].startswith("plan_")


def test_repeated_planning_is_deterministic_and_equal():
    intent_result = intent_engine.classify("What is happening in Mivida and should I negotiate?")
    plans = [tool_planner.plan(intent_result) for _ in range(100)]
    serialized = {json.dumps(plan.to_dict(), sort_keys=True) for plan in plans}

    assert len(serialized) == 1
    assert len({plan.plan_id for plan in plans}) == 1
    assert all(plan == plans[0] for plan in plans)


def test_rejects_non_intent_result_input():
    with pytest.raises(TypeError, match="intent_result must be an IntentResult"):
        tool_planner.plan({"intent": "VALUATION"})  # type: ignore[arg-type]


def test_planner_imports_are_in_process_standard_library_and_intent_contract_only():
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "planner"
    allowed_import_roots = {
        "__future__",
        "dataclasses",
        "enum",
        "hashlib",
        "json",
        "typing",
    }
    forbidden_imports = []

    for source_path in package_root.glob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                imported = [node.module or ""]
            else:
                continue
            forbidden_imports.extend(
                module
                for module in imported
                if module.split(".", maxsplit=1)[0] not in allowed_import_roots
                and not module.startswith("app.copilot.orchestrator.intents")
                and not module.startswith("app.copilot.orchestrator.planner")
            )

    assert forbidden_imports == []


def test_planner_source_has_no_external_dependency_references():
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "planner"
    source = "\n".join(
        source_path.read_text(encoding="utf-8").casefold()
        for source_path in package_root.glob("*.py")
    )
    forbidden_terms = (
        "anthropic",
        "catboost",
        "fastapi",
        "gemini",
        "httpx",
        "openai",
        "requests",
        "sklearn",
        "socket",
        "sqlalchemy",
        "transformers",
        "urllib",
    )

    assert [term for term in forbidden_terms if term in source] == []


@pytest.mark.performance
def test_tool_planner_average_latency_is_below_one_millisecond():
    intent_result = intent_engine.classify("What is happening in Mivida and should I negotiate?")
    iterations = 20_000
    started = time.perf_counter()

    for _ in range(iterations):
        tool_planner.plan(intent_result)

    average_latency_ms = ((time.perf_counter() - started) * 1000) / iterations
    assert average_latency_ms < 1
