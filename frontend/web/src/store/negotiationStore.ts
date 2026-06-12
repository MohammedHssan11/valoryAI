import { create } from "zustand";
import { runNegotiationAnalysis } from "@/services/negotiationService";
import type {
  NegotiationRunContext,
  NegotiationRunRecord,
  NegotiationToolRequest,
  NegotiationToolResponse,
} from "@/types/negotiation";

function toError(error: unknown): Error {
  if (error instanceof Error) return error;
  return new Error("Unable to run negotiation intelligence.");
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

function runKey(request: NegotiationToolRequest, context?: NegotiationRunContext): string {
  return JSON.stringify({
    target: context?.target ?? "base",
    scenario_id: request.scenario_id ?? null,
    asking_price_egp: request.asking_price_egp,
    what_if_modifications: stableComparableValue(request.what_if_modifications ?? null),
  });
}

interface NegotiationState {
  lastRequest: NegotiationToolRequest | null;
  lastResponse: NegotiationToolResponse | null;
  runs: NegotiationRunRecord[];
  isLoading: boolean;
  error: Error | null;
  runNegotiation: (
    request: NegotiationToolRequest,
    context?: NegotiationRunContext,
    signal?: AbortSignal,
  ) => Promise<NegotiationToolResponse>;
  clearResults: () => void;
  reset: () => void;
}

export const initialNegotiationState = {
  lastRequest: null,
  lastResponse: null,
  runs: [],
  isLoading: false,
  error: null,
};

export const useNegotiationStore = create<NegotiationState>((set) => ({
  ...initialNegotiationState,
  runNegotiation: async (request, context, signal) => {
    set({ lastRequest: request, isLoading: true, error: null });
    try {
      const result = await runNegotiationAnalysis(request, signal);
      const key = runKey(request, context);
      const record: NegotiationRunRecord = {
        key,
        target: context?.target ?? "base",
        label: context?.label ?? "Base valuation",
        scenarioId: context?.scenarioId ?? request.scenario_id ?? null,
        request,
        response: result.data,
        createdAt: new Date().toISOString(),
      };

      set((state) => ({
        lastResponse: result.data,
        runs: [...state.runs.filter((item) => item.key !== key), record].slice(-6),
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
  clearResults: () => set({ lastRequest: null, lastResponse: null, runs: [], error: null }),
  reset: () => set(initialNegotiationState),
}));
