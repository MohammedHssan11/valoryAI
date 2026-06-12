import { beforeEach, describe, expect, it, vi } from "vitest";
import { http } from "@/api/http";
import { sampleCopilotResponse } from "@/test/fixtures";
import { runCopilot } from "./copilotService";

vi.mock("@/api/http", () => ({
  http: {
    post: vi.fn(),
  },
}));

const postMock = vi.mocked(http.post);

describe("copilot service", () => {
  beforeEach(() => {
    postMock.mockReset();
  });

  it("posts typed orchestrator requests to the respond endpoint", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleCopilotResponse,
        meta: { request_id: "copilot-req-1" },
      },
    });

    const result = await runCopilot({
      workspace_id: 11,
      scenario_id: null,
      broker_session_id: null,
      message: "Should I buy this property?",
      tool_inputs: {
        INVESTMENT_TOOL: {
          workspace_id: 11,
          property_id: 22,
          scenario_id: null,
          asking_price_egp: 118000,
        },
      },
    });

    expect(postMock).toHaveBeenCalledWith(
      "/v1/copilot/orchestrator/respond",
      {
        workspace_id: 11,
        scenario_id: null,
        broker_session_id: null,
        message: "Should I buy this property?",
        tool_inputs: {
          INVESTMENT_TOOL: {
            workspace_id: 11,
            property_id: 22,
            scenario_id: null,
            asking_price_egp: 118000,
          },
        },
      },
      { signal: undefined },
    );
    expect(result.data.runtime_id).toBe("COPILOT_ORCHESTRATOR_LLM_V1");
    expect(result.data.audit.memory_id).toBe("memory_fixture");
    expect(result.data.citation_package?.valuation_ids).toEqual(["val-investment-1"]);
    expect(result.meta.request_id).toBe("copilot-req-1");
  });

  it("passes abort signals through to Axios", async () => {
    const controller = new AbortController();
    postMock.mockResolvedValueOnce({ data: sampleCopilotResponse });

    await runCopilot(
      {
        workspace_id: 11,
        message: "Market insight",
        tool_inputs: {
          MARKET_INSIGHT_TOOL: {
            workspace_id: 11,
            time_window: "all",
          },
        },
      },
      controller.signal,
    );

    expect(postMock).toHaveBeenCalledWith(
      "/v1/copilot/orchestrator/respond",
      {
        workspace_id: 11,
        scenario_id: null,
        broker_session_id: null,
        message: "Market insight",
        tool_inputs: {
          MARKET_INSIGHT_TOOL: {
            workspace_id: 11,
            time_window: "all",
          },
        },
      },
      { signal: controller.signal },
    );
  });

  it("rejects invalid requests before making a network call", async () => {
    await expect(
      runCopilot({
        workspace_id: 0,
        message: "Should I buy this property?",
        tool_inputs: {},
      }),
    ).rejects.toMatchObject({ code: "INVALID_COPILOT_REQUEST" });

    await expect(
      runCopilot({
        workspace_id: 11,
        message: "",
        tool_inputs: {},
      }),
    ).rejects.toMatchObject({ code: "INVALID_COPILOT_REQUEST" });

    expect(postMock).not.toHaveBeenCalled();
  });

  it("rejects malformed orchestrator response payloads", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: {
          ...sampleCopilotResponse,
          response: {
            ...(sampleCopilotResponse.response as unknown as Record<string, unknown>),
            citations: {
              valuation_ids: [123],
              tool_event_ids: [],
              comparable_ids: [],
              unavailable_optional_citation_types: [],
            },
          },
        },
        meta: { request_id: "bad-copilot" },
      },
    });

    await expect(
      runCopilot({
        workspace_id: 11,
        message: "Should I buy this property?",
        tool_inputs: {},
      }),
    ).rejects.toMatchObject({
      code: "INVALID_API_RESPONSE",
      requestId: "bad-copilot",
    });
  });
});
