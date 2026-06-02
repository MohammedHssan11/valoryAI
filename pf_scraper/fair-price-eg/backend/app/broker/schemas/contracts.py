from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.copilot_tools import (
    ExplainabilityToolResponse as CopilotExplainabilityToolResponse,
    ValuationToolResponse as CopilotValuationToolResponse,
)
from app.api.schemas.pricing import CompItem, ConfidenceDTO, RentFairPriceRequest, RentFairPriceResponse


class BrokerIntent(str, Enum):
    VALUATION_ANALYSIS = "valuation_analysis"
    VALUATION_EXPLANATION = "valuation_explanation"
    COMPARABLE_REVIEW = "comparable_review"
    COMPARABLE_ANALYSIS = "comparable_analysis"
    DISTRICT_INTELLIGENCE = "district_intelligence"
    DISTRICT_COMPARISON = "district_comparison"
    INVESTOR_BRIEF = "investor_brief"
    INVESTMENT_OPPORTUNITY = "investment_opportunity"
    CONFIDENCE_DISCUSSION = "confidence_discussion"
    ANOMALY_INVESTIGATION = "anomaly_investigation"
    MARKET_CONDITION = "market_condition"
    INVESTOR_WORKFLOW_GUIDANCE = "investor_workflow_guidance"
    GENERAL_GUIDANCE = "general_guidance"
    FALLBACK = "fallback"


class BrokerStage(str, Enum):
    CLASSIFY_INTENT = "classify_intent"
    BUILD_REASONING_PLAN = "build_reasoning_plan"
    EXECUTE_TOOLS = "execute_tools"
    ASSEMBLE_CONTEXT = "assemble_context"
    GENERATE_NARRATION = "generate_narration"
    VALIDATE_GROUNDING = "validate_grounding"
    FINALIZE_RESPONSE = "finalize_response"
    INTENT_ANALYSIS = "intent_analysis"
    TOOL_SELECTION = "tool_selection"
    EVIDENCE_GATHERING = "evidence_gathering"
    CONTEXT_ASSEMBLY = "context_assembly"
    RESPONSE_GENERATION = "response_generation"
    RESPONSE_VALIDATION = "response_validation"


class BrokerToolName(str, Enum):
    VALUATION_ANALYSIS = "valuation_analysis"
    COMPARABLE_ANALYSIS = "comparable_analysis"
    EXPLAINABILITY = "explainability"
    DISTRICT_INTELLIGENCE = "district_intelligence"
    CONFIDENCE_ANALYSIS = "confidence_analysis"


class ToolExecutionStatus(str, Enum):
    SUCCESS = "success"
    SKIPPED = "skipped"
    FAILED = "failed"


class InvestorPreferences(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk_tolerance: str | None = Field(default=None, max_length=80)
    investment_horizon: str | None = Field(default=None, max_length=80)
    target_yield: float | None = Field(default=None, ge=0, le=1)
    budget_ceiling_egp: int | None = Field(default=None, gt=0)
    notes: list[str] = Field(default_factory=list, max_length=20)


class BrokerIntentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str | None = Field(default=None, min_length=3, max_length=80)
    message: str = Field(min_length=1, max_length=4000)
    has_valuation_request: bool = False


class BrokerAnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str | None = Field(default=None, min_length=3, max_length=80)
    workspace_id: int = Field(gt=0)
    scenario_id: int = Field(gt=0)
    message: str = Field(
        default="Analyze this property as an institutional real-estate analyst.",
        min_length=1,
        max_length=4000,
    )
    valuation_request: RentFairPriceRequest
    investor_preferences: InvestorPreferences | None = None


class BrokerChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str | None = Field(default=None, min_length=3, max_length=80)
    workspace_id: int = Field(gt=0)
    scenario_id: int = Field(gt=0)
    message: str = Field(min_length=1, max_length=4000)
    valuation_request: RentFairPriceRequest | None = None
    investor_preferences: InvestorPreferences | None = None


class BrokerReasonRequest(BrokerChatRequest):
    pass


class BrokerIntentSignal(BaseModel):
    name: str
    weight: float = Field(ge=0, le=1)
    matched_terms: list[str] = Field(default_factory=list)


class BrokerIntentClassification(BaseModel):
    intent: BrokerIntent
    confidence: float = Field(ge=0, le=1)
    matched_signals: list[BrokerIntentSignal] = Field(default_factory=list)
    fallback: bool = False
    routing_reason: str
    has_valuation_request: bool = False


class BrokerReasoningPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:12]}")
    intent: BrokerIntent
    stages: list[BrokerStage]
    selected_tools: list[BrokerToolName] = Field(default_factory=list)
    requires_valuation: bool = False
    evidence_requirements: list[str] = Field(default_factory=list)
    narration_mode: str
    governance_checks: list[str] = Field(default_factory=list)
    degraded_mode_reasons: list[str] = Field(default_factory=list)


class BrokerNarrationTelemetry(BaseModel):
    provider: str
    model: str | None = None
    used_llm: bool = False
    latency_ms: float = 0
    token_usage: dict[str, Any] = Field(default_factory=dict)
    fallback_reason: str | None = None


class ResponseGovernanceCheck(BaseModel):
    name: str
    status: Literal["passed", "failed", "skipped"]
    details: dict[str, Any] = Field(default_factory=dict)


class ResponseGovernanceReport(BaseModel):
    status: Literal["passed", "failed"]
    checks: list[ResponseGovernanceCheck] = Field(default_factory=list)
    violations: list[str] = Field(default_factory=list)
    sanitized: bool = False


class BrokerStageFailure(BaseModel):
    stage: BrokerStage
    code: str
    message: str
    retryable: bool = False


class BrokerStageEvent(BaseModel):
    event_id: str
    stage: BrokerStage
    event_type: Literal[
        "stage_started",
        "stage_progress",
        "stage_completed",
        "stage_failed",
        "tool_started",
        "tool_completed",
        "validation",
        "reasoning_event",
        "narration_delta",
        "narration_chunk",
        "governance_check",
        "governance_update",
        "confidence_update",
        "final_response",
        "stream_completed",
        "stream_error",
    ]
    message: str
    elapsed_ms: float | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BrokerToolResult(BaseModel):
    tool_name: BrokerToolName
    status: ToolExecutionStatus
    duration_ms: float
    evidence_ids: list[str] = Field(default_factory=list)
    data: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    error_code: str | None = None


class ValuationAnalysisToolRequest(BaseModel):
    user_id: int = Field(gt=0)
    workspace_id: int = Field(gt=0)
    scenario_id: int = Field(gt=0)


class ValuationAnalysisToolResponse(BaseModel):
    property_id: int = Field(gt=0)
    scenario_id: int = Field(gt=0)
    valuation: CopilotValuationToolResponse
    explainability: CopilotExplainabilityToolResponse


class ComparableAnalysisToolRequest(BaseModel):
    valuation: RentFairPriceResponse


class ComparableAnalysisToolResponse(BaseModel):
    comps_count: int
    tier_used: int
    top_comps: list[CompItem] = Field(default_factory=list)
    price_points_egp: list[int] = Field(default_factory=list)
    min_price_egp: int | None = None
    max_price_egp: int | None = None
    evidence_ids: list[str] = Field(default_factory=list)


class ExplainabilityToolRequest(BaseModel):
    explainability: CopilotExplainabilityToolResponse


class ExplainabilityToolResponse(BaseModel):
    valuation_id: str
    summary: str
    why_this_price: str
    strongest_factors: str
    confidence_reason: str
    fairness_status: str
    feature_drivers: list[dict[str, Any]] = Field(default_factory=list)
    comparable_evidence: list[dict[str, Any]] = Field(default_factory=list)
    timestamp: datetime
    source: Literal["TruthLayer"] = "TruthLayer"


class DistrictIntelligenceToolRequest(BaseModel):
    valuation: RentFairPriceResponse


class DistrictIntelligenceToolResponse(BaseModel):
    area: dict[str, Any] = Field(default_factory=dict)
    active_district: str | None = None
    tier_used: int
    market_signals: list[str] = Field(default_factory=list)


class ConfidenceAnalysisToolRequest(BaseModel):
    valuation: RentFairPriceResponse


class ConfidenceAnalysisToolResponse(BaseModel):
    confidence: ConfidenceDTO
    flag: str
    consistency_notes: list[str] = Field(default_factory=list)


class BrokerEvidenceRef(BaseModel):
    evidence_id: str
    source: BrokerToolName
    kind: str
    summary: str
    payload: dict[str, Any] = Field(default_factory=dict)


class BrokerTokenBudget(BaseModel):
    max_context_tokens: int
    estimated_context_tokens: int
    truncated: bool = False


class BrokerValuationSummary(BaseModel):
    valuation_id: str
    fair_price_egp: int
    range_low_egp: int
    range_high_egp: int
    confidence_label: str
    engine_used: str
    routing_reason: str
    source: Literal["TruthLayer"] = "TruthLayer"
    fairness_status: str | None = None
    why_this_price: str | None = None
    strongest_factors: str | None = None
    confidence_reason: str | None = None
    flag: str | None = None
    tier_used: int | None = None
    comps_count: int | None = None
    confidence_score: float | None = None
    area: dict[str, Any] = Field(default_factory=dict)
    property_category: str | None = None
    valuation_contract: dict[str, Any] = Field(default_factory=dict)
    amenity_intelligence: dict[str, Any] = Field(default_factory=dict)


class BrokerComparableEvidence(BaseModel):
    evidence_id: str
    listing_id: str
    price_egp: int
    size_sqm: float | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    area_name: str | None = None
    distance_m: float | None = None
    age_days: float | None = None
    weight: float | None = None
    reason_code: str | None = None
    similarity_score: float | None = None
    listing_date: str | None = None
    amenity_similarity: float | None = None
    matched_amenities: list[str] = Field(default_factory=list)
    missing_amenities: list[str] = Field(default_factory=list)


class BrokerContext(BaseModel):
    intent: BrokerIntent
    session_id: str
    user_message: str
    valuation_summary: BrokerValuationSummary | None = None
    comparable_evidence: list[BrokerComparableEvidence] = Field(default_factory=list)
    confidence_factors: dict[str, float] = Field(default_factory=dict)
    explainability_trace: list[dict[str, Any]] = Field(default_factory=list)
    explainability: dict[str, Any] = Field(default_factory=dict)
    valuation_contract: dict[str, Any] = Field(default_factory=dict)
    amenity_intelligence: dict[str, Any] = Field(default_factory=dict)
    district_intelligence: dict[str, Any] = Field(default_factory=dict)
    market_signals: list[str] = Field(default_factory=list)
    session_state: dict[str, Any] = Field(default_factory=dict)
    evidence: list[BrokerEvidenceRef] = Field(default_factory=list)
    token_budget: BrokerTokenBudget
    deterministic_authority: dict[str, Any] = Field(default_factory=dict)


class BrokerAuthoritativeValues(BaseModel):
    valuation_id: str
    fair_price_egp: int
    range_low_egp: int
    range_high_egp: int
    confidence_label: str
    engine_used: str
    routing_reason: str
    source: Literal["TruthLayer"] = "TruthLayer"
    flag: str | None = None
    tier_used: int | None = None
    comps_count: int | None = None
    confidence_score: float | None = None
    property_category: str | None = None


class BrokerAnalyticalResponse(BaseModel):
    executive_summary: str
    valuation_interpretation: str
    comparable_reasoning: str
    district_insights: str
    confidence_explanation: str
    opportunity_risk_notes: list[str] = Field(default_factory=list)
    analytical_conclusion: str
    authoritative_values: BrokerAuthoritativeValues | None = None
    evidence_ids: list[str] = Field(default_factory=list)
    referenced_comp_listing_ids: list[str] = Field(default_factory=list)


class GroundingReport(BaseModel):
    status: Literal["passed", "failed"]
    violations: list[str] = Field(default_factory=list)
    checked_values: dict[str, Any] = Field(default_factory=dict)


class BrokerOrchestrationResponse(BaseModel):
    session_id: str
    intent: BrokerIntent
    response: BrokerAnalyticalResponse
    grounding: GroundingReport
    context: BrokerContext
    tool_results: list[BrokerToolResult]
    events: list[BrokerStageEvent]
    degraded_mode: bool = False
    intent_classification: BrokerIntentClassification | None = None
    reasoning_plan: BrokerReasoningPlan | None = None
    narration: BrokerNarrationTelemetry | None = None
    governance: ResponseGovernanceReport | None = None


class BrokerSessionTurn(BaseModel):
    message: str
    intent: BrokerIntent
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BrokerSessionValuation(BaseModel):
    fair_price_egp: int
    range_low_egp: int
    range_high_egp: int
    confidence_label: str
    area_name: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BrokerSessionSnapshot(BaseModel):
    session_id: str
    user_id: int
    workspace_id: int
    scenario_id: int
    created_at: datetime
    updated_at: datetime
    previous_requests: list[BrokerSessionTurn] = Field(default_factory=list)
    previous_valuations: list[BrokerSessionValuation] = Field(default_factory=list)
    active_district: str | None = None
    investor_preferences: InvestorPreferences | None = None
    analytical_context: dict[str, Any] = Field(default_factory=dict)
