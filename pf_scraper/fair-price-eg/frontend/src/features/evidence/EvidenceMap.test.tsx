import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { useComparableAnalysisStore } from "@/store/comparableAnalysisStore";
import { sampleComparable, sampleValuation, secondaryComparable } from "@/test/fixtures";
import { EvidenceMap } from "./EvidenceMap";

describe("EvidenceMap", () => {
  beforeEach(() => {
    useComparableAnalysisStore.setState({ selectedComparable: null });
  });

  it("renders governed subject radius and synchronizes comparable selection", () => {
    render(<EvidenceMap result={sampleValuation} comparables={[sampleComparable, secondaryComparable]} />);

    expect(screen.getByRole("img", { name: /deterministic comparable evidence map/i })).toBeInTheDocument();
    expect(screen.getAllByText(/radius 500m/i).length).toBeGreaterThan(0);

    fireEvent.click(screen.getByRole("button", { name: /select comparable comp-002/i }));

    expect(useComparableAnalysisStore.getState().selectedComparable?.listing_id).toBe("comp-002");
  });
});
