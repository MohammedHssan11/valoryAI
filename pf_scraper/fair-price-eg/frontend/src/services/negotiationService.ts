import { http } from "@/api/http";
import { ApiMeta, ApiSuccessEnvelope, isApiSuccessEnvelope, ValorApiError } from "@/api/contracts";
import type {
  BrokerTalkingPoint,
  NegotiationComparableSummary,
  NegotiationEvidenceReference,
  NegotiationEvidenceSummary,
  NegotiationPosition,
  NegotiationToolRequest,
  NegotiationToolResponse,
  NegotiationWhatIfSummary,
  RecommendedOfferBand,
} from "@/types/negotiation";
import type { FairnessStatus, FeatureChange, FeatureChanges } from "@/types/whatIf";

export interface NegotiationAnalysisResult {
  data: NegotiationToolResponse;
  meta: ApiMeta;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function invalidNegotiationResponse(requestId?: string): ValorApiError {
  return new ValorApiError(
    {
      code: "INVALID_API_RESPONSE",
      message: "The ValorAI API returned an unexpected negotiation response.",
      details: [],
    },
    { requestId },
  );
}

function invalidNegotiationRequest(message: string, field?: string): ValorApiError {
  return new ValorApiError({
    code: "INVALID_NEGOTIATION_REQUEST",
    message,
    details: field ? [{ code: "INVALID_NEGOTIATION_REQUEST", message, field }] : [],
  });
}

function assertPositiveInteger(value: unknown, field: string): asserts value is number {
  if (typeof value !== "number" || !Number.isInteger(value) || value <= 0) {
    throw invalidNegotiationRequest(`${field} must be a positive integer.`, field);
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

function assertNegotiationRequest(request: NegotiationToolRequest): NegotiationToolRequest {
  assertPositiveInteger(request.workspace_id, "workspace_id");
  assertPositiveInteger(request.property_id, "property_id");
  assertPositiveInteger(request.asking_price_egp, "asking_price_egp");
  if (request.scenario_id != null) {
    assertPositiveInteger(request.scenario_id, "scenario_id");
  }

  const safeRequest: NegotiationToolRequest = {
    workspace_id: request.workspace_id,
    property_id: request.property_id,
    scenario_id: request.scenario_id ?? null,
    asking_price_egp: request.asking_price_egp,
  };

  if (request.what_if_modifications != null) {
    const modifications = compactUndefined(request.what_if_modifications);
    if (!isRecord(modifications) || Object.keys(modifications).length === 0) {
      throw invalidNegotiationRequest(
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
  throw invalidNegotiationResponse(requestId);
}

function numberValue(value: unknown, requestId?: string): number {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  throw invalidNegotiationResponse(requestId);
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
  throw invalidNegotiationResponse(requestId);
}

function sourceValue(value: unknown, requestId?: string): "TruthLayer" {
  if (value === "TruthLayer") return "TruthLayer";
  throw invalidNegotiationResponse(requestId);
}

function derivedSourceValue(value: unknown, requestId?: string): "TruthLayer-derived" {
  if (value === "TruthLayer-derived") return "TruthLayer-derived";
  throw invalidNegotiationResponse(requestId);
}

function fairnessStatusValue(value: unknown, requestId?: string): FairnessStatus {
  if (value === "Below Fair Value" || value === "Within Fair Value" || value === "Above Fair Value") return value;
  throw invalidNegotiationResponse(requestId);
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
  throw invalidNegotiationResponse(requestId);
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
  throw invalidNegotiationResponse(requestId);
}

function assertEvidenceReference(value: unknown, requestId?: string): NegotiationEvidenceReference {
  if (!isRecord(value)) throw invalidNegotiationResponse(requestId);
  return {
    source_tool: sourceToolValue(value.source_tool, requestId),
    valuation_id: nullableStringValue(value.valuation_id, requestId),
    field: stringValue(value.field, requestId),
    comparable_id: nullableStringValue(value.comparable_id, requestId),
  };
}

function assertTalkingPoint(value: unknown, requestId?: string): BrokerTalkingPoint {
  if (!isRecord(value)) throw invalidNegotiationResponse(requestId);
  return {
    text: stringValue(value.text, requestId),
    evidence: arrayValue(value.evidence, requestId).map((item) => assertEvidenceReference(item, requestId)),
  };
}

function assertPriceRange(value: unknown, requestId?: string): { low: number; high: number } {
  if (!isRecord(value)) throw invalidNegotiationResponse(requestId);
  return {
    low: numberValue(value.low, requestId),
    high: numberValue(value.high, requestId),
  };
}

function assertEvidenceSummary(value: unknown, requestId?: string): NegotiationEvidenceSummary {
  if (!isRecord(value)) throw invalidNegotiationResponse(requestId);
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
  if (!isRecord(value)) throw invalidNegotiationResponse(requestId);
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
  if (!isRecord(value)) throw invalidNegotiationResponse(requestId);
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
  if (!isRecord(value)) throw invalidNegotiationResponse(requestId);
  return {
    feature: stringValue(value.feature, requestId),
    before: value.before ?? null,
    after: value.after ?? null,
    unit: nullableStringValue(value.unit, requestId),
  };
}

function assertFeatureChanges(value: unknown, requestId?: string): FeatureChanges {
  if (!isRecord(value)) throw invalidNegotiationResponse(requestId);
  return {
    added: arrayValue(value.added ?? [], requestId).map((item) => assertFeatureChange(item, requestId)),
    removed: arrayValue(value.removed ?? [], requestId).map((item) => assertFeatureChange(item, requestId)),
    modified: arrayValue(value.modified ?? [], requestId).map((item) => assertFeatureChange(item, requestId)),
  };
}

function assertWhatIfSummary(value: unknown, requestId?: string): NegotiationWhatIfSummary | null {
  if (value === null || value === undefined) return null;
  if (!isRecord(value)) throw invalidNegotiationResponse(requestId);
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

function assertNegotiationResponse(value: unknown, requestId?: string): NegotiationToolResponse {
  if (!isRecord(value) || value.tool_name !== "negotiation") throw invalidNegotiationResponse(requestId);

  return {
    tool_name: "negotiation",
    valuation_id: stringValue(value.valuation_id, requestId),
    asking_price: numberValue(value.asking_price, requestId),
    fair_price: numberValue(value.fair_price, requestId),
    fairness_status: fairnessStatusValue(value.fairness_status, requestId),
    price_gap: numberValue(value.price_gap, requestId),
    price_gap_percentage: numberValue(value.price_gap_percentage, requestId),
    confidence_level: stringValue(value.confidence_level, requestId),
    confidence_reason: stringValue(value.confidence_reason, requestId),
    negotiation_position: negotiationPositionValue(value.negotiation_position, requestId),
    negotiation_position_reason: stringValue(value.negotiation_position_reason, requestId),
    negotiation_position_evidence: arrayValue(value.negotiation_position_evidence, requestId).map((item) =>
      assertEvidenceReference(item, requestId),
    ),
    broker_talking_points: arrayValue(value.broker_talking_points, requestId).map((item) =>
      assertTalkingPoint(item, requestId),
    ),
    evidence_summary: assertEvidenceSummary(value.evidence_summary, requestId),
    comparable_summary: assertComparableSummary(value.comparable_summary, requestId),
    recommended_offer_band: assertRecommendedOfferBand(value.recommended_offer_band, requestId),
    risk_notes: arrayValue(value.risk_notes, requestId).map((item) => assertTalkingPoint(item, requestId)),
    what_if_analysis: assertWhatIfSummary(value.what_if_analysis, requestId),
    timestamp: stringValue(value.timestamp, requestId),
    source: sourceValue(value.source, requestId),
  };
}

export async function runNegotiationAnalysis(
  request: NegotiationToolRequest,
  signal?: AbortSignal,
): Promise<NegotiationAnalysisResult> {
  const safeRequest = assertNegotiationRequest(request);
  const response = await http.post<ApiSuccessEnvelope<NegotiationToolResponse> | NegotiationToolResponse>(
    "/v1/copilot/tools/negotiation",
    safeRequest,
    { signal },
  );

  if (isApiSuccessEnvelope<NegotiationToolResponse>(response.data)) {
    return {
      data: assertNegotiationResponse(response.data.data, response.data.meta.request_id),
      meta: response.data.meta,
    };
  }

  return {
    data: assertNegotiationResponse(response.data),
    meta: {},
  };
}
