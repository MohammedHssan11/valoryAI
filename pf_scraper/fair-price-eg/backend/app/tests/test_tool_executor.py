from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.copilot.orchestrator.executor import DeterministicToolExecutor, ExecutionStatus
from app.copilot.orchestrator.intents import intent_engine
from app.copilot.orchestrator.planner import PlannedToolCall, tool_planner


def test_clarification_plan_executes_nothing():
    plan = tool_planner.plan(intent_engine.classify("Tell me more"))

    result = DeterministicToolExecutor().execute(plan, user_id=1, tool_inputs={})

    assert result.status == ExecutionStatus.CLARIFICATION_REQUIRED
    assert result.tool_results == ()
    assert result.failed_tools == ()
    assert result.partial_success is False
    assert result.audit_metadata.executed_tools == ()
    assert result.audit_metadata.successful_tools == ()
    assert result.audit_metadata.failed_tools == ()


def test_missing_tool_input_is_a_structured_failure_without_invocation():
    plan = tool_planner.plan(intent_engine.classify("What is the fair price for this property?"))

    result = DeterministicToolExecutor().execute(plan, user_id=1, tool_inputs={})

    assert result.status == ExecutionStatus.FAILED
    assert result.tool_results == ()
    assert result.partial_success is True
    assert len(result.failed_tools) == 1
    assert result.failed_tools[0].planned_tool == PlannedToolCall.VALUATION_TOOL
    assert result.failed_tools[0].tool_name == "valuation"
    assert result.failed_tools[0].error_type == "MissingToolInputError"
    assert result.audit_metadata.failed_tools == (PlannedToolCall.VALUATION_TOOL,)


def test_rejects_invalid_executor_inputs():
    with pytest.raises(ValueError, match="timeout_seconds must be greater than zero"):
        DeterministicToolExecutor(timeout_seconds=0)

    plan = tool_planner.plan(intent_engine.classify("Tell me more"))
    with pytest.raises(TypeError, match="plan must be an ExecutionPlan"):
        DeterministicToolExecutor().execute({}, user_id=1, tool_inputs={})  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="user_id must be greater than zero"):
        DeterministicToolExecutor().execute(plan, user_id=0, tool_inputs={})


def test_execution_result_serializes_required_contract_and_audit_fields():
    plan = tool_planner.plan(intent_engine.classify("What is the fair price for this property?"))

    result = DeterministicToolExecutor().execute(plan, user_id=1, tool_inputs={}).to_dict()

    assert result == {
        "execution_id": result["execution_id"],
        "plan_id": plan.plan_id,
        "primary_intent": "VALUATION",
        "secondary_intents": [],
        "status": "FAILED",
        "tool_results": [],
        "failed_tools": [
            {
                "planned_tool": "VALUATION_TOOL",
                "tool_name": "valuation",
                "error_type": "MissingToolInputError",
                "error_message": "Missing input payload for VALUATION_TOOL",
                "execution_time_ms": 0.0,
                "ordering_metadata": {
                    "order_index": 0,
                    "parallel_group_index": None,
                },
            }
        ],
        "execution_time_ms": result["execution_time_ms"],
        "partial_success": True,
        "audit_metadata": {
            "executed_tools": ["VALUATION_TOOL"],
            "successful_tools": [],
            "failed_tools": ["VALUATION_TOOL"],
            "execution_strategy": "SEQUENTIAL",
            "timeout_seconds": 30.0,
        },
    }
    assert result["execution_id"].startswith("exec_")


def test_executor_source_preserves_phase_boundary():
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "executor"
    source = "\n".join(
        source_path.read_text(encoding="utf-8").casefold()
        for source_path in package_root.glob("*.py")
    )
    forbidden_terms = (
        "anthropic",
        "catboost",
        "composer",
        "delta",
        "embedding",
        "fair_price",
        "gemini",
        "median",
        "openai",
        "price_gap",
        "prompt",
        "summar",
        "transformers",
    )

    assert [term for term in forbidden_terms if term in source] == []
    assert ".query(" not in source


def test_executor_imports_do_not_include_forbidden_sdk_dependencies():
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "executor"
    forbidden_import_roots = {
        "anthropic",
        "catboost",
        "google",
        "httpx",
        "openai",
        "requests",
        "sklearn",
        "transformers",
    }
    imported_roots = []

    for source_path in package_root.glob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                imported = [node.module or ""]
            else:
                continue
            imported_roots.extend(module.split(".", maxsplit=1)[0] for module in imported)

    assert sorted(set(imported_roots) & forbidden_import_roots) == []
