import { beforeEach, describe, expect, it, vi } from "vitest";
import { runCopilot } from "@/services/copilotService";
import { useInvestmentStore, initialInvestmentState } from "@/store/investmentStore";
import { useMarketInsightStore, initialMarketInsightState } from "@/store/marketInsightStore";
import { useNegotiationStore, initialNegotiationState } from "@/store/negotiationStore";
import { usePropertyContextStore } from "@/store/propertyContextStore";
import { useScenarioHistoryStore, initialScenarioHistoryState } from "@/store/scenarioHistoryStore";
import { useValuationStore, defaultValuationRequest } from "@/store/valuationStore";
import { useWhatIfStore, initialWhatIfState } from "@/store/whatIfStore";
import {
  sampleCopilotResponse,
  sampleInvestmentResponse,
  sampleMarketInsightResponse,
  sampleNegotiationResponse,
  sampleRequest,
  sampleValuation,
  sampleWhatIfResponse,
} from "@/test/fixtures";
import { initialCopilotState, useCopilotStore } from "./copilotStore";

vi.mock("@/services/copilotService", () => ({
  runCopilot: vi.fn(),
}));

const runMock = vi.mocked(runCopilot);

function resetStores() {
  runMock.mockReset();
  useCopilotStore.setState(initialCopilotState);
  usePropertyContextStore.setState({
    activeWorkspaceId: null,
    activePropertyId: null,
    activeScenarioId: null,
    bridgeStatus: "idle",
    lastBridgeRequestId: undefined,
    lastBridgeError: undefined,
    lastBoundAt: undefined,
  });
  useValuationStore.setState({
    draft: defaultValuationRequest,
    lastResult: null,
    lastRequest: null,
    lastRequestId: undefined,
  });
  useWhatIfStore.setState(initialWhatIfState);
  useNegotiationStore.setState(initialNegotiationState);
  useInvestmentStore.setState(initialInvestmentState);
  useMarketInsightStore.setState(initialMarketInsightState);
  useScenarioHistoryStore.setState(initialScenarioHistoryState);
}

describe("copilot store", () => {
  beforeEach(() => {
    resetStores();
  });

  it("builds property-aware investment tool inputs for buy questions", async () => {
    runMock.mockResolvedValueOnce({ data: sampleCopilotResponse, meta: { request_id: "copilot-1" } });
    usePropertyContextStore.setState({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: null,
      bridgeStatus: "ready",
    });
    useValuationStore.setState({
      draft: sampleRequest,
      lastResult: sampleValuation,
      lastRequest: sampleRequest,
      lastRequestId: "valuation-1",
    });

    const response = await useCopilotStore.getState().sendMessage({ message: "Should I buy this property?" });

    expect(response.intent).toBe("INVESTMENT");
    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        workspace_id: 11,
        scenario_id: null,
        message: "Should I buy this property? Is this a good investment?",
        tool_inputs: expect.objectContaining({
          VALUATION_TOOL: {
            workspace_id: 11,
            property_id: 22,
            scenario_id: null,
          },
          INVESTMENT_TOOL: {
            workspace_id: 11,
            property_id: 22,
            scenario_id: null,
            asking_price_egp: 95000,
            what_if_modifications: null,
          },
          MARKET_INSIGHT_TOOL: expect.objectContaining({
            workspace_id: 11,
            property_type: "Apartment",
          }),
        }),
      }),
      undefined,
    );
    expect(useCopilotStore.getState().conversation).toHaveLength(2);
    expect(useCopilotStore.getState().memoryContext?.activeProperty).toContain("Property 22");
    expect(useCopilotStore.getState().citations?.valuation_ids).toEqual(["val-investment-1"]);
  });

  it("preserves scenario-aware what-if modifications and recent workflow context", async () => {
    runMock.mockResolvedValueOnce({ data: sampleCopilotResponse, meta: {} });
    usePropertyContextStore.setState({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: 33,
      bridgeStatus: "ready",
    });
    useValuationStore.setState({
      draft: sampleRequest,
      lastResult: sampleValuation,
      lastRequest: sampleRequest,
      lastRequestId: "valuation-1",
    });
    useWhatIfStore.setState({
      ...initialWhatIfState,
      lastRequest: {
        workspace_id: 11,
        property_id: 22,
        scenario_id: 33,
        modifications: { size_sqm: 180 },
      },
      lastResponse: sampleWhatIfResponse,
    });
    useNegotiationStore.setState({
      ...initialNegotiationState,
      lastResponse: sampleNegotiationResponse,
      runs: [
        {
          key: "neg",
          target: "active_scenario",
          label: "Scenario A",
          scenarioId: 33,
          request: {
            workspace_id: 11,
            property_id: 22,
            scenario_id: 33,
            asking_price_egp: 95000,
          },
          response: sampleNegotiationResponse,
          createdAt: "2026-06-10T00:00:00Z",
        },
      ],
    });
    useInvestmentStore.setState({
      ...initialInvestmentState,
      lastResponse: sampleInvestmentResponse,
    });
    useMarketInsightStore.setState({
      ...initialMarketInsightState,
      lastResponse: sampleMarketInsightResponse,
    });

    await useCopilotStore.getState().sendMessage({ message: "Which scenario is strongest?" });

    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        scenario_id: 33,
        tool_inputs: expect.objectContaining({
          WHAT_IF_TOOL: {
            workspace_id: 11,
            property_id: 22,
            scenario_id: 33,
            modifications: { size_sqm: 180 },
          },
          NEGOTIATION_TOOL: expect.objectContaining({
            what_if_modifications: { size_sqm: 180 },
          }),
          INVESTMENT_TOOL: expect.objectContaining({
            what_if_modifications: { size_sqm: 180 },
          }),
        }),
      }),
      undefined,
    );
    expect(useCopilotStore.getState().memoryContext?.activeScenario).toContain("Scenario 33");
    expect(useCopilotStore.getState().memoryContext?.latestNegotiation).toContain("Overpriced");
    expect(useCopilotStore.getState().memoryContext?.latestMarketInsight).toContain("6 valuations");
  });

  it("requires an active workspace before sending", async () => {
    await expect(useCopilotStore.getState().sendMessage({ message: "Should I buy this property?" })).rejects.toThrow(
      "Run a valuation first",
    );

    expect(runMock).not.toHaveBeenCalled();
    expect(useCopilotStore.getState().error?.message).toContain("Run a valuation first");
  });
});
