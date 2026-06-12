import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { ComponentProps } from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { runInvestmentAnalysis } from "@/services/investmentService";
import { initialInvestmentState, useInvestmentStore } from "@/store/investmentStore";
import { sampleInvestmentResponse, sampleRequest, sampleValuation, sampleWhatIfResponse } from "@/test/fixtures";
import type { ScenarioState } from "@/types/scenarioHistory";
import { InvestmentIntelligencePanel } from "./InvestmentIntelligencePanel";

vi.mock("@/services/investmentService", () => ({
  runInvestmentAnalysis: vi.fn(),
}));

const runMock = vi.mocked(runInvestmentAnalysis);

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

const comparedScenario: ScenarioState = {
  ...selectedScenario,
  id: 8,
  name: "Scenario B",
  modifications: {
    bathrooms: 3,
  },
};

function renderPanel(overrides: Partial<ComponentProps<typeof InvestmentIntelligencePanel>> = {}) {
  return render(
    <InvestmentIntelligencePanel
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

describe("InvestmentIntelligencePanel", () => {
  beforeEach(() => {
    runMock.mockReset();
    useInvestmentStore.setState(initialInvestmentState);
  });

  it("keeps investment disabled until backend property context exists", () => {
    renderPanel({ workspaceId: null, propertyId: null });

    expect(screen.getByText(/property context ready/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /run investment/i })).toBeDisabled();
  });

  it("runs investment analysis on the base valuation", async () => {
    runMock.mockResolvedValueOnce({
      data: {
        ...sampleInvestmentResponse,
        what_if_summary: {
          status: "Insufficient Evidence",
          reason: "No optional What-if Tool sensitivity request was supplied.",
          analysis: null,
          source: "Insufficient Evidence",
        },
      },
      meta: {},
    });
    renderPanel();

    fireEvent.change(screen.getByLabelText(/investment asking price/i), { target: { value: "118000" } });
    fireEvent.click(screen.getByRole("button", { name: /run investment/i }));

    await waitFor(() => expect(screen.getAllByText("High Risk").length).toBeGreaterThan(0));
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
    expect(screen.getByText("Investment Recommendation")).toBeInTheDocument();
    expect(screen.getByText("Investment Scorecard")).toBeInTheDocument();
    expect(screen.getByText("Strengths")).toBeInTheDocument();
    expect(screen.getByText("Risks")).toBeInTheDocument();
    expect(screen.getByText("Upside")).toBeInTheDocument();
    expect(screen.getByText("Downside")).toBeInTheDocument();
    expect(screen.getByText("Supporting Evidence")).toBeInTheDocument();
  });

  it("runs investment analysis on the active unsaved scenario with what-if modifications", async () => {
    runMock.mockResolvedValueOnce({ data: sampleInvestmentResponse, meta: {} });
    renderPanel({
      activeScenarioRequest,
      activeScenarioResponse: sampleWhatIfResponse,
    });

    fireEvent.change(screen.getByLabelText(/investment asking price/i), { target: { value: "118000" } });
    fireEvent.click(screen.getByRole("button", { name: /run investment/i }));

    await waitFor(() => expect(screen.getByText(/scenario delta/i)).toBeInTheDocument());
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

  it("runs investment analysis on the selected restored scenario with scenario_id", async () => {
    runMock.mockResolvedValueOnce({ data: sampleInvestmentResponse, meta: {} });
    renderPanel({ selectedScenario });

    fireEvent.click(screen.getByRole("button", { name: /scenario a/i }));
    fireEvent.change(screen.getByLabelText(/investment asking price/i), { target: { value: "110000" } });
    fireEvent.click(screen.getByRole("button", { name: /run investment/i }));

    await waitFor(() => expect(screen.getAllByText("High Risk").length).toBeGreaterThan(0));
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

  it("renders sparse investment responses without fabricating missing evidence", async () => {
    runMock.mockResolvedValueOnce({
      data: {
        ...sampleInvestmentResponse,
        strengths: [],
        risks: [],
        comparable_summary: {
          ...sampleInvestmentResponse.comparable_summary,
          comparable_count: 0,
          comparable_ids: [],
          observed_prices: [],
          lowest_observed_price: null,
          highest_observed_price: null,
        },
        what_if_summary: {
          status: "Insufficient Evidence",
          reason: "No optional What-if Tool sensitivity request was supplied.",
          analysis: null,
          source: "Insufficient Evidence",
        },
      },
      meta: {},
    });
    renderPanel();

    fireEvent.click(screen.getByRole("button", { name: /run investment/i }));

    await waitFor(() => expect(screen.getByText(/no strengths were returned/i)).toBeInTheDocument());
    expect(screen.getByText(/no risks were returned/i)).toBeInTheDocument();
    expect(screen.getByText(/no comparable ids were returned/i)).toBeInTheDocument();
    expect(screen.getByText(/observed prices unavailable/i)).toBeInTheDocument();
  });

  it("renders service errors", async () => {
    runMock.mockRejectedValueOnce(new Error("Investment failed"));
    renderPanel();

    fireEvent.click(screen.getByRole("button", { name: /run investment/i }));

    await waitFor(() => expect(screen.getByText(/investment failed/i)).toBeInTheDocument());
    expect(screen.getByText(/investment error/i)).toBeInTheDocument();
  });

  it("compares investment outcomes across base and saved scenarios", async () => {
    const scenarioAResponse = {
      ...sampleInvestmentResponse,
      valuation_id: "val-scenario-a",
      asking_price: 90000,
      fair_price: 108000,
      price_gap: -18000,
      price_gap_percentage: -16.6667,
      investment_position: "Strong Opportunity" as const,
      strengths: [...sampleInvestmentResponse.strengths, sampleInvestmentResponse.strengths[0]],
      risks: sampleInvestmentResponse.risks.slice(0, 1),
    };
    const scenarioBResponse = {
      ...sampleInvestmentResponse,
      valuation_id: "val-scenario-b",
      asking_price: 104000,
      fair_price: 104000,
      price_gap: 0,
      price_gap_percentage: 0,
      investment_position: "Fairly Priced" as const,
    };
    runMock
      .mockResolvedValueOnce({ data: sampleInvestmentResponse, meta: {} })
      .mockResolvedValueOnce({ data: scenarioAResponse, meta: {} })
      .mockResolvedValueOnce({ data: scenarioBResponse, meta: {} });
    renderPanel({ selectedScenario, comparedScenarios: [comparedScenario] });

    fireEvent.click(screen.getByRole("button", { name: /base valuation/i }));
    fireEvent.click(screen.getByRole("button", { name: /run investment/i }));
    await waitFor(() => expect(screen.getAllByText("High Risk").length).toBeGreaterThan(0));

    fireEvent.click(screen.getByRole("button", { name: /scenario a/i }));
    fireEvent.click(screen.getByRole("button", { name: /run investment/i }));
    await waitFor(() => expect(screen.getAllByText("Strong Opportunity").length).toBeGreaterThan(0));

    fireEvent.click(screen.getByRole("button", { name: /scenario b/i }));
    fireEvent.click(screen.getByRole("button", { name: /run investment/i }));

    await waitFor(() => expect(screen.getByText(/investment scenario comparison/i)).toBeInTheDocument());
    expect(screen.getAllByText("Base valuation").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Scenario A").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Scenario B").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Improved").length).toBeGreaterThan(0);
  });
});
