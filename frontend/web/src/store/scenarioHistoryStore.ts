import { create } from "zustand";
import {
  createScenario,
  getScenarioLineage,
  getScenarioTree,
  listPropertyScenarios,
  restoreScenario as restoreScenarioRequest,
} from "@/services/scenarioHistoryService";
import { usePropertyContextStore } from "@/store/propertyContextStore";
import type { ScenarioState, ScenarioStateCreate, ScenarioTreeNode } from "@/types/scenarioHistory";

function toError(error: unknown): Error {
  if (error instanceof Error) return error;
  return new Error("Unable to load scenario history.");
}

function syncActiveScenarioContext(scenario: ScenarioState): void {
  usePropertyContextStore.getState().setActivePropertyContext({
    activeWorkspaceId: scenario.workspace_id,
    activePropertyId: scenario.property_state_id,
    activeScenarioId: scenario.id,
  });
}

function clearActiveScenarioContext(): void {
  const context = usePropertyContextStore.getState();
  if (typeof context.activeWorkspaceId !== "number" || typeof context.activePropertyId !== "number") return;
  context.setActivePropertyContext({
    activeWorkspaceId: context.activeWorkspaceId,
    activePropertyId: context.activePropertyId,
    activeScenarioId: null,
  });
}

interface ScenarioHistoryState {
  scenarios: ScenarioState[];
  tree: ScenarioTreeNode[];
  selectedScenario: ScenarioState | null;
  selectedLineage: ScenarioState[];
  comparedScenarioIds: number[];
  isComparisonOpen: boolean;
  isLoading: boolean;
  isSaving: boolean;
  isRestoring: boolean;
  error: Error | null;
  loadHistory: (propertyId: number, signal?: AbortSignal) => Promise<void>;
  saveScenario: (request: ScenarioStateCreate, signal?: AbortSignal) => Promise<ScenarioState>;
  selectScenario: (scenario: ScenarioState | null, signal?: AbortSignal) => Promise<ScenarioState[]>;
  restoreScenario: (scenarioId: number, signal?: AbortSignal) => Promise<ScenarioState>;
  toggleComparedScenario: (scenarioId: number) => void;
  clearComparison: () => void;
  openComparison: () => void;
  closeComparison: () => void;
  reset: () => void;
}

export const initialScenarioHistoryState = {
  scenarios: [],
  tree: [],
  selectedScenario: null,
  selectedLineage: [],
  comparedScenarioIds: [],
  isComparisonOpen: false,
  isLoading: false,
  isSaving: false,
  isRestoring: false,
  error: null,
};

export const useScenarioHistoryStore = create<ScenarioHistoryState>((set, get) => ({
  ...initialScenarioHistoryState,
  loadHistory: async (propertyId, signal) => {
    set({ isLoading: true, error: null });
    try {
      const [scenarios, tree] = await Promise.all([
        listPropertyScenarios(propertyId, signal),
        getScenarioTree(propertyId, signal),
      ]);
      const knownIds = new Set(scenarios.map((scenario) => scenario.id));
      const selectedScenario = get().selectedScenario;
      const retainedScenario = selectedScenario && knownIds.has(selectedScenario.id) ? selectedScenario : null;
      if (retainedScenario) {
        syncActiveScenarioContext(retainedScenario);
      }
      set({
        scenarios,
        tree,
        selectedScenario: retainedScenario,
        selectedLineage: retainedScenario ? get().selectedLineage : [],
        comparedScenarioIds: get().comparedScenarioIds.filter((id) => knownIds.has(id)),
        isLoading: false,
        error: null,
      });
    } catch (error) {
      set({ isLoading: false, error: toError(error) });
      throw error;
    }
  },
  saveScenario: async (request, signal) => {
    set({ isSaving: true, error: null });
    try {
      const scenario = await createScenario(request, signal);
      const [scenarios, tree, selectedLineage] = await Promise.all([
        listPropertyScenarios(request.property_state_id, signal),
        getScenarioTree(request.property_state_id, signal),
        getScenarioLineage(scenario.id, signal),
      ]);
      syncActiveScenarioContext(scenario);
      set({
        scenarios,
        tree,
        selectedScenario: scenario,
        selectedLineage,
        comparedScenarioIds: Array.from(new Set([...get().comparedScenarioIds, scenario.id])).slice(-3),
        isSaving: false,
        error: null,
      });
      return scenario;
    } catch (error) {
      set({ isSaving: false, error: toError(error) });
      throw error;
    }
  },
  selectScenario: async (scenario, signal) => {
    if (scenario === null) {
      clearActiveScenarioContext();
      set({ selectedScenario: null, selectedLineage: [], error: null });
      return [];
    }
    set({ isLoading: true, error: null });
    try {
      const selectedLineage = await getScenarioLineage(scenario.id, signal);
      const latest = selectedLineage[selectedLineage.length - 1] ?? scenario;
      syncActiveScenarioContext(latest);
      set({ selectedScenario: latest, selectedLineage, isLoading: false, error: null });
      return selectedLineage;
    } catch (error) {
      set({ isLoading: false, error: toError(error) });
      throw error;
    }
  },
  restoreScenario: async (scenarioId, signal) => {
    set({ isRestoring: true, error: null });
    try {
      const scenario = await restoreScenarioRequest(scenarioId, signal);
      const [scenarios, tree, selectedLineage] = await Promise.all([
        listPropertyScenarios(scenario.property_state_id, signal),
        getScenarioTree(scenario.property_state_id, signal),
        getScenarioLineage(scenario.id, signal),
      ]);
      syncActiveScenarioContext(scenario);
      set({
        scenarios,
        tree,
        selectedScenario: scenario,
        selectedLineage,
        isRestoring: false,
        error: null,
      });
      return scenario;
    } catch (error) {
      set({ isRestoring: false, error: toError(error) });
      throw error;
    }
  },
  toggleComparedScenario: (scenarioId) =>
    set((state) => {
      const exists = state.comparedScenarioIds.includes(scenarioId);
      return {
        comparedScenarioIds: exists
          ? state.comparedScenarioIds.filter((id) => id !== scenarioId)
          : [...state.comparedScenarioIds, scenarioId].slice(-3),
      };
    }),
  clearComparison: () => set({ comparedScenarioIds: [], isComparisonOpen: false }),
  openComparison: () => set({ isComparisonOpen: true }),
  closeComparison: () => set({ isComparisonOpen: false }),
  reset: () => set(initialScenarioHistoryState),
}));
