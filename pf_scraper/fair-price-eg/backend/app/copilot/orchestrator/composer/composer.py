from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

from pydantic import BaseModel, ValidationError

from app.api.schemas.copilot_tools import (
    ComparableToolResponse,
    ExplainabilityToolResponse,
    FairnessToolResponse,
    InvestmentToolResponse,
    MarketInsightToolResponse,
    NegotiationToolResponse,
    ValuationToolResponse,
    WhatIfToolResponse,
)
from app.copilot.orchestrator.composer.contracts import ComposedResponse, CompositionStatus
from app.copilot.orchestrator.executor.contracts import (
    ExecutionResult,
    ExecutionStatus,
    ToolExecutionFailure,
    ToolExecutionResult,
)
from app.copilot.orchestrator.intents import Intent
from app.copilot.orchestrator.planner import PlannedToolCall


SCHEMA_VERSION = "1.0"
TOP_N_COMPARABLES = 3
TOP_N_FEATURE_DRIVERS = 3
TOP_N_MARKET_ITEMS = 3


class ComposerNormalizationError(ValueError):
    pass


@dataclass(frozen=True)
class _ToolBinding:
    tool_name: str
    response_model: type[BaseModel]


@dataclass(frozen=True)
class _NormalizedToolOutput:
    planned_tool: PlannedToolCall
    tool_name: str
    payload: dict[str, Any]
    ordering_metadata: dict[str, Any]


_TOOL_BINDINGS = {
    PlannedToolCall.VALUATION_TOOL: _ToolBinding("valuation", ValuationToolResponse),
    PlannedToolCall.EXPLAINABILITY_TOOL: _ToolBinding("explainability", ExplainabilityToolResponse),
    PlannedToolCall.COMPARABLES_TOOL: _ToolBinding("comparable", ComparableToolResponse),
    PlannedToolCall.FAIRNESS_TOOL: _ToolBinding("fairness", FairnessToolResponse),
    PlannedToolCall.WHAT_IF_TOOL: _ToolBinding("what_if", WhatIfToolResponse),
    PlannedToolCall.NEGOTIATION_TOOL: _ToolBinding("negotiation", NegotiationToolResponse),
    PlannedToolCall.INVESTMENT_TOOL: _ToolBinding("investment", InvestmentToolResponse),
    PlannedToolCall.MARKET_INSIGHT_TOOL: _ToolBinding("market_insight", MarketInsightToolResponse),
    PlannedToolCall.VALUATION_TOOL_PROPERTY_A: _ToolBinding("valuation", ValuationToolResponse),
    PlannedToolCall.VALUATION_TOOL_PROPERTY_B: _ToolBinding("valuation", ValuationToolResponse),
}


def _stable_response_id(execution_result: ExecutionResult) -> str:
    serialized = json.dumps(
        execution_result.to_dict(),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return f"response_{digest}"


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _ordering_metadata(result: ToolExecutionResult | ToolExecutionFailure) -> dict[str, Any]:
    return result.ordering_metadata.to_dict()


def _comparable_statistics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    prices = [row["price"] for row in rows if _is_number(row.get("price"))]
    return {
        "comparable_count": len(prices),
        "average_price": round(sum(prices) / len(prices), 4) if prices else None,
        "minimum_price": min(prices) if prices else None,
        "maximum_price": max(prices) if prices else None,
    }


def _comparable_context(
    planned_tool: PlannedToolCall,
    rows: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    eligible = [
        row
        for row in rows
        if isinstance(row.get("comparable_id"), str)
        and row["comparable_id"]
        and _is_number(row.get("distance_km"))
    ]
    ordered = sorted(eligible, key=lambda row: (row["distance_km"], row["comparable_id"]))
    top_rows = ordered[:TOP_N_COMPARABLES]
    disclosure = {
        "category": f"{planned_tool.value}.comparables",
        "received_count": len(rows),
        "eligible_count": len(eligible),
        "shown_count": len(top_rows),
        "excluded_from_top_n_count": len(rows) - len(eligible),
        "truncated": len(eligible) > TOP_N_COMPARABLES,
        "ordering": ["distance_km ASC", "comparable_id ASC"],
    }
    return {
        "statistics": _comparable_statistics(rows),
        "top_comparables": top_rows,
    }, disclosure


def _normalized_comparables(output: _NormalizedToolOutput) -> list[dict[str, Any]]:
    payload = output.payload
    if output.tool_name == "comparable":
        return [dict(item) for item in payload["comparables"]]
    if output.tool_name == "explainability":
        return [
            {
                "comparable_id": item["property_id"],
                "price": item["price"],
                "size_sqm": item["size_sqm"],
                "bedrooms": item["bedrooms"],
                "bathrooms": item["bathrooms"],
                "compound_name": item.get("compound_name"),
                "distance_km": item["distance_km"],
                "similarity_reason": item.get("similarity_reason"),
            }
            for item in payload["comparable_evidence"]
        ]
    if output.tool_name == "what_if":
        return [dict(item) for item in payload["comparables"]["comparables"]]
    return []


def _compressed_feature_drivers(payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    positive = []
    negative = []
    for driver in payload.get("feature_drivers", []):
        if driver.get("direction") == "Positive" and len(positive) < TOP_N_FEATURE_DRIVERS:
            positive.append(driver)
        elif driver.get("direction") == "Negative" and len(negative) < TOP_N_FEATURE_DRIVERS:
            negative.append(driver)
    return {"positive": positive, "negative": negative}


def _observed_price_statistics(payload: dict[str, Any]) -> dict[str, Any]:
    return _comparable_statistics(
        [{"price": price} for price in payload["comparable_summary"]["observed_prices"]]
    )


def _normalized_failure(failure: ToolExecutionFailure) -> dict[str, Any]:
    if failure.error_type == "ToolTimeoutError":
        category = "TOOL_TIMEOUT"
    elif failure.error_type == "MissingToolInputError":
        category = "MISSING_TOOL_INPUT"
    else:
        category = "TOOL_FAILURE"
    return {
        "planned_tool": failure.planned_tool.value,
        "tool_name": failure.tool_name,
        "error_type": failure.error_type,
        "failure_category": category,
        "ordering_metadata": _ordering_metadata(failure),
    }


def _normalization_failure(result: ToolExecutionResult) -> dict[str, Any]:
    return {
        "planned_tool": result.planned_tool.value,
        "tool_name": result.tool_name,
        "error_type": "ComposerNormalizationError",
        "failure_category": "COMPOSER_NORMALIZATION_FAILURE",
        "ordering_metadata": _ordering_metadata(result),
    }


class DeterministicResponseComposer:
    def compose(self, execution_result: ExecutionResult) -> ComposedResponse:
        if not isinstance(execution_result, ExecutionResult):
            raise TypeError("execution_result must be an ExecutionResult")

        normalized_outputs = []
        normalization_failures = []
        for result in execution_result.tool_results:
            try:
                normalized_outputs.append(self._normalize(result))
            except ComposerNormalizationError:
                normalization_failures.append(_normalization_failure(result))

        source_failures = [_normalized_failure(failure) for failure in execution_result.failed_tools]
        failures = [*source_failures, *normalization_failures]
        citations = self._citation_package(execution_result.tool_results)
        tool_summaries, disclosures = self._tool_summaries(normalized_outputs)
        property_comparison = self._property_comparison(execution_result, normalized_outputs)
        sparse_evidence = self._sparse_evidence(normalized_outputs)
        conflicts = self._evidence_conflicts(normalized_outputs)
        status = self._status(execution_result, normalized_outputs, failures, sparse_evidence, conflicts)
        evidence_summary = {
            "tool_summaries": tool_summaries,
            "property_comparison": property_comparison,
            "sparse_evidence": sparse_evidence,
            "evidence_conflicts": conflicts,
            "failed_tools": failures,
        }
        frontend_payload = {
            "schema_version": SCHEMA_VERSION,
            "composition_status": status.value,
            "tool_outputs": [self._frontend_tool_output(output) for output in normalized_outputs],
            "failed_tools": failures,
            "full_evidence": self._full_evidence(normalized_outputs),
            "citations": citations,
        }
        compressed_context = {
            "schema_version": SCHEMA_VERSION,
            "composition_status": status.value,
            "intent": {
                "primary": execution_result.primary_intent.value,
                "secondary": [intent.value for intent in execution_result.secondary_intents],
            },
            "evidence": {
                "tool_summaries": tool_summaries,
                "property_comparison": property_comparison,
                "sparse_evidence": sparse_evidence,
                "evidence_conflicts": conflicts,
            },
            "failures": failures,
            "compression_disclosures": disclosures,
        }
        return ComposedResponse(
            response_id=_stable_response_id(execution_result),
            execution_id=execution_result.execution_id,
            plan_id=execution_result.plan_id,
            primary_intent=execution_result.primary_intent,
            secondary_intents=execution_result.secondary_intents,
            status=status,
            evidence_summary=evidence_summary,
            citation_package=citations,
            compressed_context=compressed_context,
            frontend_payload=frontend_payload,
            composer_metadata={
                "schema_version": SCHEMA_VERSION,
                "composer_mode": "DETERMINISTIC_ONLY",
                "source_execution_status": execution_result.status.value,
                "arithmetic_authority": "RESPONSE_COMPOSER",
                "composition_time_ms": 0.0,
                "warnings": [
                    failure["failure_category"]
                    for failure in normalization_failures
                ],
            },
        )

    @staticmethod
    def _normalize(result: ToolExecutionResult) -> _NormalizedToolOutput:
        binding = _TOOL_BINDINGS.get(result.planned_tool)
        if binding is None or binding.tool_name != result.tool_name:
            raise ComposerNormalizationError("Successful Tool envelope does not match an approved Tool binding")
        try:
            payload = binding.response_model.model_validate(result.payload).model_dump(mode="json")
        except ValidationError as exc:
            raise ComposerNormalizationError("Successful Tool payload does not match its approved schema") from exc
        return _NormalizedToolOutput(
            planned_tool=result.planned_tool,
            tool_name=result.tool_name,
            payload=payload,
            ordering_metadata=_ordering_metadata(result),
        )

    def _tool_summaries(
        self,
        outputs: list[_NormalizedToolOutput],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        summaries = []
        disclosures = []
        for output in outputs:
            summary, output_disclosures = self._tool_summary(output)
            summaries.append(
                {
                    "planned_tool": output.planned_tool.value,
                    "tool_name": output.tool_name,
                    "status": "SUCCESS",
                    "summary": summary,
                }
            )
            disclosures.extend(output_disclosures)
        return summaries, disclosures

    def _tool_summary(
        self,
        output: _NormalizedToolOutput,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        payload = output.payload
        if output.tool_name == "valuation":
            return {
                "valuation_id": payload["valuation_id"],
                "fair_price": payload["fair_price"],
                "price_range": payload["price_range"],
                "confidence_level": payload["confidence_level"],
                "engine_used": payload["engine_used"],
                "routing_reason": payload["routing_reason"],
                "source": payload["source"],
            }, []
        if output.tool_name == "explainability":
            comparables, disclosure = _comparable_context(output.planned_tool, _normalized_comparables(output))
            return {
                "valuation_id": payload["valuation_id"],
                "fairness_status": payload["fairness_status"],
                "feature_drivers": _compressed_feature_drivers(payload),
                "comparables": comparables,
                "source": payload["source"],
            }, [disclosure]
        if output.tool_name == "comparable":
            comparables, disclosure = _comparable_context(output.planned_tool, _normalized_comparables(output))
            return {
                "valuation_id": payload["valuation_id"],
                "comparables": comparables,
                "source": payload["source"],
            }, [disclosure]
        if output.tool_name == "fairness":
            return {
                "valuation_id": payload["valuation_id"],
                "fair_price": payload["fair_price"],
                "target_price": payload["target_price"],
                "fairness_status": payload["fairness_status"],
                "confidence_level": payload["confidence_level"],
                "source": payload["source"],
            }, []
        if output.tool_name == "what_if":
            comparables, disclosure = _comparable_context(output.planned_tool, _normalized_comparables(output))
            return {
                "base_valuation": payload["base_valuation"],
                "scenario_valuation": payload["scenario_valuation"],
                "base_valuation_id": payload["base_valuation_id"],
                "scenario_valuation_id": payload["scenario_valuation_id"],
                "fairness_valuation_id": payload["fairness_valuation_id"],
                "delta_value": payload["delta_value"],
                "delta_percentage": payload["delta_percentage"],
                "fairness_status": payload["fairness_status"],
                "confidence_level": payload["confidence_level"],
                "assumptions_used": payload["assumptions_used"],
                "feature_changes": payload["feature_changes"],
                "comparables": comparables,
                "source": payload["source"],
            }, [disclosure]
        if output.tool_name == "negotiation":
            return {
                "valuation_id": payload["valuation_id"],
                "asking_price": payload["asking_price"],
                "fair_price": payload["fair_price"],
                "fairness_status": payload["fairness_status"],
                "price_gap": payload["price_gap"],
                "price_gap_percentage": payload["price_gap_percentage"],
                "confidence_level": payload["confidence_level"],
                "negotiation_position": payload["negotiation_position"],
                "comparable_statistics": _observed_price_statistics(payload),
                "recommended_offer_band": {
                    "low": payload["recommended_offer_band"]["low"],
                    "high": payload["recommended_offer_band"]["high"],
                    "comparable_ids_used": payload["recommended_offer_band"]["comparable_ids_used"],
                    "source": payload["recommended_offer_band"]["source"],
                },
                "source": payload["source"],
            }, []
        if output.tool_name == "investment":
            return {
                "valuation_id": payload["valuation_id"],
                "asking_price": payload["asking_price"],
                "fair_price": payload["fair_price"],
                "fairness_status": payload["fairness_status"],
                "price_gap": payload["price_gap"],
                "price_gap_percentage": payload["price_gap_percentage"],
                "investment_position": payload["investment_position"],
                "confidence_level": payload["confidence_level"],
                "comparable_statistics": _observed_price_statistics(payload),
                "negotiation_summary": {
                    "negotiation_position": payload["negotiation_summary"]["negotiation_position"],
                    "recommended_offer_band": {
                        "low": payload["negotiation_summary"]["recommended_offer_band"]["low"],
                        "high": payload["negotiation_summary"]["recommended_offer_band"]["high"],
                        "comparable_ids_used": payload["negotiation_summary"]["recommended_offer_band"][
                            "comparable_ids_used"
                        ],
                        "source": payload["negotiation_summary"]["recommended_offer_band"]["source"],
                    },
                    "source": payload["negotiation_summary"]["source"],
                },
                "what_if_summary": payload["what_if_summary"],
                "source": payload["source"],
            }, []
        if output.tool_name == "market_insight":
            disclosures = [
                self._list_disclosure(output.planned_tool, "active_compounds", payload["active_compounds"]),
                self._list_disclosure(output.planned_tool, "active_areas", payload["active_areas"]),
                self._list_disclosure(
                    output.planned_tool,
                    "evidence_statements",
                    payload["evidence_summary"]["statements"],
                ),
            ]
            return {
                "valuation_volume": payload["valuation_volume"],
                "confidence_distribution": payload["confidence_distribution"],
                "fair_value_distribution": payload["fair_value_distribution"],
                "comparable_density": payload["comparable_density"],
                "active_compounds": payload["active_compounds"][:TOP_N_MARKET_ITEMS],
                "active_areas": payload["active_areas"][:TOP_N_MARKET_ITEMS],
                "evidence_summary": {
                    "valuation_ids": payload["evidence_summary"]["valuation_ids"],
                    "source_record_counts": payload["evidence_summary"]["source_record_counts"],
                    "filters_used": payload["evidence_summary"]["filters_used"],
                    "statements": payload["evidence_summary"]["statements"][:TOP_N_MARKET_ITEMS],
                },
                "data_sources_used": payload["data_sources_used"],
                "source": payload["source"],
            }, disclosures
        raise ComposerNormalizationError("Approved Tool binding has no summary normalizer")

    @staticmethod
    def _list_disclosure(
        planned_tool: PlannedToolCall,
        category: str,
        values: list[Any],
    ) -> dict[str, Any]:
        return {
            "category": f"{planned_tool.value}.{category}",
            "received_count": len(values),
            "shown_count": min(len(values), TOP_N_MARKET_ITEMS),
            "truncated": len(values) > TOP_N_MARKET_ITEMS,
            "ordering": ["Tool-owned source order"],
        }

    @staticmethod
    def _frontend_tool_output(output: _NormalizedToolOutput) -> dict[str, Any]:
        return {
            "planned_tool": output.planned_tool.value,
            "tool_name": output.tool_name,
            "payload": output.payload,
            "ordering_metadata": output.ordering_metadata,
        }

    @staticmethod
    def _full_evidence(outputs: list[_NormalizedToolOutput]) -> dict[str, Any]:
        comparables = []
        feature_drivers = []
        market_insights = []
        for output in outputs:
            comparables.extend(
                {
                    "planned_tool": output.planned_tool.value,
                    "comparable": row,
                }
                for row in _normalized_comparables(output)
            )
            if output.tool_name == "explainability":
                feature_drivers.extend(
                    {
                        "planned_tool": output.planned_tool.value,
                        "feature_driver": driver,
                    }
                    for driver in output.payload["feature_drivers"]
                )
            elif output.tool_name == "what_if":
                feature_drivers.extend(
                    {
                        "planned_tool": output.planned_tool.value,
                        "feature_driver": driver,
                    }
                    for driver in output.payload["explainability"]["feature_drivers"]
                )
            elif output.tool_name == "market_insight":
                market_insights.append(
                    {
                        "planned_tool": output.planned_tool.value,
                        "active_compounds": output.payload["active_compounds"],
                        "active_areas": output.payload["active_areas"],
                        "statements": output.payload["evidence_summary"]["statements"],
                    }
                )
        return {
            "comparables": comparables,
            "feature_drivers": feature_drivers,
            "market_insights": market_insights,
        }

    @staticmethod
    def _property_comparison(
        execution_result: ExecutionResult,
        outputs: list[_NormalizedToolOutput],
    ) -> dict[str, Any] | None:
        intents = (execution_result.primary_intent, *execution_result.secondary_intents)
        if Intent.PROPERTY_COMPARISON not in intents:
            return None
        by_slot = {output.planned_tool: output for output in outputs}
        available_slots = []
        failed_slots = []
        for slot_name, planned_tool in (
            ("PROPERTY_A", PlannedToolCall.VALUATION_TOOL_PROPERTY_A),
            ("PROPERTY_B", PlannedToolCall.VALUATION_TOOL_PROPERTY_B),
        ):
            if planned_tool in by_slot:
                available_slots.append(slot_name)
            else:
                failed_slots.append(slot_name)
        if failed_slots:
            return {
                "status": "UNAVAILABLE",
                "unavailable_reason_code": "PROPERTY_COMPARISON_REQUIRES_TWO_SUCCESSFUL_VALUATIONS",
                "available_slots": available_slots,
                "failed_slots": failed_slots,
            }
        property_a = by_slot[PlannedToolCall.VALUATION_TOOL_PROPERTY_A].payload
        property_b = by_slot[PlannedToolCall.VALUATION_TOOL_PROPERTY_B].payload
        price_delta = property_b["fair_price"] - property_a["fair_price"]
        comparison = {
            "status": "AVAILABLE",
            "property_a": {
                "valuation_id": property_a["valuation_id"],
                "fair_price": property_a["fair_price"],
                "confidence_level_label": property_a["confidence_level"],
            },
            "property_b": {
                "valuation_id": property_b["valuation_id"],
                "fair_price": property_b["fair_price"],
                "confidence_level_label": property_b["confidence_level"],
            },
            "price_delta": price_delta,
            "price_percentage_delta": (
                round((price_delta / property_a["fair_price"]) * 100, 4)
                if property_a["fair_price"]
                else None
            ),
            "confidence_level_label": {
                "property_a": property_a["confidence_level"],
                "property_b": property_b["confidence_level"],
            },
        }
        if not property_a["fair_price"]:
            comparison["percentage_unavailable_reason_code"] = "PROPERTY_A_FAIR_PRICE_ZERO"
        return comparison

    @staticmethod
    def _sparse_evidence(outputs: list[_NormalizedToolOutput]) -> list[dict[str, Any]]:
        sparse = []
        for output in outputs:
            payload = output.payload
            reason = None
            if output.tool_name == "comparable" and payload["comparable_count"] == 0:
                reason = "COMPARABLE_COUNT_ZERO"
            elif output.tool_name == "what_if" and payload["comparables"]["comparable_count"] == 0:
                reason = "WHAT_IF_COMPARABLE_COUNT_ZERO"
            elif output.tool_name == "negotiation" and payload["comparable_summary"]["comparable_count"] == 0:
                reason = "NEGOTIATION_COMPARABLE_COUNT_ZERO"
            elif output.tool_name == "investment" and payload["comparable_summary"]["comparable_count"] == 0:
                reason = "INVESTMENT_COMPARABLE_COUNT_ZERO"
            elif output.tool_name == "market_insight" and payload["valuation_volume"] == 0:
                reason = "MARKET_INSIGHT_VALUATION_VOLUME_ZERO"
            elif (
                output.tool_name == "market_insight"
                and payload["comparable_density"]["density_level"] in {"Sparse", "Insufficient Evidence"}
            ):
                reason = "MARKET_INSIGHT_COMPARABLE_DENSITY_SPARSE"
            if reason is not None:
                sparse.append(
                    {
                        "planned_tool": output.planned_tool.value,
                        "tool_name": output.tool_name,
                        "reason_code": reason,
                    }
                )
        return sparse

    @staticmethod
    def _evidence_conflicts(outputs: list[_NormalizedToolOutput]) -> list[dict[str, Any]]:
        values: dict[tuple[str, str], list[int]] = {}
        for output in outputs:
            valuation_id = output.payload.get("valuation_id")
            fair_price = output.payload.get("fair_price")
            if isinstance(valuation_id, str) and isinstance(fair_price, int):
                values.setdefault((valuation_id, "fair_price"), []).append(fair_price)
        conflicts = []
        for (valuation_id, field), received in values.items():
            unique_values = list(dict.fromkeys(received))
            if len(unique_values) > 1:
                conflicts.append(
                    {
                        "valuation_id": valuation_id,
                        "field": field,
                        "received_values": unique_values,
                        "resolution": "UNRESOLVED",
                    }
                )
        return conflicts

    @staticmethod
    def _citation_package(results: tuple[ToolExecutionResult, ...]) -> dict[str, Any]:
        valuation_ids = []
        tool_event_ids = []
        comparable_ids = []

        def append(values: list[str], value: Any) -> None:
            if isinstance(value, str) and value:
                values.append(value)

        def walk(value: Any) -> None:
            if isinstance(value, dict):
                comparable_evidence = value.get("comparable_evidence")
                if isinstance(comparable_evidence, list):
                    for item in comparable_evidence:
                        if isinstance(item, dict):
                            append(comparable_ids, item.get("property_id"))
                for key, item in value.items():
                    if key in {"valuation_id", "base_valuation_id", "scenario_valuation_id", "fairness_valuation_id"}:
                        append(valuation_ids, item)
                    elif key == "valuation_ids" and isinstance(item, list):
                        for identifier in item:
                            append(valuation_ids, identifier)
                    elif key == "tool_event_id":
                        append(tool_event_ids, item)
                    elif key == "tool_event_ids" and isinstance(item, list):
                        for identifier in item:
                            append(tool_event_ids, identifier)
                    elif key == "comparable_id":
                        append(comparable_ids, item)
                    elif key in {"comparable_ids", "comparable_ids_used"} and isinstance(item, list):
                        for identifier in item:
                            append(comparable_ids, identifier)
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        for result in results:
            walk(result.payload)
        valuation_ids = _unique(valuation_ids)
        tool_event_ids = _unique(tool_event_ids)
        comparable_ids = _unique(comparable_ids)
        unavailable = []
        if not tool_event_ids:
            unavailable.append("tool_event_id")
        if not comparable_ids:
            unavailable.append("comparable_id")
        return {
            "valuation_ids": valuation_ids,
            "tool_event_ids": tool_event_ids,
            "comparable_ids": comparable_ids,
            "unavailable_optional_citation_types": unavailable,
        }

    @staticmethod
    def _status(
        execution_result: ExecutionResult,
        outputs: list[_NormalizedToolOutput],
        failures: list[dict[str, Any]],
        sparse_evidence: list[dict[str, Any]],
        conflicts: list[dict[str, Any]],
    ) -> CompositionStatus:
        if execution_result.status == ExecutionStatus.CLARIFICATION_REQUIRED:
            return CompositionStatus.CLARIFICATION_REQUIRED
        if not outputs:
            return CompositionStatus.FAILED
        if failures or conflicts:
            return CompositionStatus.PARTIAL_SUCCESS
        if sparse_evidence:
            return CompositionStatus.SPARSE_EVIDENCE
        return CompositionStatus.SUCCESS


response_composer = DeterministicResponseComposer()
