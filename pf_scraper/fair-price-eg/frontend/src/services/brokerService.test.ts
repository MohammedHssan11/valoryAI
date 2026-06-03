import { beforeEach, describe, expect, it, vi } from "vitest";
import { http } from "@/api/http";
import { sampleBrokerResponse, sampleRequest } from "@/test/fixtures";
import { requestBrokerReason, streamBrokerReason } from "./brokerService";

vi.mock("@/api/http", () => ({
  http: {
    post: vi.fn(),
  },
}));

const postMock = vi.mocked(http.post);

describe("broker service", () => {
  beforeEach(() => {
    postMock.mockReset();
    vi.unstubAllGlobals();
  });

  it("unwraps broker reason success envelopes", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleBrokerResponse,
        meta: { request_id: "broker-req-1" },
      },
    });

    const result = await requestBrokerReason({ message: "Explain the valuation", valuation_request: sampleRequest });

    expect(postMock).toHaveBeenCalledWith(
      "/v1/broker/reason",
      { message: "Explain the valuation", valuation_request: sampleRequest },
      { signal: undefined },
    );
    expect(result.data.session_id).toBe("broker-session-1");
    expect(result.meta.request_id).toBe("broker-req-1");
  });

  it("rejects malformed broker payloads", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: { response: {} },
        meta: { request_id: "broker-bad-shape" },
      },
    });

    await expect(requestBrokerReason({ message: "Explain the valuation" })).rejects.toMatchObject({
      code: "INVALID_API_RESPONSE",
      requestId: "broker-bad-shape",
    });
  });

  it("parses POST SSE stage events and final broker response", async () => {
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
      { session_id: "broker-session-1", message: "Explain the valuation", valuation_request: sampleRequest },
      { onEvent, onFinalResponse },
    );

    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/v1/broker/stream",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          session_id: "broker-session-1",
          message: "Explain the valuation",
          valuation_request: sampleRequest,
        }),
      }),
    );
    expect(onEvent).toHaveBeenCalledWith(stageEvent);
    expect(onFinalResponse).toHaveBeenCalledWith(sampleBrokerResponse);
    expect(result).toEqual(sampleBrokerResponse);
  });
});
