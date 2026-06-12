import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { sampleValuation } from "@/test/fixtures";
import { ConfidenceVisualization } from "./ConfidenceVisualization";

describe("ConfidenceVisualization", () => {
  it("renders separate valuation evidence and location confidence dimensions", () => {
    render(<ConfidenceVisualization result={sampleValuation} />);

    expect(screen.getByText(/valuation confidence/i)).toBeInTheDocument();
    expect(screen.getByText(/evidence confidence/i)).toBeInTheDocument();
    expect(screen.getByText(/location confidence/i)).toBeInTheDocument();
    expect(screen.getByText(/high-quality cluster/i)).toBeInTheDocument();
  });
});
