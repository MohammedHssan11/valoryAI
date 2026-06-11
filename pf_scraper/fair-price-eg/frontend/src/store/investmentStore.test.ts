import { beforeEach, describe, expect, it, vi } from "vitest";
import { runInvestmentAnalysis } from "@/services/investmentService";
import { sampleInvestmentResponse } from "@/test/fixtures";
import { initialInvestmentState, useInvestmentStore } from "./investmentStore";

vi.mock("@/services/investmentService", () => ({
  runInvestmentAnalysis: vi.fn(),
}));

const runMock = vi.mocked(runInvestmentAnalysis);

const request = {
  workspace_id: 11,
  property_id: 22,
  scenario_id: null,
  asking_price_egp: 118000,
};

describe("investment store", () => {
  beforeEach(() => {
    runMock.mockReset();
    useInvestmentStore.setState(initialInvestmentState);
  });

  it("runs investment analysis and stores request, response, selected scenario, and comparison run", async () => {
    runMock.mockResolvedValueOnce({ data: sampleInvestmentResponse, meta: { request_id: "investment-req-1" } });

    const result = await useInvestmentStore.getState().runInvestmentAnalysis(request, {
      target: "base",
      label: "Base valuation",
      scenarioId: null,
    });

    expect(runMock).toHaveBeenCalledWith(request, undefined);
    expect(result.investment_position).toBe("High Risk");
    expect(useInvestmentStore.getState().lastRequest).toEqual(request);
    expect(useInvestmentStore.getState().lastResponse).toEqual(sampleInvestmentResponse);
    expect(useInvestmentStore.getState().selectedScenarioId).toBeNull();
    expect(useInvestmentStore.getState().selectedScenarioName).toBe("Base valuation");
    expect(useInvestmentStore.getState().runs).toHaveLength(1);
  });

  it("passes abort signals to the service", async () => {
    const controller = new AbortController();
    runMock.mockResolvedValueOnce({ data: sampleInvestmentResponse, meta: {} });

    await useInvestmentStore.getState().runInvestmentAnalysis(request, undefined, controller.signal);

    expect(runMock).toHaveBeenCalledWith(request, controller.signal);
  });

  it("replaces duplicate run keys and preserves scenario comparison outcomes", async () => {
    const scenarioResponse = {
      ...sampleInvestmentResponse,
      valuation_id: "val-selected-scenario",
      asking_price: 90000,
      fair_price: 108000,
      price_gap: -18000,
      price_gap_percentage: -16.6667,
      investment_position: "Strong Opportunity" as const,
      risks: sampleInvestmentResponse.risks.slice(0, 1),
      strengths: [...sampleInvestmentResponse.strengths, sampleInvestmentResponse.strengths[0]],
    };
    runMock
      .mockResolvedValueOnce({ data: sampleInvestmentResponse, meta: {} })
      .mockResolvedValueOnce({ data: scenarioResponse, meta: {} })
      .mockResolvedValueOnce({ data: sampleInvestmentResponse, meta: {} });

    await useInvestmentStore.getState().runInvestmentAnalysis(request, {
      target: "base",
      label: "Base valuation",
      scenarioId: null,
    });
    await useInvestmentStore.getState().runInvestmentAnalysis(
      { ...request, scenario_id: 7 },
      {
        target: "selected_scenario",
        label: "Scenario A",
        scenarioId: 7,
      },
    );
    await useInvestmentStore.getState().runInvestmentAnalysis(request, {
      target: "base",
      label: "Base valuation",
      scenarioId: null,
    });

    expect(useInvestmentStore.getState().runs).toHaveLength(2);
    expect(useInvestmentStore.getState().runs.map((run) => run.label)).toEqual(["Scenario A", "Base valuation"]);
  });

  it("captures errors without dropping the last attempted request", async () => {
    runMock.mockRejectedValueOnce(new Error("Investment failed"));

    await expect(useInvestmentStore.getState().runInvestmentAnalysis(request)).rejects.toThrow("Investment failed");

    expect(useInvestmentStore.getState().lastRequest).toEqual(request);
    expect(useInvestmentStore.getState().lastResponse).toBeNull();
    expect(useInvestmentStore.getState().isLoading).toBe(false);
    expect(useInvestmentStore.getState().error?.message).toBe("Investment failed");
  });

  it("selects, clears, and resets investment state", () => {
    useInvestmentStore.getState().selectScenario(7, "Scenario A");
    expect(useInvestmentStore.getState().selectedScenarioId).toBe(7);
    expect(useInvestmentStore.getState().selectedScenarioName).toBe("Scenario A");

    useInvestmentStore.setState({
      lastRequest: request,
      lastResponse: sampleInvestmentResponse,
      runs: [
        {
          key: "base",
          target: "base",
          label: "Base valuation",
          scenarioId: null,
          request,
          response: sampleInvestmentResponse,
          createdAt: "2026-06-09T00:00:00Z",
        },
      ],
      isLoading: false,
      error: new Error("old"),
    });

    useInvestmentStore.getState().clearInvestment();
    expect(useInvestmentStore.getState().lastRequest).toBeNull();
    expect(useInvestmentStore.getState().lastResponse).toBeNull();
    expect(useInvestmentStore.getState().runs).toEqual([]);
    expect(useInvestmentStore.getState().error).toBeNull();
    expect(useInvestmentStore.getState().selectedScenarioId).toBe(7);

    useInvestmentStore.getState().resetInvestment();
    expect(useInvestmentStore.getState()).toMatchObject(initialInvestmentState);
  });
});
