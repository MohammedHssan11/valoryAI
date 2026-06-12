import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { ValorApiError } from "@/api/contracts";
import { sampleValuation } from "@/test/fixtures";
import { HeroValuationCard } from "./HeroValuationCard";

describe("HeroValuationCard", () => {
  it("renders loading state with a cancellation affordance", () => {
    const onCancel = vi.fn();

    render(<HeroValuationCard result={null} isLoading onCancel={onCancel} />);

    expect(screen.getByText(/retrieving comparable evidence/i)).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /cancel/i }));
    expect(onCancel).toHaveBeenCalledTimes(1);
  });

  it("renders valuation result, confidence, range, and trace request id", () => {
    render(<HeroValuationCard result={sampleValuation} targetPrice={95000} requestId="req-ui-1" />);

    expect(screen.getByText("EGP 90,000")).toBeInTheDocument();
    expect(screen.getByText(/EGP 82,000 - EGP 105,000/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /high 82%/i })).toBeInTheDocument();
    expect(screen.getByText(/request req-ui-1/i)).toBeInTheDocument();
  });

  it("renders API errors with details and retry action", () => {
    const onRetry = vi.fn();
    const error = new ValorApiError(
      {
        code: "INVALID_SIZE",
        message: "Request validation failed",
        details: [{ code: "INVALID_SIZE", message: "Input should be greater than 0", field: "size_sqm" }],
      },
      { requestId: "req-error-1", status: 422 },
    );

    render(<HeroValuationCard result={null} error={error} onRetry={onRetry} />);

    expect(screen.getByText("INVALID_SIZE")).toBeInTheDocument();
    expect(screen.getByText(/input should be greater than 0/i)).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /retry/i }));
    expect(onRetry).toHaveBeenCalledTimes(1);
  });
});
