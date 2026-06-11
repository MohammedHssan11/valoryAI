import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

export type PropertyContextBridgeStatus = "idle" | "binding" | "ready" | "error";

export interface ActivePropertyContextIds {
  activeWorkspaceId: number;
  activePropertyId: number;
  activeScenarioId?: number | null;
  requestId?: string;
}

interface PropertyContextState {
  activeWorkspaceId: number | null;
  activePropertyId: number | null;
  activeScenarioId: number | null;
  bridgeStatus: PropertyContextBridgeStatus;
  lastBridgeRequestId?: string;
  lastBridgeError?: string;
  lastBoundAt?: number;
  setBridgePending: (requestId?: string) => void;
  setBridgeError: (message: string, requestId?: string) => void;
  setActivePropertyContext: (context: ActivePropertyContextIds) => void;
  clearActivePropertyContext: () => void;
}

export const usePropertyContextStore = create<PropertyContextState>()(
  persist(
    (set) => ({
      activeWorkspaceId: null,
      activePropertyId: null,
      activeScenarioId: null,
      bridgeStatus: "idle",
      lastBridgeRequestId: undefined,
      lastBridgeError: undefined,
      lastBoundAt: undefined,
      setBridgePending: (requestId) =>
        set({
          bridgeStatus: "binding",
          lastBridgeRequestId: requestId,
          lastBridgeError: undefined,
        }),
      setBridgeError: (message, requestId) =>
        set({
          bridgeStatus: "error",
          lastBridgeRequestId: requestId,
          lastBridgeError: message,
        }),
      setActivePropertyContext: (context) =>
        set({
          activeWorkspaceId: context.activeWorkspaceId,
          activePropertyId: context.activePropertyId,
          activeScenarioId: context.activeScenarioId ?? null,
          bridgeStatus: "ready",
          lastBridgeRequestId: context.requestId,
          lastBridgeError: undefined,
          lastBoundAt: Date.now(),
        }),
      clearActivePropertyContext: () =>
        set({
          activeWorkspaceId: null,
          activePropertyId: null,
          activeScenarioId: null,
          bridgeStatus: "idle",
          lastBridgeRequestId: undefined,
          lastBridgeError: undefined,
          lastBoundAt: undefined,
        }),
    }),
    {
      name: "valorai-property-context",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        activeWorkspaceId: state.activeWorkspaceId,
        activePropertyId: state.activePropertyId,
        activeScenarioId: state.activeScenarioId,
        bridgeStatus: state.bridgeStatus === "ready" ? state.bridgeStatus : "idle",
        lastBridgeRequestId: state.lastBridgeRequestId,
        lastBoundAt: state.lastBoundAt,
      }),
    },
  ),
);
