import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { runMarketInsight } from "@/services/marketInsightService";
import { APP_ROUTES } from "@/navigation/routes";
import { initialMarketInsightState, useMarketInsightStore } from "@/store/marketInsightStore";
import { usePropertyContextStore } from "@/store/propertyContextStore";
import {
  sampleEmptyMarketInsightResponse,
  sampleMarketInsightResponse,
  sampleSparseMarketInsightResponse,
} from "@/test/fixtures";
import { MarketIntelligencePanel } from "./MarketIntelligencePanel";

vi.mock("@/services/marketInsightService", () => ({
  runMarketInsight: vi.fn(),
}));

const runMock = vi.mocked(runMarketInsight);

function renderPanel(workspaceId: number | null = 11) {
  usePropertyContextStore.setState({
    activeWorkspaceId: workspaceId,
    activePropertyId: workspaceId === null ? null : 22,
    activeScenarioId: null,
    bridgeStatus: workspaceId === null ? "idle" : "ready",
  });

  return render(
    <MemoryRouter>
      <MarketIntelligencePanel />
    </MemoryRouter>,
  );
}

describe("MarketIntelligencePanel", () => {
  beforeEach(() => {
    runMock.mockReset();
    useMarketInsightStore.setState(initialMarketInsightState);
    usePropertyContextStore.setState({
      activeWorkspaceId: null,
      activePropertyId: null,
      activeScenarioId: null,
      bridgeStatus: "idle",
      lastBridgeRequestId: undefined,
      lastBridgeError: undefined,
      lastBoundAt: undefined,
    });
  });

  it("renders a no-workspace state without calling Tool 8", () => {
    renderPanel(null);

    expect(screen.getByText(/needs a workspace with persisted TruthLayer valuation history/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /open valuation/i })).toHaveAttribute("href", APP_ROUTES.valuation);
    expect(runMock).not.toHaveBeenCalled();
  });

  it("runs Tool 8 with active workspace and default filters", async () => {
    runMock.mockResolvedValueOnce({ data: sampleMarketInsightResponse, meta: { request_id: "market-req-1" } });
    renderPanel(44);

    fireEvent.click(screen.getByRole("button", { name: /run market intelligence/i }));

    await waitFor(() => expect(screen.getAllByText(/Observed 6 persisted TruthLayer valuations/i).length).toBeGreaterThan(0));
    expect(runMock).toHaveBeenCalledWith(
      {
        workspace_id: 44,
        time_window: "all",
      },
      expect.any(AbortSignal),
    );
    expect(screen.getByText("Valuation Volume")).toBeInTheDocument();
    expect(screen.getByText("EGP 4,450,000")).toBeInTheDocument();
    expect(screen.getByText("Confidence Distribution")).toBeInTheDocument();
    expect(screen.getByText("Comparable Density")).toBeInTheDocument();
    expect(screen.getByText("Nile Quarter")).toBeInTheDocument();
    expect(screen.getByText("Central Cairo")).toBeInTheDocument();
    expect(screen.getAllByText(/Median observed fair value is EGP 4,450,000/i).length).toBeGreaterThan(0);
    expect(screen.getByText("Source Counts")).toBeInTheDocument();
    expect(screen.getByText("Traceability Notes")).toBeInTheDocument();
  });

  it("maps filter controls exactly to backend request fields", async () => {
    runMock.mockResolvedValueOnce({ data: sampleMarketInsightResponse, meta: {} });
    renderPanel(11);

    fireEvent.change(screen.getByLabelText("compound_name"), { target: { value: "Nile Quarter" } });
    fireEvent.change(screen.getByLabelText("property_type"), { target: { value: "Apartment" } });
    fireEvent.change(screen.getByLabelText("h3_res9"), { target: { value: "89754e64993ffff" } });
    fireEvent.click(screen.getByRole("button", { name: "90d" }));
    fireEvent.click(screen.getByRole("button", { name: /run market intelligence/i }));

    await waitFor(() =>
      expect(runMock).toHaveBeenCalledWith(
        {
          workspace_id: 11,
          compound_name: "Nile Quarter",
          property_type: "Apartment",
          h3_res9: "89754e64993ffff",
          time_window: "90d",
        },
        expect.any(AbortSignal),
      ),
    );
  });

  it("renders the empty state without unsupported Pulse claims", async () => {
    runMock.mockResolvedValueOnce({ data: sampleEmptyMarketInsightResponse, meta: {} });
    renderPanel(11);

    fireEvent.change(screen.getByLabelText("compound_name"), { target: { value: "Unknown Compound" } });
    fireEvent.click(screen.getByRole("button", { name: "30d" }));
    fireEvent.click(screen.getByRole("button", { name: /run market intelligence/i }));

    await waitFor(() =>
      expect(screen.getByText("No persisted TruthLayer valuations match these filters.")).toBeInTheDocument(),
    );
    expect(screen.getByRole("link", { name: /open valuation/i })).toHaveAttribute("href", APP_ROUTES.valuation);
    expect(screen.queryByText(/Buy Signal/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Yield Variance/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Liquidity Index/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Capital Inflow/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Live Anomalies/i)).not.toBeInTheDocument();
  });

  it("shows sparse evidence warnings while keeping returned data visible", async () => {
    runMock.mockResolvedValueOnce({ data: sampleSparseMarketInsightResponse, meta: {} });
    renderPanel(11);

    fireEvent.click(screen.getByRole("button", { name: /run market intelligence/i }));

    await waitFor(() => expect(screen.getAllByText("Evidence Quality").length).toBeGreaterThan(0));
    expect(screen.getByText(/Evidence is sparse/i)).toBeInTheDocument();
    expect(screen.getAllByText("Sparse").length).toBeGreaterThan(0);
    expect(screen.getAllByText("EGP 3,900,000").length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Observed 1 persisted TruthLayer valuation/i).length).toBeGreaterThan(0);
  });

  it("renders service errors without showing stale results", async () => {
    useMarketInsightStore.setState({ lastResponse: sampleMarketInsightResponse });
    runMock.mockRejectedValueOnce(new Error("Tool 8 failed"));
    renderPanel(11);

    fireEvent.click(screen.getByRole("button", { name: /run market intelligence/i }));

    await waitFor(() => expect(screen.getByText("Market Intelligence Error")).toBeInTheDocument());
    expect(screen.getByText("Tool 8 failed")).toBeInTheDocument();
    expect(screen.queryByText("Valuation Volume")).not.toBeInTheDocument();
  });

  it("does not render the removed unsupported Pulse vocabulary", () => {
    renderPanel(11);

    expect(screen.queryByText(/Buy Signal/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Yield Variance/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Liquidity Index/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Capital Inflow/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Live Anomalies/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Future Price/i)).not.toBeInTheDocument();
  });
});
