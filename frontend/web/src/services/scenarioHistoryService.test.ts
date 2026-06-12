import { beforeEach, describe, expect, it, vi } from "vitest";
import { http } from "@/api/http";
import { SCENARIO_HISTORY_META_KEY } from "@/types/scenarioHistory";
import {
  createScenario,
  getScenarioLineage,
  getScenarioTree,
  listPropertyScenarios,
  restoreScenario,
} from "./scenarioHistoryService";

vi.mock("@/api/http", () => ({
  http: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
  },
}));

const getMock = vi.mocked(http.get);
const postMock = vi.mocked(http.post);

const scenarioPayload = {
  id: 7,
  created_at: "2026-06-09T09:00:00Z",
  updated_at: "2026-06-09T09:00:00Z",
  version: 1,
  is_deleted: false,
  deleted_at: null,
  user_id: 3,
  workspace_id: 11,
  property_state_id: 22,
  parent_scenario_id: null,
  name: "Scenario A",
  modifications: {
    size_sqm: 180,
    [SCENARIO_HISTORY_META_KEY]: {
      signed_delta_value: -5000,
    },
  },
  delta_value: "5000",
};

describe("scenario history service", () => {
  beforeEach(() => {
    getMock.mockReset();
    postMock.mockReset();
  });

  it("loads property scenarios and normalizes decimal fields", async () => {
    getMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: [scenarioPayload],
        meta: { request_id: "scenario-req-1" },
      },
    });

    const scenarios = await listPropertyScenarios(22);

    expect(getMock).toHaveBeenCalledWith("/v1/copilot/properties/22/scenarios", { signal: undefined });
    expect(scenarios[0].delta_value).toBe(5000);
    expect(scenarios[0].modifications[SCENARIO_HISTORY_META_KEY]).toEqual({ signed_delta_value: -5000 });
  });

  it("creates scenario states with a compact backend payload", async () => {
    postMock.mockResolvedValueOnce({ data: scenarioPayload });

    const scenario = await createScenario({
      property_state_id: 22,
      name: " Scenario A ",
      modifications: { size_sqm: 180, view_type: undefined },
    });

    expect(postMock).toHaveBeenCalledWith(
      "/v1/copilot/scenarios",
      {
        property_state_id: 22,
        parent_scenario_id: null,
        name: "Scenario A",
        modifications: { size_sqm: 180 },
        delta_value: null,
      },
      { signal: undefined },
    );
    expect(scenario.id).toBe(7);
  });

  it("loads lineage and recursive scenario trees", async () => {
    getMock.mockResolvedValueOnce({ data: [scenarioPayload] });
    getMock.mockResolvedValueOnce({
      data: [
        {
          ...scenarioPayload,
          children: [{ ...scenarioPayload, id: 8, parent_scenario_id: 7, name: "Scenario B", children: [] }],
        },
      ],
    });

    const lineage = await getScenarioLineage(7);
    const tree = await getScenarioTree(22);

    expect(lineage[0].name).toBe("Scenario A");
    expect(tree[0].children[0].parent_scenario_id).toBe(7);
  });

  it("restores scenario states through the backend restore endpoint", async () => {
    postMock.mockResolvedValueOnce({ data: scenarioPayload });

    const restored = await restoreScenario(7);

    expect(postMock).toHaveBeenCalledWith("/v1/copilot/scenarios/7/restore", {}, { signal: undefined });
    expect(restored.name).toBe("Scenario A");
  });
});
