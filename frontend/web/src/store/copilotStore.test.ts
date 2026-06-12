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

  function activatePreparedProperty() {
    usePropertyContextStore.setState({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: null,
      bridgeStatus: "ready",
      lastBridgeRequestId: undefined,
    });
    useValuationStore.setState({
      draft: sampleRequest,
      lastResult: null,
      lastRequest: null,
      lastRequestId: undefined,
    });
  }

  it("builds valuation, comparable, and market inputs for a property evaluation before valuation is run", async () => {
    runMock.mockResolvedValueOnce({ data: { ...sampleCopilotResponse, intent: "PROPERTY_EVALUATION" }, meta: {} });
    activatePreparedProperty();

    await useCopilotStore.getState().sendMessage({ message: "Evaluate this property" });

    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        workspace_id: 11,
        message: "Evaluate this property",
        tool_inputs: expect.objectContaining({
          VALUATION_TOOL: {
            workspace_id: 11,
            property_id: 22,
            scenario_id: null,
          },
          COMPARABLES_TOOL: {
            workspace_id: 11,
            property_id: 22,
            scenario_id: null,
            valuation_id: null,
          },
          MARKET_INSIGHT_TOOL: expect.objectContaining({
            workspace_id: 11,
            property_type: "Apartment",
          }),
        }),
      }),
      undefined,
    );
  });

  it("uses the direct valuation request id for valuation explanation follow-ups", async () => {
    runMock.mockResolvedValueOnce({ data: { ...sampleCopilotResponse, intent: "EXPLAINABILITY" }, meta: {} });
    activatePreparedProperty();
    usePropertyContextStore.setState({ lastBridgeRequestId: "req_direct_001" });

    await useCopilotStore.getState().sendMessage({ message: "Show valuation explanation" });

    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        tool_inputs: expect.objectContaining({
          EXPLAINABILITY_TOOL: {
            workspace_id: 11,
            valuation_id: "req_direct_001",
          },
        }),
      }),
      undefined,
    );
  });

  it.each([
    ["Generate investment analysis", "INVESTMENT_TOOL"],
    ["What are the risks?", "INVESTMENT_TOOL"],
    ["Compare with market", "COMPARABLES_TOOL"],
    ["Find negotiation opportunities", "NEGOTIATION_TOOL"],
  ])("keeps active-property inputs available for %s", async (message, expectedTool) => {
    runMock.mockResolvedValueOnce({ data: sampleCopilotResponse, meta: {} });
    activatePreparedProperty();

    await useCopilotStore.getState().sendMessage({ message });

    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        tool_inputs: expect.objectContaining({
          [expectedTool]: expect.objectContaining({
            workspace_id: 11,
            property_id: 22,
          }),
        }),
      }),
      undefined,
    );
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
      "Open or prepare a property first",
    );

    expect(runMock).not.toHaveBeenCalled();
    expect(useCopilotStore.getState().error?.message).toContain("Open or prepare a property first");
  });
});
