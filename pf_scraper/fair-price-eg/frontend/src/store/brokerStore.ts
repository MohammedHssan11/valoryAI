import { create } from "zustand";
import type { RentFairPriceData } from "@/types/valuation";
import type { BrokerOrchestrationResponse, BrokerStageEvent } from "@/types/broker";

export interface BrokerSessionContext {
  events: BrokerStageEvent[];
  response: BrokerOrchestrationResponse | null;
  partialNarration: string;
  message: string;
}

interface BrokerState {
  activeValuation: RentFairPriceData | null;
  reasoningMode: "idle" | "valuation_context";
  setActiveValuation: (valuation: RentFairPriceData | null) => void;
  brokerContext: BrokerSessionContext | null;
  setBrokerContext: (context: BrokerSessionContext | null) => void;
}

export const useBrokerStore = create<BrokerState>((set) => ({
  activeValuation: null,
  reasoningMode: "idle",
  brokerContext: null,
  setActiveValuation: (activeValuation) =>
    set({
      activeValuation,
      reasoningMode: activeValuation ? "valuation_context" : "idle",
      brokerContext: null,
    }),
  setBrokerContext: (brokerContext) => set({ brokerContext }),
}));
