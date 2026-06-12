import { beforeEach, describe, expect, it, vi } from "vitest";
import { http } from "@/api/http";
import {
  sampleEmptyMarketInsightResponse,
  sampleMarketInsightResponse,
} from "@/test/fixtures";
import { runMarketInsight } from "./marketInsightService";

vi.mock("@/api/http", () => ({
  http: {
    post: vi.fn(),
  },
}));

const postMock = vi.mocked(http.post);

describe("market insight service", () => {
  beforeEach(() => {
    postMock.mockReset();
  });

  it("posts sanitized filters to the Market Insight Tool 8 endpoint", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleMarketInsightResponse,
        meta: { request_id: "market-req-1" },
      },
    });

    const result = await runMarketInsight({
      workspace_id: 11,
      compound_name: "  Nile Quarter  ",
      property_type: " Apartment ",
      h3_res9: "89754e64993ffff",
      time_window: "90d",
    });

    expect(postMock).toHaveBeenCalledWith(
      "/v1/copilot/tools/market-insight",
      {
        workspace_id: 11,
        compound_name: "Nile Quarter",
        property_type: "Apartment",
        h3_res9: "89754e64993ffff",
        time_window: "90d",
      },
      { signal: undefined },
    );
    expect(result.data.tool_name).toBe("market_insight");
    expect(result.data.source).toBe("TruthLayer");
    expect(result.meta.request_id).toBe("market-req-1");
  });

  it("defaults time_window to all and strips empty optional filters", async () => {
    postMock.mockResolvedValueOnce({ data: sampleMarketInsightResponse });

    await runMarketInsight({
      workspace_id: 11,
      compound_name: "",
      property_type: "   ",
      h3_res9: undefined,
      time_window: undefined,
    });

    expect(postMock).toHaveBeenCalledWith(
      "/v1/copilot/tools/market-insight",
      {
        workspace_id: 11,
        time_window: "all",
      },
      { signal: undefined },
    );
  });

  it("keeps compatibility with unenveloped market insight payloads", async () => {
    postMock.mockResolvedValueOnce({ data: sampleMarketInsightResponse });

    const result = await runMarketInsight({ workspace_id: 11, time_window: "all" });

    expect(result.data.valuation_volume).toBe(6);
    expect(result.meta).toEqual({});
  });

  it("preserves null fair-value and comparable fields for empty evidence", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: sampleEmptyMarketInsightResponse,
        meta: {},
      },
    });

    const result = await runMarketInsight({ workspace_id: 11, time_window: "30d" });

    expect(result.data.valuation_volume).toBe(0);
    expect(result.data.fair_value_distribution.median_fair_value).toBeNull();
    expect(result.data.comparable_density.median_comparable_count).toBeNull();
    expect(result.data.active_compounds).toEqual([]);
  });

  it("passes abort signals through to Axios", async () => {
    const controller = new AbortController();
    postMock.mockResolvedValueOnce({ data: sampleMarketInsightResponse });

    await runMarketInsight({ workspace_id: 11, time_window: "all" }, controller.signal);

    expect(postMock).toHaveBeenCalledWith(
      "/v1/copilot/tools/market-insight",
      { workspace_id: 11, time_window: "all" },
      { signal: controller.signal },
    );
  });

  it("rejects invalid workspace and time-window values before making a network call", async () => {
    await expect(runMarketInsight({ workspace_id: 0, time_window: "all" })).rejects.toMatchObject({
      code: "INVALID_MARKET_INSIGHT_REQUEST",
    });
    await expect(runMarketInsight({ workspace_id: 11, time_window: "0d" })).rejects.toMatchObject({
      code: "INVALID_MARKET_INSIGHT_REQUEST",
    });
    await expect(runMarketInsight({ workspace_id: 11, time_window: "recent" })).rejects.toMatchObject({
      code: "INVALID_MARKET_INSIGHT_REQUEST",
    });

    expect(postMock).not.toHaveBeenCalled();
  });

  it("rejects malformed market insight payloads before they reach the UI", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: {
          ...sampleMarketInsightResponse,
          comparable_density: {
            ...sampleMarketInsightResponse.comparable_density,
            density_level: "Unsupported",
          },
        },
        meta: { request_id: "market-bad-shape" },
      },
    });

    await expect(runMarketInsight({ workspace_id: 11 })).rejects.toMatchObject({
      code: "INVALID_API_RESPONSE",
      requestId: "market-bad-shape",
    });
  });
});
