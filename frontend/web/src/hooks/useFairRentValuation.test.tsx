import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { ValorApiError } from "@/api/contracts";
import { sampleRequest } from "@/test/fixtures";
import { renderWithQueryClient } from "@/test/test-utils";
import { requestFairRentPrice } from "@/services/valuationService";
import { shouldRetryValuationRequest, useFairRentValuation } from "./useFairRentValuation";

vi.mock("@/services/valuationService", () => ({
  requestFairRentPrice: vi.fn(),
}));

const requestMock = vi.mocked(requestFairRentPrice);

describe("useFairRentValuation", () => {
  beforeEach(() => {
    requestMock.mockReset();
  });

  it("does not retry validation or cancellation failures", () => {
    const validationError = new ValorApiError({ code: "INVALID_SIZE", message: "Invalid size", details: [] });
    const cancelledError = new ValorApiError({ code: "REQUEST_CANCELLED", message: "Cancelled", details: [] });
    const offlineError = new ValorApiError({ code: "OFFLINE", message: "Offline", details: [] });
    const malformedError = new ValorApiError({ code: "INVALID_API_RESPONSE", message: "Malformed", details: [] });
    const networkError = new ValorApiError({ code: "NETWORK_ERROR", message: "Network failed", details: [] });

    expect(shouldRetryValuationRequest(0, validationError)).toBe(false);
    expect(shouldRetryValuationRequest(0, cancelledError)).toBe(false);
    expect(shouldRetryValuationRequest(0, offlineError)).toBe(false);
    expect(shouldRetryValuationRequest(0, malformedError)).toBe(false);
    expect(shouldRetryValuationRequest(0, networkError)).toBe(true);
    expect(shouldRetryValuationRequest(2, networkError)).toBe(false);
  });

  it("aborts the previous valuation when a newer mutation starts", async () => {
    const signals: AbortSignal[] = [];
    requestMock.mockImplementation((_request, signal) => {
      signals.push(signal as AbortSignal);
      return new Promise(() => {});
    });

    function Harness() {
      const valuation = useFairRentValuation();
      return (
        <button type="button" onClick={() => valuation.mutate(sampleRequest)}>
          Run valuation
        </button>
      );
    }

    renderWithQueryClient(<Harness />);

    fireEvent.click(screen.getByRole("button", { name: /run valuation/i }));
    await waitFor(() => expect(signals).toHaveLength(1));
    expect(signals[0].aborted).toBe(false);

    fireEvent.click(screen.getByRole("button", { name: /run valuation/i }));
    await waitFor(() => expect(signals).toHaveLength(2));

    expect(signals[0].aborted).toBe(true);
    expect(signals[1].aborted).toBe(false);
  });

  it("cancels the active request when the consumer calls cancel", async () => {
    const signals: AbortSignal[] = [];
    requestMock.mockImplementation((_request, signal) => {
      signals.push(signal as AbortSignal);
      return new Promise(() => {});
    });

    function Harness() {
      const valuation = useFairRentValuation();
      return (
        <>
          <button type="button" onClick={() => valuation.mutate(sampleRequest)}>
            Run valuation
          </button>
          <button type="button" onClick={valuation.cancel}>
            Cancel valuation
          </button>
        </>
      );
    }

    renderWithQueryClient(<Harness />);

    fireEvent.click(screen.getByRole("button", { name: /run valuation/i }));
    await waitFor(() => expect(signals).toHaveLength(1));
    fireEvent.click(screen.getByRole("button", { name: /cancel valuation/i }));

    expect(signals[0].aborted).toBe(true);
  });
});
