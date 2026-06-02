from __future__ import annotations

import json
from typing import Any

from app.broker.schemas.contracts import (
    BrokerComparableEvidence,
    BrokerContext,
    BrokerEvidenceRef,
    BrokerIntent,
    BrokerSessionSnapshot,
    BrokerTokenBudget,
    BrokerToolName,
    BrokerToolResult,
    BrokerValuationSummary,
    ToolExecutionStatus,
)
from app.core.config import settings


def _estimate_tokens(payload: dict[str, Any]) -> int:
    return max(1, len(json.dumps(payload, default=str)) // 4)


def _tool_data(results: list[BrokerToolResult], tool_name: BrokerToolName) -> dict[str, Any]:
    for result in results:
        if result.tool_name == tool_name and result.status == ToolExecutionStatus.SUCCESS:
            return result.data
    return {}


class BrokerContextAssembler:
    def assemble(
        self,
        *,
        intent: BrokerIntent,
        session: BrokerSessionSnapshot,
        message: str,
        tool_results: list[BrokerToolResult],
        dialogue_context: dict[str, Any] | None = None,
    ) -> BrokerContext:
        valuation_data = _tool_data(tool_results, BrokerToolName.VALUATION_ANALYSIS).get("valuation")
        explainability_data = _tool_data(tool_results, BrokerToolName.EXPLAINABILITY)

        valuation_summary = None
        evidence: list[BrokerEvidenceRef] = []
        comparable_evidence: list[BrokerComparableEvidence] = []
        confidence_factors: dict[str, float] = {}
        explainability_trace: list[dict[str, Any]] = []
        valuation_contract: dict[str, Any] = {}
        amenity_intelligence: dict[str, Any] = {}
        district_data: dict[str, Any] = {}

        if valuation_data:
            price_range = valuation_data["price_range"]
            valuation_summary = BrokerValuationSummary(
                valuation_id=str(valuation_data["valuation_id"]),
                fair_price_egp=int(valuation_data["fair_price"]),
                range_low_egp=int(price_range["low"]),
                range_high_egp=int(price_range["high"]),
                confidence_label=str(valuation_data["confidence_level"]),
                engine_used=str(valuation_data["engine_used"]),
                routing_reason=str(valuation_data["routing_reason"]),
                source=str(valuation_data["source"]),
                fairness_status=explainability_data.get("fairness_status"),
                why_this_price=explainability_data.get("why_this_price"),
                strongest_factors=explainability_data.get("strongest_factors"),
                confidence_reason=explainability_data.get("confidence_reason"),
            )
            evidence.append(
                BrokerEvidenceRef(
                    evidence_id="valuation.authoritative",
                    source=BrokerToolName.VALUATION_ANALYSIS,
                    kind="truth_layer_valuation",
                    summary="Authoritative TruthLayer valuation returned by Copilot Valuation Tool.",
                    payload=valuation_summary.model_dump(mode="json"),
                )
            )

        if explainability_data:
            evidence.append(
                BrokerEvidenceRef(
                    evidence_id="explainability.truth_layer",
                    source=BrokerToolName.EXPLAINABILITY,
                    kind="truth_layer_explainability",
                    summary="TruthLayer explanation returned by Copilot Explainability Tool.",
                    payload=explainability_data,
                )
            )

        for comp in (explainability_data.get("comparable_evidence") or [])[: settings.BROKER_MAX_CONTEXT_COMPS]:
            listing_id = str(comp.get("property_id"))
            evidence_id = f"comp.{listing_id}"
            comparable_evidence.append(
                BrokerComparableEvidence(
                    evidence_id=evidence_id,
                    listing_id=listing_id,
                    price_egp=int(comp.get("price")),
                    size_sqm=float(comp["size_sqm"]) if comp.get("size_sqm") is not None else None,
                    bedrooms=comp.get("bedrooms"),
                    bathrooms=comp.get("bathrooms"),
                    distance_m=float(comp["distance_km"]) * 1000 if comp.get("distance_km") is not None else None,
                    similarity_score=(
                        float(comp["similarity_score"]) if comp.get("similarity_score") is not None else None
                    ),
                    listing_date=comp.get("listing_date"),
                )
            )
            evidence.append(
                BrokerEvidenceRef(
                    evidence_id=evidence_id,
                    source=BrokerToolName.EXPLAINABILITY,
                    kind="truth_layer_comparable",
                    summary=f"TruthLayer comparable listing {listing_id} at {comp.get('price')} EGP.",
                    payload=comp,
                )
            )

        session_state = {
            "previous_request_count": len(session.previous_requests),
            "previous_valuation_count": len(session.previous_valuations),
            "active_district": session.active_district,
            "investor_preferences": (
                session.investor_preferences.model_dump(mode="json")
                if session.investor_preferences is not None
                else None
            ),
            "dialogue": dialogue_context or {},
        }

        context_payload = {
            "intent": intent.value,
            "session_id": session.session_id,
            "valuation_summary": valuation_summary.model_dump(mode="json") if valuation_summary else None,
            "comparable_evidence": [item.model_dump(mode="json") for item in comparable_evidence],
            "confidence_factors": confidence_factors,
            "explainability": explainability_data,
            "valuation_contract": valuation_contract,
            "amenity_intelligence": amenity_intelligence,
            "district_intelligence": district_data,
            "session_state": session_state,
        }
        estimated_tokens = _estimate_tokens(context_payload)

        return BrokerContext(
            intent=intent,
            session_id=session.session_id,
            user_message=message,
            valuation_summary=valuation_summary,
            comparable_evidence=comparable_evidence,
            confidence_factors=confidence_factors,
            explainability_trace=explainability_trace,
            explainability=explainability_data,
            valuation_contract=valuation_contract,
            amenity_intelligence=amenity_intelligence,
            district_intelligence=district_data,
            market_signals=list(district_data.get("market_signals") or []),
            session_state=session_state,
            evidence=evidence,
            token_budget=BrokerTokenBudget(
                max_context_tokens=settings.BROKER_MAX_CONTEXT_TOKENS,
                estimated_context_tokens=estimated_tokens,
                truncated=(
                    len(explainability_data.get("comparable_evidence") or []) > settings.BROKER_MAX_CONTEXT_COMPS
                ),
            ),
            deterministic_authority={
                "source_of_truth": "copilot_tool_layer",
                "valuation_tool": "valuation",
                "explainability_tool": "explainability",
                "valuation_id": valuation_summary.valuation_id if valuation_summary else None,
                "llm_may_override": False,
                "valuation_must_match_engine": True,
                "confidence_must_match_engine": True,
            },
        )


context_assembler = BrokerContextAssembler()
