import { beforeEach, describe, expect, it, vi } from "vitest";
import { runMarketInsight } from "@/services/marketInsightService";
import {
  sampleMarketInsightResponse,
  sampleSparseMarketInsightResponse,
} from "@/test/fixtures";
import {
  defaultMarketInsightFilters,
  initialMarketInsightState,
  useMarketInsightStore,
} from "./marketInsightStore";

vi.mock("@/services/marketInsightService", () => ({
  runMarketInsight: vi.fn(),
}));

const runMock = vi.mocked(runMarketInsight);

const request = {
  workspace_id: 11,
  compound_name: "Nile Quarter",
  property_type: "Apartment",
  h3_res9: "89754e64993ffff",
  time_window: "90d",
};

describe("market insight store", () => {
  beforeEach(() => {
    runMock.mockReset();
    useMarketInsightStore.setState(initialMarketInsightState);
  });

  it("runs market insight and stores request, response, and run history", async () => {
    runMock.mockResolvedValueOnce({ data: sampleMarketInsightResponse, meta: { request_id: "market-req-1" } });

    const result = await useMarketInsightStore.getState().runMarketInsight(request);

    expect(runMock).toHaveBeenCalledWith(request, undefined);
    expect(result.market_summary).toContain("Observed 6");
    expect(useMarketInsightStore.getState().lastRequest).toEqual(request);
    expect(useMarketInsightStore.getState().lastResponse).toEqual(sampleMarketInsightResponse);
    expect(useMarketInsightStore.getState().isLoading).toBe(false);
    expect(useMarketInsightStore.getState().error).toBeNull();
    expect(useMarketInsightStore.getState().runs).toHaveLength(1);
  });

  it("passes abort signals to the service", async () => {
    const controller = new AbortController();
    runMock.mockResolvedValueOnce({ data: sampleMarketInsightResponse, meta: {} });

    await useMarketInsightStore.getState().runMarketInsight({ workspace_id: 11, time_window: "all" }, controller.signal);

    expect(runMock).toHaveBeenCalledWith({ workspace_id: 11, time_window: "all" }, controller.signal);
  });

  it("updates and resets filters without touching the latest response", () => {
    useMarketInsightStore.setState({ lastResponse: sampleMarketInsightResponse });

    useMarketInsightStore.getState().setFilters({
      compound_name: "Nile Quarter",
      property_type: "Apartment",
      time_window: "30d",
    });

    expect(useMarketInsightStore.getState().filters).toMatchObject({
      compound_name: "Nile Quarter",
      property_type: "Apartment",
      time_window: "30d",
    });
    expect(useMarketInsightStore.getState().lastResponse).toEqual(sampleMarketInsightResponse);

    useMarketInsightStore.getState().resetFilters();
    expect(useMarketInsightStore.getState().filters).toEqual(defaultMarketInsightFilters);
    expect(useMarketInsightStore.getState().lastResponse).toEqual(sampleMarketInsightResponse);
  });

  it("replaces duplicate run keys and keeps filtered outcomes", async () => {
    runMock
      .mockResolvedValueOnce({ data: sampleMarketInsightResponse, meta: {} })
      .mockResolvedValueOnce({ data: sampleSparseMarketInsightResponse, meta: {} })
      .mockResolvedValueOnce({ data: sampleMarketInsightResponse, meta: {} });

    await useMarketInsightStore.getState().runMarketInsight({ workspace_id: 11, time_window: "all" });
    await useMarketInsightStore.getState().runMarketInsight({ workspace_id: 11, compound_name: "Nile Quarter", time_window: "30d" });
    await useMarketInsightStore.getState().runMarketInsight({ workspace_id: 11, time_window: "all" });

    expect(useMarketInsightStore.getState().runs).toHaveLength(2);
    expect(useMarketInsightStore.getState().runs[0].request).toMatchObject({
      compound_name: "Nile Quarter",
      time_window: "30d",
    });
    expect(useMarketInsightStore.getState().runs[1].request).toMatchObject({
      time_window: "all",
    });
  });

  it("clears stale errors when a new run starts and maps thrown values to Error", async () => {
    runMock.mockRejectedValueOnce("service unavailable");

    await expect(useMarketInsightStore.getState().runMarketInsight(request)).rejects.toThrow(
      "Unable to run market intelligence.",
    );
    expect(useMarketInsightStore.getState().lastRequest).toEqual(request);
    expect(useMarketInsightStore.getState().lastResponse).toBeNull();
    expect(useMarketInsightStore.getState().error?.message).toBe("Unable to run market intelligence.");

    runMock.mockResolvedValueOnce({ data: sampleMarketInsightResponse, meta: {} });
    const promise = useMarketInsightStore.getState().runMarketInsight({ workspace_id: 11, time_window: "all" });
    expect(useMarketInsightStore.getState().error).toBeNull();
    await promise;
  });

  it("clears and resets market insight state", () => {
    useMarketInsightStore.setState({
      lastRequest: request,
      lastResponse: sampleMarketInsightResponse,
      filters: {
        ...defaultMarketInsightFilters,
        compound_name: "Nile Quarter",
      },
      runs: [
        {
          key: "market",
          request,
          response: sampleMarketInsightResponse,
          createdAt: "2026-06-10T00:00:00Z",
        },
      ],
      isLoading: false,
      error: new Error("old"),
    });

    useMarketInsightStore.getState().clearMarketInsight();
    expect(useMarketInsightStore.getState().lastRequest).toBeNull();
    expect(useMarketInsightStore.getState().lastResponse).toBeNull();
    expect(useMarketInsightStore.getState().runs).toEqual([]);
    expect(useMarketInsightStore.getState().filters.compound_name).toBe("Nile Quarter");

    useMarketInsightStore.getState().resetMarketInsight();
    expect(useMarketInsightStore.getState()).toMatchObject(initialMarketInsightState);
  });
});
