import type { RentFairPriceRequest } from "@/types/valuation";
import type { PropertyCategory } from "@/types/valuation";

export type BrokerIntent =
  | "valuation_analysis"
  | "valuation_explanation"
  | "comparable_review"
  | "comparable_analysis"
  | "district_intelligence"
  | "district_comparison"
  | "investor_brief"
  | "investment_opportunity"
  | "confidence_discussion"
  | "anomaly_investigation"
  | "market_condition"
  | "investor_workflow_guidance"
  | "general_guidance"
  | "fallback";

export type BrokerStage =
  | "classify_intent"
  | "build_reasoning_plan"
  | "execute_tools"
  | "assemble_context"
  | "generate_narration"
  | "validate_grounding"
  | "finalize_response"
  | "intent_analysis"
  | "tool_selection"
  | "evidence_gathering"
  | "context_assembly"
  | "response_generation"
  | "response_validation";

export type BrokerToolName =
  | "valuation_analysis"
  | "comparable_analysis"
  | "explainability"
  | "district_intelligence"
  | "confidence_analysis";

export type BrokerStageEventType =
  | "stage_started"
  | "stage_progress"
  | "stage_completed"
  | "stage_failed"
  | "tool_started"
  | "tool_completed"
  | "validation"
  | "reasoning_event"
  | "narration_delta"
  | "narration_chunk"
  | "governance_check"
  | "governance_update"
  | "confidence_update"
  | "stream_completed"
  | "stream_error"
  | "final_response";

export interface InvestorPreferences {
  risk_tolerance?: string | null;
  investment_horizon?: string | null;
  target_yield?: number | null;
  budget_ceiling_egp?: number | null;
  notes?: string[];
}

export interface BrokerReasonRequest {
  session_id?: string | null;
  workspace_id: number;
  scenario_id: number;
  message: string;
  valuation_request?: RentFairPriceRequest | null;
  investor_preferences?: InvestorPreferences | null;
}

export type BrokerChatRequest = BrokerReasonRequest;

export interface BrokerIntentSignal {
  name: string;
  weight: number;
  matched_terms: string[];
}

export interface BrokerIntentClassification {
  intent: BrokerIntent;
  confidence: number;
  matched_signals: BrokerIntentSignal[];
  fallback: boolean;
  routing_reason: string;
  has_valuation_request: boolean;
}

export interface BrokerReasoningPlan {
  plan_id: string;
  intent: BrokerIntent;
  stages: BrokerStage[];
  selected_tools: BrokerToolName[];
  requires_valuation: boolean;
  evidence_requirements: string[];
  narration_mode: string;
  governance_checks: string[];
  degraded_mode_reasons: string[];
}

export interface BrokerStageEvent {
  event_id: string;
  stage: BrokerStage;
  event_type: BrokerStageEventType;
  message: string;
  elapsed_ms?: number | null;
  payload: Record<string, unknown>;
  created_at: string;
}

export interface BrokerToolResult {
  tool_name: BrokerToolName;
  status: "success" | "skipped" | "failed";
  duration_ms: number;
  evidence_ids: string[];
  data: Record<string, unknown>;
  warnings: string[];
  error_code?: string | null;
}

export interface BrokerEvidenceRef {
  evidence_id: string;
  source: BrokerToolName;
  kind: string;
  summary: string;
  payload: Record<string, unknown>;
}

export interface BrokerTokenBudget {
  max_context_tokens: number;
  estimated_context_tokens: number;
  truncated: boolean;
}

export interface BrokerValuationSummary {
  valuation_id: string;
  fair_price_egp: number;
  range_low_egp: number;
  range_high_egp: number;
  confidence_label: string;
  engine_used: string;
  routing_reason: string;
  source: "TruthLayer";
  fairness_status?: string | null;
  why_this_price?: string | null;
  strongest_factors?: string | null;
  confidence_reason?: string | null;
  flag?: string | null;
  tier_used?: number | null;
  comps_count?: number | null;
  confidence_score?: number | null;
  area: Record<string, unknown>;
  property_category?: PropertyCategory | string | null;
  valuation_contract?: Record<string, unknown>;
  amenity_intelligence?: Record<string, unknown>;
}

export interface BrokerComparableEvidence {
  evidence_id: string;
  listing_id: string;
  price_egp: number;
  size_sqm?: number | null;
  bedrooms?: number | null;
  bathrooms?: number | null;
  area_name?: string | null;
  distance_m?: number | null;
  age_days?: number | null;
  weight?: number | null;
  reason_code?: string | null;
  similarity_score?: number | null;
  listing_date?: string | null;
  amenity_similarity?: number | null;
  matched_amenities?: string[];
  missing_amenities?: string[];
}

export interface BrokerContext {
  intent: BrokerIntent;
  session_id: string;
  user_message: string;
  valuation_summary?: BrokerValuationSummary | null;
  comparable_evidence: BrokerComparableEvidence[];
  confidence_factors: Record<string, number>;
  explainability_trace: Array<Record<string, unknown>>;
  explainability?: Record<string, unknown>;
  valuation_contract?: Record<string, unknown>;
  amenity_intelligence?: Record<string, unknown>;
  district_intelligence: Record<string, unknown>;
  market_signals: string[];
  session_state: Record<string, unknown>;
  evidence: BrokerEvidenceRef[];
  token_budget: BrokerTokenBudget;
  deterministic_authority: Record<string, unknown>;
}

export interface BrokerAuthoritativeValues {
  valuation_id: string;
  fair_price_egp: number;
  range_low_egp: number;
  range_high_egp: number;
  confidence_label: string;
  engine_used: string;
  routing_reason: string;
  source: "TruthLayer";
  flag?: string | null;
  tier_used?: number | null;
  comps_count?: number | null;
  confidence_score?: number | null;
  property_category?: PropertyCategory | string | null;
}

export interface BrokerAnalyticalResponse {
  executive_summary: string;
  valuation_interpretation: string;
  comparable_reasoning: string;
  district_insights: string;
  confidence_explanation: string;
  opportunity_risk_notes: string[];
  analytical_conclusion: string;
  authoritative_values?: BrokerAuthoritativeValues | null;
  evidence_ids: string[];
  referenced_comp_listing_ids: string[];
}

export interface GroundingReport {
  status: "passed" | "failed";
  violations: string[];
  checked_values: Record<string, unknown>;
}

export interface ResponseGovernanceCheck {
  name: string;
  status: "passed" | "failed" | "skipped";
  details: Record<string, unknown>;
}

export interface ResponseGovernanceReport {
  status: "passed" | "failed";
  checks: ResponseGovernanceCheck[];
  violations: string[];
  sanitized: boolean;
}

export interface BrokerNarrationTelemetry {
  provider: string;
  model?: string | null;
  used_llm: boolean;
  latency_ms: number;
  token_usage: Record<string, unknown>;
  fallback_reason?: string | null;
}

export interface BrokerOrchestrationResponse {
  session_id: string;
  intent: BrokerIntent;
  response: BrokerAnalyticalResponse;
  grounding: GroundingReport;
  context: BrokerContext;
  tool_results: BrokerToolResult[];
  events: BrokerStageEvent[];
  degraded_mode: boolean;
  intent_classification?: BrokerIntentClassification | null;
  reasoning_plan?: BrokerReasoningPlan | null;
  narration?: BrokerNarrationTelemetry | null;
  governance?: ResponseGovernanceReport | null;
}
