import { create } from "zustand";
import type { ComparableItem } from "@/types/valuation";

interface ComparableAnalysisState {
  selectedComparable: ComparableItem | null;
  setSelectedComparable: (comparable: ComparableItem | null) => void;
}

export const useComparableAnalysisStore = create<ComparableAnalysisState>((set) => ({
  selectedComparable: null,
  setSelectedComparable: (selectedComparable) => set({ selectedComparable }),
}));

