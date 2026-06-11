import { beforeEach, describe, expect, it, vi } from "vitest";
import { http } from "@/api/http";
import { sampleNegotiationResponse } from "@/test/fixtures";
import { runNegotiationAnalysis } from "./negotiationService";

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

describe("negotiation service", () => {
  beforeEach(() => {
    postMock.mockReset();
  });

  it("unwraps success envelopes and mirrors the negotiation contract endpoint", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleNegotiationResponse,
        meta: { request_id: "negotiation-req-1" },
      },
    });

    const result = await runNegotiationAnalysis(request);

    expect(postMock).toHaveBeenCalledWith("/v1/copilot/tools/negotiation", request, { signal: undefined });
    expect(result.data.negotiation_position).toBe("Overpriced");
    expect(result.data.recommended_offer_band.low).toBe(88000);
    expect(result.meta.request_id).toBe("negotiation-req-1");
  });

  it("keeps compatibility with unenveloped negotiation payloads", async () => {
    postMock.mockResolvedValueOnce({ data: sampleNegotiationResponse });

    const result = await runNegotiationAnalysis({ ...request, what_if_modifications: undefined });

    expect(result.data.fair_price).toBe(90000);
    expect(result.meta).toEqual({});
  });

  it("passes abort signals through to Axios", async () => {
    const controller = new AbortController();
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleNegotiationResponse,
        meta: {},
      },
    });

    await runNegotiationAnalysis(request, controller.signal);

    expect(postMock).toHaveBeenCalledWith("/v1/copilot/tools/negotiation", request, {
      signal: controller.signal,
    });
  });

  it("validates empty what-if modifications before making a network call", async () => {
    await expect(
      runNegotiationAnalysis({
        workspace_id: 11,
        property_id: 22,
        asking_price_egp: 118000,
        what_if_modifications: {},
      }),
    ).rejects.toMatchObject({
      code: "INVALID_NEGOTIATION_REQUEST",
    });
    expect(postMock).not.toHaveBeenCalled();
  });

  it("rejects malformed negotiation payloads before they reach the UI", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: { tool_name: "negotiation", valuation_id: "missing-fields" },
        meta: { request_id: "negotiation-bad-shape" },
      },
    });

    await expect(runNegotiationAnalysis(request)).rejects.toMatchObject({
      code: "INVALID_API_RESPONSE",
      requestId: "negotiation-bad-shape",
    });
  });
});
