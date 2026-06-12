from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import time

from app.copilot.orchestrator.executor import DeterministicToolExecutor, ExecutionStatus
from app.copilot.orchestrator.intents import intent_engine
from app.copilot.orchestrator.planner import PlannedToolCall, tool_planner
from app.db.session import SessionLocal
from app.models.copilot import ToolEvent, User


_FORBIDDEN_SOURCE_TERMS = (
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
_FORBIDDEN_IMPORT_ROOTS = {
    "anthropic",
    "catboost",
    "google",
    "httpx",
    "openai",
    "requests",
    "sklearn",
    "transformers",
}


def _args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", required=True)
    parser.add_argument("--other-subject", required=True)
    parser.add_argument("--workspace-id", required=True, type=int)
    parser.add_argument("--property-a-id", required=True, type=int)
    parser.add_argument("--property-b-id", required=True, type=int)
    parser.add_argument("--other-property-id", required=True, type=int)
    return parser.parse_args()


def _user_id(subject: str) -> int:
    with SessionLocal() as db:
        user = db.query(User).filter(User.external_subject == subject, User.is_deleted.is_(False)).one()
        return user.id


def _tool_event_count(user_id: int, workspace_id: int) -> int:
    with SessionLocal() as db:
        return (
            db.query(ToolEvent)
            .filter(ToolEvent.user_id == user_id, ToolEvent.workspace_id == workspace_id)
            .count()
        )


def _validate_source_boundary() -> tuple[list[str], list[str], bool]:
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "executor"
    forbidden_references = []
    forbidden_imports = []
    direct_queries_found = False
    for source_path in sorted(package_root.glob("*.py")):
        source = source_path.read_text(encoding="utf-8")
        lowered = source.casefold()
        forbidden_references.extend(
            f"{source_path.name}:{term}"
            for term in _FORBIDDEN_SOURCE_TERMS
            if term in lowered
        )
        direct_queries_found = direct_queries_found or ".query(" in lowered
        for node in ast.walk(ast.parse(source, filename=str(source_path))):
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                imported = [node.module or ""]
            else:
                continue
            forbidden_imports.extend(
                f"{source_path.name}:{module}"
                for module in imported
                if module.split(".", maxsplit=1)[0] in _FORBIDDEN_IMPORT_ROOTS
            )
    return forbidden_references, forbidden_imports, direct_queries_found


def main() -> None:
    args = _args()
    user_id = _user_id(args.subject)
    other_user_id = _user_id(args.other_subject)
    executor = DeterministicToolExecutor()

    valuation_plan = tool_planner.plan(intent_engine.classify("What is the fair price for this property?"))
    sequential = executor.execute(
        valuation_plan,
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.VALUATION_TOOL: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
            }
        },
    )
    fair_price = sequential.tool_results[0].payload["fair_price"]

    comparison_plan = tool_planner.plan(intent_engine.classify("Compare these two properties."))
    comparison = executor.execute(
        comparison_plan,
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.VALUATION_TOOL_PROPERTY_A: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
            },
            PlannedToolCall.VALUATION_TOOL_PROPERTY_B: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_b_id,
            },
        },
    )
    multi_plan = tool_planner.plan(
        intent_engine.classify("What is happening in Mivida and should I negotiate?")
    )
    multi = executor.execute(
        multi_plan,
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.MARKET_INSIGHT_TOOL: {"workspace_id": args.workspace_id},
            PlannedToolCall.NEGOTIATION_TOOL: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
                "asking_price_egp": fair_price,
            },
        },
    )
    partial = executor.execute(
        comparison_plan,
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.VALUATION_TOOL_PROPERTY_A: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
            },
            PlannedToolCall.VALUATION_TOOL_PROPERTY_B: {
                "workspace_id": args.workspace_id,
                "property_id": args.other_property_id,
            },
        },
    )
    tenant_isolation = executor.execute(
        valuation_plan,
        user_id=other_user_id,
        tool_inputs={
            PlannedToolCall.VALUATION_TOOL: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
            }
        },
    )
    clarification = executor.execute(
        tool_planner.plan(intent_engine.classify("Tell me more")),
        user_id=user_id,
        tool_inputs={},
    )
    timeout = DeterministicToolExecutor(timeout_seconds=0.000001).execute(
        tool_planner.plan(intent_engine.classify("What is happening in Mivida?")),
        user_id=user_id,
        tool_inputs={PlannedToolCall.MARKET_INSIGHT_TOOL: {"workspace_id": args.workspace_id}},
    )
    time.sleep(0.2)

    sequential_overhead_ms = round(
        sequential.execution_time_ms - sum(result.execution_time_ms for result in sequential.tool_results),
        3,
    )
    parallel_runtime_total_ms = round(
        sum(result.execution_time_ms for result in comparison.tool_results),
        3,
    )
    parallel_overhead_ms = round(
        comparison.execution_time_ms - max(result.execution_time_ms for result in comparison.tool_results),
        3,
    )
    forbidden_references, forbidden_imports, direct_queries_found = _validate_source_boundary()
    result = {
        "executor_only": not forbidden_references and not forbidden_imports and not direct_queries_found,
        "sequential_status": sequential.status.value,
        "sequential_tool_results": [item.planned_tool.value for item in sequential.tool_results],
        "sequential_raw_payload_source": sequential.tool_results[0].payload["source"],
        "sequential_raw_payload_tool_name": sequential.tool_results[0].payload["tool_name"],
        "sequential_overhead_ms": sequential_overhead_ms,
        "parallel_status": comparison.status.value,
        "parallel_tool_results": [item.planned_tool.value for item in comparison.tool_results],
        "parallel_group_indexes": [
            item.ordering_metadata.parallel_group_index
            for item in comparison.tool_results
        ],
        "parallel_execution_time_ms": comparison.execution_time_ms,
        "parallel_runtime_total_ms": parallel_runtime_total_ms,
        "parallel_overhead_ms": parallel_overhead_ms,
        "parallel_concurrency_proven": comparison.execution_time_ms < parallel_runtime_total_ms,
        "multi_intent_status": multi.status.value,
        "multi_intent_tool_results": [item.planned_tool.value for item in multi.tool_results],
        "property_comparison_payload_count": len(comparison.tool_results),
        "property_comparison_raw_payloads_preserved": all(
            item.payload["tool_name"] == "valuation" and item.payload["source"] == "TruthLayer"
            for item in comparison.tool_results
        ),
        "clarification_status": clarification.status.value,
        "clarification_tool_result_count": len(clarification.tool_results),
        "timeout_status": timeout.status.value,
        "timeout_partial_success": timeout.partial_success,
        "timeout_error_type": timeout.failed_tools[0].error_type,
        "partial_failure_status": partial.status.value,
        "partial_success": partial.partial_success,
        "partial_successful_tools": [item.planned_tool.value for item in partial.tool_results],
        "partial_failed_tools": [item.planned_tool.value for item in partial.failed_tools],
        "partial_error_type": partial.failed_tools[0].error_type,
        "tenant_isolation_status": tenant_isolation.status.value,
        "tenant_isolation_error_type": tenant_isolation.failed_tools[0].error_type,
        "audit_execution_id_present": sequential.execution_id.startswith("exec_"),
        "audit_plan_id_matches": sequential.plan_id == valuation_plan.plan_id,
        "audit_executed_tools": [item.value for item in comparison.audit_metadata.executed_tools],
        "audit_successful_tools": [item.value for item in comparison.audit_metadata.successful_tools],
        "audit_failed_tools": [item.value for item in comparison.audit_metadata.failed_tools],
        "tool_event_count": _tool_event_count(user_id, args.workspace_id),
        "forbidden_source_references": forbidden_references,
        "forbidden_imports": forbidden_imports,
        "direct_queries_found": direct_queries_found,
        "overhead_target_ms": 10,
        "sequential_overhead_target_passed": sequential_overhead_ms < 10,
        "parallel_overhead_target_passed": parallel_overhead_ms < 10,
    }
    failures = [
        not result["executor_only"],
        sequential.status != ExecutionStatus.SUCCESS,
        result["sequential_raw_payload_source"] != "TruthLayer",
        result["sequential_raw_payload_tool_name"] != "valuation",
        comparison.status != ExecutionStatus.SUCCESS,
        result["parallel_tool_results"] != [
            "VALUATION_TOOL:PROPERTY_A",
            "VALUATION_TOOL:PROPERTY_B",
        ],
        result["parallel_group_indexes"] != [0, 0],
        not result["parallel_concurrency_proven"],
        multi.status != ExecutionStatus.SUCCESS,
        result["multi_intent_tool_results"] != [
            "MARKET_INSIGHT_TOOL",
            "NEGOTIATION_TOOL",
        ],
        result["property_comparison_payload_count"] != 2,
        not result["property_comparison_raw_payloads_preserved"],
        clarification.status != ExecutionStatus.CLARIFICATION_REQUIRED,
        result["clarification_tool_result_count"] != 0,
        timeout.status != ExecutionStatus.FAILED,
        not timeout.partial_success,
        result["timeout_error_type"] != "ToolTimeoutError",
        partial.status != ExecutionStatus.PARTIAL_SUCCESS,
        not partial.partial_success,
        result["partial_successful_tools"] != ["VALUATION_TOOL:PROPERTY_A"],
        result["partial_failed_tools"] != ["VALUATION_TOOL:PROPERTY_B"],
        result["partial_error_type"] != "ToolResourceNotFound",
        tenant_isolation.status != ExecutionStatus.FAILED,
        result["tenant_isolation_error_type"] != "ToolResourceNotFound",
        not result["audit_execution_id_present"],
        not result["audit_plan_id_matches"],
        result["audit_executed_tools"] != [
            "VALUATION_TOOL:PROPERTY_A",
            "VALUATION_TOOL:PROPERTY_B",
        ],
        result["audit_successful_tools"] != [
            "VALUATION_TOOL:PROPERTY_A",
            "VALUATION_TOOL:PROPERTY_B",
        ],
        result["audit_failed_tools"] != [],
        not result["sequential_overhead_target_passed"],
        not result["parallel_overhead_target_passed"],
    ]
    print(json.dumps(result, indent=2, sort_keys=True))
    if any(failures):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
