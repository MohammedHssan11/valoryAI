import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  createScenario,
  getScenarioLineage,
  getScenarioTree,
  listPropertyScenarios,
  restoreScenario,
} from "@/services/scenarioHistoryService";
import type { ScenarioState, ScenarioTreeNode } from "@/types/scenarioHistory";
import { usePropertyContextStore } from "./propertyContextStore";
import { initialScenarioHistoryState, useScenarioHistoryStore } from "./scenarioHistoryStore";

vi.mock("@/services/scenarioHistoryService", () => ({
  listPropertyScenarios: vi.fn(),
  getScenarioTree: vi.fn(),
  getScenarioLineage: vi.fn(),
  createScenario: vi.fn(),
  restoreScenario: vi.fn(),
}));

const listMock = vi.mocked(listPropertyScenarios);
const treeMock = vi.mocked(getScenarioTree);
const lineageMock = vi.mocked(getScenarioLineage);
const createMock = vi.mocked(createScenario);
const restoreMock = vi.mocked(restoreScenario);

const scenarioA: ScenarioState = {
  id: 7,
  workspace_id: 11,
  property_state_id: 22,
  parent_scenario_id: null,
  name: "Scenario A",
  modifications: { size_sqm: 180 },
  delta_value: 18000,
};

const scenarioB: ScenarioState = {
  ...scenarioA,
  id: 8,
  parent_scenario_id: 7,
  name: "Scenario B",
  modifications: { bathrooms: 3 },
  delta_value: 4000,
};

const tree: ScenarioTreeNode[] = [{ ...scenarioA, children: [{ ...scenarioB, children: [] }] }];

describe("scenario history store", () => {
  beforeEach(() => {
    localStorage.clear();
    listMock.mockReset();
    treeMock.mockReset();
    lineageMock.mockReset();
    createMock.mockReset();
    restoreMock.mockReset();
    usePropertyContextStore.getState().clearActivePropertyContext();
    useScenarioHistoryStore.setState(initialScenarioHistoryState);
  });

  it("loads scenarios and lineage trees for a property", async () => {
    listMock.mockResolvedValueOnce([scenarioA, scenarioB]);
    treeMock.mockResolvedValueOnce(tree);

    await useScenarioHistoryStore.getState().loadHistory(22);

    expect(listMock).toHaveBeenCalledWith(22, undefined);
    expect(treeMock).toHaveBeenCalledWith(22, undefined);
    expect(useScenarioHistoryStore.getState().scenarios).toHaveLength(2);
    expect(useScenarioHistoryStore.getState().tree[0].children[0].id).toBe(8);
  });

  it("saves a scenario and selects its returned lineage", async () => {
    createMock.mockResolvedValueOnce(scenarioB);
    listMock.mockResolvedValueOnce([scenarioA, scenarioB]);
    treeMock.mockResolvedValueOnce(tree);
    lineageMock.mockResolvedValueOnce([scenarioA, scenarioB]);

    const saved = await useScenarioHistoryStore.getState().saveScenario({
      property_state_id: 22,
      parent_scenario_id: 7,
      name: "Scenario B",
      modifications: { bathrooms: 3 },
      delta_value: 4000,
    });

    expect(saved.id).toBe(8);
    expect(useScenarioHistoryStore.getState().selectedScenario?.id).toBe(8);
    expect(useScenarioHistoryStore.getState().selectedLineage.map((scenario) => scenario.id)).toEqual([7, 8]);
    expect(useScenarioHistoryStore.getState().comparedScenarioIds).toEqual([8]);
    expect(usePropertyContextStore.getState().activeWorkspaceId).toBe(11);
    expect(usePropertyContextStore.getState().activePropertyId).toBe(22);
    expect(usePropertyContextStore.getState().activeScenarioId).toBe(8);
  });

  it("restores and compares scenarios", async () => {
    restoreMock.mockResolvedValueOnce(scenarioA);
    listMock.mockResolvedValueOnce([scenarioA]);
    treeMock.mockResolvedValueOnce([{ ...scenarioA, children: [] }]);
    lineageMock.mockResolvedValueOnce([scenarioA]);

    await useScenarioHistoryStore.getState().restoreScenario(7);
    useScenarioHistoryStore.getState().toggleComparedScenario(7);
    useScenarioHistoryStore.getState().openComparison();

    expect(restoreMock).toHaveBeenCalledWith(7, undefined);
    expect(useScenarioHistoryStore.getState().selectedScenario?.id).toBe(7);
    expect(usePropertyContextStore.getState().activeScenarioId).toBe(7);
    expect(useScenarioHistoryStore.getState().comparedScenarioIds).toEqual([7]);
    expect(useScenarioHistoryStore.getState().isComparisonOpen).toBe(true);
  });

  it("clears active scenario context when scenario selection is cleared", async () => {
    usePropertyContextStore.getState().setActivePropertyContext({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: 7,
    });
    useScenarioHistoryStore.setState({ selectedScenario: scenarioA, selectedLineage: [scenarioA] });

    const lineage = await useScenarioHistoryStore.getState().selectScenario(null);

    expect(lineage).toEqual([]);
    expect(useScenarioHistoryStore.getState().selectedScenario).toBeNull();
    expect(usePropertyContextStore.getState().activeWorkspaceId).toBe(11);
    expect(usePropertyContextStore.getState().activePropertyId).toBe(22);
    expect(usePropertyContextStore.getState().activeScenarioId).toBeNull();
  });
});
