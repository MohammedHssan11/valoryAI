import { create } from "zustand";
import type { NavTab } from "@/navigation/tabs";

interface NavigationState {
  currentTab: NavTab;
  setTab: (tab: NavTab) => void;
}

export const useNavigationStore = create<NavigationState>((set) => ({
  currentTab: "nexus",
  setTab: (tab) => set({ currentTab: tab }),
}));

export function useNavigation() {
  return useNavigationStore();
}

