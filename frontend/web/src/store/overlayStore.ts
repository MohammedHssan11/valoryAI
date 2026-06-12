import { create } from "zustand";

type OverlayId = "confidence" | "comparable" | "explainability" | null;

interface OverlayState {
  activeOverlay: OverlayId;
  openOverlay: (overlay: Exclude<OverlayId, null>) => void;
  closeOverlay: () => void;
}

export const useOverlayStore = create<OverlayState>((set) => ({
  activeOverlay: null,
  openOverlay: (activeOverlay) => set({ activeOverlay }),
  closeOverlay: () => set({ activeOverlay: null }),
}));

