import { create } from "zustand";
import { runInvestmentAnalysis as runInvestmentAnalysisService } from "@/services/investmentService";
import type {
  InvestmentRunContext,
  InvestmentRunRecord,
  InvestmentToolRequest,
  InvestmentToolResponse,
} from "@/types/investment";

function toError(error: unknown): Error {
  if (error instanceof Error) return error;
  return new Error("Unable to run investment intelligence.");
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

function runKey(request: InvestmentToolRequest, context?: InvestmentRunContext): string {
  return JSON.stringify({
    target: context?.target ?? "base",
    label: context?.label ?? "Base valuation",
    scenario_id: request.scenario_id ?? null,
    asking_price_egp: request.asking_price_egp,
    what_if_modifications: stableComparableValue(request.what_if_modifications ?? null),
  });
}

interface InvestmentState {
  lastRequest: InvestmentToolRequest | null;
  lastResponse: InvestmentToolResponse | null;
  runs: InvestmentRunRecord[];
  isLoading: boolean;
  error: Error | null;
  selectedScenarioId: number | null;
  selectedScenarioName: string | null;
  runInvestmentAnalysis: (
    request: InvestmentToolRequest,
    context?: InvestmentRunContext,
    signal?: AbortSignal,
  ) => Promise<InvestmentToolResponse>;
  clearInvestment: () => void;
  resetInvestment: () => void;
  selectScenario: (scenarioId: number | null, scenarioName?: string | null) => void;
}

export const initialInvestmentState = {
  lastRequest: null,
  lastResponse: null,
  runs: [],
  isLoading: false,
  error: null,
  selectedScenarioId: null,
  selectedScenarioName: null,
};

export const useInvestmentStore = create<InvestmentState>((set) => ({
  ...initialInvestmentState,
  runInvestmentAnalysis: async (request, context, signal) => {
    set({
      lastRequest: request,
      isLoading: true,
      error: null,
      selectedScenarioId: context?.scenarioId ?? request.scenario_id ?? null,
      selectedScenarioName: context?.label ?? null,
    });
    try {
      const result = await runInvestmentAnalysisService(request, signal);
      const key = runKey(request, context);
      const record: InvestmentRunRecord = {
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
  clearInvestment: () => set({ lastRequest: null, lastResponse: null, runs: [], error: null }),
  resetInvestment: () => set(initialInvestmentState),
  selectScenario: (scenarioId, scenarioName = null) =>
    set({ selectedScenarioId: scenarioId, selectedScenarioName: scenarioName }),
}));
