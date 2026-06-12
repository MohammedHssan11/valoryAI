import { create } from "zustand";
import type { OrbState } from "@/components/intelligence/AiOrb";

interface AiContinuityEvent {
  at: number;
  label: string;
}

interface AiContinuityState {
  orbState: OrbState;
  timeline: AiContinuityEvent[];
  setOrbState: (state: OrbState) => void;
  pushEvent: (label: string) => void;
}

export const useAiContinuityStore = create<AiContinuityState>((set) => ({
  orbState: "idle",
  timeline: [],
  setOrbState: (orbState) => set({ orbState }),
  pushEvent: (label) =>
    set((state) => ({
      timeline: [{ at: Date.now(), label }, ...state.timeline].slice(0, 20),
    })),
}));

