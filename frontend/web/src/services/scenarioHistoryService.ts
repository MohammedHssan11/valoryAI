import { http } from "@/api/http";
import { ApiSuccessEnvelope, isApiSuccessEnvelope, ValorApiError } from "@/api/contracts";
import type {
  ScenarioState,
  ScenarioStateCreate,
  ScenarioStateUpdate,
  ScenarioTreeNode,
} from "@/types/scenarioHistory";

function invalidScenarioResponse(requestId?: string): ValorApiError {
  return new ValorApiError(
    {
      code: "INVALID_API_RESPONSE",
      message: "The ValorAI API returned an unexpected scenario history response.",
      details: [],
    },
    { requestId },
  );
}

function invalidScenarioRequest(message: string, field?: string): ValorApiError {
  return new ValorApiError({
    code: "INVALID_SCENARIO_REQUEST",
    message,
    details: field ? [{ code: "INVALID_SCENARIO_REQUEST", message, field }] : [],
  });
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

function positiveInteger(value: unknown, field: string): number {
  if (typeof value === "number" && Number.isInteger(value) && value > 0) return value;
  throw invalidScenarioRequest(`${field} must be a positive integer.`, field);
}

function optionalPositiveInteger(value: unknown, field: string): number | null {
  if (value === null || value === undefined) return null;
  return positiveInteger(value, field);
}

function stringValue(value: unknown, requestId?: string): string {
  if (typeof value === "string") return value;
  throw invalidScenarioResponse(requestId);
}

function optionalStringValue(value: unknown, requestId?: string): string | undefined {
  if (value === undefined || value === null) return undefined;
  return stringValue(value, requestId);
}

function nullableStringValue(value: unknown, requestId?: string): string | null {
  if (value === undefined || value === null) return null;
  return stringValue(value, requestId);
}

function numberValue(value: unknown, requestId?: string): number {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && value.trim().length > 0) {
    const parsed = Number(value);
    if (Number.isFinite(parsed)) return parsed;
  }
  throw invalidScenarioResponse(requestId);
}

function nullableNumberValue(value: unknown, requestId?: string): number | null {
  if (value === undefined || value === null) return null;
  return numberValue(value, requestId);
}

function booleanValue(value: unknown, requestId?: string): boolean | undefined {
  if (value === undefined || value === null) return undefined;
  if (typeof value === "boolean") return value;
  throw invalidScenarioResponse(requestId);
}

function recordValue(value: unknown, requestId?: string): Record<string, unknown> {
  if (isRecord(value)) return value;
  throw invalidScenarioResponse(requestId);
}

function assertScenario(value: unknown, requestId?: string): ScenarioState {
  if (!isRecord(value)) throw invalidScenarioResponse(requestId);

  return {
    id: positiveInteger(value.id, "id"),
    created_at: optionalStringValue(value.created_at, requestId),
    updated_at: optionalStringValue(value.updated_at, requestId),
    version: value.version === undefined ? undefined : positiveInteger(value.version, "version"),
    is_deleted: booleanValue(value.is_deleted, requestId),
    deleted_at: nullableStringValue(value.deleted_at, requestId),
    user_id: value.user_id === undefined ? undefined : positiveInteger(value.user_id, "user_id"),
    workspace_id: positiveInteger(value.workspace_id, "workspace_id"),
    property_state_id: positiveInteger(value.property_state_id, "property_state_id"),
    parent_scenario_id: optionalPositiveInteger(value.parent_scenario_id, "parent_scenario_id"),
    name: stringValue(value.name, requestId),
    modifications: recordValue(value.modifications, requestId),
    delta_value: nullableNumberValue(value.delta_value, requestId),
  };
}

function assertScenarioList(value: unknown, requestId?: string): ScenarioState[] {
  if (Array.isArray(value)) return value.map((item) => assertScenario(item, requestId));
  throw invalidScenarioResponse(requestId);
}

function assertScenarioTree(value: unknown, requestId?: string): ScenarioTreeNode {
  const scenario = assertScenario(value, requestId);
  if (!isRecord(value)) throw invalidScenarioResponse(requestId);
  const children = value.children === undefined ? [] : value.children;
  if (!Array.isArray(children)) throw invalidScenarioResponse(requestId);
  return {
    ...scenario,
    children: children.map((child) => assertScenarioTree(child, requestId)),
  };
}

function assertScenarioTreeList(value: unknown, requestId?: string): ScenarioTreeNode[] {
  if (Array.isArray(value)) return value.map((item) => assertScenarioTree(item, requestId));
  throw invalidScenarioResponse(requestId);
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

function assertCreateRequest(request: ScenarioStateCreate): ScenarioStateCreate {
  positiveInteger(request.property_state_id, "property_state_id");
  optionalPositiveInteger(request.parent_scenario_id, "parent_scenario_id");
  if (request.name.trim().length === 0) {
    throw invalidScenarioRequest("name must not be empty.", "name");
  }
  if (!isRecord(request.modifications)) {
    throw invalidScenarioRequest("modifications must be an object.", "modifications");
  }
  return {
    ...request,
    name: request.name.trim(),
    parent_scenario_id: request.parent_scenario_id ?? null,
    modifications: compactUndefined(request.modifications) as Record<string, unknown>,
    delta_value: request.delta_value ?? null,
  };
}

export async function listPropertyScenarios(propertyId: number, signal?: AbortSignal): Promise<ScenarioState[]> {
  positiveInteger(propertyId, "property_id");
  const response = await http.get<ApiSuccessEnvelope<ScenarioState[]> | ScenarioState[]>(
    `/v1/copilot/properties/${propertyId}/scenarios`,
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertScenarioList(unwrapped.data, unwrapped.requestId);
}

export async function getScenario(scenarioId: number, signal?: AbortSignal): Promise<ScenarioState> {
  positiveInteger(scenarioId, "scenario_id");
  const response = await http.get<ApiSuccessEnvelope<ScenarioState> | ScenarioState>(
    `/v1/copilot/scenarios/${scenarioId}`,
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertScenario(unwrapped.data, unwrapped.requestId);
}

export async function getScenarioLineage(scenarioId: number, signal?: AbortSignal): Promise<ScenarioState[]> {
  positiveInteger(scenarioId, "scenario_id");
  const response = await http.get<ApiSuccessEnvelope<ScenarioState[]> | ScenarioState[]>(
    `/v1/copilot/scenarios/${scenarioId}/lineage`,
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertScenarioList(unwrapped.data, unwrapped.requestId);
}

export async function getScenarioTree(propertyId: number, signal?: AbortSignal): Promise<ScenarioTreeNode[]> {
  positiveInteger(propertyId, "property_id");
  const response = await http.get<ApiSuccessEnvelope<ScenarioTreeNode[]> | ScenarioTreeNode[]>(
    `/v1/copilot/properties/${propertyId}/scenario-tree`,
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertScenarioTreeList(unwrapped.data, unwrapped.requestId);
}

export async function createScenario(request: ScenarioStateCreate, signal?: AbortSignal): Promise<ScenarioState> {
  const safeRequest = assertCreateRequest(request);
  const response = await http.post<ApiSuccessEnvelope<ScenarioState> | ScenarioState>(
    "/v1/copilot/scenarios",
    safeRequest,
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertScenario(unwrapped.data, unwrapped.requestId);
}

export async function updateScenario(
  scenarioId: number,
  request: ScenarioStateUpdate,
  signal?: AbortSignal,
): Promise<ScenarioState> {
  positiveInteger(scenarioId, "scenario_id");
  const response = await http.put<ApiSuccessEnvelope<ScenarioState> | ScenarioState>(
    `/v1/copilot/scenarios/${scenarioId}`,
    compactUndefined(request),
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertScenario(unwrapped.data, unwrapped.requestId);
}

export async function restoreScenario(scenarioId: number, signal?: AbortSignal): Promise<ScenarioState> {
  positiveInteger(scenarioId, "scenario_id");
  const response = await http.post<ApiSuccessEnvelope<ScenarioState> | ScenarioState>(
    `/v1/copilot/scenarios/${scenarioId}/restore`,
    {},
    { signal },
  );
  const unwrapped = unwrap(response.data);
  return assertScenario(unwrapped.data, unwrapped.requestId);
}
