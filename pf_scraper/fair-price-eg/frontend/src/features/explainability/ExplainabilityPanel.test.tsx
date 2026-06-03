import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { sampleValuation } from "@/test/fixtures";
import { ExplainabilityPanel } from "./ExplainabilityPanel";

describe("ExplainabilityPanel", () => {
  it("renders rationale and deterministic explanation trace codes", () => {
    render(<ExplainabilityPanel result={sampleValuation} />);

    expect(screen.getByText(/evidence trail/i)).toBeInTheDocument();
    expect(screen.getByText(/12 similar listings found/i)).toBeInTheDocument();
    expect(screen.getAllByText("SAME_AREA_MATCH").length).toBeGreaterThan(0);
    expect(screen.getByText("CONFIDENCE_FACTORS")).toBeInTheDocument();
    expect(screen.getByText("FEATURE_SIMILARITY_APPLIED")).toBeInTheDocument();
    expect(screen.getByText(/retrieval timeline/i)).toBeInTheDocument();
    expect(screen.getByText(/confidence stack/i)).toBeInTheDocument();
    expect(screen.getByText(/guardrails removed/i)).toBeInTheDocument();
    expect(screen.getByText(/category & amenity governance/i)).toBeInTheDocument();
    expect(screen.getAllByText(/residential rent/i).length).toBeGreaterThan(0);
  });
});
