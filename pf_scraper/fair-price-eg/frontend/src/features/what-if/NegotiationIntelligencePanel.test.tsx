import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { ComponentProps } from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { runNegotiationAnalysis } from "@/services/negotiationService";
import { initialNegotiationState, useNegotiationStore } from "@/store/negotiationStore";
import { sampleNegotiationResponse, sampleRequest, sampleValuation, sampleWhatIfResponse } from "@/test/fixtures";
import type { ScenarioState } from "@/types/scenarioHistory";
import { NegotiationIntelligencePanel } from "./NegotiationIntelligencePanel";

vi.mock("@/services/negotiationService", () => ({
  runNegotiationAnalysis: vi.fn(),
}));

const runMock = vi.mocked(runNegotiationAnalysis);

const activeScenarioRequest = {
  workspace_id: 11,
  property_id: 22,
  scenario_id: null,
  modifications: {
    size_sqm: 180,
  },
};

const selectedScenario: ScenarioState = {
  id: 7,
  workspace_id: 11,
  property_state_id: 22,
  parent_scenario_id: null,
  name: "Scenario A",
  modifications: {
    size_sqm: 180,
  },
  delta_value: 18000,
  created_at: "2026-06-09T09:00:00Z",
};

function renderPanel(
  overrides: Partial<ComponentProps<typeof NegotiationIntelligencePanel>> = {},
) {
  return render(
    <NegotiationIntelligencePanel
      baseRequest={sampleRequest}
      baseResult={sampleValuation}
      workspaceId={11}
      propertyId={22}
      activeScenarioRequest={null}
      activeScenarioResponse={null}
      selectedScenario={null}
      bridgeStatus="ready"
      {...overrides}
    />,
  );
}

describe("NegotiationIntelligencePanel", () => {
  beforeEach(() => {
    runMock.mockReset();
    useNegotiationStore.setState(initialNegotiationState);
  });

  it("keeps negotiation disabled until backend property context exists", () => {
    renderPanel({ workspaceId: null, propertyId: null });

    expect(screen.getByText(/property context ready/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /run negotiation/i })).toBeDisabled();
  });

  it("runs negotiation on the base valuation", async () => {
    runMock.mockResolvedValueOnce({ data: { ...sampleNegotiationResponse, what_if_analysis: null }, meta: {} });
    renderPanel();

    fireEvent.change(screen.getByLabelText(/negotiation asking price/i), { target: { value: "118000" } });
    fireEvent.click(screen.getByRole("button", { name: /run negotiation/i }));

    await waitFor(() => expect(screen.getByText("Overpriced")).toBeInTheDocument());
    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        workspace_id: 11,
        property_id: 22,
        scenario_id: null,
        asking_price_egp: 118000,
      }),
      expect.any(AbortSignal),
    );
    expect(runMock.mock.calls[0][0]).not.toHaveProperty("what_if_modifications");
    expect(screen.getByText("Fair Price")).toBeInTheDocument();
    expect(screen.getByText("Asking Price")).toBeInTheDocument();
    expect(screen.getByText("Recommended Offer")).toBeInTheDocument();
    expect(screen.getByText("Negotiation Range")).toBeInTheDocument();
    expect(screen.getByText("Buyer Position")).toBeInTheDocument();
    expect(screen.getByText("Seller Position")).toBeInTheDocument();
    expect(screen.getByText("Strengths")).toBeInTheDocument();
    expect(screen.getByText("Risks")).toBeInTheDocument();
    expect(screen.getByText("Talking Points")).toBeInTheDocument();
    expect(screen.getByText("Evidence")).toBeInTheDocument();
  });

  it("runs negotiation on the active unsaved scenario with what-if modifications", async () => {
    runMock.mockResolvedValueOnce({ data: sampleNegotiationResponse, meta: {} });
    renderPanel({
      activeScenarioRequest,
      activeScenarioResponse: sampleWhatIfResponse,
    });

    fireEvent.change(screen.getByLabelText(/negotiation asking price/i), { target: { value: "118000" } });
    fireEvent.click(screen.getByRole("button", { name: /run negotiation/i }));

    await waitFor(() => expect(screen.getByText(/scenario awareness/i)).toBeInTheDocument());
    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        workspace_id: 11,
        property_id: 22,
        scenario_id: null,
        asking_price_egp: 118000,
        what_if_modifications: {
          size_sqm: 180,
        },
      }),
      expect.any(AbortSignal),
    );
  });

  it("runs negotiation on the selected restored scenario with scenario_id", async () => {
    runMock.mockResolvedValueOnce({ data: { ...sampleNegotiationResponse, what_if_analysis: null }, meta: {} });
    renderPanel({ selectedScenario });

    fireEvent.click(screen.getByRole("button", { name: /scenario a/i }));
    fireEvent.change(screen.getByLabelText(/negotiation asking price/i), { target: { value: "110000" } });
    fireEvent.click(screen.getByRole("button", { name: /run negotiation/i }));

    await waitFor(() => expect(screen.getByText("Overpriced")).toBeInTheDocument());
    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        workspace_id: 11,
        property_id: 22,
        scenario_id: 7,
        asking_price_egp: 110000,
      }),
      expect.any(AbortSignal),
    );
    expect(runMock.mock.calls[0][0]).not.toHaveProperty("what_if_modifications");
  });

  it("renders service errors", async () => {
    runMock.mockRejectedValueOnce(new Error("Negotiation failed"));
    renderPanel();

    fireEvent.click(screen.getByRole("button", { name: /run negotiation/i }));

    await waitFor(() => expect(screen.getByText(/negotiation failed/i)).toBeInTheDocument());
    expect(screen.getByText(/negotiation error/i)).toBeInTheDocument();
  });

  it("compares negotiation outcomes after multiple scenario runs", async () => {
    const scenarioResponse = {
      ...sampleNegotiationResponse,
      valuation_id: "val-selected-scenario",
      asking_price: 110000,
      fair_price: 108000,
      price_gap: 2000,
      price_gap_percentage: 1.8519,
      negotiation_position: "Negotiation Recommended" as const,
      what_if_analysis: null,
    };
    runMock
      .mockResolvedValueOnce({ data: { ...sampleNegotiationResponse, what_if_analysis: null }, meta: {} })
      .mockResolvedValueOnce({ data: scenarioResponse, meta: {} });
    renderPanel({ selectedScenario });

    fireEvent.click(screen.getByRole("button", { name: /base valuation/i }));
    fireEvent.click(screen.getByRole("button", { name: /run negotiation/i }));
    await waitFor(() => expect(screen.getByText("Overpriced")).toBeInTheDocument());

    fireEvent.click(screen.getByRole("button", { name: /scenario a/i }));
    fireEvent.click(screen.getByRole("button", { name: /run negotiation/i }));

    await waitFor(() => expect(screen.getByText(/outcome comparison/i)).toBeInTheDocument());
    expect(screen.getAllByText("Base valuation").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Scenario A").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Negotiation Recommended").length).toBeGreaterThan(0);
  });
});
