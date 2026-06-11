import { http } from "@/api/http";
import { ApiMeta, ApiSuccessEnvelope, isApiSuccessEnvelope, ValorApiError } from "@/api/contracts";
import type {
  InvestmentFinding,
  InvestmentNegotiationSummary,
  InvestmentPosition,
  InvestmentToolRequest,
  InvestmentToolResponse,
  InvestmentWhatIfSummary,
} from "@/types/investment";
import type {
  BrokerTalkingPoint,
  NegotiationComparableSummary,
  NegotiationEvidenceReference,
  NegotiationEvidenceSummary,
  NegotiationPosition,
  NegotiationWhatIfSummary,
  RecommendedOfferBand,
} from "@/types/negotiation";
import type { FairnessStatus, FeatureChange, FeatureChanges } from "@/types/whatIf";

export interface InvestmentAnalysisResult {
  data: InvestmentToolResponse;
  meta: ApiMeta;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function invalidInvestmentResponse(requestId?: string): ValorApiError {
  return new ValorApiError(
    {
      code: "INVALID_API_RESPONSE",
      message: "The ValorAI API returned an unexpected investment response.",
      details: [],
    },
    { requestId },
  );
}

function invalidInvestmentRequest(message: string, field?: string): ValorApiError {
  return new ValorApiError({
    code: "INVALID_INVESTMENT_REQUEST",
    message,
    details: field ? [{ code: "INVALID_INVESTMENT_REQUEST", message, field }] : [],
  });
}

function assertPositiveInteger(value: unknown, field: string): asserts value is number {
  if (typeof value !== "number" || !Number.isInteger(value) || value <= 0) {
    throw invalidInvestmentRequest(`${field} must be a positive integer.`, field);
  }
}

function compactUndefined(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(compactUndefined);
  if (!isRecord(value)) return value;

  return Object.fromEntries(
    Object.entries(value)
      .filter(([, entry]) => entry !== undefined)
      .map(([key, entry]) => [key, compactUndefined(entry)]),
  );
}

function assertInvestmentRequest(request: InvestmentToolRequest): InvestmentToolRequest {
  assertPositiveInteger(request.workspace_id, "workspace_id");
  assertPositiveInteger(request.property_id, "property_id");
  assertPositiveInteger(request.asking_price_egp, "asking_price_egp");
  if (request.scenario_id != null) {
    assertPositiveInteger(request.scenario_id, "scenario_id");
  }

  const safeRequest: InvestmentToolRequest = {
    workspace_id: request.workspace_id,
    property_id: request.property_id,
    scenario_id: request.scenario_id ?? null,
    asking_price_egp: request.asking_price_egp,
  };

  if (request.what_if_modifications != null) {
    const modifications = compactUndefined(request.what_if_modifications);
    if (!isRecord(modifications) || Object.keys(modifications).length === 0) {
      throw invalidInvestmentRequest(
        "what_if_modifications must include at least one property change.",
        "what_if_modifications",
      );
    }
    safeRequest.what_if_modifications = modifications;
  }

  return safeRequest;
}

function stringValue(value: unknown, requestId?: string): string {
  if (typeof value === "string") return value;
  throw invalidInvestmentResponse(requestId);
}

function numberValue(value: unknown, requestId?: string): number {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  throw invalidInvestmentResponse(requestId);
}

function nullableStringValue(value: unknown, requestId?: string): string | null {
  if (value === null || value === undefined) return null;
  return stringValue(value, requestId);
}

function nullableNumberValue(value: unknown, requestId?: string): number | null {
  if (value === null || value === undefined) return null;
  return numberValue(value, requestId);
}

function arrayValue(value: unknown, requestId?: string): unknown[] {
  if (Array.isArray(value)) return value;
  throw invalidInvestmentResponse(requestId);
}

function sourceValue(value: unknown, requestId?: string): "TruthLayer" {
  if (value === "TruthLayer") return "TruthLayer";
  throw invalidInvestmentResponse(requestId);
}

function investmentWhatIfSourceValue(value: unknown, requestId?: string): "TruthLayer" | "Insufficient Evidence" {
  if (value === "TruthLayer" || value === "Insufficient Evidence") return value;
  throw invalidInvestmentResponse(requestId);
}

function derivedSourceValue(value: unknown, requestId?: string): "TruthLayer-derived" {
  if (value === "TruthLayer-derived") return "TruthLayer-derived";
  throw invalidInvestmentResponse(requestId);
}

function fairnessStatusValue(value: unknown, requestId?: string): FairnessStatus {
  if (value === "Below Fair Value" || value === "Within Fair Value" || value === "Above Fair Value") return value;
  throw invalidInvestmentResponse(requestId);
}

function negotiationPositionValue(value: unknown, requestId?: string): NegotiationPosition {
  if (
    value === "Strong Buy Opportunity" ||
    value === "Negotiation Recommended" ||
    value === "Fair Market Position" ||
    value === "Premium Justified" ||
    value === "Overpriced"
  ) {
    return value;
  }
  throw invalidInvestmentResponse(requestId);
}

function investmentPositionValue(value: unknown, requestId?: string): InvestmentPosition {
  if (
    value === "Strong Opportunity" ||
    value === "Moderate Opportunity" ||
    value === "Fairly Priced" ||
    value === "Caution" ||
    value === "High Risk"
  ) {
    return value;
  }
  throw invalidInvestmentResponse(requestId);
}

function sourceToolValue(value: unknown, requestId?: string): NegotiationEvidenceReference["source_tool"] {
  if (
    value === "input" ||
    value === "valuation" ||
    value === "explainability" ||
    value === "comparable" ||
    value === "fairness" ||
    value === "negotiation" ||
    value === "what_if"
  ) {
    return value;
  }
  throw invalidInvestmentResponse(requestId);
}

function assertEvidenceReference(value: unknown, requestId?: string): NegotiationEvidenceReference {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    source_tool: sourceToolValue(value.source_tool, requestId),
    valuation_id: nullableStringValue(value.valuation_id, requestId),
    field: stringValue(value.field, requestId),
    comparable_id: nullableStringValue(value.comparable_id, requestId),
  };
}

function assertTalkingPoint(value: unknown, requestId?: string): BrokerTalkingPoint {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    text: stringValue(value.text, requestId),
    evidence: arrayValue(value.evidence, requestId).map((item) => assertEvidenceReference(item, requestId)),
  };
}

function assertInvestmentFinding(value: unknown, requestId?: string): InvestmentFinding {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    text: stringValue(value.text, requestId),
    evidence: arrayValue(value.evidence, requestId).map((item) => assertEvidenceReference(item, requestId)),
  };
}

function assertPriceRange(value: unknown, requestId?: string): { low: number; high: number } {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    low: numberValue(value.low, requestId),
    high: numberValue(value.high, requestId),
  };
}

function assertEvidenceSummary(value: unknown, requestId?: string): NegotiationEvidenceSummary {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    valuation_id: stringValue(value.valuation_id, requestId),
    price_range: assertPriceRange(value.price_range, requestId),
    explainability_summary: stringValue(value.explainability_summary, requestId),
    why_this_price: stringValue(value.why_this_price, requestId),
    strongest_factors: stringValue(value.strongest_factors, requestId),
    source: sourceValue(value.source, requestId),
  };
}

function assertComparableSummary(value: unknown, requestId?: string): NegotiationComparableSummary {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    valuation_id: stringValue(value.valuation_id, requestId),
    comparable_count: numberValue(value.comparable_count, requestId),
    comparable_ids: arrayValue(value.comparable_ids, requestId).map((item) => stringValue(item, requestId)),
    observed_prices: arrayValue(value.observed_prices, requestId).map((item) => numberValue(item, requestId)),
    lowest_observed_price: nullableNumberValue(value.lowest_observed_price, requestId),
    highest_observed_price: nullableNumberValue(value.highest_observed_price, requestId),
    source: sourceValue(value.source, requestId),
  };
}

function assertRecommendedOfferBand(value: unknown, requestId?: string): RecommendedOfferBand {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    low: nullableNumberValue(value.low, requestId),
    high: nullableNumberValue(value.high, requestId),
    derivation: stringValue(value.derivation, requestId),
    comparable_ids_used: arrayValue(value.comparable_ids_used ?? [], requestId).map((item) =>
      stringValue(item, requestId),
    ),
    evidence: arrayValue(value.evidence, requestId).map((item) => assertEvidenceReference(item, requestId)),
    source: derivedSourceValue(value.source, requestId),
  };
}

function assertFeatureChange(value: unknown, requestId?: string): FeatureChange {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    feature: stringValue(value.feature, requestId),
    before: value.before ?? null,
    after: value.after ?? null,
    unit: nullableStringValue(value.unit, requestId),
  };
}

function assertFeatureChanges(value: unknown, requestId?: string): FeatureChanges {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    added: arrayValue(value.added ?? [], requestId).map((item) => assertFeatureChange(item, requestId)),
    removed: arrayValue(value.removed ?? [], requestId).map((item) => assertFeatureChange(item, requestId)),
    modified: arrayValue(value.modified ?? [], requestId).map((item) => assertFeatureChange(item, requestId)),
  };
}

function assertNegotiationWhatIfSummary(value: unknown, requestId?: string): NegotiationWhatIfSummary | null {
  if (value === null || value === undefined) return null;
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    base_valuation: numberValue(value.base_valuation, requestId),
    scenario_valuation: numberValue(value.scenario_valuation, requestId),
    base_valuation_id: stringValue(value.base_valuation_id, requestId),
    scenario_valuation_id: stringValue(value.scenario_valuation_id, requestId),
    delta_value: numberValue(value.delta_value, requestId),
    delta_percentage: numberValue(value.delta_percentage, requestId),
    fairness_status: fairnessStatusValue(value.fairness_status, requestId),
    assumptions_used: arrayValue(value.assumptions_used, requestId).map((item) => stringValue(item, requestId)),
    feature_changes: assertFeatureChanges(value.feature_changes, requestId),
    source: sourceValue(value.source, requestId),
  };
}

function assertInvestmentNegotiationSummary(value: unknown, requestId?: string): InvestmentNegotiationSummary {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  return {
    negotiation_position: negotiationPositionValue(value.negotiation_position, requestId),
    negotiation_position_reason: stringValue(value.negotiation_position_reason, requestId),
    recommended_offer_band: assertRecommendedOfferBand(value.recommended_offer_band, requestId),
    broker_talking_points: arrayValue(value.broker_talking_points, requestId).map((item) =>
      assertTalkingPoint(item, requestId),
    ),
    source: sourceValue(value.source, requestId),
  };
}

function assertInvestmentWhatIfSummary(value: unknown, requestId?: string): InvestmentWhatIfSummary {
  if (!isRecord(value)) throw invalidInvestmentResponse(requestId);
  const status = value.status;
  if (status !== "Available" && status !== "Insufficient Evidence") {
    throw invalidInvestmentResponse(requestId);
  }

  return {
    status,
    reason: stringValue(value.reason, requestId),
    analysis: assertNegotiationWhatIfSummary(value.analysis, requestId),
    source: investmentWhatIfSourceValue(value.source, requestId),
  };
}

function assertInvestmentResponse(value: unknown, requestId?: string): InvestmentToolResponse {
  if (!isRecord(value) || value.tool_name !== "investment") throw invalidInvestmentResponse(requestId);

  return {
    tool_name: "investment",
    valuation_id: stringValue(value.valuation_id, requestId),
    asking_price: numberValue(value.asking_price, requestId),
    fair_price: numberValue(value.fair_price, requestId),
    fairness_status: fairnessStatusValue(value.fairness_status, requestId),
    price_gap: numberValue(value.price_gap, requestId),
    price_gap_percentage: numberValue(value.price_gap_percentage, requestId),
    investment_position: investmentPositionValue(value.investment_position, requestId),
    investment_position_reason: stringValue(value.investment_position_reason, requestId),
    investment_position_evidence: arrayValue(value.investment_position_evidence, requestId).map((item) =>
      assertEvidenceReference(item, requestId),
    ),
    confidence_level: stringValue(value.confidence_level, requestId),
    confidence_reason: stringValue(value.confidence_reason, requestId),
    investment_summary: stringValue(value.investment_summary, requestId),
    strengths: arrayValue(value.strengths, requestId).map((item) => assertInvestmentFinding(item, requestId)),
    risks: arrayValue(value.risks, requestId).map((item) => assertInvestmentFinding(item, requestId)),
    evidence_summary: assertEvidenceSummary(value.evidence_summary, requestId),
    comparable_summary: assertComparableSummary(value.comparable_summary, requestId),
    negotiation_summary: assertInvestmentNegotiationSummary(value.negotiation_summary, requestId),
    what_if_summary: assertInvestmentWhatIfSummary(value.what_if_summary, requestId),
    timestamp: stringValue(value.timestamp, requestId),
    source: sourceValue(value.source, requestId),
  };
}

export async function runInvestmentAnalysis(
  request: InvestmentToolRequest,
  signal?: AbortSignal,
): Promise<InvestmentAnalysisResult> {
  const safeRequest = assertInvestmentRequest(request);
  const response = await http.post<ApiSuccessEnvelope<InvestmentToolResponse> | InvestmentToolResponse>(
    "/v1/copilot/tools/investment",
    safeRequest,
    { signal },
  );

  if (isApiSuccessEnvelope<InvestmentToolResponse>(response.data)) {
    return {
      data: assertInvestmentResponse(response.data.data, response.data.meta.request_id),
      meta: response.data.meta,
    };
  }

  return {
    data: assertInvestmentResponse(response.data),
    meta: {},
  };
}
