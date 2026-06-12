import { create } from "zustand";
import type { RentFairPriceData, RentFairPriceRequest } from "@/types/valuation";

export const defaultValuationRequest: RentFairPriceRequest = {
  location_mode: "address_resolution",
  address: "",
  canonical_entity_id: null,
  lat: undefined,
  lng: undefined,
  property_type: "Apartment",
  property_category: "residential_rent",
  bedrooms: 3,
  bathrooms: 2,
  size_sqm: 150,
  target_price_egp: 30000,
  amenities: [],
  furnishing_status: null,
  floor_number: null,
  compound_name: null,
  view_type: null,
  building_quality: null,
};

interface ValuationState {
  draft: RentFairPriceRequest;
  lastResult: RentFairPriceData | null;
  lastRequest: RentFairPriceRequest | null;
  lastRequestId?: string;
  setDraft: (draft: RentFairPriceRequest) => void;
  updateDraft: <TKey extends keyof RentFairPriceRequest>(key: TKey, value: RentFairPriceRequest[TKey]) => void;
  setLastResult: (result: RentFairPriceData | null, requestId?: string, request?: RentFairPriceRequest | null) => void;
  resetDraft: () => void;
}

export const useValuationStore = create<ValuationState>((set) => ({
  draft: defaultValuationRequest,
  lastResult: null,
  lastRequest: null,
  lastRequestId: undefined,
  setDraft: (draft) => set({ draft }),
  updateDraft: (key, value) =>
    set((state) => ({
      draft: {
        ...state.draft,
        [key]: value,
      },
    })),
  setLastResult: (result, requestId, request) =>
    set({
      lastResult: result,
      lastRequestId: requestId,
      lastRequest: result ? request ?? null : null,
    }),
  resetDraft: () => set({ draft: defaultValuationRequest }),
}));
