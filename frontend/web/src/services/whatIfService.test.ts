import { beforeEach, describe, expect, it, vi } from "vitest";
import { http } from "@/api/http";
import { sampleWhatIfResponse } from "@/test/fixtures";
import { runWhatIfAnalysis } from "./whatIfService";

vi.mock("@/api/http", () => ({
  http: {
    post: vi.fn(),
  },
}));

const postMock = vi.mocked(http.post);

const request = {
  workspace_id: 11,
  property_id: 22,
  scenario_id: null,
  modifications: {
    size_sqm: 180,
    amenities: ["BA", "CP", "SE"],
  },
};

describe("what-if service", () => {
  beforeEach(() => {
    postMock.mockReset();
  });

  it("unwraps typed success envelopes and returns API metadata", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleWhatIfResponse,
        meta: { request_id: "what-if-req-1" },
      },
    });

    const result = await runWhatIfAnalysis(request);

    expect(postMock).toHaveBeenCalledWith("/v1/copilot/tools/what-if", request, { signal: undefined });
    expect(result.data.scenario_valuation).toBe(108000);
    expect(result.meta.request_id).toBe("what-if-req-1");
  });

  it("keeps compatibility with unenveloped what-if payloads", async () => {
    postMock.mockResolvedValueOnce({ data: sampleWhatIfResponse });

    const result = await runWhatIfAnalysis(request);

    expect(result.data.delta_value).toBe(18000);
    expect(result.meta).toEqual({});
  });

  it("passes abort signals through to Axios", async () => {
    const controller = new AbortController();
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleWhatIfResponse,
        meta: {},
      },
    });

    await runWhatIfAnalysis(request, controller.signal);

    expect(postMock).toHaveBeenCalledWith("/v1/copilot/tools/what-if", request, { signal: controller.signal });
  });

  it("accepts sparse but contract-valid nested arrays", async () => {
    const sparseResponse = {
      ...sampleWhatIfResponse,
      assumptions_used: [],
      feature_changes: { added: [], removed: [], modified: [] },
      explainability: {
        ...sampleWhatIfResponse.explainability,
        feature_drivers: [],
        comparable_evidence: [],
      },
      comparables: {
        ...sampleWhatIfResponse.comparables,
        comparable_count: 0,
        comparables: [],
      },
    };
    postMock.mockResolvedValueOnce({ data: sparseResponse });

    const result = await runWhatIfAnalysis(request);

    expect(result.data.assumptions_used).toEqual([]);
    expect(result.data.feature_changes.modified).toEqual([]);
    expect(result.data.comparables.comparables).toEqual([]);
  });

  it("rejects malformed what-if payloads before they reach the UI", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: { tool_name: "what_if", base_valuation: 90000 },
        meta: { request_id: "what-if-bad-shape" },
      },
    });

    await expect(runWhatIfAnalysis(request)).rejects.toMatchObject({
      code: "INVALID_API_RESPONSE",
      requestId: "what-if-bad-shape",
    });
  });

  it("validates empty scenario modifications before making a network call", async () => {
    await expect(
      runWhatIfAnalysis({
        workspace_id: 11,
        property_id: 22,
        modifications: {},
      }),
    ).rejects.toMatchObject({
      code: "INVALID_WHAT_IF_REQUEST",
    });
    expect(postMock).not.toHaveBeenCalled();
  });
});
