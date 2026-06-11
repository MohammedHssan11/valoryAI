import { beforeEach, describe, expect, it, vi } from "vitest";
import { createScenario } from "@/services/scenarioHistoryService";
import type { ScenarioState } from "@/types/scenarioHistory";
import { resolveBrokerExecutionContext } from "./brokerStore";
import { usePropertyContextStore } from "./propertyContextStore";
import { initialScenarioHistoryState, useScenarioHistoryStore } from "./scenarioHistoryStore";

vi.mock("@/services/scenarioHistoryService", () => ({
  createScenario: vi.fn(),
}));

const createScenarioMock = vi.mocked(createScenario);

const baseScenario: ScenarioState = {
  id: 33,
  workspace_id: 11,
  property_state_id: 22,
  parent_scenario_id: null,
  name: "Base valuation",
  modifications: {},
  delta_value: null,
};

describe("broker store context resolver", () => {
  beforeEach(() => {
    localStorage.clear();
    createScenarioMock.mockReset();
    usePropertyContextStore.getState().clearActivePropertyContext();
    useScenarioHistoryStore.setState(initialScenarioHistoryState);
  });

  it("uses the active workspace and scenario when both are already bound", async () => {
    usePropertyContextStore.getState().setActivePropertyContext({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: 33,
    });

    const context = await resolveBrokerExecutionContext();

    expect(context).toEqual({
      workspaceId: 11,
      propertyId: 22,
      scenarioId: 33,
      scenarioSource: "active_scenario",
    });
    expect(createScenarioMock).not.toHaveBeenCalled();
  });

  it("promotes a selected scenario into active Broker context", async () => {
    usePropertyContextStore.getState().setActivePropertyContext({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: null,
    });
    useScenarioHistoryStore.setState({ selectedScenario: baseScenario });

    const context = await resolveBrokerExecutionContext();

    expect(context.scenarioId).toBe(33);
    expect(context.scenarioSource).toBe("selected_scenario");
    expect(usePropertyContextStore.getState().activeScenarioId).toBe(33);
    expect(createScenarioMock).not.toHaveBeenCalled();
  });

  it("creates a baseline scenario when no active scenario exists", async () => {
    createScenarioMock.mockResolvedValueOnce(baseScenario);
    usePropertyContextStore.getState().setActivePropertyContext({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: null,
    });

    const context = await resolveBrokerExecutionContext();

    expect(createScenarioMock).toHaveBeenCalledWith(
      {
        property_state_id: 22,
        parent_scenario_id: null,
        name: "Base valuation",
        modifications: {},
        delta_value: null,
      },
      undefined,
    );
    expect(context).toEqual({
      workspaceId: 11,
      propertyId: 22,
      scenarioId: 33,
      scenarioSource: "created_base_scenario",
    });
    expect(usePropertyContextStore.getState().activeScenarioId).toBe(33);
    expect(useScenarioHistoryStore.getState().selectedScenario?.id).toBe(33);
  });

  it("reuses an existing baseline scenario before creating a duplicate", async () => {
    usePropertyContextStore.getState().setActivePropertyContext({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: null,
    });
    useScenarioHistoryStore.setState({ scenarios: [baseScenario], selectedScenario: null, selectedLineage: [] });

    const context = await resolveBrokerExecutionContext();

    expect(context.scenarioId).toBe(33);
    expect(context.scenarioSource).toBe("history_base_scenario");
    expect(createScenarioMock).not.toHaveBeenCalled();
  });

  it("rejects a created baseline scenario when the backend returns mismatched context", async () => {
    createScenarioMock.mockResolvedValueOnce({ ...baseScenario, workspace_id: 99 });
    usePropertyContextStore.getState().setActivePropertyContext({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: null,
    });

    await expect(resolveBrokerExecutionContext()).rejects.toMatchObject({
      code: "INVALID_BROKER_CONTEXT",
      details: [expect.objectContaining({ field: "scenario_id" })],
    });
  });

  it("fails before calling the backend when workspace context is missing", async () => {
    await expect(resolveBrokerExecutionContext()).rejects.toMatchObject({
      code: "INVALID_BROKER_CONTEXT",
      details: [expect.objectContaining({ field: "workspace_id" })],
    });
    expect(createScenarioMock).not.toHaveBeenCalled();
  });
});
