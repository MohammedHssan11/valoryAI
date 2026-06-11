import type { InvestmentToolRequest, InvestmentToolResponse } from "@/types/investment";
import type { MarketInsightToolRequest, MarketInsightToolResponse } from "@/types/marketInsight";
import type { NegotiationToolRequest, NegotiationToolResponse } from "@/types/negotiation";
import type { WhatIfToolRequest, WhatIfToolResponse } from "@/types/whatIf";

export type CopilotRuntimeId = "COPILOT_ORCHESTRATOR_LLM_V1";

export type CopilotIntent =
  | "VALUATION"
  | "EXPLAINABILITY"
  | "COMPARABLES"
  | "FAIRNESS"
  | "WHAT_IF"
  | "NEGOTIATION"
  | "INVESTMENT"
  | "MARKET_INSIGHT"
  | "PROPERTY_COMPARISON"
  | "GENERAL_QUESTION";

export type CopilotNarrationStatus =
  | "ACCEPT_NARRATION"
  | "DETERMINISTIC_ONLY"
  | "REJECT_NARRATION"
  | "ACCESS_DENIED";

export type CopilotDeliveryMode =
  | "GROUNDED_NARRATION"
  | "DETERMINISTIC_FALLBACK"
  | "ACCESS_DENIED";

export type CopilotCompositionStatus =
  | "SUCCESS"
  | "PARTIAL_SUCCESS"
  | "FAILED"
  | "SPARSE_EVIDENCE"
  | "CLARIFICATION_REQUIRED";

export type CopilotPlannedToolCall =
  | "VALUATION_TOOL"
  | "EXPLAINABILITY_TOOL"
  | "COMPARABLES_TOOL"
  | "FAIRNESS_TOOL"
  | "WHAT_IF_TOOL"
  | "NEGOTIATION_TOOL"
  | "INVESTMENT_TOOL"
  | "MARKET_INSIGHT_TOOL"
  | "VALUATION_TOOL:PROPERTY_A"
  | "VALUATION_TOOL:PROPERTY_B";

export interface CopilotValuationToolRequest {
  workspace_id: number;
  property_id: number;
  scenario_id?: number | null;
}

export interface CopilotExplainabilityToolRequest {
  workspace_id: number;
  valuation_id: string;
}

export interface CopilotComparableToolRequest {
  workspace_id: number;
  property_id: number;
  scenario_id?: number | null;
  valuation_id?: string | null;
}

export interface CopilotFairnessToolRequest {
  workspace_id: number;
  property_id: number;
  scenario_id?: number | null;
  target_price_egp: number;
}

export interface CopilotToolPriceRange {
  low: number;
  high: number;
}

export interface CopilotValuationToolResponse {
  tool_name: "valuation";
  valuation_id: string;
  fair_price: number;
  price_range: CopilotToolPriceRange;
  confidence_level: string;
  engine_used: string;
  routing_reason: string;
  timestamp: string;
  source: "TruthLayer";
}

export type CopilotToolInput =
  | CopilotValuationToolRequest
  | CopilotExplainabilityToolRequest
  | CopilotComparableToolRequest
  | CopilotFairnessToolRequest
  | WhatIfToolRequest
  | NegotiationToolRequest
  | InvestmentToolRequest
  | MarketInsightToolRequest;

export type CopilotToolPayload =
  | CopilotValuationToolResponse
  | WhatIfToolResponse
  | NegotiationToolResponse
  | InvestmentToolResponse
  | MarketInsightToolResponse
  | Record<string, unknown>;

export interface CopilotToolOrderingMetadata {
  order_index: number;
  parallel_group_index: number | null;
}

export interface CopilotFrontendToolOutput {
  planned_tool: CopilotPlannedToolCall;
  tool_name: string;
  payload: CopilotToolPayload;
  ordering_metadata: CopilotToolOrderingMetadata;
}

export interface CopilotFailedTool {
  planned_tool: CopilotPlannedToolCall | string;
  tool_name: string;
  error_type: string;
  failure_category?: string;
  ordering_metadata: CopilotToolOrderingMetadata;
}

export interface CopilotCitationPackage {
  valuation_ids: string[];
  tool_event_ids: string[];
  comparable_ids: string[];
  unavailable_optional_citation_types: string[];
}

export interface CopilotFrontendEvidence {
  comparables?: Array<Record<string, unknown>>;
  feature_drivers?: Array<Record<string, unknown>>;
  market_insights?: Array<Record<string, unknown>>;
  [key: string]: unknown;
}

export interface CopilotFrontendPayload {
  schema_version: "1.0";
  composition_status: CopilotCompositionStatus;
  tool_outputs: CopilotFrontendToolOutput[];
  failed_tools: CopilotFailedTool[];
  full_evidence: CopilotFrontendEvidence;
  citations: CopilotCitationPackage;
}

export interface CopilotAudit {
  plan_id?: string;
  execution_id?: string;
  composition_status?: CopilotCompositionStatus;
  memory_id?: string;
  memory_status?: string;
  narration_status: CopilotNarrationStatus | string;
  [key: string]: unknown;
}

export interface CopilotOrchestratorRequest {
  workspace_id: number;
  scenario_id?: number | null;
  broker_session_id?: string | null;
  message: string;
  tool_inputs: Partial<Record<CopilotPlannedToolCall, CopilotToolInput>>;
}

export interface CopilotOrchestratorResponse {
  runtime_id: CopilotRuntimeId;
  response_id: string;
  intent: CopilotIntent | string;
  status: CopilotNarrationStatus | string;
  delivery_mode: CopilotDeliveryMode | string;
  response: CopilotFrontendPayload | string | null;
  citation_package: CopilotCitationPackage | null;
  audit: CopilotAudit;
}

export interface CopilotConversationTurn {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
  response?: CopilotOrchestratorResponse;
}

export interface CopilotHumanContext {
  activeProperty: string;
  activeScenario: string;
  latestValuation: string;
  latestNegotiation: string;
  latestInvestment: string;
  latestMarketInsight: string;
  relevantHistory: string[];
  memoryId?: string;
  memoryStatus?: string;
}

export interface CopilotSendMessageInput {
  message: string;
  brokerSessionId?: string | null;
  signal?: AbortSignal;
}
