from __future__ import annotations

from app.broker.schemas.contracts import (
    BrokerAnalyticalResponse,
    BrokerAuthoritativeValues,
    BrokerContext,
    BrokerValuationSummary,
    GroundingReport,
)


def _egp(value: int | None) -> str:
    if value is None:
        return "not available"
    return f"{value:,} EGP"


def _confidence_phrase(score: float | None, label: str) -> str:
    return f"{label} ({score:.2f})" if score is not None else label


def authoritative_values(summary: BrokerValuationSummary) -> BrokerAuthoritativeValues:
    return BrokerAuthoritativeValues(
        valuation_id=summary.valuation_id,
        fair_price_egp=summary.fair_price_egp,
        range_low_egp=summary.range_low_egp,
        range_high_egp=summary.range_high_egp,
        confidence_label=summary.confidence_label,
        engine_used=summary.engine_used,
        routing_reason=summary.routing_reason,
        source=summary.source,
        flag=summary.flag,
        tier_used=summary.tier_used,
        comps_count=summary.comps_count,
        confidence_score=summary.confidence_score,
        property_category=summary.property_category,
    )


class AIResponseFormatter:
    def format(self, context: BrokerContext) -> BrokerAnalyticalResponse:
        summary = context.valuation_summary
        if summary is None:
            return BrokerAnalyticalResponse(
                executive_summary=(
                    "No deterministic valuation is available for this broker turn, so the broker cannot issue "
                    "a price opinion."
                ),
                valuation_interpretation=(
                    "ValorAI requires an authoritative valuation output before it can discuss price, range, "
                    "comparables, or confidence."
                ),
                comparable_reasoning="No comparable set was provided by the deterministic retrieval system.",
                district_insights="No resolved district intelligence is available for this turn.",
                confidence_explanation="No confidence score is available without a deterministic valuation.",
                opportunity_risk_notes=[
                    "Provide property location, size, type, and room inputs to run the valuation engine.",
                    "The broker is operating in deterministic-safety fallback mode.",
                ],
                analytical_conclusion=(
                    "The correct next step is to run the deterministic valuation engine, then generate broker analysis "
                    "from that grounded evidence."
                ),
                evidence_ids=[],
            )

        evidence_ids = [item.evidence_id for item in context.evidence]
        comp_ids = [item.listing_id for item in context.comparable_evidence]
        comparable_prices = [item.price_egp for item in context.comparable_evidence]

        if comparable_prices:
            comp_range = f"{_egp(min(comparable_prices))} to {_egp(max(comparable_prices))}"
        else:
            comp_range = "no exposed top-comparable price range"

        risk_notes = []
        if summary.flag == "INSUFFICIENT_DATA":
            risk_notes.append("Insufficient comparable depth prevents a reliable price opinion.")
        if summary.confidence_label.lower() == "low":
            risk_notes.append("Low confidence means the analysis should be treated as directional, not decisive.")
        if context.token_budget.truncated:
            risk_notes.append("Comparable context was intentionally capped for token control.")
        if not risk_notes:
            risk_notes.append("Primary risk is market movement outside the current comparable snapshot.")
        risk_notes.append("The LLM layer is not permitted to alter valuation, range, confidence, or comparable facts.")

        authoritative = authoritative_values(summary)
        comparable_count = len(context.comparable_evidence)
        fairness = f" Tool 2 classifies the asking-price position as {summary.fairness_status}." if summary.fairness_status else ""

        return BrokerAnalyticalResponse(
            executive_summary=(
                f"The TruthLayer {summary.engine_used} engine values the asset at {_egp(summary.fair_price_egp)}, "
                f"with an institutional fair range of {_egp(summary.range_low_egp)} to "
                f"{_egp(summary.range_high_egp)}."
            ),
            valuation_interpretation=(
                f"Copilot Valuation Tool returned valuation {summary.valuation_id} through routing reason "
                f"{summary.routing_reason}.{fairness}"
            ),
            comparable_reasoning=(
                f"Copilot Explainability Tool exposed {comparable_count} comparable evidence record(s). "
                f"The exposed price range is {comp_range}."
            ),
            district_insights=(
                "District detail is intentionally limited because the normalized Tool 1 and Tool 2 contracts do not "
                "expose a resolved district field."
            ),
            confidence_explanation=(
                f"Confidence is {_confidence_phrase(summary.confidence_score, summary.confidence_label)}. "
                f"{summary.confidence_reason or 'Detailed confidence factors are not exposed by the normalized Tool 1 contract.'}"
            ),
            opportunity_risk_notes=risk_notes,
            analytical_conclusion=(
                "The broker view supports an evidence-led discussion, but the deterministic backend remains the "
                "authority for price, range, confidence, and comparable evidence."
            ),
            authoritative_values=authoritative,
            evidence_ids=evidence_ids,
            referenced_comp_listing_ids=comp_ids,
        )

    def safety_fallback(self, context: BrokerContext, grounding: GroundingReport) -> BrokerAnalyticalResponse:
        authoritative = None
        if context.valuation_summary is not None:
            authoritative = authoritative_values(context.valuation_summary)
        return BrokerAnalyticalResponse(
            executive_summary="Broker response validation failed, so the analytical narrative was withheld.",
            valuation_interpretation="The deterministic backend remains authoritative; no unvalidated valuation text is returned.",
            comparable_reasoning="Comparable reasoning is withheld until grounding violations are resolved.",
            district_insights="District insights are withheld until grounding violations are resolved.",
            confidence_explanation="Confidence explanation is withheld until grounding violations are resolved.",
            opportunity_risk_notes=[
                "Grounding validation failed.",
                *grounding.violations,
            ],
            analytical_conclusion="Retry after correcting the broker response generation path.",
            authoritative_values=authoritative,
            evidence_ids=[item.evidence_id for item in context.evidence],
            referenced_comp_listing_ids=[item.listing_id for item in context.comparable_evidence],
        )


response_formatter = AIResponseFormatter()
