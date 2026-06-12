import { beforeEach, describe, expect, it, vi } from "vitest";
import { http } from "@/api/http";
import { sampleRequest, sampleValuation } from "@/test/fixtures";
import { requestFairRentPrice } from "./valuationService";

vi.mock("@/api/http", () => ({
  http: {
    post: vi.fn(),
  },
}));

const postMock = vi.mocked(http.post);

describe("valuation service", () => {
  beforeEach(() => {
    postMock.mockReset();
  });

  it("unwraps typed success envelopes and returns API metadata", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleValuation,
        meta: { request_id: "api-req-1" },
      },
    });

    const result = await requestFairRentPrice(sampleRequest);

    expect(postMock).toHaveBeenCalledWith("/v1/valuation/fair-price", sampleRequest, { signal: undefined });
    expect(result.data.fair_price_egp).toBe(90000);
    expect(result.meta.request_id).toBe("api-req-1");
  });

  it("keeps backward compatibility with unenveloped valuation payloads", async () => {
    postMock.mockResolvedValueOnce({ data: sampleValuation });

    const result = await requestFairRentPrice(sampleRequest);

    expect(result.data).toEqual(sampleValuation);
    expect(result.meta).toEqual({});
  });

  it("passes abort signals through to Axios for cancellation", async () => {
    const controller = new AbortController();
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleValuation,
        meta: {},
      },
    });

    await requestFairRentPrice(sampleRequest, controller.signal);

    expect(postMock).toHaveBeenCalledWith("/v1/valuation/fair-price", sampleRequest, { signal: controller.signal });
  });

  it("rejects malformed valuation payloads before they reach the UI", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: { fair_price_egp: 90000 },
        meta: { request_id: "api-bad-shape" },
      },
    });

    await expect(requestFairRentPrice(sampleRequest)).rejects.toMatchObject({
      code: "INVALID_API_RESPONSE",
      requestId: "api-bad-shape",
    });
  });
});
