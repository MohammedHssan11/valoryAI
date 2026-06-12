import { http } from "@/api/http";
import { ApiMeta, ApiSuccessEnvelope, isApiSuccessEnvelope, ValorApiError } from "@/api/contracts";
import type {
  MarketInsightComparableDensity,
  MarketInsightConfidenceDistribution,
  MarketInsightDensityLevel,
  MarketInsightEvidenceSummary,
  MarketInsightFairValueDistribution,
  MarketInsightSegment,
  MarketInsightStatement,
  MarketInsightToolRequest,
  MarketInsightToolResponse,
} from "@/types/marketInsight";

export interface MarketInsightResult {
  data: MarketInsightToolResponse;
  meta: ApiMeta;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function invalidMarketInsightResponse(requestId?: string): ValorApiError {
  return new ValorApiError(
    {
      code: "INVALID_API_RESPONSE",
      message: "The ValorAI API returned an unexpected market intelligence response.",
      details: [],
    },
    { requestId },
  );
}

function invalidMarketInsightRequest(message: string, field?: string): ValorApiError {
  return new ValorApiError({
    code: "INVALID_MARKET_INSIGHT_REQUEST",
    message,
    details: field ? [{ code: "INVALID_MARKET_INSIGHT_REQUEST", message, field }] : [],
  });
}

function assertPositiveInteger(value: unknown, field: string): asserts value is number {
  if (typeof value !== "number" || !Number.isInteger(value) || value <= 0) {
    throw invalidMarketInsightRequest(`${field} must be a positive integer.`, field);
  }
}

function normalizedOptionalString(value: unknown, field: string, maxLength: number): string | undefined {
  if (value === null || value === undefined) return undefined;
  if (typeof value !== "string") {
    throw invalidMarketInsightRequest(`${field} must be a string.`, field);
  }
  const trimmed = value.trim();
  if (trimmed.length === 0) return undefined;
  if (trimmed.length > maxLength) {
    throw invalidMarketInsightRequest(`${field} must be ${maxLength} characters or fewer.`, field);
  }
  return trimmed;
}

function normalizedTimeWindow(value: unknown): string {
  if (value === null || value === undefined || value === "") return "all";
  if (typeof value !== "string") {
    throw invalidMarketInsightRequest("time_window must be all or a positive day window.", "time_window");
  }
  const trimmed = value.trim();
  if (!/^(all|[1-9][0-9]*d)$/.test(trimmed)) {
    throw invalidMarketInsightRequest("time_window must be all or a positive day window.", "time_window");
  }
  return trimmed;
}

export function normalizeMarketInsightRequest(request: MarketInsightToolRequest): MarketInsightToolRequest {
  assertPositiveInteger(request.workspace_id, "workspace_id");

  const safeRequest: MarketInsightToolRequest = {
    workspace_id: request.workspace_id,
    time_window: normalizedTimeWindow(request.time_window),
  };
  const compoundName = normalizedOptionalString(request.compound_name, "compound_name", 255);
  const h3Res9 = normalizedOptionalString(request.h3_res9, "h3_res9", 32);
  const propertyType = normalizedOptionalString(request.property_type, "property_type", 120);

  if (compoundName) safeRequest.compound_name = compoundName;
  if (h3Res9) safeRequest.h3_res9 = h3Res9;
  if (propertyType) safeRequest.property_type = propertyType;

  return safeRequest;
}

function stringValue(value: unknown, requestId?: string): string {
  if (typeof value === "string") return value;
  throw invalidMarketInsightResponse(requestId);
}

function numberValue(value: unknown, requestId?: string): number {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  throw invalidMarketInsightResponse(requestId);
}

function integerValue(value: unknown, requestId?: string): number {
  const number = numberValue(value, requestId);
  if (Number.isInteger(number) && number >= 0) return number;
  throw invalidMarketInsightResponse(requestId);
}

function nullableNumberValue(value: unknown, requestId?: string): number | null {
  if (value === null || value === undefined) return null;
  return numberValue(value, requestId);
}

function nullableStringValue(value: unknown, requestId?: string): string | null {
  if (value === null || value === undefined) return null;
  return stringValue(value, requestId);
}

function arrayValue(value: unknown, requestId?: string): unknown[] {
  if (Array.isArray(value)) return value;
  throw invalidMarketInsightResponse(requestId);
}

function sourceValue(value: unknown, requestId?: string): "TruthLayer" {
  if (value === "TruthLayer") return "TruthLayer";
  throw invalidMarketInsightResponse(requestId);
}

function densityLevelValue(value: unknown, requestId?: string): MarketInsightDensityLevel {
  if (value === "High" || value === "Moderate" || value === "Sparse" || value === "Insufficient Evidence") {
    return value;
  }
  throw invalidMarketInsightResponse(requestId);
}

function countRecordValue(value: unknown, requestId?: string): Record<string, number> {
  if (!isRecord(value)) throw invalidMarketInsightResponse(requestId);
  return Object.fromEntries(
    Object.entries(value).map(([key, entry]) => [key, integerValue(entry, requestId)]),
  );
}

function unknownRecordValue(value: unknown, requestId?: string): Record<string, unknown> {
  if (!isRecord(value)) throw invalidMarketInsightResponse(requestId);
  return { ...value };
}

function assertConfidenceDistribution(
  value: unknown,
  requestId?: string,
): MarketInsightConfidenceDistribution {
  if (!isRecord(value)) throw invalidMarketInsightResponse(requestId);
  return {
    valuation_count: integerValue(value.valuation_count, requestId),
    counts: countRecordValue(value.counts, requestId),
    predominant_level: nullableStringValue(value.predominant_level, requestId),
  };
}

function assertFairValueDistribution(
  value: unknown,
  requestId?: string,
): MarketInsightFairValueDistribution {
  if (!isRecord(value)) throw invalidMarketInsightResponse(requestId);
  return {
    valuation_count: integerValue(value.valuation_count, requestId),
    minimum_fair_value: nullableNumberValue(value.minimum_fair_value, requestId),
    median_fair_value: nullableNumberValue(value.median_fair_value, requestId),
    maximum_fair_value: nullableNumberValue(value.maximum_fair_value, requestId),
  };
}

function assertComparableDensity(value: unknown, requestId?: string): MarketInsightComparableDensity {
  if (!isRecord(value)) throw invalidMarketInsightResponse(requestId);
  return {
    valuation_count: integerValue(value.valuation_count, requestId),
    minimum_comparable_count: nullableNumberValue(value.minimum_comparable_count, requestId),
    median_comparable_count: nullableNumberValue(value.median_comparable_count, requestId),
    maximum_comparable_count: nullableNumberValue(value.maximum_comparable_count, requestId),
    density_level: densityLevelValue(value.density_level, requestId),
    measurement_sources: countRecordValue(value.measurement_sources, requestId),
  };
}

function assertSegment(value: unknown, requestId?: string): MarketInsightSegment {
  if (!isRecord(value)) throw invalidMarketInsightResponse(requestId);
  return {
    name: stringValue(value.name, requestId),
    valuation_count: integerValue(value.valuation_count, requestId),
    median_fair_value: numberValue(value.median_fair_value, requestId),
    confidence_distribution: countRecordValue(value.confidence_distribution, requestId),
    comparable_density: densityLevelValue(value.comparable_density, requestId),
    median_comparable_count: nullableNumberValue(value.median_comparable_count, requestId),
  };
}

function assertStatement(value: unknown, requestId?: string): MarketInsightStatement {
  if (!isRecord(value)) throw invalidMarketInsightResponse(requestId);
  return {
    text: stringValue(value.text, requestId),
    evidence: arrayValue(value.evidence, requestId).map((item) => stringValue(item, requestId)),
  };
}

function assertEvidenceSummary(value: unknown, requestId?: string): MarketInsightEvidenceSummary {
  if (!isRecord(value)) throw invalidMarketInsightResponse(requestId);
  return {
    valuation_ids: arrayValue(value.valuation_ids, requestId).map((item) => stringValue(item, requestId)),
    source_record_counts: countRecordValue(value.source_record_counts, requestId),
    filters_used: unknownRecordValue(value.filters_used, requestId),
    statements: arrayValue(value.statements, requestId).map((item) => assertStatement(item, requestId)),
    traceability_note: stringValue(value.traceability_note, requestId),
  };
}

function assertMarketInsightResponse(value: unknown, requestId?: string): MarketInsightToolResponse {
  if (!isRecord(value) || value.tool_name !== "market_insight") throw invalidMarketInsightResponse(requestId);
  return {
    tool_name: "market_insight",
    market_summary: stringValue(value.market_summary, requestId),
    valuation_volume: integerValue(value.valuation_volume, requestId),
    confidence_distribution: assertConfidenceDistribution(value.confidence_distribution, requestId),
    fair_value_distribution: assertFairValueDistribution(value.fair_value_distribution, requestId),
    comparable_density: assertComparableDensity(value.comparable_density, requestId),
    active_compounds: arrayValue(value.active_compounds, requestId).map((item) => assertSegment(item, requestId)),
    active_areas: arrayValue(value.active_areas, requestId).map((item) => assertSegment(item, requestId)),
    evidence_summary: assertEvidenceSummary(value.evidence_summary, requestId),
    data_sources_used: arrayValue(value.data_sources_used, requestId).map((item) => stringValue(item, requestId)),
    timestamp: stringValue(value.timestamp, requestId),
    source: sourceValue(value.source, requestId),
  };
}

export async function runMarketInsight(
  request: MarketInsightToolRequest,
  signal?: AbortSignal,
): Promise<MarketInsightResult> {
  const safeRequest = normalizeMarketInsightRequest(request);
  const response = await http.post<ApiSuccessEnvelope<MarketInsightToolResponse> | MarketInsightToolResponse>(
    "/v1/copilot/tools/market-insight",
    safeRequest,
    { signal },
  );

  if (isApiSuccessEnvelope<MarketInsightToolResponse>(response.data)) {
    return {
      data: assertMarketInsightResponse(response.data.data, response.data.meta.request_id),
      meta: response.data.meta,
    };
  }

  return {
    data: assertMarketInsightResponse(response.data),
    meta: {},
  };
}
