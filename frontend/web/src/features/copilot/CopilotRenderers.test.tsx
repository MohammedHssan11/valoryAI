import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { sampleCopilotResponse } from "@/test/fixtures";
import type { CopilotFrontendPayload } from "@/types/copilot";
import { CitationViewer } from "./CitationViewer";
import { ContextSummaryBar } from "./ContextSummaryBar";
import { EvidenceDrawer } from "./EvidenceDrawer";
import { ToolExecutionTimeline } from "./ToolExecutionTimeline";

const payload = sampleCopilotResponse.response as CopilotFrontendPayload;

describe("Copilot structured renderers", () => {
  it("renders valuation, tool-event, comparable, and unavailable citation groups", () => {
    render(<CitationViewer citations={sampleCopilotResponse.citation_package} />);

    expect(screen.getByText("Valuation IDs")).toBeInTheDocument();
    expect(screen.getByText("val-investment-1")).toBeInTheDocument();
    expect(screen.getByText("Tool Event IDs")).toBeInTheDocument();
    expect(screen.getByText("Comparable IDs")).toBeInTheDocument();
    expect(screen.getAllByText("scenario-comp-1").length).toBeGreaterThan(0);
    expect(screen.getByText(/Optional unavailable: tool_event_id/i)).toBeInTheDocument();
  });

  it("renders tool execution status and results used", () => {
    render(<ToolExecutionTimeline payload={payload} />);

    expect(screen.getByText("Tool Execution")).toBeInTheDocument();
    expect(screen.getByText("INVESTMENT Tool")).toBeInTheDocument();
    expect(screen.getByText("investment")).toBeInTheDocument();
    expect(screen.getByText(/Results used from order 1/i)).toBeInTheDocument();
  });

  it("renders human-readable memory context without raw backend payloads", () => {
    render(
      <ContextSummaryBar
        context={{
          activeProperty: "Apartment at Nile Quarter (Property 22)",
          activeScenario: "Base valuation",
          latestValuation: "EGP 90,000 fair price, High confidence",
          latestNegotiation: "Overpriced",
          latestInvestment: "High Risk",
          latestMarketInsight: "6 valuations, High density",
          relevantHistory: ["Scenario: Scenario A"],
          memoryId: "memory_fixture",
          memoryStatus: "SUCCESS",
        }}
      />,
    );

    expect(screen.getByText("Apartment at Nile Quarter (Property 22)")).toBeInTheDocument();
    expect(screen.getByText("SUCCESS")).toBeInTheDocument();
    expect(screen.getByText("Scenario: Scenario A")).toBeInTheDocument();
    expect(screen.queryByText(/workspace_context/i)).not.toBeInTheDocument();
  });

  it("renders evidence drawer rows and closes through the icon button", () => {
    const onClose = vi.fn();
    render(<EvidenceDrawer isOpen payload={payload} onClose={onClose} />);

    expect(screen.getByText("Evidence Package")).toBeInTheDocument();
    expect(screen.getByText("Comparable Evidence")).toBeInTheDocument();
    expect(screen.getAllByText("scenario-comp-1").length).toBeGreaterThan(0);
    fireEvent.click(screen.getByRole("button", { name: /close evidence/i }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
