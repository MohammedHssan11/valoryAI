from __future__ import annotations

import time

from sqlalchemy.orm import Session

from app.api.schemas.pricing import RentFairPriceResponse
from app.broker.schemas.contracts import (
    BrokerToolName,
    BrokerToolResult,
    ComparableAnalysisToolRequest,
    ComparableAnalysisToolResponse,
    ConfidenceAnalysisToolRequest,
    ConfidenceAnalysisToolResponse,
    DistrictIntelligenceToolRequest,
    DistrictIntelligenceToolResponse,
    ExplainabilityToolRequest,
    ExplainabilityToolResponse,
    ToolExecutionStatus,
    ValuationAnalysisToolResponse,
)
from app.broker.tools.base import BrokerTool


def _success_result(tool_name: BrokerToolName, start: float, data, evidence_ids: list[str]) -> BrokerToolResult:
    return BrokerToolResult(
        tool_name=tool_name,
        status=ToolExecutionStatus.SUCCESS,
        duration_ms=round((time.perf_counter() - start) * 1000, 2),
        evidence_ids=evidence_ids,
        data=data.model_dump(mode="json"),
    )


def _prices(top_comps) -> list[int]:
    return [int(comp.price_egp) for comp in top_comps if comp.price_egp is not None]


class ComparableAnalysisTool(BrokerTool):
    name = BrokerToolName.COMPARABLE_ANALYSIS
    description = "Summarizes deterministic comparable evidence returned by the valuation engine."

    def execute(self, *, db: Session, valuation: RentFairPriceResponse | None = None, **kwargs) -> BrokerToolResult:
        start = time.perf_counter()
        if valuation is None:
            return BrokerToolResult(
                tool_name=self.name,
                status=ToolExecutionStatus.SKIPPED,
                duration_ms=0,
                warnings=["Valuation evidence is required before comparable analysis."],
            )
        request = ComparableAnalysisToolRequest(valuation=valuation)
        prices = _prices(request.valuation.top_comps)
        evidence_ids = [f"comp.{comp.listing_id}" for comp in request.valuation.top_comps]
        response = ComparableAnalysisToolResponse(
            comps_count=request.valuation.comps_count,
            tier_used=request.valuation.tier_used,
            top_comps=request.valuation.top_comps,
            price_points_egp=prices,
            min_price_egp=min(prices) if prices else None,
            max_price_egp=max(prices) if prices else None,
            evidence_ids=evidence_ids,
        )
        return _success_result(self.name, start, response, evidence_ids)


class ExplainabilityTool(BrokerTool):
    name = BrokerToolName.EXPLAINABILITY
    description = "Packages the TruthLayer explanation already retrieved through Copilot Explainability Tool."

    def execute(self, *, db: Session, valuation: ValuationAnalysisToolResponse | None = None, **kwargs) -> BrokerToolResult:
        start = time.perf_counter()
        if valuation is None:
            return BrokerToolResult(
                tool_name=self.name,
                status=ToolExecutionStatus.SKIPPED,
                duration_ms=0,
                warnings=["Valuation evidence is required before explainability analysis."],
            )
        request = ExplainabilityToolRequest(explainability=valuation.explainability)
        response = ExplainabilityToolResponse(
            **request.explainability.model_dump(mode="json"),
        )
        return _success_result(self.name, start, response, ["explainability.truth_layer"])


class DistrictIntelligenceTool(BrokerTool):
    name = BrokerToolName.DISTRICT_INTELLIGENCE
    description = "Derives district context strictly from resolved area and comparable evidence."

    def execute(self, *, db: Session, valuation: RentFairPriceResponse | None = None, **kwargs) -> BrokerToolResult:
        start = time.perf_counter()
        if valuation is None:
            return BrokerToolResult(
                tool_name=self.name,
                status=ToolExecutionStatus.SKIPPED,
                duration_ms=0,
                warnings=["Valuation evidence is required before district intelligence."],
            )
        request = DistrictIntelligenceToolRequest(valuation=valuation)
        area_name = request.valuation.area.get("name")
        market_signals = []
        if area_name:
            market_signals.append(f"Resolved deterministic area: {area_name}.")
        contract_label = (request.valuation.valuation_contract or {}).get("label")
        if contract_label:
            market_signals.append(f"Governed property category: {contract_label}.")
        amenity_average = (request.valuation.amenity_intelligence or {}).get("average_amenity_similarity")
        if amenity_average is not None:
            market_signals.append(f"Average amenity similarity: {float(amenity_average):.2f}.")
        market_signals.append(f"Comparable retrieval tier used: {request.valuation.tier_used}.")
        market_signals.append(f"Retained comparable count: {request.valuation.comps_count}.")
        response = DistrictIntelligenceToolResponse(
            area=request.valuation.area,
            active_district=area_name,
            tier_used=request.valuation.tier_used,
            market_signals=market_signals,
        )
        return _success_result(self.name, start, response, ["district.resolved_area"])


class ConfidenceAnalysisTool(BrokerTool):
    name = BrokerToolName.CONFIDENCE_ANALYSIS
    description = "Explains deterministic confidence and pricing flag consistency."

    def execute(self, *, db: Session, valuation: RentFairPriceResponse | None = None, **kwargs) -> BrokerToolResult:
        start = time.perf_counter()
        if valuation is None:
            return BrokerToolResult(
                tool_name=self.name,
                status=ToolExecutionStatus.SKIPPED,
                duration_ms=0,
                warnings=["Valuation evidence is required before confidence analysis."],
            )
        request = ConfidenceAnalysisToolRequest(valuation=valuation)
        notes = [
            f"Deterministic confidence label is {request.valuation.confidence.label}.",
            f"Price flag is {request.valuation.flag}.",
        ]
        if request.valuation.flag == "INSUFFICIENT_DATA":
            notes.append("The deterministic engine did not produce a fair-price estimate due to insufficient evidence.")
        response = ConfidenceAnalysisToolResponse(
            confidence=request.valuation.confidence,
            flag=str(request.valuation.flag),
            consistency_notes=notes,
        )
        return _success_result(self.name, start, response, ["confidence.deterministic"])
