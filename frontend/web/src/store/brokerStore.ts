import { create } from "zustand";
import { ValorApiError } from "@/api/contracts";
import { createScenario } from "@/services/scenarioHistoryService";
import { usePropertyContextStore } from "@/store/propertyContextStore";
import { useScenarioHistoryStore } from "@/store/scenarioHistoryStore";
import type { ScenarioState } from "@/types/scenarioHistory";
import type { RentFairPriceData } from "@/types/valuation";
import type { BrokerOrchestrationResponse, BrokerStageEvent } from "@/types/broker";

export type BrokerScenarioSource = "active_scenario" | "selected_scenario" | "history_base_scenario" | "created_base_scenario";

export interface BrokerExecutionContext {
  workspaceId: number;
  propertyId: number;
  scenarioId: number;
  scenarioSource: BrokerScenarioSource;
}

export interface BrokerSessionContext {
  events: BrokerStageEvent[];
  response: BrokerOrchestrationResponse | null;
  partialNarration: string;
  message: string;
}

function invalidBrokerContext(message: string, field?: string): ValorApiError {
  return new ValorApiError({
    code: "INVALID_BROKER_CONTEXT",
    message,
    details: field ? [{ code: "INVALID_BROKER_CONTEXT", message, field }] : [],
  });
}

function positiveInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isInteger(value) && value > 0 ? value : null;
}

function scenarioMatchesContext(
  scenario: ScenarioState | null,
  workspaceId: number,
  propertyId: number,
): scenario is ScenarioState {
  return Boolean(
    scenario &&
      scenario.workspace_id === workspaceId &&
      scenario.property_state_id === propertyId &&
      positiveInteger(scenario.id),
  );
}

function rememberScenario(scenario: ScenarioState): void {
  usePropertyContextStore.getState().setActivePropertyContext({
    activeWorkspaceId: scenario.workspace_id,
    activePropertyId: scenario.property_state_id,
    activeScenarioId: scenario.id,
  });

  useScenarioHistoryStore.setState((state) => ({
    scenarios: state.scenarios.some((item) => item.id === scenario.id) ? state.scenarios : [...state.scenarios, scenario],
    selectedScenario: scenario,
    selectedLineage: [scenario],
  }));
}

function existingBaseScenario(workspaceId: number, propertyId: number): ScenarioState | null {
  return (
    useScenarioHistoryStore
      .getState()
      .scenarios.find(
        (scenario) =>
          scenario.workspace_id === workspaceId &&
          scenario.property_state_id === propertyId &&
          scenario.parent_scenario_id === null &&
          Object.keys(scenario.modifications).length === 0,
      ) ?? null
  );
}

async function createBaseScenario(propertyId: number, signal?: AbortSignal): Promise<ScenarioState> {
  return createScenario(
    {
      property_state_id: propertyId,
      parent_scenario_id: null,
      name: "Base valuation",
      modifications: {},
      delta_value: null,
    },
    signal,
  );
}

export async function resolveBrokerExecutionContext(signal?: AbortSignal): Promise<BrokerExecutionContext> {
  const propertyContext = usePropertyContextStore.getState();
  const selectedScenario = useScenarioHistoryStore.getState().selectedScenario;
  const selectedWorkspaceId = positiveInteger(selectedScenario?.workspace_id);
  const selectedPropertyId = positiveInteger(selectedScenario?.property_state_id);
  const workspaceId = positiveInteger(propertyContext.activeWorkspaceId) ?? selectedWorkspaceId;
  const propertyId = positiveInteger(propertyContext.activePropertyId) ?? selectedPropertyId;

  if (workspaceId === null) {
    throw invalidBrokerContext("Run a valuation first so Broker has an active workspace.", "workspace_id");
  }
  if (propertyId === null) {
    throw invalidBrokerContext("Run a valuation first so Broker has an active property context.", "property_id");
  }

  const activeScenarioId = positiveInteger(propertyContext.activeScenarioId);
  if (activeScenarioId !== null) {
    return {
      workspaceId,
      propertyId,
      scenarioId: activeScenarioId,
      scenarioSource: "active_scenario",
    };
  }

  if (scenarioMatchesContext(selectedScenario, workspaceId, propertyId)) {
    rememberScenario(selectedScenario);
    return {
      workspaceId,
      propertyId,
      scenarioId: selectedScenario.id,
      scenarioSource: "selected_scenario",
    };
  }

  const historyBaseScenario = existingBaseScenario(workspaceId, propertyId);
  if (historyBaseScenario) {
    rememberScenario(historyBaseScenario);
    return {
      workspaceId,
      propertyId,
      scenarioId: historyBaseScenario.id,
      scenarioSource: "history_base_scenario",
    };
  }

  const scenario = await createBaseScenario(propertyId, signal);
  if (scenario.workspace_id !== workspaceId || scenario.property_state_id !== propertyId) {
    throw invalidBrokerContext("The created Broker scenario did not match the active property context.", "scenario_id");
  }

  rememberScenario(scenario);
  return {
    workspaceId,
    propertyId,
    scenarioId: scenario.id,
    scenarioSource: "created_base_scenario",
  };
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
