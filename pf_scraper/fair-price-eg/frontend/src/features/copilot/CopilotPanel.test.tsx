import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { runCopilot } from "@/services/copilotService";
import { initialCopilotState, useCopilotStore } from "@/store/copilotStore";
import { initialInvestmentState, useInvestmentStore } from "@/store/investmentStore";
import { initialMarketInsightState, useMarketInsightStore } from "@/store/marketInsightStore";
import { initialNegotiationState, useNegotiationStore } from "@/store/negotiationStore";
import { usePropertyContextStore } from "@/store/propertyContextStore";
import { useValuationStore } from "@/store/valuationStore";
import { initialWhatIfState, useWhatIfStore } from "@/store/whatIfStore";
import {
  sampleCopilotResponse,
  sampleInvestmentResponse,
  sampleMarketInsightResponse,
  sampleNegotiationResponse,
  sampleRequest,
  sampleValuation,
} from "@/test/fixtures";
import { CopilotPanel } from "./CopilotPanel";

vi.mock("@/services/copilotService", () => ({
  runCopilot: vi.fn(),
}));

const runMock = vi.mocked(runCopilot);

describe("CopilotPanel", () => {
  beforeEach(() => {
    runMock.mockReset();
    useCopilotStore.setState(initialCopilotState);
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
    useWhatIfStore.setState(initialWhatIfState);
    useNegotiationStore.setState({
      ...initialNegotiationState,
      lastResponse: sampleNegotiationResponse,
    });
    useInvestmentStore.setState({
      ...initialInvestmentState,
      lastResponse: sampleInvestmentResponse,
    });
    useMarketInsightStore.setState({
      ...initialMarketInsightState,
      lastResponse: sampleMarketInsightResponse,
    });
  });

  it("submits contextual questions and renders structured orchestrator output", async () => {
    runMock.mockResolvedValueOnce({ data: sampleCopilotResponse, meta: { request_id: "copilot-1" } });
    render(<CopilotPanel />);

    expect(screen.getByRole("button", { name: "Should I buy this property?" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /ask copilot/i }));

    await waitFor(() => expect(screen.getByText(/High Risk:/i)).toBeInTheDocument());
    expect(screen.getByText("Tool Execution")).toBeInTheDocument();
    expect(screen.getByText("INVESTMENT Tool")).toBeInTheDocument();
    expect(screen.getByText("Citations")).toBeInTheDocument();
    expect(screen.getByText("val-investment-1")).toBeInTheDocument();
    expect(screen.getAllByText("SUCCESS").length).toBeGreaterThan(0);
    expect(screen.getByText(/Copilot returned deterministic fallback/i)).toBeInTheDocument();
    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        workspace_id: 11,
        message: "Should I buy this property? Is this a good investment?",
      }),
      expect.any(AbortSignal),
    );
  });

  it("shows property-context pending state when no workspace is active", () => {
    usePropertyContextStore.setState({
      activeWorkspaceId: null,
      activePropertyId: null,
      activeScenarioId: null,
      bridgeStatus: "idle",
    });

    render(<CopilotPanel />);

    expect(screen.getByText("Property Context Pending")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /ask copilot/i })).toBeDisabled();
  });
});
