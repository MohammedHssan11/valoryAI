import { beforeEach, describe, expect, it, vi } from "vitest";
import { runNegotiationAnalysis } from "@/services/negotiationService";
import { sampleNegotiationResponse } from "@/test/fixtures";
import { initialNegotiationState, useNegotiationStore } from "./negotiationStore";

vi.mock("@/services/negotiationService", () => ({
  runNegotiationAnalysis: vi.fn(),
}));

const runMock = vi.mocked(runNegotiationAnalysis);

const request = {
  workspace_id: 11,
  property_id: 22,
  scenario_id: null,
  asking_price_egp: 118000,
};

describe("negotiation store", () => {
  beforeEach(() => {
    runMock.mockReset();
    useNegotiationStore.setState(initialNegotiationState);
  });

  it("runs negotiation and stores request, response, and comparison run", async () => {
    runMock.mockResolvedValueOnce({ data: sampleNegotiationResponse, meta: { request_id: "negotiation-req-1" } });

    const result = await useNegotiationStore.getState().runNegotiation(request, {
      target: "base",
      label: "Base valuation",
      scenarioId: null,
    });

    expect(runMock).toHaveBeenCalledWith(request, undefined);
    expect(result.negotiation_position).toBe("Overpriced");
    expect(useNegotiationStore.getState().lastRequest).toEqual(request);
    expect(useNegotiationStore.getState().lastResponse).toEqual(sampleNegotiationResponse);
    expect(useNegotiationStore.getState().runs).toHaveLength(1);
    expect(useNegotiationStore.getState().runs[0]).toMatchObject({
      target: "base",
      label: "Base valuation",
      scenarioId: null,
    });
  });

  it("passes abort signals to the service", async () => {
    const controller = new AbortController();
    runMock.mockResolvedValueOnce({ data: sampleNegotiationResponse, meta: {} });

    await useNegotiationStore.getState().runNegotiation(request, undefined, controller.signal);

    expect(runMock).toHaveBeenCalledWith(request, controller.signal);
  });

  it("replaces duplicate run keys and preserves scenario comparison outcomes", async () => {
    const scenarioResponse = {
      ...sampleNegotiationResponse,
      valuation_id: "val-selected-scenario",
      asking_price: 110000,
      fair_price: 108000,
      price_gap: 2000,
      price_gap_percentage: 1.8519,
      negotiation_position: "Negotiation Recommended" as const,
    };
    runMock
      .mockResolvedValueOnce({ data: sampleNegotiationResponse, meta: {} })
      .mockResolvedValueOnce({ data: scenarioResponse, meta: {} })
      .mockResolvedValueOnce({ data: sampleNegotiationResponse, meta: {} });

    await useNegotiationStore.getState().runNegotiation(request, {
      target: "base",
      label: "Base valuation",
      scenarioId: null,
    });
    await useNegotiationStore.getState().runNegotiation(
      { ...request, scenario_id: 7 },
      {
        target: "selected_scenario",
        label: "Scenario A",
        scenarioId: 7,
      },
    );
    await useNegotiationStore.getState().runNegotiation(request, {
      target: "base",
      label: "Base valuation",
      scenarioId: null,
    });

    expect(useNegotiationStore.getState().runs).toHaveLength(2);
    expect(useNegotiationStore.getState().runs.map((run) => run.label)).toEqual(["Scenario A", "Base valuation"]);
  });

  it("captures errors without dropping the last attempted request", async () => {
    runMock.mockRejectedValueOnce(new Error("Negotiation failed"));

    await expect(useNegotiationStore.getState().runNegotiation(request)).rejects.toThrow("Negotiation failed");

    expect(useNegotiationStore.getState().lastRequest).toEqual(request);
    expect(useNegotiationStore.getState().lastResponse).toBeNull();
    expect(useNegotiationStore.getState().isLoading).toBe(false);
    expect(useNegotiationStore.getState().error?.message).toBe("Negotiation failed");
  });

  it("clears and resets negotiation state", () => {
    useNegotiationStore.setState({
      lastRequest: request,
      lastResponse: sampleNegotiationResponse,
      runs: [
        {
          key: "base",
          target: "base",
          label: "Base valuation",
          scenarioId: null,
          request,
          response: sampleNegotiationResponse,
          createdAt: "2026-06-09T00:00:00Z",
        },
      ],
      isLoading: false,
      error: new Error("old"),
    });

    useNegotiationStore.getState().clearResults();
    expect(useNegotiationStore.getState().lastRequest).toBeNull();
    expect(useNegotiationStore.getState().lastResponse).toBeNull();
    expect(useNegotiationStore.getState().runs).toEqual([]);
    expect(useNegotiationStore.getState().error).toBeNull();

    useNegotiationStore.setState({ lastRequest: request, lastResponse: sampleNegotiationResponse, runs: [], isLoading: true, error: null });
    useNegotiationStore.getState().reset();
    expect(useNegotiationStore.getState()).toMatchObject(initialNegotiationState);
  });
});
