import { beforeEach, describe, expect, it, vi } from "vitest";
import { authSessionManager } from "@/auth/authSessionManager";
import { http } from "@/api/http";
import { sampleBrokerResponse, sampleRequest } from "@/test/fixtures";
import { requestBrokerChat, requestBrokerReason, streamBrokerReason } from "./brokerService";
import type { BrokerReasonRequest } from "@/types/broker";

vi.mock("@/api/http", () => ({
  http: {
    post: vi.fn(),
  },
}));

const postMock = vi.mocked(http.post);

const sampleBrokerRequest: BrokerReasonRequest = {
  workspace_id: 11,
  scenario_id: 33,
  message: "Explain the valuation",
  valuation_request: sampleRequest,
};

describe("broker service", () => {
  beforeEach(async () => {
    postMock.mockReset();
    vi.unstubAllGlobals();
    sessionStorage.clear();
    await authSessionManager.logout();
  });

  it("unwraps broker reason success envelopes", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleBrokerResponse,
        meta: { request_id: "broker-req-1" },
      },
    });

    const result = await requestBrokerReason(sampleBrokerRequest);

    expect(postMock).toHaveBeenCalledWith(
      "/v1/broker/reason",
      sampleBrokerRequest,
      { signal: undefined },
    );
    expect(result.data.session_id).toBe("broker-session-1");
    expect(result.meta.request_id).toBe("broker-req-1");
  });

  it("rejects broker requests without backend-required context", async () => {
    await expect(requestBrokerReason({ message: "Explain the valuation" } as BrokerReasonRequest)).rejects.toMatchObject({
      code: "INVALID_BROKER_REQUEST",
      details: [expect.objectContaining({ field: "workspace_id" })],
    });
    expect(postMock).not.toHaveBeenCalled();
  });

  it("sends only backend contract fields for broker reason requests", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleBrokerResponse,
        meta: { request_id: "broker-req-2" },
      },
    });

    await requestBrokerReason({
      ...sampleBrokerRequest,
      session_id: "broker-session-1",
      extra_client_state: "must-not-leak",
    } as BrokerReasonRequest & { extra_client_state: string });

    expect(postMock).toHaveBeenCalledWith(
      "/v1/broker/reason",
      {
        session_id: "broker-session-1",
        workspace_id: 11,
        scenario_id: 33,
        message: "Explain the valuation",
        valuation_request: sampleRequest,
      },
      { signal: undefined },
    );
  });

  it("uses the same aligned contract for broker chat requests", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleBrokerResponse,
        meta: { request_id: "broker-chat-1" },
      },
    });

    const result = await requestBrokerChat(sampleBrokerRequest);

    expect(postMock).toHaveBeenCalledWith("/v1/broker/chat", sampleBrokerRequest, { signal: undefined });
    expect(result.meta.request_id).toBe("broker-chat-1");
  });

  it("rejects malformed broker payloads", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: { response: {} },
        meta: { request_id: "broker-bad-shape" },
      },
    });

    await expect(requestBrokerReason(sampleBrokerRequest)).rejects.toMatchObject({
      code: "INVALID_API_RESPONSE",
      requestId: "broker-bad-shape",
    });
  });

  it("parses POST SSE stage events and final broker response", async () => {
    sessionStorage.setItem("valorai_access_token", "stream-jwt");
    sessionStorage.setItem("valorai_access_token_expires_at", new Date(Date.now() + 3_600_000).toISOString());
    sessionStorage.setItem(
      "valorai_user_metadata",
      JSON.stringify({ id: 1, external_subject: "firebase-user", display_name: "Firebase User" }),
    );
    await authSessionManager.restoreSession();
    const encoder = new TextEncoder();
    const stageEvent = sampleBrokerResponse.events[0];
    const body = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(
          encoder.encode(`event: ${stageEvent.event_type}\ndata: ${JSON.stringify(stageEvent)}\n\n`),
        );
        controller.enqueue(
          encoder.encode(`event: final_response\ndata: ${JSON.stringify(sampleBrokerResponse)}\n\n`),
        );
        controller.close();
      },
    });

    const fetchMock = vi.fn().mockResolvedValueOnce(
      new Response(body, {
        status: 200,
        headers: { "Content-Type": "text/event-stream" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const onEvent = vi.fn();
    const onFinalResponse = vi.fn();
    const result = await streamBrokerReason(
      { ...sampleBrokerRequest, session_id: "broker-session-1" },
      { onEvent, onFinalResponse },
    );

    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/v1/broker/stream",
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({
          Authorization: "Bearer stream-jwt",
        }),
      }),
    );
    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(JSON.parse(String(init.body))).toEqual({
      session_id: "broker-session-1",
      workspace_id: 11,
      scenario_id: 33,
      message: "Explain the valuation",
      valuation_request: sampleRequest,
    });
    expect(onEvent).toHaveBeenCalledWith(stageEvent);
    expect(onFinalResponse).toHaveBeenCalledWith(sampleBrokerResponse);
    expect(result).toEqual(sampleBrokerResponse);
  });
});
