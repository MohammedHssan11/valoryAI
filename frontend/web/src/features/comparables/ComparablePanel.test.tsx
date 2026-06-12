import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { useComparableAnalysisStore } from "@/store/comparableAnalysisStore";
import { sampleComparable, sampleValuation, secondaryComparable } from "@/test/fixtures";
import { ComparablePanel } from "./ComparablePanel";

describe("ComparablePanel", () => {
  beforeEach(() => {
    useComparableAnalysisStore.setState({ selectedComparable: null });
  });

  it("renders deterministic comparable evidence and stores selected comparable", () => {
    render(<ComparablePanel comparables={[sampleComparable]} result={sampleValuation} subjectPropertyType="Apartment" />);

    expect(screen.getByText(/top deterministic matches/i)).toBeInTheDocument();
    expect(screen.getAllByText("Central Cairo").length).toBeGreaterThan(0);
    expect(screen.getByText("EGP 90,000")).toBeInTheDocument();
    expect(screen.getByText(/confidence contribution/i)).toBeInTheDocument();
    expect(screen.getByText(/amenity similarity/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /select comparable comp-001/i }));

    expect(useComparableAnalysisStore.getState().selectedComparable?.listing_id).toBe("comp-001");
  });

  it("sorts comparable cards deterministically by weighted contribution then listing id", () => {
    render(<ComparablePanel comparables={[secondaryComparable, sampleComparable]} result={sampleValuation} subjectPropertyType="Apartment" />);

    const cards = screen.getAllByTestId(/comparable-card-/);

    expect(cards[0]).toHaveAttribute("data-testid", "comparable-card-comp-001");
    expect(cards[1]).toHaveAttribute("data-testid", "comparable-card-comp-002");
  });

  it("filters exploration comparables without mutating selected valuation evidence", () => {
    render(<ComparablePanel comparables={[sampleComparable, secondaryComparable]} result={sampleValuation} subjectPropertyType="Apartment" />);

    fireEvent.change(screen.getByLabelText(/comparable similarity filter/i), { target: { value: "0.8" } });

    expect(screen.getByTestId("comparable-card-comp-001")).toBeInTheDocument();
    expect(screen.queryByTestId("comparable-card-comp-002")).not.toBeInTheDocument();
    expect(screen.getByText(/authoritative valuation frozen/i)).toBeInTheDocument();
  });

  it("renders an empty state when no comparable evidence is returned", () => {
    render(<ComparablePanel comparables={[]} />);

    expect(screen.getByText(/no comparable listings were returned/i)).toBeInTheDocument();
  });
});
