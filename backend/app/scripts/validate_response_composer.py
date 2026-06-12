from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import time
from typing import Any

from app.copilot.orchestrator.composer import CompositionStatus, DeterministicResponseComposer
from app.copilot.orchestrator.executor import (
    DeterministicToolExecutor,
    ExecutionAuditMetadata,
    ExecutionResult,
    ExecutionStatus,
    ToolExecutionFailure,
    ToolExecutionResult,
    ToolOrderingMetadata,
)
from app.copilot.orchestrator.intents import Intent, intent_engine
from app.copilot.orchestrator.planner import ExecutionStrategy, PlannedToolCall, tool_planner
from app.db.session import SessionLocal
from app.models.copilot import User


_FORBIDDEN_SOURCE_TERMS = (
    "anthropic",
    "catboost",
    "copilottoolsservice",
    "embedding",
    "gemini",
    "httpx",
    "openai",
    "price_listing",
    "requests",
    "router_service",
    "sqlalchemy",
    "transformers",
)
_FORBIDDEN_IMPORT_ROOTS = {
    "anthropic",
    "catboost",
    "fastapi",
    "google",
    "httpx",
    "openai",
    "requests",
    "sklearn",
    "sqlalchemy",
    "transformers",
}
_PROHIBITED_COMPARISON_FIELDS = {
    "feature_delta",
    "numeric_confidence_delta",
    "recommendation",
    "sqm_delta",
    "winner",
}


def _args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("initial", "replay"), required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--workspace-id", required=True, type=int)
    parser.add_argument("--empty-workspace-id", required=True, type=int)
    parser.add_argument("--property-a-id", required=True, type=int)
    parser.add_argument("--property-b-id", required=True, type=int)
    parser.add_argument("--other-property-id", required=True, type=int)
    parser.add_argument("--replay-path", required=True)
    return parser.parse_args()


def _user_id(subject: str) -> int:
    with SessionLocal() as db:
        user = db.query(User).filter(User.external_subject == subject, User.is_deleted.is_(False)).one()
        return user.id


def _execution_from_dict(data: dict[str, Any]) -> ExecutionResult:
    audit = data["audit_metadata"]
    return ExecutionResult(
        execution_id=data["execution_id"],
        plan_id=data["plan_id"],
        primary_intent=Intent(data["primary_intent"]),
        secondary_intents=tuple(Intent(intent) for intent in data["secondary_intents"]),
        status=ExecutionStatus(data["status"]),
        tool_results=tuple(
            ToolExecutionResult(
                planned_tool=PlannedToolCall(item["planned_tool"]),
                tool_name=item["tool_name"],
                payload=item["payload"],
                execution_time_ms=item["execution_time_ms"],
                ordering_metadata=ToolOrderingMetadata(**item["ordering_metadata"]),
            )
            for item in data["tool_results"]
        ),
        failed_tools=tuple(
            ToolExecutionFailure(
                planned_tool=PlannedToolCall(item["planned_tool"]),
                tool_name=item["tool_name"],
                error_type=item["error_type"],
                error_message=item["error_message"],
                execution_time_ms=item["execution_time_ms"],
                ordering_metadata=ToolOrderingMetadata(**item["ordering_metadata"]),
            )
            for item in data["failed_tools"]
        ),
        execution_time_ms=data["execution_time_ms"],
        partial_success=data["partial_success"],
        audit_metadata=ExecutionAuditMetadata(
            executed_tools=tuple(PlannedToolCall(item) for item in audit["executed_tools"]),
            successful_tools=tuple(PlannedToolCall(item) for item in audit["successful_tools"]),
            failed_tools=tuple(PlannedToolCall(item) for item in audit["failed_tools"]),
            execution_strategy=ExecutionStrategy(audit["execution_strategy"]),
            timeout_seconds=audit["timeout_seconds"],
        ),
    )


def _validate_source_boundary() -> tuple[list[str], list[str], bool]:
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "composer"
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


def _compose(execution_result: ExecutionResult):
    return DeterministicResponseComposer().compose(execution_result)


def _execute(
    executor: DeterministicToolExecutor,
    *,
    message: str,
    user_id: int,
    tool_inputs: dict[PlannedToolCall, dict[str, Any]],
) -> ExecutionResult:
    return executor.execute(
        tool_planner.plan(intent_engine.classify(message)),
        user_id=user_id,
        tool_inputs=tool_inputs,
    )


def _replay(args: argparse.Namespace) -> None:
    replay_path = Path(args.replay_path)
    stored = json.loads(replay_path.read_text(encoding="utf-8"))
    execution_result = _execution_from_dict(stored["execution_result"])
    recomposed = _compose(execution_result).to_dict()
    expected = stored["composed_response"]
    result = {
        "replay_equal": recomposed == expected,
        "response_id": recomposed["response_id"],
        "execution_id": recomposed["execution_id"],
        "plan_id": recomposed["plan_id"],
        "status": recomposed["status"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["replay_equal"]:
        raise SystemExit(1)


def _initial(args: argparse.Namespace) -> None:
    user_id = _user_id(args.subject)
    executor = DeterministicToolExecutor()

    valuation = _execute(
        executor,
        message="What is the fair price for this property?",
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.VALUATION_TOOL: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
            }
        },
    )
    fair_price = valuation.tool_results[0].payload["fair_price"]
    comparison_execution = _execute(
        executor,
        message="Compare these two properties.",
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
    comparables_execution = _execute(
        executor,
        message="Show me nearby comparable properties.",
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.COMPARABLES_TOOL: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
            }
        },
    )
    negotiation_execution = _execute(
        executor,
        message="Should I negotiate?",
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.NEGOTIATION_TOOL: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
                "asking_price_egp": fair_price,
            }
        },
    )
    investment_execution = _execute(
        executor,
        message="Is this a good investment?",
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.INVESTMENT_TOOL: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
                "asking_price_egp": fair_price,
            }
        },
    )
    market_execution = _execute(
        executor,
        message="What is happening in Mivida?",
        user_id=user_id,
        tool_inputs={PlannedToolCall.MARKET_INSIGHT_TOOL: {"workspace_id": args.workspace_id}},
    )
    multi_execution = _execute(
        executor,
        message="What is happening in Mivida and should I negotiate?",
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
    sparse_execution = _execute(
        executor,
        message="What is happening in Mivida?",
        user_id=user_id,
        tool_inputs={PlannedToolCall.MARKET_INSIGHT_TOOL: {"workspace_id": args.empty_workspace_id}},
    )
    partial_execution = _execute(
        executor,
        message="Compare these two properties.",
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
    failed_execution = _execute(
        executor,
        message="Compare these two properties.",
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.VALUATION_TOOL_PROPERTY_A: {
                "workspace_id": args.workspace_id,
                "property_id": args.other_property_id,
            },
            PlannedToolCall.VALUATION_TOOL_PROPERTY_B: {
                "workspace_id": args.workspace_id,
                "property_id": args.other_property_id,
            },
        },
    )
    clarification_execution = _execute(
        executor,
        message="Tell me more",
        user_id=user_id,
        tool_inputs={},
    )

    comparison = _compose(comparison_execution)
    comparables = _compose(comparables_execution)
    negotiation = _compose(negotiation_execution)
    investment = _compose(investment_execution)
    market = _compose(market_execution)
    multi = _compose(multi_execution)
    sparse = _compose(sparse_execution)
    partial = _compose(partial_execution)
    failed = _compose(failed_execution)
    clarification = _compose(clarification_execution)
    deterministic_outputs = {
        json.dumps(_compose(comparison_execution).to_dict(), sort_keys=True)
        for _ in range(100)
    }
    performance_iterations = 1_000
    started = time.perf_counter()
    for _ in range(performance_iterations):
        _compose(comparison_execution)
    average_latency_ms = ((time.perf_counter() - started) * 1000) / performance_iterations

    comparison_payload = comparison.evidence_summary["property_comparison"]
    comparable_summary = comparables.evidence_summary["tool_summaries"][0]["summary"]["comparables"]
    frontend_comparable_count = len(comparables.frontend_payload["full_evidence"]["comparables"])
    forbidden_references, forbidden_imports, direct_queries_found = _validate_source_boundary()
    replay_path = Path(args.replay_path)
    replay_path.write_text(
        json.dumps(
            {
                "execution_result": comparison_execution.to_dict(),
                "composed_response": comparison.to_dict(),
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    result = {
        "composer_only": not forbidden_references and not forbidden_imports and not direct_queries_found,
        "execution_result_primary_intent": comparison_execution.primary_intent.value,
        "execution_result_secondary_intents": [
            intent.value for intent in multi_execution.secondary_intents
        ],
        "comparison_status": comparison.status.value,
        "comparison_price_delta": comparison_payload["price_delta"],
        "comparison_percentage_delta": comparison_payload["price_percentage_delta"],
        "comparison_confidence_labels": comparison_payload["confidence_level_label"],
        "comparison_prohibited_fields": sorted(_PROHIBITED_COMPARISON_FIELDS & comparison_payload.keys()),
        "comparison_arithmetic_valid": (
            comparison_payload["price_delta"]
            == comparison_payload["property_b"]["fair_price"] - comparison_payload["property_a"]["fair_price"]
        ),
        "deterministic_output_count": len(deterministic_outputs),
        "deterministic_response_id": comparison.response_id,
        "citation_valuation_count": len(comparables.citation_package["valuation_ids"]),
        "citation_comparable_count": len(comparables.citation_package["comparable_ids"]),
        "citation_optional_unavailable": comparables.citation_package[
            "unavailable_optional_citation_types"
        ],
        "compressed_top_comparable_count": len(comparable_summary["top_comparables"]),
        "frontend_comparable_count": frontend_comparable_count,
        "comparable_statistics": comparable_summary["statistics"],
        "dual_channel_delivery": bool(comparables.compressed_context and comparables.frontend_payload),
        "negotiation_status": negotiation.status.value,
        "investment_status": investment.status.value,
        "market_status": market.status.value,
        "multi_intent_status": multi.status.value,
        "sparse_status": sparse.status.value,
        "partial_status": partial.status.value,
        "failed_status": failed.status.value,
        "clarification_status": clarification.status.value,
        "forbidden_source_references": forbidden_references,
        "forbidden_imports": forbidden_imports,
        "direct_queries_found": direct_queries_found,
        "average_latency_ms": round(average_latency_ms, 6),
        "latency_target_ms": 15,
        "latency_target_passed": average_latency_ms < 15,
        "replay_path": str(replay_path),
    }
    failures = [
        not result["composer_only"],
        result["execution_result_primary_intent"] != "PROPERTY_COMPARISON",
        result["execution_result_secondary_intents"] != ["NEGOTIATION"],
        comparison.status != CompositionStatus.SUCCESS,
        bool(result["comparison_prohibited_fields"]),
        not result["comparison_arithmetic_valid"],
        len(deterministic_outputs) != 1,
        not comparison.response_id.startswith("response_"),
        result["citation_valuation_count"] < 1,
        result["citation_comparable_count"] < 1,
        result["compressed_top_comparable_count"] > 3,
        result["frontend_comparable_count"] < result["compressed_top_comparable_count"],
        not result["dual_channel_delivery"],
        negotiation.status != CompositionStatus.SUCCESS,
        investment.status != CompositionStatus.SUCCESS,
        market.status not in {CompositionStatus.SUCCESS, CompositionStatus.SPARSE_EVIDENCE},
        multi.status not in {CompositionStatus.SUCCESS, CompositionStatus.SPARSE_EVIDENCE},
        sparse.status != CompositionStatus.SPARSE_EVIDENCE,
        partial.status != CompositionStatus.PARTIAL_SUCCESS,
        failed.status != CompositionStatus.FAILED,
        clarification.status != CompositionStatus.CLARIFICATION_REQUIRED,
        average_latency_ms >= 15,
    ]
    print(json.dumps(result, indent=2, sort_keys=True))
    if any(failures):
        raise SystemExit(1)


def main() -> None:
    args = _args()
    if args.mode == "replay":
        _replay(args)
    else:
        _initial(args)


if __name__ == "__main__":
    main()
