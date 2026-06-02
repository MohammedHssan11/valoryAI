from __future__ import annotations

import ast
import json
from pathlib import Path
import time

from app.copilot.orchestrator.intents import Intent, intent_engine
from app.copilot.orchestrator.planner import ExecutionStrategy, PlannedToolCall, tool_planner


_DIRECT_CASES = (
    ("VALUATION", "What is the fair price for this property?", PlannedToolCall.VALUATION_TOOL),
    ("EXPLAINABILITY", "Explain the valuation.", PlannedToolCall.EXPLAINABILITY_TOOL),
    ("COMPARABLES", "Show me nearby comparable properties.", PlannedToolCall.COMPARABLES_TOOL),
    ("FAIRNESS", "Is the asking price fair?", PlannedToolCall.FAIRNESS_TOOL),
    ("WHAT_IF", "What if I add a gym?", PlannedToolCall.WHAT_IF_TOOL),
    ("NEGOTIATION", "Should I negotiate?", PlannedToolCall.NEGOTIATION_TOOL),
    ("INVESTMENT", "Is this a good investment?", PlannedToolCall.INVESTMENT_TOOL),
    ("MARKET_INSIGHT", "What is happening in Mivida?", PlannedToolCall.MARKET_INSIGHT_TOOL),
)
_FORBIDDEN_SOURCE_TERMS = (
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
_ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "dataclasses",
    "enum",
    "hashlib",
    "json",
    "typing",
}


def _validate_source_boundary() -> tuple[list[str], list[str]]:
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "planner"
    forbidden_references: list[str] = []
    forbidden_imports: list[str] = []

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
                if module.split(".", maxsplit=1)[0] not in _ALLOWED_IMPORT_ROOTS
                and not module.startswith("app.copilot.orchestrator.intents")
                and not module.startswith("app.copilot.orchestrator.planner")
            )
    return forbidden_references, forbidden_imports


def main() -> None:
    direct_plans = {
        name: tool_planner.plan(intent_engine.classify(message))
        for name, message, _ in _DIRECT_CASES
    }
    failed_direct_cases = [
        name
        for name, _, expected_tool in _DIRECT_CASES
        if direct_plans[name].tools != (expected_tool,)
        or direct_plans[name].execution_strategy != ExecutionStrategy.SEQUENTIAL
    ]

    property_comparison = tool_planner.plan(
        intent_engine.classify("Compare these two properties.")
    )
    expected_comparison_tools = (
        PlannedToolCall.VALUATION_TOOL_PROPERTY_A,
        PlannedToolCall.VALUATION_TOOL_PROPERTY_B,
    )
    multi_intent = tool_planner.plan(
        intent_engine.classify("What is happening in Mivida and should I negotiate?")
    )
    expected_multi_intent_tools = (
        PlannedToolCall.MARKET_INSIGHT_TOOL,
        PlannedToolCall.NEGOTIATION_TOOL,
    )
    clarification = tool_planner.plan(intent_engine.classify("Tell me more"))
    deterministic_outputs = {
        json.dumps(
            tool_planner.plan(
                intent_engine.classify("What is happening in Mivida and should I negotiate?")
            ).to_dict(),
            sort_keys=True,
        )
        for _ in range(100)
    }
    forbidden_references, forbidden_imports = _validate_source_boundary()

    performance_input = intent_engine.classify(
        "What is happening in Mivida and should I negotiate?"
    )
    iterations = 20_000
    started = time.perf_counter()
    for _ in range(iterations):
        tool_planner.plan(performance_input)
    average_latency_ms = ((time.perf_counter() - started) * 1000) / iterations

    result = {
        "planner_only": not forbidden_references and not forbidden_imports,
        "direct_intent_count": len(direct_plans),
        "failed_direct_cases": failed_direct_cases,
        "property_comparison_tools": [tool.value for tool in property_comparison.tools],
        "property_comparison_parallel_groups": [
            [tool.value for tool in group]
            for group in property_comparison.parallel_groups
        ],
        "property_comparison_strategy": property_comparison.execution_strategy.value,
        "multi_intent_primary": multi_intent.primary_intent.value,
        "multi_intent_secondary": [intent.value for intent in multi_intent.secondary_intents],
        "multi_intent_tools": [tool.value for tool in multi_intent.tools],
        "multi_intent_strategy": multi_intent.execution_strategy.value,
        "clarification_primary": clarification.primary_intent.value,
        "clarification_tools": [tool.value for tool in clarification.tools],
        "clarification_strategy": clarification.execution_strategy.value,
        "clarification_required": clarification.requires_clarification,
        "deterministic_output_count": len(deterministic_outputs),
        "forbidden_source_references": forbidden_references,
        "forbidden_imports": forbidden_imports,
        "average_latency_ms": round(average_latency_ms, 6),
        "latency_target_ms": 1,
        "latency_target_passed": average_latency_ms < 1,
    }
    failures = [
        bool(failed_direct_cases),
        property_comparison.primary_intent != Intent.PROPERTY_COMPARISON,
        property_comparison.tools != expected_comparison_tools,
        property_comparison.parallel_groups != (expected_comparison_tools,),
        property_comparison.execution_strategy != ExecutionStrategy.PARALLEL,
        multi_intent.primary_intent != Intent.MARKET_INSIGHT,
        multi_intent.secondary_intents != (Intent.NEGOTIATION,),
        multi_intent.tools != expected_multi_intent_tools,
        multi_intent.parallel_groups != (expected_multi_intent_tools,),
        multi_intent.execution_strategy != ExecutionStrategy.PARALLEL,
        clarification.tools != (),
        clarification.execution_strategy != ExecutionStrategy.CLARIFICATION_REQUIRED,
        not clarification.requires_clarification,
        len(deterministic_outputs) != 1,
        bool(forbidden_references),
        bool(forbidden_imports),
        average_latency_ms >= 1,
    ]
    print(json.dumps(result, indent=2, sort_keys=True))
    if any(failures):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
