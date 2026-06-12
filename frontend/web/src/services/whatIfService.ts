import { http } from "@/api/http";
import { ApiMeta, ApiSuccessEnvelope, isApiSuccessEnvelope, ValorApiError } from "@/api/contracts";
import type {
  ComparableToolItem,
  ComparableToolResponse,
  ExplainabilityToolResponse,
  FeatureChange,
  FeatureChanges,
  WhatIfToolRequest,
  WhatIfToolResponse,
} from "@/types/whatIf";

export interface WhatIfAnalysisResult {
  data: WhatIfToolResponse;
  meta: ApiMeta;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function invalidWhatIfResponse(requestId?: string): ValorApiError {
  return new ValorApiError(
    {
      code: "INVALID_API_RESPONSE",
      message: "The ValorAI API returned an unexpected what-if response.",
      details: [],
    },
    { requestId },
  );
}

function invalidWhatIfRequest(message: string, field?: string): ValorApiError {
  return new ValorApiError({
    code: "INVALID_WHAT_IF_REQUEST",
    message,
    details: field ? [{ code: "INVALID_WHAT_IF_REQUEST", message, field }] : [],
  });
}

function assertPositiveInteger(value: unknown, field: string): asserts value is number {
  if (typeof value !== "number" || !Number.isInteger(value) || value <= 0) {
    throw invalidWhatIfRequest(`${field} must be a positive integer.`, field);
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

function assertWhatIfRequest(request: WhatIfToolRequest): WhatIfToolRequest {
  assertPositiveInteger(request.workspace_id, "workspace_id");
  assertPositiveInteger(request.property_id, "property_id");
  if (request.scenario_id != null) {
    assertPositiveInteger(request.scenario_id, "scenario_id");
  }

  const modifications = compactUndefined(request.modifications);
  if (!isRecord(modifications) || Object.keys(modifications).length === 0) {
    throw invalidWhatIfRequest("modifications must include at least one property change.", "modifications");
  }

  return {
    ...request,
    scenario_id: request.scenario_id ?? null,
    modifications,
  };
}

function stringValue(value: unknown, requestId?: string): string {
  if (typeof value === "string") return value;
  throw invalidWhatIfResponse(requestId);
}

function numberValue(value: unknown, requestId?: string): number {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  throw invalidWhatIfResponse(requestId);
}

function nullableStringValue(value: unknown, requestId?: string): string | null {
  if (value === null || value === undefined) return null;
  return stringValue(value, requestId);
}

function sourceValue(value: unknown, requestId?: string): "TruthLayer" {
  if (value === "TruthLayer") return "TruthLayer";
  throw invalidWhatIfResponse(requestId);
}

function arrayValue(value: unknown, requestId?: string): unknown[] {
  if (Array.isArray(value)) return value;
  throw invalidWhatIfResponse(requestId);
}

function assertFeatureChange(value: unknown, requestId?: string): FeatureChange {
  if (!isRecord(value)) throw invalidWhatIfResponse(requestId);
  return {
    feature: stringValue(value.feature, requestId),
    before: value.before ?? null,
    after: value.after ?? null,
    unit: nullableStringValue(value.unit, requestId),
  };
}

function assertFeatureChanges(value: unknown, requestId?: string): FeatureChanges {
  if (!isRecord(value)) throw invalidWhatIfResponse(requestId);
  return {
    added: arrayValue(value.added ?? [], requestId).map((item) => assertFeatureChange(item, requestId)),
    removed: arrayValue(value.removed ?? [], requestId).map((item) => assertFeatureChange(item, requestId)),
    modified: arrayValue(value.modified ?? [], requestId).map((item) => assertFeatureChange(item, requestId)),
  };
}

function assertExplainability(value: unknown, requestId?: string): ExplainabilityToolResponse {
  if (!isRecord(value)) throw invalidWhatIfResponse(requestId);
  return {
    tool_name: value.tool_name === "explainability" ? "explainability" : (() => { throw invalidWhatIfResponse(requestId); })(),
    valuation_id: stringValue(value.valuation_id, requestId),
    summary: stringValue(value.summary, requestId),
    why_this_price: stringValue(value.why_this_price, requestId),
    strongest_factors: stringValue(value.strongest_factors, requestId),
    confidence_reason: stringValue(value.confidence_reason, requestId),
    fairness_status: stringValue(value.fairness_status, requestId),
    feature_drivers: arrayValue(value.feature_drivers, requestId).map((item) => (isRecord(item) ? item : (() => { throw invalidWhatIfResponse(requestId); })())),
    comparable_evidence: arrayValue(value.comparable_evidence, requestId).map((item) => (isRecord(item) ? item : (() => { throw invalidWhatIfResponse(requestId); })())),
    timestamp: stringValue(value.timestamp, requestId),
    source: sourceValue(value.source, requestId),
  };
}

function assertComparable(value: unknown, requestId?: string): ComparableToolItem {
  if (!isRecord(value)) throw invalidWhatIfResponse(requestId);
  return {
    comparable_id: stringValue(value.comparable_id, requestId),
    price: numberValue(value.price, requestId),
    size_sqm: numberValue(value.size_sqm, requestId),
    bedrooms: numberValue(value.bedrooms, requestId),
    bathrooms: numberValue(value.bathrooms, requestId),
    compound_name: nullableStringValue(value.compound_name, requestId),
    distance_km: numberValue(value.distance_km, requestId),
    similarity_reason: nullableStringValue(value.similarity_reason, requestId),
    source: sourceValue(value.source, requestId),
  };
}

function assertComparableResponse(value: unknown, requestId?: string): ComparableToolResponse {
  if (!isRecord(value)) throw invalidWhatIfResponse(requestId);
  return {
    tool_name: value.tool_name === "comparable" ? "comparable" : (() => { throw invalidWhatIfResponse(requestId); })(),
    valuation_id: stringValue(value.valuation_id, requestId),
    comparable_count: numberValue(value.comparable_count, requestId),
    comparables: arrayValue(value.comparables, requestId).map((item) => assertComparable(item, requestId)),
    timestamp: stringValue(value.timestamp, requestId),
    source: sourceValue(value.source, requestId),
  };
}

function assertFairnessStatus(value: unknown, requestId?: string): WhatIfToolResponse["fairness_status"] {
  if (value === "Below Fair Value" || value === "Within Fair Value" || value === "Above Fair Value") return value;
  throw invalidWhatIfResponse(requestId);
}

function assertWhatIfResponse(value: unknown, requestId?: string): WhatIfToolResponse {
  if (!isRecord(value)) throw invalidWhatIfResponse(requestId);
  if (value.tool_name !== "what_if") throw invalidWhatIfResponse(requestId);

  return {
    tool_name: "what_if",
    base_valuation: numberValue(value.base_valuation, requestId),
    scenario_valuation: numberValue(value.scenario_valuation, requestId),
    base_valuation_id: stringValue(value.base_valuation_id, requestId),
    scenario_valuation_id: stringValue(value.scenario_valuation_id, requestId),
    fairness_valuation_id: stringValue(value.fairness_valuation_id, requestId),
    delta_value: numberValue(value.delta_value, requestId),
    delta_percentage: numberValue(value.delta_percentage, requestId),
    fairness_status: assertFairnessStatus(value.fairness_status, requestId),
    confidence_level: stringValue(value.confidence_level, requestId),
    assumptions_used: arrayValue(value.assumptions_used, requestId).map((item) => stringValue(item, requestId)),
    feature_changes: assertFeatureChanges(value.feature_changes, requestId),
    explainability: assertExplainability(value.explainability, requestId),
    comparables: assertComparableResponse(value.comparables, requestId),
    timestamp: stringValue(value.timestamp, requestId),
    source: sourceValue(value.source, requestId),
  };
}

export async function runWhatIfAnalysis(
  request: WhatIfToolRequest,
  signal?: AbortSignal,
): Promise<WhatIfAnalysisResult> {
  const safeRequest = assertWhatIfRequest(request);
  const response = await http.post<ApiSuccessEnvelope<WhatIfToolResponse> | WhatIfToolResponse>(
    "/v1/copilot/tools/what-if",
    safeRequest,
    { signal },
  );

  if (isApiSuccessEnvelope<WhatIfToolResponse>(response.data)) {
    return {
      data: assertWhatIfResponse(response.data.data, response.data.meta.request_id),
      meta: response.data.meta,
    };
  }

  return {
    data: assertWhatIfResponse(response.data),
    meta: {},
  };
}
