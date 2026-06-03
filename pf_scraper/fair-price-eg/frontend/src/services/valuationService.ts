import { http } from "@/api/http";
import { ApiMeta, ApiSuccessEnvelope, isApiSuccessEnvelope, ValorApiError } from "@/api/contracts";
import { RentFairPriceData, RentFairPriceRequest } from "@/types/valuation";

export interface FairRentValuationResult {
  data: RentFairPriceData;
  meta: ApiMeta;
}

function isRentFairPriceData(value: unknown): value is RentFairPriceData {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Partial<RentFairPriceData>;
  return (
    typeof candidate.fair_price_egp === "number" &&
    typeof candidate.range_low_egp === "number" &&
    typeof candidate.range_high_egp === "number" &&
    typeof candidate.tier_used === "number" &&
    typeof candidate.comps_count === "number" &&
    typeof candidate.confidence === "object" &&
    candidate.confidence !== null &&
    Array.isArray(candidate.explanation) &&
    Array.isArray(candidate.explanation_trace) &&
    Array.isArray(candidate.top_comps)
  );
}

function assertRentFairPriceData(value: unknown, requestId?: string): RentFairPriceData {
  if (isRentFairPriceData(value)) return value;
  throw new ValorApiError(
    {
      code: "INVALID_API_RESPONSE",
      message: "The ValorAI API returned an unexpected valuation response.",
      details: [],
    },
    { requestId },
  );
}

export async function requestFairRentPrice(
  request: RentFairPriceRequest,
  signal?: AbortSignal,
): Promise<FairRentValuationResult> {
  const response = await http.post<ApiSuccessEnvelope<RentFairPriceData> | RentFairPriceData>(
    "/v1/valuation/fair-price",
    request,
    { signal },
  );

  if (isApiSuccessEnvelope<RentFairPriceData>(response.data)) {
    return {
      data: assertRentFairPriceData(response.data.data, response.data.meta.request_id),
      meta: response.data.meta,
    };
  }

  return {
    data: assertRentFairPriceData(response.data),
    meta: {},
  };
}
