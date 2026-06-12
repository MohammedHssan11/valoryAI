from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import time

from app.copilot.orchestrator.composer import DeterministicResponseComposer
from app.copilot.orchestrator.executor import DeterministicToolExecutor
from app.copilot.orchestrator.intents import intent_engine
from app.copilot.orchestrator.memory import (
    ACTIVE_ASSUMPTIONS_LIMIT,
    MEMORY_DECISION_ACTION,
    RECENT_CONVERSATION_METADATA_LIMIT,
    RECENT_DECISIONS_LIMIT,
    RECENT_TOOL_EVENTS_LIMIT,
    RECENT_VALUATIONS_LIMIT,
    DeterministicMemoryIntegration,
    MemoryStatus,
    derive_memory_id,
)
from app.copilot.orchestrator.planner import PlannedToolCall, tool_planner
from app.db.session import SessionLocal
from app.models.copilot import DecisionHistory, User


_FORBIDDEN_SOURCE_TERMS = (
    "anthropic",
    "chroma",
    "embedding",
    "faiss",
    "gemini",
    "openai",
    "pinecone",
    "weaviate",
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
    parser.add_argument("--mode", choices=("initial", "replay"), required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--other-subject", required=True)
    parser.add_argument("--workspace-id", required=True, type=int)
    parser.add_argument("--empty-workspace-id", required=True, type=int)
    parser.add_argument("--scenario-id", required=True, type=int)
    parser.add_argument("--property-a-id", required=True, type=int)
    parser.add_argument("--property-b-id", required=True, type=int)
    parser.add_argument("--broker-session-id", required=True)
    parser.add_argument("--replay-path", required=True)
    parser.add_argument("--expected-memory-id")
    return parser.parse_args()


def _user_id(subject: str) -> int:
    with SessionLocal() as db:
        return (
            db.query(User)
            .filter(User.external_subject == subject, User.is_deleted.is_(False))
            .one()
            .id
        )


def _validate_source_boundary() -> tuple[list[str], list[str]]:
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "memory"
    forbidden_references = []
    forbidden_imports = []
    for source_path in sorted(package_root.glob("*.py")):
        source = source_path.read_text(encoding="utf-8")
        lowered = source.casefold()
        forbidden_references.extend(
            f"{source_path.name}:{term}"
            for term in _FORBIDDEN_SOURCE_TERMS
            if term in lowered
        )
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
    return forbidden_references, forbidden_imports


def _load(args: argparse.Namespace, user_id: int):
    with SessionLocal() as db:
        return DeterministicMemoryIntegration(db).load_context(
            user_id=user_id,
            workspace_id=args.workspace_id,
            scenario_id=args.scenario_id,
            broker_session_id=args.broker_session_id,
        )


def _replay(args: argparse.Namespace) -> None:
    user_id = _user_id(args.subject)
    recovered = _load(args, user_id).to_dict()
    replay_path = Path(args.replay_path)
    if replay_path.exists():
        replay_equal = recovered == json.loads(replay_path.read_text(encoding="utf-8"))
        comparison_mode = "FULL_CONTEXT"
    else:
        replay_equal = recovered["memory_id"] == args.expected_memory_id
        comparison_mode = "DETERMINISTIC_MEMORY_ID"
    result = {
        "replay_equal": replay_equal,
        "comparison_mode": comparison_mode,
        "memory_id": recovered["memory_id"],
        "status": recovered["status"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["replay_equal"]:
        raise SystemExit(1)


def _initial(args: argparse.Namespace) -> None:
    user_id = _user_id(args.subject)
    other_user_id = _user_id(args.other_subject)
    comparison_execution = DeterministicToolExecutor().execute(
        tool_planner.plan(intent_engine.classify("Compare these two properties.")),
        user_id=user_id,
        tool_inputs={
            PlannedToolCall.VALUATION_TOOL_PROPERTY_A: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_a_id,
                "scenario_id": args.scenario_id,
            },
            PlannedToolCall.VALUATION_TOOL_PROPERTY_B: {
                "workspace_id": args.workspace_id,
                "property_id": args.property_b_id,
            },
        },
    )
    composed = DeterministicResponseComposer().compose(comparison_execution)

    with SessionLocal() as db:
        integration = DeterministicMemoryIntegration(db)
        context = integration.remember(
            user_id=user_id,
            workspace_id=args.workspace_id,
            scenario_id=args.scenario_id,
            broker_session_id=args.broker_session_id,
            execution_result=comparison_execution,
            composed_response=composed,
        )
        idempotent = integration.remember(
            user_id=user_id,
            workspace_id=args.workspace_id,
            scenario_id=args.scenario_id,
            broker_session_id=args.broker_session_id,
            execution_result=comparison_execution,
            composed_response=composed,
        )
        empty = integration.load_context(
            user_id=user_id,
            workspace_id=args.empty_workspace_id,
        )
        denied = integration.load_context(
            user_id=other_user_id,
            workspace_id=args.workspace_id,
            scenario_id=args.scenario_id,
        )
        remembered_decision_count = (
            db.query(DecisionHistory)
            .filter(
                DecisionHistory.user_id == user_id,
                DecisionHistory.workspace_id == args.workspace_id,
                DecisionHistory.action == MEMORY_DECISION_ACTION,
            )
            .count()
        )

    deterministic = {_load(args, user_id).memory_id for _ in range(10)}
    context_dict = context.to_dict()
    hash_payload = {key: value for key, value in context_dict.items() if key != "memory_id"}
    iterations = 1_000
    started = time.perf_counter()
    for _ in range(iterations):
        derive_memory_id(hash_payload)
    average_overhead_ms = ((time.perf_counter() - started) * 1000) / iterations

    forbidden_references, forbidden_imports = _validate_source_boundary()
    Path(args.replay_path).write_text(
        json.dumps(context_dict, sort_keys=True),
        encoding="utf-8",
    )
    result = {
        "memory_only": not forbidden_references and not forbidden_imports,
        "status": context.status.value,
        "memory_id": context.memory_id,
        "idempotent_memory_equal": context.to_dict() == idempotent.to_dict(),
        "remembered_decision_count": remembered_decision_count,
        "deterministic_memory_id_count": len(deterministic),
        "empty_workspace_status": empty.status.value,
        "tenant_isolation_status": denied.status.value,
        "broker_session_recovered": context.broker_session_context["session_id"] == args.broker_session_id,
        "active_comparison_recovered": context.active_comparison_context["status"] == "AVAILABLE",
        "citation_workspace_preserved": context.citation_package["workspace_id"] == args.workspace_id,
        "citation_scenario_preserved": context.citation_package["scenario_id"] == args.scenario_id,
        "citation_valuation_count": len(context.citation_package["valuation_ids"]),
        "citation_tool_event_count": len(context.citation_package["tool_event_ids"]),
        "recent_tool_history_count": len(context.recent_tool_history),
        "recent_decision_count": len(context.recent_decisions),
        "recent_valuation_count": len(context.recent_valuations),
        "recent_conversation_metadata_count": len(context.recent_conversation_metadata),
        "tool_history_compressed": context.memory_metadata["compression"]["recent_tool_history_truncated"],
        "conversation_metadata_compressed": context.memory_metadata["compression"][
            "recent_conversation_metadata_truncated"
        ],
        "forbidden_source_references": forbidden_references,
        "forbidden_imports": forbidden_imports,
        "average_overhead_ms_excluding_database": round(average_overhead_ms, 6),
        "latency_target_ms": 25,
        "latency_target_passed": average_overhead_ms < 25,
        "governed_limits": context.memory_metadata["governed_limits"],
    }
    failures = [
        not result["memory_only"],
        context.status != MemoryStatus.SUCCESS,
        not result["memory_id"].startswith("memory_"),
        not result["idempotent_memory_equal"],
        result["remembered_decision_count"] != 1,
        result["deterministic_memory_id_count"] != 1,
        empty.status != MemoryStatus.EMPTY_CONTEXT,
        denied.status != MemoryStatus.ACCESS_DENIED,
        not result["broker_session_recovered"],
        not result["active_comparison_recovered"],
        not result["citation_workspace_preserved"],
        not result["citation_scenario_preserved"],
        result["citation_valuation_count"] < 2,
        result["citation_tool_event_count"] < 1,
        result["recent_tool_history_count"] > RECENT_TOOL_EVENTS_LIMIT,
        result["recent_decision_count"] > RECENT_DECISIONS_LIMIT,
        result["recent_valuation_count"] > RECENT_VALUATIONS_LIMIT,
        result["recent_conversation_metadata_count"] > RECENT_CONVERSATION_METADATA_LIMIT,
        not result["tool_history_compressed"],
        not result["conversation_metadata_compressed"],
        average_overhead_ms >= 25,
        result["governed_limits"]["active_assumptions"] != ACTIVE_ASSUMPTIONS_LIMIT,
        result["governed_limits"]["recent_valuations"] != RECENT_VALUATIONS_LIMIT,
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
