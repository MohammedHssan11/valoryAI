import type { FairnessStatus, FeatureChanges, ToolPriceRange, TruthLayerSource } from "@/types/whatIf";

export type NegotiationSourceTool =
  | "input"
  | "valuation"
  | "explainability"
  | "comparable"
  | "fairness"
  | "negotiation"
  | "what_if";

export type NegotiationPosition =
  | "Strong Buy Opportunity"
  | "Negotiation Recommended"
  | "Fair Market Position"
  | "Premium Justified"
  | "Overpriced";

export type NegotiationRunTarget = "base" | "active_scenario" | "selected_scenario";

export interface NegotiationToolRequest {
  workspace_id: number;
  property_id: number;
  scenario_id?: number | null;
  asking_price_egp: number;
  what_if_modifications?: Record<string, unknown> | null;
}

export interface NegotiationEvidenceReference {
  source_tool: NegotiationSourceTool;
  valuation_id: string | null;
  field: string;
  comparable_id: string | null;
}

export interface BrokerTalkingPoint {
  text: string;
  evidence: NegotiationEvidenceReference[];
}

export interface NegotiationEvidenceSummary {
  valuation_id: string;
  price_range: ToolPriceRange;
  explainability_summary: string;
  why_this_price: string;
  strongest_factors: string;
  source: TruthLayerSource;
}

export interface NegotiationComparableSummary {
  valuation_id: string;
  comparable_count: number;
  comparable_ids: string[];
  observed_prices: number[];
  lowest_observed_price: number | null;
  highest_observed_price: number | null;
  source: TruthLayerSource;
}

export interface RecommendedOfferBand {
  low: number | null;
  high: number | null;
  derivation: string;
  comparable_ids_used: string[];
  evidence: NegotiationEvidenceReference[];
  source: "TruthLayer-derived";
}

export interface NegotiationWhatIfSummary {
  base_valuation: number;
  scenario_valuation: number;
  base_valuation_id: string;
  scenario_valuation_id: string;
  delta_value: number;
  delta_percentage: number;
  fairness_status: FairnessStatus;
  assumptions_used: string[];
  feature_changes: FeatureChanges;
  source: TruthLayerSource;
}

export interface NegotiationToolResponse {
  tool_name: "negotiation";
  valuation_id: string;
  asking_price: number;
  fair_price: number;
  fairness_status: FairnessStatus;
  price_gap: number;
  price_gap_percentage: number;
  confidence_level: string;
  confidence_reason: string;
  negotiation_position: NegotiationPosition;
  negotiation_position_reason: string;
  negotiation_position_evidence: NegotiationEvidenceReference[];
  broker_talking_points: BrokerTalkingPoint[];
  evidence_summary: NegotiationEvidenceSummary;
  comparable_summary: NegotiationComparableSummary;
  recommended_offer_band: RecommendedOfferBand;
  risk_notes: BrokerTalkingPoint[];
  what_if_analysis: NegotiationWhatIfSummary | null;
  timestamp: string;
  source: TruthLayerSource;
}

export interface NegotiationRunContext {
  target: NegotiationRunTarget;
  label: string;
  scenarioId: number | null;
}

export interface NegotiationRunRecord extends NegotiationRunContext {
  key: string;
  request: NegotiationToolRequest;
  response: NegotiationToolResponse;
  createdAt: string;
}
