import { beforeEach, describe, expect, it, vi } from "vitest";
import { http } from "@/api/http";
import { sampleInvestmentResponse } from "@/test/fixtures";
import { runInvestmentAnalysis } from "./investmentService";

vi.mock("@/api/http", () => ({
  http: {
    post: vi.fn(),
  },
}));

const postMock = vi.mocked(http.post);

const request = {
  workspace_id: 11,
  property_id: 22,
  scenario_id: 7,
  asking_price_egp: 118000,
  what_if_modifications: {
    size_sqm: 180,
  },
};

describe("investment service", () => {
  beforeEach(() => {
    postMock.mockReset();
  });

  it("unwraps success envelopes and mirrors the investment contract endpoint", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleInvestmentResponse,
        meta: { request_id: "investment-req-1" },
      },
    });

    const result = await runInvestmentAnalysis(request);

    expect(postMock).toHaveBeenCalledWith("/v1/copilot/tools/investment", request, { signal: undefined });
    expect(result.data.investment_position).toBe("High Risk");
    expect(result.data.negotiation_summary.negotiation_position).toBe("Overpriced");
    expect(result.meta.request_id).toBe("investment-req-1");
  });

  it("keeps compatibility with unenveloped investment payloads", async () => {
    postMock.mockResolvedValueOnce({ data: sampleInvestmentResponse });

    const result = await runInvestmentAnalysis({ ...request, what_if_modifications: undefined });

    expect(result.data.fair_price).toBe(90000);
    expect(result.meta).toEqual({});
  });

  it("passes abort signals through to Axios", async () => {
    const controller = new AbortController();
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleInvestmentResponse,
        meta: {},
      },
    });

    await runInvestmentAnalysis(request, controller.signal);

    expect(postMock).toHaveBeenCalledWith("/v1/copilot/tools/investment", request, {
      signal: controller.signal,
    });
  });

  it("validates empty what-if modifications before making a network call", async () => {
    await expect(
      runInvestmentAnalysis({
        workspace_id: 11,
        property_id: 22,
        asking_price_egp: 118000,
        what_if_modifications: {},
      }),
    ).rejects.toMatchObject({
      code: "INVALID_INVESTMENT_REQUEST",
    });
    expect(postMock).not.toHaveBeenCalled();
  });

  it("rejects malformed investment payloads before they reach the UI", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: { tool_name: "investment", valuation_id: "missing-fields" },
        meta: { request_id: "investment-bad-shape" },
      },
    });

    await expect(runInvestmentAnalysis(request)).rejects.toMatchObject({
      code: "INVALID_API_RESPONSE",
      requestId: "investment-bad-shape",
    });
  });

  it("accepts sparse contract-safe nullable response fields", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: {
          ...sampleInvestmentResponse,
          strengths: [],
          comparable_summary: {
            ...sampleInvestmentResponse.comparable_summary,
            comparable_count: 0,
            comparable_ids: [],
            observed_prices: [],
            lowest_observed_price: null,
            highest_observed_price: null,
          },
          what_if_summary: {
            status: "Insufficient Evidence",
            reason: "No optional What-if Tool sensitivity request was supplied.",
            analysis: null,
            source: "Insufficient Evidence",
          },
        },
        meta: {},
      },
    });

    const result = await runInvestmentAnalysis({ workspace_id: 11, property_id: 22, asking_price_egp: 118000 });

    expect(result.data.strengths).toEqual([]);
    expect(result.data.comparable_summary.lowest_observed_price).toBeNull();
    expect(result.data.what_if_summary.analysis).toBeNull();
  });
});
