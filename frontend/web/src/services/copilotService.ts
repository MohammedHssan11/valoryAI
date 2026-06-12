import { http } from "@/api/http";
import { ApiMeta, ApiSuccessEnvelope, isApiSuccessEnvelope, ValorApiError } from "@/api/contracts";
import type {
  CopilotAudit,
  CopilotCitationPackage,
  CopilotCompositionStatus,
  CopilotFailedTool,
  CopilotFrontendPayload,
  CopilotFrontendToolOutput,
  CopilotOrchestratorRequest,
  CopilotOrchestratorResponse,
  CopilotToolOrderingMetadata,
} from "@/types/copilot";

export interface CopilotResult {
  data: CopilotOrchestratorResponse;
  meta: ApiMeta;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function invalidCopilotResponse(requestId?: string): ValorApiError {
  return new ValorApiError(
    {
      code: "INVALID_API_RESPONSE",
      message: "The ValorAI API returned an unexpected Copilot orchestrator response.",
      details: [],
    },
    { requestId },
  );
}

function invalidCopilotRequest(message: string, field?: string): ValorApiError {
  return new ValorApiError({
    code: "INVALID_COPILOT_REQUEST",
    message,
    details: field ? [{ code: "INVALID_COPILOT_REQUEST", message, field }] : [],
  });
}

function assertPositiveInteger(value: unknown, field: string): asserts value is number {
  if (typeof value !== "number" || !Number.isInteger(value) || value <= 0) {
    throw invalidCopilotRequest(`${field} must be a positive integer.`, field);
  }
}

function stringValue(value: unknown, requestId?: string): string {
  if (typeof value === "string") return value;
  throw invalidCopilotResponse(requestId);
}

function nullableStringValue(value: unknown, requestId?: string): string | null {
  if (value === null || value === undefined) return null;
  return stringValue(value, requestId);
}

function numberValue(value: unknown, requestId?: string): number {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  throw invalidCopilotResponse(requestId);
}

function nullableNumberValue(value: unknown, requestId?: string): number | null {
  if (value === null || value === undefined) return null;
  return numberValue(value, requestId);
}

function stringArrayValue(value: unknown, requestId?: string): string[] {
  if (!Array.isArray(value)) throw invalidCopilotResponse(requestId);
  return value.map((item) => stringValue(item, requestId));
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

function assertRequest(request: CopilotOrchestratorRequest): CopilotOrchestratorRequest {
  assertPositiveInteger(request.workspace_id, "workspace_id");
  if (request.scenario_id != null) {
    assertPositiveInteger(request.scenario_id, "scenario_id");
  }
  if (typeof request.message !== "string" || request.message.trim().length === 0) {
    throw invalidCopilotRequest("message must be a non-empty string.", "message");
  }
  if (request.message.length > 4000) {
    throw invalidCopilotRequest("message must be 4000 characters or fewer.", "message");
  }
  if (request.broker_session_id != null) {
    if (typeof request.broker_session_id !== "string" || request.broker_session_id.trim().length === 0) {
      throw invalidCopilotRequest("broker_session_id must be a non-empty string when supplied.", "broker_session_id");
    }
  }
  if (!isRecord(request.tool_inputs)) {
    throw invalidCopilotRequest("tool_inputs must be an object.", "tool_inputs");
  }

  const toolInputs = Object.fromEntries(
    Object.entries(request.tool_inputs).map(([key, value]) => {
      if (!isRecord(value)) {
        throw invalidCopilotRequest(`${key} input must be an object.`, `tool_inputs.${key}`);
      }
      return [key, compactUndefined(value)];
    }),
  );

  return {
    workspace_id: request.workspace_id,
    scenario_id: request.scenario_id ?? null,
    broker_session_id: request.broker_session_id ?? null,
    message: request.message.trim(),
    tool_inputs: toolInputs as CopilotOrchestratorRequest["tool_inputs"],
  };
}

function compositionStatusValue(value: unknown, requestId?: string): CopilotCompositionStatus {
  if (
    value === "SUCCESS" ||
    value === "PARTIAL_SUCCESS" ||
    value === "FAILED" ||
    value === "SPARSE_EVIDENCE" ||
    value === "CLARIFICATION_REQUIRED"
  ) {
    return value;
  }
  throw invalidCopilotResponse(requestId);
}

function assertOrderingMetadata(value: unknown, requestId?: string): CopilotToolOrderingMetadata {
  if (!isRecord(value)) throw invalidCopilotResponse(requestId);
  return {
    order_index: numberValue(value.order_index, requestId),
    parallel_group_index: nullableNumberValue(value.parallel_group_index, requestId),
  };
}

function assertCitationPackage(value: unknown, requestId?: string): CopilotCitationPackage {
  if (!isRecord(value)) throw invalidCopilotResponse(requestId);
  return {
    valuation_ids: stringArrayValue(value.valuation_ids, requestId),
    tool_event_ids: stringArrayValue(value.tool_event_ids, requestId),
    comparable_ids: stringArrayValue(value.comparable_ids, requestId),
    unavailable_optional_citation_types: stringArrayValue(
      value.unavailable_optional_citation_types,
      requestId,
    ),
  };
}

function assertToolOutput(value: unknown, requestId?: string): CopilotFrontendToolOutput {
  if (!isRecord(value) || !isRecord(value.payload)) throw invalidCopilotResponse(requestId);
  return {
    planned_tool: stringValue(value.planned_tool, requestId) as CopilotFrontendToolOutput["planned_tool"],
    tool_name: stringValue(value.tool_name, requestId),
    payload: { ...value.payload },
    ordering_metadata: assertOrderingMetadata(value.ordering_metadata, requestId),
  };
}

function assertFailedTool(value: unknown, requestId?: string): CopilotFailedTool {
  if (!isRecord(value)) throw invalidCopilotResponse(requestId);
  return {
    planned_tool: stringValue(value.planned_tool, requestId),
    tool_name: stringValue(value.tool_name, requestId),
    error_type: stringValue(value.error_type, requestId),
    failure_category:
      value.failure_category === undefined ? undefined : stringValue(value.failure_category, requestId),
    ordering_metadata: assertOrderingMetadata(value.ordering_metadata, requestId),
  };
}

function assertFrontendPayload(value: unknown, requestId?: string): CopilotFrontendPayload {
  if (!isRecord(value)) throw invalidCopilotResponse(requestId);
  const citations = assertCitationPackage(value.citations, requestId);
  const evidence = value.full_evidence;
  if (!isRecord(evidence)) throw invalidCopilotResponse(requestId);
  const responseSections = value.response_sections;
  return {
    schema_version: value.schema_version === "1.0" ? "1.0" : (() => { throw invalidCopilotResponse(requestId); })(),
    composition_status: compositionStatusValue(value.composition_status, requestId),
    tool_outputs: Array.isArray(value.tool_outputs)
      ? value.tool_outputs.map((item) => assertToolOutput(item, requestId))
      : (() => { throw invalidCopilotResponse(requestId); })(),
    failed_tools: Array.isArray(value.failed_tools)
      ? value.failed_tools.map((item) => assertFailedTool(item, requestId))
      : (() => { throw invalidCopilotResponse(requestId); })(),
    full_evidence: { ...evidence },
    citations,
    response_sections: isRecord(responseSections) ? { ...responseSections } : undefined,
  };
}

function assertAudit(value: unknown, requestId?: string): CopilotAudit {
  if (!isRecord(value)) throw invalidCopilotResponse(requestId);
  return {
    ...value,
    plan_id: value.plan_id === undefined ? undefined : stringValue(value.plan_id, requestId),
    execution_id: value.execution_id === undefined ? undefined : stringValue(value.execution_id, requestId),
    composition_status:
      value.composition_status === undefined
        ? undefined
        : compositionStatusValue(value.composition_status, requestId),
    memory_id: value.memory_id === undefined ? undefined : stringValue(value.memory_id, requestId),
    memory_status: value.memory_status === undefined ? undefined : stringValue(value.memory_status, requestId),
    narration_status: stringValue(value.narration_status, requestId),
  };
}

function assertCopilotResponse(value: unknown, requestId?: string): CopilotOrchestratorResponse {
  if (!isRecord(value)) throw invalidCopilotResponse(requestId);
  const runtimeId = stringValue(value.runtime_id, requestId);
  if (runtimeId !== "COPILOT_ORCHESTRATOR_LLM_V1") throw invalidCopilotResponse(requestId);
  const response = value.response;
  return {
    runtime_id: runtimeId,
    response_id: stringValue(value.response_id, requestId),
    intent: stringValue(value.intent, requestId),
    status: stringValue(value.status, requestId),
    delivery_mode: stringValue(value.delivery_mode, requestId),
    response:
      response === null || response === undefined
        ? null
        : typeof response === "string"
          ? response
          : assertFrontendPayload(response, requestId),
    citation_package:
      value.citation_package === null || value.citation_package === undefined
        ? null
        : assertCitationPackage(value.citation_package, requestId),
    audit: assertAudit(value.audit, requestId),
  };
}

export async function runCopilot(
  request: CopilotOrchestratorRequest,
  signal?: AbortSignal,
): Promise<CopilotResult> {
  const safeRequest = assertRequest(request);
  const response = await http.post<ApiSuccessEnvelope<CopilotOrchestratorResponse> | CopilotOrchestratorResponse>(
    "/v1/copilot/orchestrator/respond",
    safeRequest,
    { signal },
  );

  if (isApiSuccessEnvelope<CopilotOrchestratorResponse>(response.data)) {
    return {
      data: assertCopilotResponse(response.data.data, response.data.meta.request_id),
      meta: response.data.meta,
    };
  }

  return {
    data: assertCopilotResponse(response.data),
    meta: {},
  };
}
