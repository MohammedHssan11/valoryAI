import type {
  BrokerTalkingPoint,
  NegotiationComparableSummary,
  NegotiationEvidenceReference,
  NegotiationEvidenceSummary,
  NegotiationPosition,
  NegotiationWhatIfSummary,
  RecommendedOfferBand,
} from "@/types/negotiation";
import type { FairnessStatus, TruthLayerSource } from "@/types/whatIf";

export type InvestmentPosition =
  | "Strong Opportunity"
  | "Moderate Opportunity"
  | "Fairly Priced"
  | "Caution"
  | "High Risk";

export type InvestmentRunTarget = "base" | "active_scenario" | "selected_scenario" | "compared_scenario";

export interface InvestmentToolRequest {
  workspace_id: number;
  property_id: number;
  scenario_id?: number | null;
  asking_price_egp: number;
  what_if_modifications?: Record<string, unknown> | null;
}

export interface InvestmentFinding {
  text: string;
  evidence: NegotiationEvidenceReference[];
}

export interface InvestmentNegotiationSummary {
  negotiation_position: NegotiationPosition;
  negotiation_position_reason: string;
  recommended_offer_band: RecommendedOfferBand;
  broker_talking_points: BrokerTalkingPoint[];
  source: TruthLayerSource;
}

export interface InvestmentWhatIfSummary {
  status: "Available" | "Insufficient Evidence";
  reason: string;
  analysis: NegotiationWhatIfSummary | null;
  source: TruthLayerSource | "Insufficient Evidence";
}

export interface InvestmentToolResponse {
  tool_name: "investment";
  valuation_id: string;
  asking_price: number;
  fair_price: number;
  fairness_status: FairnessStatus;
  price_gap: number;
  price_gap_percentage: number;
  investment_position: InvestmentPosition;
  investment_position_reason: string;
  investment_position_evidence: NegotiationEvidenceReference[];
  confidence_level: string;
  confidence_reason: string;
  investment_summary: string;
  strengths: InvestmentFinding[];
  risks: InvestmentFinding[];
  evidence_summary: NegotiationEvidenceSummary;
  comparable_summary: NegotiationComparableSummary;
  negotiation_summary: InvestmentNegotiationSummary;
  what_if_summary: InvestmentWhatIfSummary;
  timestamp: string;
  source: TruthLayerSource;
}

export interface InvestmentRunContext {
  target: InvestmentRunTarget;
  label: string;
  scenarioId: number | null;
}

export interface InvestmentRunRecord extends InvestmentRunContext {
  key: string;
  request: InvestmentToolRequest;
  response: InvestmentToolResponse;
  createdAt: string;
}
