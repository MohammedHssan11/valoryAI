import * as React from "react";
import { useMutation } from "@tanstack/react-query";
import { ValorApiError } from "@/api/contracts";
import { requestFairRentPrice, FairRentValuationResult } from "@/services/valuationService";
import { RentFairPriceRequest } from "@/types/valuation";

const NON_RETRYABLE_CODES = new Set([
  "REQUEST_CANCELLED",
  "OFFLINE",
  "RATE_LIMIT_EXCEEDED",
  "REQUEST_TOO_LARGE",
  "INVALID_API_RESPONSE",
  "VALIDATION_ERROR",
  "INVALID_PROPERTY_TYPE",
  "INVALID_COORDINATES",
  "INVALID_ROOM_COUNT",
  "INVALID_TARGET_PRICE",
  "INVALID_SIZE",
]);

export function shouldRetryValuationRequest(failureCount: number, error: ValorApiError): boolean {
  return !NON_RETRYABLE_CODES.has(error.code) && failureCount < 2;
}

export function useFairRentValuation() {
  const abortRef = React.useRef<AbortController | null>(null);

  const mutation = useMutation<FairRentValuationResult, ValorApiError, RentFairPriceRequest>({
    mutationKey: ["valuation", "rent", "fair-price"],
    networkMode: "online",
    mutationFn: async (request) => {
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      try {
        return await requestFairRentPrice(request, controller.signal);
      } finally {
        if (abortRef.current === controller) {
          abortRef.current = null;
        }
      }
    },
    retry: shouldRetryValuationRequest,
    retryDelay: (attempt) => Math.min(1000 * 2 ** attempt, 4000),
  });

  const cancel = React.useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
  }, []);

  React.useEffect(() => cancel, [cancel]);

  return {
    ...mutation,
    cancel,
  };
}
