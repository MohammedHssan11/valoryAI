import { beforeEach, describe, expect, it } from "vitest";
import { sampleValuation } from "@/test/fixtures";
import { defaultValuationRequest, useValuationStore } from "./valuationStore";

describe("valuation store", () => {
  beforeEach(() => {
    useValuationStore.setState({
      draft: defaultValuationRequest,
      lastResult: null,
      lastRequest: null,
      lastRequestId: undefined,
    });
  });

  it("updates individual draft fields without dropping the rest of the request", () => {
    useValuationStore.getState().updateDraft("size_sqm", 220);

    const draft = useValuationStore.getState().draft;
    expect(draft.size_sqm).toBe(220);
    expect(draft.property_type).toBe("Apartment");
    expect(draft.property_category).toBe("residential_rent");
    expect(draft.amenities).toEqual([]);
  });

  it("stores the latest valuation result with request id for traceability", () => {
    useValuationStore.getState().setLastResult(sampleValuation, "req-valuation-1", defaultValuationRequest);

    expect(useValuationStore.getState().lastResult?.fair_price_egp).toBe(90000);
    expect(useValuationStore.getState().lastRequest?.property_type).toBe("Apartment");
    expect(useValuationStore.getState().lastRequestId).toBe("req-valuation-1");
  });

  it("resets draft back to the deterministic default request", () => {
    useValuationStore.getState().updateDraft("bedrooms", 5);
    useValuationStore.getState().resetDraft();

    expect(useValuationStore.getState().draft).toEqual(defaultValuationRequest);
  });
});
