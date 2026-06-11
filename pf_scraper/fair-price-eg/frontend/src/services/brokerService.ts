import { http } from "@/api/http";
import { ApiMeta, ApiSuccessEnvelope, isApiErrorEnvelope, isApiSuccessEnvelope, ValorApiError } from "@/api/contracts";
import { authSessionManager } from "@/auth/authSessionManager";
import { appConfig } from "@/core/config";
import type { BrokerChatRequest, BrokerOrchestrationResponse, BrokerReasonRequest, BrokerStageEvent } from "@/types/broker";

export interface BrokerResult {
  data: BrokerOrchestrationResponse;
  meta: ApiMeta;
}

export interface BrokerStreamHandlers {
  onEvent?: (event: BrokerStageEvent) => void;
  onFinalResponse?: (response: BrokerOrchestrationResponse) => void;
}

function makeRequestId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `valor-broker-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function invalidBrokerResponse(requestId?: string): ValorApiError {
  return new ValorApiError(
    {
      code: "INVALID_API_RESPONSE",
      message: "The ValorAI API returned an unexpected broker response.",
      details: [],
    },
    { requestId },
  );
}

function invalidBrokerRequest(message: string, field?: string): ValorApiError {
  return new ValorApiError({
    code: "INVALID_BROKER_REQUEST",
    message,
    details: field ? [{ code: "INVALID_BROKER_REQUEST", message, field }] : [],
  });
}

function positiveInteger(value: unknown, field: string): number {
  if (typeof value === "number" && Number.isInteger(value) && value > 0) return value;
  throw invalidBrokerRequest(`${field} must be a positive integer.`, field);
}

function brokerRequestPayload(request: BrokerReasonRequest): BrokerReasonRequest {
  const message = request.message.trim();
  if (message.length === 0) {
    throw invalidBrokerRequest("message must not be empty.", "message");
  }
  if (message.length > 4000) {
    throw invalidBrokerRequest("message must be 4000 characters or fewer.", "message");
  }
  if (request.session_id != null && (request.session_id.length < 3 || request.session_id.length > 80)) {
    throw invalidBrokerRequest("session_id must be between 3 and 80 characters.", "session_id");
  }

  const payload: BrokerReasonRequest = {
    workspace_id: positiveInteger(request.workspace_id, "workspace_id"),
    scenario_id: positiveInteger(request.scenario_id, "scenario_id"),
    message,
  };

  if (request.session_id !== undefined) {
    payload.session_id = request.session_id;
  }
  if (request.valuation_request !== undefined) {
    payload.valuation_request = request.valuation_request;
  }
  if (request.investor_preferences !== undefined) {
    payload.investor_preferences = request.investor_preferences;
  }

  return payload;
}

function isBrokerStageEvent(value: unknown): value is BrokerStageEvent {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Partial<BrokerStageEvent>;
  return (
    typeof candidate.event_id === "string" &&
    typeof candidate.stage === "string" &&
    typeof candidate.event_type === "string" &&
    typeof candidate.message === "string"
  );
}

function assertBrokerStageEvent(value: unknown): BrokerStageEvent {
  if (isBrokerStageEvent(value)) return value;
  throw invalidBrokerResponse();
}

function isBrokerOrchestrationResponse(value: unknown): value is BrokerOrchestrationResponse {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Partial<BrokerOrchestrationResponse>;
  return (
    typeof candidate.session_id === "string" &&
    typeof candidate.intent === "string" &&
    typeof candidate.response === "object" &&
    candidate.response !== null &&
    typeof candidate.context === "object" &&
    candidate.context !== null &&
    Array.isArray(candidate.events)
  );
}

function assertBrokerOrchestrationResponse(value: unknown, requestId?: string): BrokerOrchestrationResponse {
  if (isBrokerOrchestrationResponse(value)) return value;
  throw invalidBrokerResponse(requestId);
}

function unwrapBrokerResponse(
  value: ApiSuccessEnvelope<BrokerOrchestrationResponse> | BrokerOrchestrationResponse,
): BrokerResult {
  if (isApiSuccessEnvelope<BrokerOrchestrationResponse>(value)) {
    return {
      data: assertBrokerOrchestrationResponse(value.data, value.meta.request_id),
      meta: value.meta,
    };
  }

  return {
    data: assertBrokerOrchestrationResponse(value),
    meta: {},
  };
}

export async function requestBrokerReason(request: BrokerReasonRequest, signal?: AbortSignal): Promise<BrokerResult> {
  const payload = brokerRequestPayload(request);
  const response = await http.post<ApiSuccessEnvelope<BrokerOrchestrationResponse> | BrokerOrchestrationResponse>(
    "/v1/broker/reason",
    payload,
    { signal },
  );

  return unwrapBrokerResponse(response.data);
}

export async function requestBrokerChat(request: BrokerChatRequest, signal?: AbortSignal): Promise<BrokerResult> {
  const payload = brokerRequestPayload(request);
  const response = await http.post<ApiSuccessEnvelope<BrokerOrchestrationResponse> | BrokerOrchestrationResponse>(
    "/v1/broker/chat",
    payload,
    { signal },
  );

  return unwrapBrokerResponse(response.data);
}

async function throwFetchError(response: Response, requestId: string): Promise<never> {
  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (isApiErrorEnvelope(payload)) {
    throw new ValorApiError(payload.error, {
      requestId: payload.meta.request_id ?? requestId,
      correlationId: typeof payload.meta.correlation_id === "string" ? payload.meta.correlation_id : undefined,
      status: response.status,
    });
  }

  throw new ValorApiError(
    {
      code: "BROKER_STREAM_ERROR",
      message: response.statusText || "Unable to stream broker reasoning events.",
      details: [],
    },
    { requestId, status: response.status },
  );
}

function parseSseBlock(block: string): { eventType: string; data: unknown } | null {
  const lines = block.split(/\r?\n/);
  let eventType = "message";
  const dataLines: string[] = [];

  for (const line of lines) {
    if (line.startsWith(":")) continue;
    if (line.startsWith("event:")) {
      eventType = line.slice("event:".length).trim();
      continue;
    }
    if (line.startsWith("data:")) {
      dataLines.push(line.slice("data:".length).trimStart());
    }
  }

  if (dataLines.length === 0) return null;
  return {
    eventType,
    data: JSON.parse(dataLines.join("\n")),
  };
}

export async function streamBrokerReason(
  request: BrokerReasonRequest,
  handlers: BrokerStreamHandlers = {},
  signal?: AbortSignal,
): Promise<BrokerOrchestrationResponse | null> {
  const requestId = makeRequestId();
  const payload = brokerRequestPayload(request);
  const fetchStream = async (token: string | null) =>
    fetch(`${appConfig.apiBaseUrl}/v1/broker/stream`, {
      method: "POST",
      headers: {
        Accept: "text/event-stream",
        "Content-Type": "application/json",
        "X-Request-ID": requestId,
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(payload),
      signal,
    });

  let response = await fetchStream(await authSessionManager.getValidAccessToken());
  if (response.status === 401) {
    try {
      response = await fetchStream(await authSessionManager.renewSession());
    } catch {
      await authSessionManager.expireSession();
    }
  }

  if (!response.ok) {
    if (response.status === 401) {
      await authSessionManager.expireSession();
    }
    if (response.status === 403) {
      authSessionManager.markAccessDenied();
    }
    return throwFetchError(response, requestId);
  }

  if (!response.body) {
    const payload = await response.json();
    const finalResponse = assertBrokerOrchestrationResponse(payload, requestId);
    handlers.onFinalResponse?.(finalResponse);
    return finalResponse;
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let finalResponse: BrokerOrchestrationResponse | null = null;

  const processBlock = (block: string) => {
    const parsed = parseSseBlock(block);
    if (!parsed) return;

    if (parsed.eventType === "final_response") {
      finalResponse = assertBrokerOrchestrationResponse(parsed.data, requestId);
      handlers.onFinalResponse?.(finalResponse);
      return;
    }

    handlers.onEvent?.(assertBrokerStageEvent(parsed.data));
  };

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const blocks = buffer.split(/\r?\n\r?\n/);
    buffer = blocks.pop() ?? "";
    for (const block of blocks) {
      processBlock(block);
    }
  }

  buffer += decoder.decode();
  if (buffer.trim().length > 0) {
    processBlock(buffer);
  }

  return finalResponse;
}
