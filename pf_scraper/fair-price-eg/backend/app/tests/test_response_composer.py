from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path

from app.copilot.orchestrator.composer import (
    CompositionStatus,
    DeterministicResponseComposer,
)
from app.copilot.orchestrator.executor import (
    ExecutionAuditMetadata,
    ExecutionResult,
    ExecutionStatus,
    ToolExecutionFailure,
    ToolExecutionResult,
    ToolOrderingMetadata,
)
from app.copilot.orchestrator.intents import Intent
from app.copilot.orchestrator.planner import ExecutionStrategy, PlannedToolCall


_TIMESTAMP = datetime(2026, 6, 1, tzinfo=timezone.utc).isoformat()


def _valuation(valuation_id: str, fair_price: int, confidence: str = "High") -> dict:
    return {
        "tool_name": "valuation",
        "valuation_id": valuation_id,
        "fair_price": fair_price,
        "price_range": {"low": max(0, fair_price - 100_000), "high": fair_price + 100_000},
        "confidence_level": confidence,
        "engine_used": "CMT",
        "routing_reason": "GoldilocksZone",
        "timestamp": _TIMESTAMP,
        "source": "TruthLayer",
    }


def _comparable(index: int, *, distance_km: float | None = None) -> dict:
    return {
        "comparable_id": f"comp_{index:03d}",
        "price": 1_000_000 + index * 10_000,
        "size_sqm": 200.0 + index,
        "bedrooms": 4,
        "bathrooms": 3,
        "compound_name": "Mivida",
        "distance_km": float(index) if distance_km is None else distance_km,
        "similarity_reason": "governed evidence",
        "source": "TruthLayer",
    }


def _market_insight(*, valuation_volume: int, density_level: str) -> dict:
    return {
        "tool_name": "market_insight",
        "market_summary": "Tool-owned descriptive analytics.",
        "valuation_volume": valuation_volume,
        "confidence_distribution": {
            "valuation_count": valuation_volume,
            "counts": {},
            "predominant_level": None,
        },
        "fair_value_distribution": {
            "valuation_count": valuation_volume,
            "minimum_fair_value": None,
            "median_fair_value": None,
            "maximum_fair_value": None,
        },
        "comparable_density": {
            "valuation_count": valuation_volume,
            "minimum_comparable_count": None,
            "median_comparable_count": None,
            "maximum_comparable_count": None,
            "density_level": density_level,
            "measurement_sources": {},
        },
        "active_compounds": [],
        "active_areas": [],
        "evidence_summary": {
            "valuation_ids": [],
            "source_record_counts": {},
            "filters_used": {},
            "statements": [],
            "traceability_note": "Tool-owned descriptive analytics only.",
        },
        "data_sources_used": [],
        "timestamp": _TIMESTAMP,
        "source": "TruthLayer",
    }


def _success(planned_tool: PlannedToolCall, payload: dict, index: int = 0) -> ToolExecutionResult:
    return ToolExecutionResult(
        planned_tool=planned_tool,
        tool_name=payload["tool_name"],
        payload=payload,
        execution_time_ms=1.0,
        ordering_metadata=ToolOrderingMetadata(order_index=index, parallel_group_index=0),
    )


def _failure(planned_tool: PlannedToolCall, index: int) -> ToolExecutionFailure:
    return ToolExecutionFailure(
        planned_tool=planned_tool,
        tool_name="valuation",
        error_type="ToolResourceNotFound",
        error_message="Property not found",
        execution_time_ms=1.0,
        ordering_metadata=ToolOrderingMetadata(order_index=index, parallel_group_index=0),
    )


def _execution(
    *,
    primary_intent: Intent,
    results: tuple[ToolExecutionResult, ...] = (),
    failures: tuple[ToolExecutionFailure, ...] = (),
    status: ExecutionStatus | None = None,
    secondary_intents: tuple[Intent, ...] = (),
) -> ExecutionResult:
    executed = tuple(result.planned_tool for result in results) + tuple(
        failure.planned_tool for failure in failures
    )
    source_status = status or (
        ExecutionStatus.PARTIAL_SUCCESS
        if results and failures
        else ExecutionStatus.SUCCESS
        if results
        else ExecutionStatus.FAILED
    )
    return ExecutionResult(
        execution_id="exec_contract_fixture",
        plan_id="plan_contract_fixture",
        primary_intent=primary_intent,
        secondary_intents=secondary_intents,
        status=source_status,
        tool_results=results,
        failed_tools=failures,
        execution_time_ms=5.0,
        partial_success=bool(failures),
        audit_metadata=ExecutionAuditMetadata(
            executed_tools=executed,
            successful_tools=tuple(result.planned_tool for result in results),
            failed_tools=tuple(failure.planned_tool for failure in failures),
            execution_strategy=(
                ExecutionStrategy.PARALLEL if len(executed) > 1 else ExecutionStrategy.SEQUENTIAL
            ),
            timeout_seconds=30.0,
        ),
    )


def test_property_comparison_success_is_deterministic_and_v1_limited():
    execution = _execution(
        primary_intent=Intent.PROPERTY_COMPARISON,
        results=(
            _success(PlannedToolCall.VALUATION_TOOL_PROPERTY_A, _valuation("val_a", 1_000_000), 0),
            _success(
                PlannedToolCall.VALUATION_TOOL_PROPERTY_B,
                _valuation("val_b", 1_250_000, "Medium"),
                1,
            ),
        ),
    )

    first = DeterministicResponseComposer().compose(execution).to_dict()
    second = DeterministicResponseComposer().compose(execution).to_dict()
    comparison = first["evidence_summary"]["property_comparison"]

    assert first == second
    assert first["response_id"].startswith("response_")
    assert first["status"] == "SUCCESS"
    assert comparison["price_delta"] == 250_000
    assert comparison["price_percentage_delta"] == 25.0
    assert comparison["confidence_level_label"] == {
        "property_a": "High",
        "property_b": "Medium",
    }
    assert {
        "sqm_delta",
        "feature_delta",
        "numeric_confidence_delta",
        "winner",
        "recommendation",
    }.isdisjoint(comparison)


def test_property_comparison_partial_and_full_failures_do_not_calculate_deltas():
    successful_a = _success(PlannedToolCall.VALUATION_TOOL_PROPERTY_A, _valuation("val_a", 1_000_000))
    failed_b = _failure(PlannedToolCall.VALUATION_TOOL_PROPERTY_B, 1)
    failed_a = _failure(PlannedToolCall.VALUATION_TOOL_PROPERTY_A, 0)

    partial = DeterministicResponseComposer().compose(
        _execution(
            primary_intent=Intent.PROPERTY_COMPARISON,
            results=(successful_a,),
            failures=(failed_b,),
        )
    ).to_dict()
    failed = DeterministicResponseComposer().compose(
        _execution(
            primary_intent=Intent.PROPERTY_COMPARISON,
            failures=(failed_a, failed_b),
        )
    ).to_dict()

    assert partial["status"] == "PARTIAL_SUCCESS"
    assert failed["status"] == "FAILED"
    for response in (partial, failed):
        comparison = response["evidence_summary"]["property_comparison"]
        assert comparison["status"] == "UNAVAILABLE"
        assert "price_delta" not in comparison
        assert "price_percentage_delta" not in comparison


def test_citations_top_n_large_payload_and_arithmetic_offload():
    comparables = [_comparable(index) for index in range(49, 0, -1)]
    comparables.extend([_comparable(1), _comparable(2)])
    comparables[0]["distance_km"] = 0.5
    comparables[0]["comparable_id"] = "comp_tie_b"
    comparables[1]["distance_km"] = 0.5
    comparables[1]["comparable_id"] = "comp_tie_a"
    payload = {
        "tool_name": "comparable",
        "valuation_id": "val_comparable",
        "tool_event_id": "event_1",
        "tool_event_ids": ["event_1", "event_2"],
        "comparable_count": len(comparables),
        "comparables": comparables,
        "timestamp": _TIMESTAMP,
        "source": "TruthLayer",
    }
    response = DeterministicResponseComposer().compose(
        _execution(
            primary_intent=Intent.COMPARABLES,
            results=(_success(PlannedToolCall.COMPARABLES_TOOL, payload),),
        )
    ).to_dict()
    summary = response["evidence_summary"]["tool_summaries"][0]["summary"]["comparables"]
    top_ids = [item["comparable_id"] for item in summary["top_comparables"]]

    assert summary["statistics"] == {
        "comparable_count": 51,
        "average_price": round(sum(item["price"] for item in comparables) / 51, 4),
        "minimum_price": min(item["price"] for item in comparables),
        "maximum_price": max(item["price"] for item in comparables),
    }
    assert top_ids == ["comp_tie_a", "comp_tie_b", "comp_001"]
    assert len(response["frontend_payload"]["full_evidence"]["comparables"]) == 51
    assert response["citation_package"]["tool_event_ids"] == ["event_1", "event_2"]
    assert response["citation_package"]["comparable_ids"].count("comp_001") == 1
    assert response["compressed_context"]["compression_disclosures"][0]["truncated"] is True


def test_sparse_clarification_and_multi_intent_statuses_are_preserved():
    sparse = DeterministicResponseComposer().compose(
        _execution(
            primary_intent=Intent.MARKET_INSIGHT,
            results=(
                _success(
                    PlannedToolCall.MARKET_INSIGHT_TOOL,
                    _market_insight(valuation_volume=0, density_level="Insufficient Evidence"),
                ),
            ),
        )
    )
    clarification = DeterministicResponseComposer().compose(
        _execution(
            primary_intent=Intent.GENERAL_QUESTION,
            status=ExecutionStatus.CLARIFICATION_REQUIRED,
        )
    )
    multi = DeterministicResponseComposer().compose(
        _execution(
            primary_intent=Intent.VALUATION,
            secondary_intents=(Intent.MARKET_INSIGHT,),
            results=(
                _success(PlannedToolCall.VALUATION_TOOL, _valuation("val_multi", 1_000_000), 0),
                _success(
                    PlannedToolCall.MARKET_INSIGHT_TOOL,
                    _market_insight(valuation_volume=1, density_level="High"),
                    1,
                ),
            ),
        )
    )

    assert sparse.status == CompositionStatus.SPARSE_EVIDENCE
    assert clarification.status == CompositionStatus.CLARIFICATION_REQUIRED
    assert multi.status == CompositionStatus.SUCCESS
    assert multi.secondary_intents == (Intent.MARKET_INSIGHT,)
    assert multi.compressed_context["intent"]["secondary"] == ["MARKET_INSIGHT"]


def test_malformed_successful_payload_fails_closed():
    malformed = {
        "tool_name": "valuation",
        "valuation_id": "val_missing_required_fields",
    }

    response = DeterministicResponseComposer().compose(
        _execution(
            primary_intent=Intent.VALUATION,
            results=(_success(PlannedToolCall.VALUATION_TOOL, malformed),),
        )
    )

    assert response.status == CompositionStatus.FAILED
    assert response.evidence_summary["tool_summaries"] == []
    assert response.evidence_summary["failed_tools"][0]["failure_category"] == (
        "COMPOSER_NORMALIZATION_FAILURE"
    )


def test_composer_source_preserves_phase_boundary():
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "composer"
    source = "\n".join(
        source_path.read_text(encoding="utf-8").casefold()
        for source_path in package_root.glob("*.py")
    )
    forbidden_terms = (
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

    assert [term for term in forbidden_terms if term in source] == []
    assert ".query(" not in source


def test_composer_imports_do_not_include_forbidden_dependencies():
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "composer"
    forbidden_import_roots = {
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
