import { http } from "@/api/http";
import { ApiSuccessEnvelope, isApiSuccessEnvelope, ValorApiError } from "@/api/contracts";
import type {
  BackendPropertyContext,
  BackendToolEvent,
  BackendWorkspaceContext,
  PropertyContextBinding,
  PropertyContextBridgeInput,
} from "@/types/propertyContext";
import type { RentFairPriceData, RentFairPriceRequest } from "@/types/valuation";

const DEFAULT_WORKSPACE_NAME = "ValorAI Active Valuations";
const PROPERTY_SIGNATURE_EXCLUDED_FIELDS = new Set(["target_price_egp"]);

function invalidPropertyContextResponse(requestId?: string): ValorApiError {
  return new ValorApiError(
    {
      code: "INVALID_API_RESPONSE",
      message: "The ValorAI API returned an unexpected property context response.",
      details: [],
    },
    { requestId },
  );
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function unwrap<T>(value: ApiSuccessEnvelope<T> | T): { data: T; requestId?: string } {
  if (isApiSuccessEnvelope<T>(value)) {
    return { data: value.data, requestId: value.meta.request_id };
  }
  return { data: value };
}

function assertWorkspace(value: unknown, requestId?: string): BackendWorkspaceContext {
  if (isRecord(value) && typeof value.id === "number" && typeof value.name === "string") {
    return value as unknown as BackendWorkspaceContext;
  }
  throw invalidPropertyContextResponse(requestId);
}

function assertWorkspaceList(value: unknown, requestId?: string): BackendWorkspaceContext[] {
  if (Array.isArray(value)) return value.map((item) => assertWorkspace(item, requestId));
  throw invalidPropertyContextResponse(requestId);
}

function assertPropertyContext(value: unknown, requestId?: string): BackendPropertyContext {
  if (
    isRecord(value) &&
    typeof value.id === "number" &&
    typeof value.workspace_id === "number" &&
    typeof value.label === "string" &&
    typeof value.location === "string" &&
    isRecord(value.valuation_inputs)
  ) {
    return value as unknown as BackendPropertyContext;
  }
  throw invalidPropertyContextResponse(requestId);
}

function assertPropertyContextList(value: unknown, requestId?: string): BackendPropertyContext[] {
  if (Array.isArray(value)) return value.map((item) => assertPropertyContext(item, requestId));
  throw invalidPropertyContextResponse(requestId);
}

function assertToolEvent(value: unknown, requestId?: string): BackendToolEvent {
  if (
    isRecord(value) &&
    typeof value.id === "number" &&
    typeof value.workspace_id === "number" &&
    typeof value.tool_name === "string" &&
    typeof value.event_type === "string" &&
    isRecord(value.payload)
  ) {
    return value as unknown as BackendToolEvent;
  }
  throw invalidPropertyContextResponse(requestId);
}

function compactJson(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(compactJson);
  }

  if (isRecord(value)) {
    return Object.fromEntries(
      Object.entries(value)
        .filter(([, entry]) => entry !== undefined)
        .map(([key, entry]) => [key, compactJson(entry)]),
    );
  }

  return value;
}

function stableComparableValue(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(stableComparableValue);
  }

  if (isRecord(value)) {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, stableComparableValue(value[key])]),
    );
  }

  return value;
}

function stableStringify(value: unknown): string {
  return JSON.stringify(stableComparableValue(value));
}

function normalizedValuationInputs(request: RentFairPriceRequest): Record<string, unknown> {
  const normalized = compactJson({
    ...request,
    property_category: request.property_category ?? "residential_rent",
    amenities: [...(request.amenities ?? [])].sort(),
  });

  return isRecord(normalized) ? normalized : {};
}

function propertySignatureFromInputs(inputs: Record<string, unknown>): string {
  const intrinsicInputs = Object.fromEntries(
    Object.entries(inputs).filter(([key]) => !PROPERTY_SIGNATURE_EXCLUDED_FIELDS.has(key)),
  );
  return stableStringify(intrinsicInputs);
}

function propertySignature(request: RentFairPriceRequest): string {
  return propertySignatureFromInputs(normalizedValuationInputs(request));
}

function firstString(...values: unknown[]): string | undefined {
  for (const value of values) {
    if (typeof value === "string" && value.trim().length > 0) {
      return value.trim();
    }
  }
  return undefined;
}

function readAreaName(valuation: RentFairPriceData): string | undefined {
  return firstString(
    valuation.area?.name,
    valuation.area?.area_name,
    valuation.resolved_location?.name,
    valuation.resolved_location?.area_name,
  );
}

function coordinatesLabel(request: RentFairPriceRequest): string | undefined {
  if (typeof request.lat === "number" && typeof request.lng === "number") {
    return `${request.lat.toFixed(6)}, ${request.lng.toFixed(6)}`;
  }
  return undefined;
}

function boundedText(value: string, maxLength: number): string {
  return value.length > maxLength ? value.slice(0, maxLength) : value;
}

function buildPropertyLabel(request: RentFairPriceRequest, valuation: RentFairPriceData): string {
  const areaName = firstString(request.compound_name, readAreaName(valuation), request.address, coordinatesLabel(request));
  return boundedText(`${request.property_type}${areaName ? ` - ${areaName}` : ""}`, 255);
}

function buildPropertyLocation(request: RentFairPriceRequest, valuation: RentFairPriceData): string {
  return boundedText(
    firstString(request.address, request.compound_name, readAreaName(valuation), coordinatesLabel(request), "Valuation property") ??
      "Valuation property",
    255,
  );
}

function nonNegativeInteger(value: number | null | undefined): number {
  if (typeof value !== "number" || !Number.isFinite(value)) return 0;
  return Math.max(0, Math.round(value));
}

function valuationEventPayload(
  request: RentFairPriceRequest,
  valuation: RentFairPriceData,
  requestId: string | undefined,
): Record<string, unknown> {
  return {
    source: "direct_valuation",
    request_id: requestId,
    property_context_signature: propertySignature(request),
    valuation_request: normalizedValuationInputs(request),
    valuation_result: {
      fair_price_egp: valuation.fair_price_egp,
      range_low_egp: valuation.range_low_egp,
      range_high_egp: valuation.range_high_egp,
      flag: valuation.flag,
      tier_used: valuation.tier_used,
      comps_count: valuation.comps_count,
      confidence: valuation.confidence,
      engine_used: valuation.engine_used,
      routing_reason: valuation.routing_reason,
      explainability: valuation.explainability,
      property_category: valuation.property_category,
      area: valuation.area,
      resolved_location: valuation.resolved_location,
      valuation_contract: valuation.valuation_contract,
      top_comparable_listing_ids: valuation.top_comps.map((comparable) => comparable.listing_id),
    },
  };
}

async function listWorkspaces(signal?: AbortSignal): Promise<BackendWorkspaceContext[]> {
  const response = await http.get<ApiSuccessEnvelope<BackendWorkspaceContext[]> | BackendWorkspaceContext[]>(
    "/v1/copilot/workspaces",
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertWorkspaceList(unwrapped.data, unwrapped.requestId);
}

async function createWorkspace(signal?: AbortSignal): Promise<BackendWorkspaceContext> {
  const response = await http.post<ApiSuccessEnvelope<BackendWorkspaceContext> | BackendWorkspaceContext>(
    "/v1/copilot/workspaces",
    { name: DEFAULT_WORKSPACE_NAME },
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertWorkspace(unwrapped.data, unwrapped.requestId);
}

async function listProperties(workspaceId: number, signal?: AbortSignal): Promise<BackendPropertyContext[]> {
  const response = await http.get<ApiSuccessEnvelope<BackendPropertyContext[]> | BackendPropertyContext[]>(
    `/v1/copilot/workspaces/${workspaceId}/properties`,
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertPropertyContextList(unwrapped.data, unwrapped.requestId);
}

async function createPropertyContext(
  workspace: BackendWorkspaceContext,
  request: RentFairPriceRequest,
  valuation: RentFairPriceData,
  signal?: AbortSignal,
): Promise<BackendPropertyContext> {
  const response = await http.post<ApiSuccessEnvelope<BackendPropertyContext> | BackendPropertyContext>(
    "/v1/copilot/properties",
    {
      workspace_id: workspace.id,
      label: buildPropertyLabel(request, valuation),
      location: buildPropertyLocation(request, valuation),
      area: request.size_sqm,
      bedrooms: nonNegativeInteger(request.bedrooms),
      bathrooms: nonNegativeInteger(request.bathrooms),
      amenities: { codes: [...(request.amenities ?? [])].sort() },
      property_type: request.property_type,
      property_category: request.property_category ?? valuation.property_category ?? "residential_rent",
      valuation_inputs: normalizedValuationInputs(request),
    },
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertPropertyContext(unwrapped.data, unwrapped.requestId);
}

async function recordValuationContextEvent(
  workspace: BackendWorkspaceContext,
  property: BackendPropertyContext,
  request: RentFairPriceRequest,
  valuation: RentFairPriceData,
  requestId: string | undefined,
  signal?: AbortSignal,
): Promise<BackendToolEvent> {
  const response = await http.post<ApiSuccessEnvelope<BackendToolEvent> | BackendToolEvent>(
    "/v1/copilot/tool-events",
    {
      workspace_id: workspace.id,
      property_state_id: property.id,
      scenario_state_id: null,
      tool_name: "direct_valuation",
      event_type: "valuation.completed",
      payload: valuationEventPayload(request, valuation, requestId),
    },
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertToolEvent(unwrapped.data, unwrapped.requestId);
}

function selectWorkspace(
  workspaces: BackendWorkspaceContext[],
  preferredWorkspaceId?: number | null,
): { workspace: BackendWorkspaceContext | null; reusedWorkspace: boolean } {
  const preferred = preferredWorkspaceId
    ? workspaces.find((workspace) => workspace.id === preferredWorkspaceId)
    : undefined;

  return {
    workspace: preferred ?? workspaces[0] ?? null,
    reusedWorkspace: Boolean(preferred ?? workspaces[0]),
  };
}

function findMatchingProperty(
  properties: BackendPropertyContext[],
  request: RentFairPriceRequest,
): BackendPropertyContext | undefined {
  const signature = propertySignature(request);
  return properties.find((property) => propertySignatureFromInputs(property.valuation_inputs) === signature);
}

export async function bridgeValuationToPropertyContext(input: PropertyContextBridgeInput): Promise<PropertyContextBinding> {
  const workspaces = await listWorkspaces(input.signal);
  const selected = selectWorkspace(workspaces, input.preferredWorkspaceId);
  const workspace = selected.workspace ?? (await createWorkspace(input.signal));
  const properties = await listProperties(workspace.id, input.signal);
  const matchedProperty = findMatchingProperty(properties, input.request);
  const property = matchedProperty ?? (await createPropertyContext(workspace, input.request, input.valuation, input.signal));
  const valuationEvent = await recordValuationContextEvent(
    workspace,
    property,
    input.request,
    input.valuation,
    input.requestId,
    input.signal,
  );

  return {
    activeWorkspaceId: workspace.id,
    activePropertyId: property.id,
    activeScenarioId: null,
    workspace,
    property,
    valuationEvent,
    reusedWorkspace: selected.reusedWorkspace,
    reusedProperty: Boolean(matchedProperty),
    requestId: input.requestId,
  };
}
