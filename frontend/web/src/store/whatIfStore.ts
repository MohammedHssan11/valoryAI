import { create } from "zustand";
import { runWhatIfAnalysis } from "@/services/whatIfService";
import type { WhatIfToolRequest, WhatIfToolResponse } from "@/types/whatIf";

function toError(error: unknown): Error {
  if (error instanceof Error) return error;
  return new Error("Unable to run what-if scenario.");
}

interface WhatIfState {
  lastRequest: WhatIfToolRequest | null;
  lastResponse: WhatIfToolResponse | null;
  isLoading: boolean;
  error: Error | null;
  runScenario: (request: WhatIfToolRequest, signal?: AbortSignal) => Promise<WhatIfToolResponse>;
  clearScenario: () => void;
  reset: () => void;
}

export const initialWhatIfState = {
  lastRequest: null,
  lastResponse: null,
  isLoading: false,
  error: null,
};

export const useWhatIfStore = create<WhatIfState>((set) => ({
  ...initialWhatIfState,
  runScenario: async (request, signal) => {
    set({ lastRequest: request, isLoading: true, error: null });
    try {
      const result = await runWhatIfAnalysis(request, signal);
      set({ lastResponse: result.data, isLoading: false, error: null });
      return result.data;
    } catch (error) {
      const mapped = toError(error);
      set({ isLoading: false, error: mapped });
      throw mapped;
    }
  },
  clearScenario: () => set({ lastRequest: null, lastResponse: null, error: null }),
  reset: () => set(initialWhatIfState),
}));
