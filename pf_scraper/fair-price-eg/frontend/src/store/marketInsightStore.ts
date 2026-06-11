import { create } from "zustand";
import { runMarketInsight as runMarketInsightService } from "@/services/marketInsightService";
import type {
  MarketInsightFilters,
  MarketInsightRunRecord,
  MarketInsightToolRequest,
  MarketInsightToolResponse,
} from "@/types/marketInsight";

export const defaultMarketInsightFilters: MarketInsightFilters = {
  compound_name: "",
  h3_res9: "",
  property_type: "",
  time_window: "all",
};

function toError(error: unknown): Error {
  if (error instanceof Error) return error;
  return new Error("Unable to run market intelligence.");
}

function stableComparableValue(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(stableComparableValue);
  if (typeof value === "object" && value !== null) {
    return Object.fromEntries(
      Object.keys(value as Record<string, unknown>)
        .sort()
        .map((key) => [key, stableComparableValue((value as Record<string, unknown>)[key])]),
    );
  }
  return value;
}

function runKey(request: MarketInsightToolRequest): string {
  return JSON.stringify(stableComparableValue(request));
}

interface MarketInsightState {
  lastRequest: MarketInsightToolRequest | null;
  lastResponse: MarketInsightToolResponse | null;
  filters: MarketInsightFilters;
  runs: MarketInsightRunRecord[];
  isLoading: boolean;
  error: Error | null;
  setFilters: (filters: Partial<MarketInsightFilters>) => void;
  resetFilters: () => void;
  runMarketInsight: (
    request: MarketInsightToolRequest,
    signal?: AbortSignal,
  ) => Promise<MarketInsightToolResponse>;
  clearMarketInsight: () => void;
  resetMarketInsight: () => void;
}

export const initialMarketInsightState = {
  lastRequest: null,
  lastResponse: null,
  filters: defaultMarketInsightFilters,
  runs: [],
  isLoading: false,
  error: null,
};

export const useMarketInsightStore = create<MarketInsightState>((set) => ({
  ...initialMarketInsightState,
  setFilters: (filters) =>
    set((state) => ({
      filters: {
        ...state.filters,
        ...filters,
      },
    })),
  resetFilters: () => set({ filters: defaultMarketInsightFilters }),
  runMarketInsight: async (request, signal) => {
    set({ lastRequest: request, isLoading: true, error: null });
    try {
      const result = await runMarketInsightService(request, signal);
      const key = runKey(request);
      const record: MarketInsightRunRecord = {
        key,
        request,
        response: result.data,
        createdAt: new Date().toISOString(),
      };

      set((state) => ({
        lastResponse: result.data,
        runs: [...state.runs.filter((item) => item.key !== key), record].slice(-8),
        isLoading: false,
        error: null,
      }));
      return result.data;
    } catch (error) {
      const mapped = toError(error);
      set({ isLoading: false, error: mapped });
      throw mapped;
    }
  },
  clearMarketInsight: () => set({ lastRequest: null, lastResponse: null, runs: [], error: null }),
  resetMarketInsight: () => set(initialMarketInsightState),
}));
