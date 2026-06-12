from __future__ import annotations

from app.broker.schemas.contracts import (
    BrokerIntent,
    BrokerIntentClassification,
    BrokerReasoningPlan,
    BrokerStage,
    BrokerToolName,
)


class ReasoningPlanBuilder:
    def build(
        self,
        *,
        classification: BrokerIntentClassification,
        selected_tools: list[BrokerToolName],
    ) -> BrokerReasoningPlan:
        intent = classification.intent
        evidence_requirements = ["deterministic_authority"]
        governance_checks = [
            "authoritative_value_consistency",
            "evidence_reference_consistency",
            "forbidden_output_detection",
            "numeric_consistency",
            "confidence_consistency",
        ]

        if selected_tools:
            evidence_requirements.extend(tool.value for tool in selected_tools)

        degraded_reasons: list[str] = []
        if classification.fallback:
            degraded_reasons.append("intent_classifier_low_confidence")
        if classification.has_valuation_request and not selected_tools:
            degraded_reasons.append("no_tools_selected_despite_valuation_request")
        if not classification.has_valuation_request:
            degraded_reasons.append("no_new_deterministic_valuation_request")

        narration_mode = self._narration_mode(intent)
        return BrokerReasoningPlan(
            intent=intent,
            stages=[
                BrokerStage.CLASSIFY_INTENT,
                BrokerStage.BUILD_REASONING_PLAN,
                BrokerStage.EXECUTE_TOOLS,
                BrokerStage.ASSEMBLE_CONTEXT,
                BrokerStage.GENERATE_NARRATION,
                BrokerStage.VALIDATE_GROUNDING,
                BrokerStage.FINALIZE_RESPONSE,
            ],
            selected_tools=selected_tools,
            requires_valuation=classification.has_valuation_request,
            evidence_requirements=evidence_requirements,
            narration_mode=narration_mode,
            governance_checks=governance_checks,
            degraded_mode_reasons=degraded_reasons,
        )

    def _narration_mode(self, intent: BrokerIntent) -> str:
        if intent in {BrokerIntent.CONFIDENCE_DISCUSSION, BrokerIntent.ANOMALY_INVESTIGATION}:
            return "confidence_and_anomaly_explanation"
        if intent in {BrokerIntent.INVESTOR_BRIEF, BrokerIntent.INVESTMENT_OPPORTUNITY}:
            return "investor_grade_opportunity_risk"
        if intent in {BrokerIntent.DISTRICT_INTELLIGENCE, BrokerIntent.DISTRICT_COMPARISON, BrokerIntent.MARKET_CONDITION}:
            return "district_market_context"
        if intent in {BrokerIntent.COMPARABLE_REVIEW, BrokerIntent.COMPARABLE_ANALYSIS}:
            return "comparable_evidence_analysis"
        return "valuation_explainability"


reasoning_plan_builder = ReasoningPlanBuilder()
