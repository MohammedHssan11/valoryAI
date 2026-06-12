import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { runWhatIfAnalysis } from "@/services/whatIfService";
import { sampleRequest, sampleValuation, sampleWhatIfResponse } from "@/test/fixtures";
import {
  createScenario,
  getScenarioLineage,
  getScenarioTree,
  listPropertyScenarios,
  restoreScenario,
} from "@/services/scenarioHistoryService";
import { initialScenarioHistoryState, useScenarioHistoryStore } from "@/store/scenarioHistoryStore";
import { initialWhatIfState, useWhatIfStore } from "@/store/whatIfStore";
import { SCENARIO_HISTORY_META_KEY, ScenarioState, ScenarioTreeNode } from "@/types/scenarioHistory";
import {
  FeatureChangesList,
  ScenarioAssumptions,
  ScenarioComparables,
  ScenarioExplainability,
  WhatIfScenarioPanel,
} from "./WhatIfScenarioPanel";

vi.mock("@/services/whatIfService", () => ({
  runWhatIfAnalysis: vi.fn(),
}));

vi.mock("@/services/scenarioHistoryService", () => ({
  listPropertyScenarios: vi.fn(),
  getScenarioTree: vi.fn(),
  getScenarioLineage: vi.fn(),
  createScenario: vi.fn(),
  restoreScenario: vi.fn(),
}));

const runMock = vi.mocked(runWhatIfAnalysis);
const listScenariosMock = vi.mocked(listPropertyScenarios);
const treeMock = vi.mocked(getScenarioTree);
const lineageMock = vi.mocked(getScenarioLineage);
const createScenarioMock = vi.mocked(createScenario);
const restoreScenarioMock = vi.mocked(restoreScenario);

const savedScenario: ScenarioState = {
  id: 7,
  workspace_id: 11,
  property_state_id: 22,
  parent_scenario_id: null,
  name: "Scenario A",
  modifications: {
    size_sqm: 180,
    [SCENARIO_HISTORY_META_KEY]: {
      scenario_valuation: 108000,
      signed_delta_value: 18000,
      delta_percentage: 20,
      confidence_level: "High",
      fairness_status: "Above Fair Value",
    },
  },
  delta_value: 18000,
  created_at: "2026-06-09T09:00:00Z",
};

const childScenario: ScenarioState = {
  ...savedScenario,
  id: 8,
  parent_scenario_id: 7,
  name: "Scenario B",
  modifications: {
    bathrooms: 3,
    [SCENARIO_HISTORY_META_KEY]: {
      scenario_valuation: 112000,
      signed_delta_value: 4000,
      delta_percentage: 3.7,
      confidence_level: "High",
      fairness_status: "Within Fair Value",
    },
  },
  delta_value: 4000,
};

const scenarioTree: ScenarioTreeNode[] = [{ ...savedScenario, children: [{ ...childScenario, children: [] }] }];

function renderPanel(context: { workspaceId: number | null; propertyId: number | null } = { workspaceId: 11, propertyId: 22 }) {
  return render(
    <WhatIfScenarioPanel
      baseRequest={sampleRequest}
      baseResult={sampleValuation}
      workspaceId={context.workspaceId}
      propertyId={context.propertyId}
      scenarioId={null}
      bridgeStatus="ready"
    />,
  );
}

describe("WhatIfScenarioPanel", () => {
  beforeEach(() => {
    runMock.mockReset();
    listScenariosMock.mockReset();
    treeMock.mockReset();
    lineageMock.mockReset();
    createScenarioMock.mockReset();
    restoreScenarioMock.mockReset();
    listScenariosMock.mockResolvedValue([]);
    treeMock.mockResolvedValue([]);
    lineageMock.mockResolvedValue([]);
    useWhatIfStore.setState(initialWhatIfState);
    useScenarioHistoryStore.setState(initialScenarioHistoryState);
  });

  it("keeps scenario execution disabled until backend property context exists", () => {
    renderPanel({ workspaceId: null, propertyId: null });

    fireEvent.click(screen.getByRole("button", { name: /what if/i }));

    expect(screen.getAllByText(/property context ready/i).length).toBeGreaterThan(0);
    expect(screen.getByRole("button", { name: /run scenario/i })).toBeDisabled();
  });

  it("renders the empty state before a scenario is run", () => {
    renderPanel();

    fireEvent.click(screen.getByRole("button", { name: /what if/i }));

    expect(screen.getByText(/no scenario has been executed/i)).toBeInTheDocument();
    expect(screen.getByText(/scenario modifications/i)).toBeInTheDocument();
  });

  it("runs a successful scenario and renders deltas, assumptions, explainability, and comparables", async () => {
    runMock.mockResolvedValueOnce({ data: sampleWhatIfResponse, meta: { request_id: "what-if-req-1" } });
    renderPanel();

    fireEvent.click(screen.getByRole("button", { name: /what if/i }));
    fireEvent.change(screen.getByLabelText(/scenario area/i), { target: { value: "180" } });
    fireEvent.click(screen.getByRole("button", { name: /run scenario/i }));

    await waitFor(() => expect(screen.getAllByText("EGP 108,000").length).toBeGreaterThan(0));

    expect(runMock).toHaveBeenCalledWith(
      expect.objectContaining({
        workspace_id: 11,
        property_id: 22,
        scenario_id: null,
        modifications: expect.objectContaining({ size_sqm: 180 }),
      }),
      expect.any(AbortSignal),
    );
    expect(screen.getByText("+EGP 18,000")).toBeInTheDocument();
    expect(screen.getByText("Parking = Unknown")).toBeInTheDocument();
    expect(screen.getByText(/scenario valuation increased/i)).toBeInTheDocument();
    expect(screen.getByText("scenario-comp-1")).toBeInTheDocument();
  });

  it("saves the last executed scenario to scenario history", async () => {
    runMock.mockResolvedValueOnce({ data: sampleWhatIfResponse, meta: { request_id: "what-if-req-1" } });
    createScenarioMock.mockResolvedValueOnce(savedScenario);
    listScenariosMock.mockResolvedValueOnce([]).mockResolvedValueOnce([savedScenario]);
    treeMock.mockResolvedValueOnce([]).mockResolvedValueOnce(scenarioTree);
    lineageMock.mockResolvedValueOnce([savedScenario]);
    renderPanel();

    fireEvent.click(screen.getByRole("button", { name: /what if/i }));
    fireEvent.change(screen.getByLabelText(/scenario area/i), { target: { value: "180" } });
    fireEvent.click(screen.getByRole("button", { name: /run scenario/i }));

    await waitFor(() => expect(screen.getAllByText("EGP 108,000").length).toBeGreaterThan(0));
    fireEvent.change(screen.getByLabelText(/scenario name/i), { target: { value: "Expanded unit" } });
    fireEvent.click(screen.getByRole("button", { name: /save scenario/i }));

    await waitFor(() => expect(createScenarioMock).toHaveBeenCalled());
    expect(createScenarioMock).toHaveBeenCalledWith(
      expect.objectContaining({
        property_state_id: 22,
        parent_scenario_id: null,
        name: "Expanded unit",
        delta_value: 18000,
        modifications: expect.objectContaining({
          size_sqm: 180,
          [SCENARIO_HISTORY_META_KEY]: expect.objectContaining({
            scenario_valuation: 108000,
            signed_delta_value: 18000,
          }),
        }),
      }),
      expect.any(AbortSignal),
    );
  });

  it("reopens saved scenario lineage into the editable draft", async () => {
    listScenariosMock.mockResolvedValue([savedScenario]);
    treeMock.mockResolvedValue(scenarioTree);
    lineageMock.mockResolvedValue([savedScenario]);
    renderPanel();

    fireEvent.click(screen.getByRole("button", { name: /what if/i }));
    await waitFor(() => expect(screen.getAllByText("Scenario A").length).toBeGreaterThan(0));
    fireEvent.click(screen.getByRole("button", { name: /open scenario a/i }));

    await waitFor(() => expect(screen.getByLabelText(/scenario area/i)).toHaveValue(180));
    expect(screen.getByText(/active lineage/i)).toBeInTheDocument();
  });

  it("opens a comparison drawer for selected scenarios", async () => {
    listScenariosMock.mockResolvedValue([savedScenario, childScenario]);
    treeMock.mockResolvedValue(scenarioTree);
    renderPanel();

    fireEvent.click(screen.getByRole("button", { name: /what if/i }));
    await waitFor(() => expect(screen.getAllByText("Scenario A").length).toBeGreaterThan(0));
    fireEvent.click(screen.getByLabelText(/add to comparison scenario a/i));
    fireEvent.click(screen.getByLabelText(/add to comparison scenario b/i));
    fireEvent.click(screen.getByRole("button", { name: /^compare$/i }));

    expect(screen.getByText(/scenario comparison drawer/i)).toBeInTheDocument();
    expect(screen.getAllByText("Scenario B").length).toBeGreaterThan(0);
    expect(screen.getAllByText("EGP 112,000").length).toBeGreaterThan(0);
  });

  it("renders sparse scenario outputs without crashing", () => {
    const sparse = {
      ...sampleWhatIfResponse,
      assumptions_used: [],
      feature_changes: { added: [], removed: [], modified: [] },
      explainability: {
        ...sampleWhatIfResponse.explainability,
        feature_drivers: [],
      },
      comparables: {
        ...sampleWhatIfResponse.comparables,
        comparables: [],
      },
    };
    render(
      <>
        <FeatureChangesList changes={sparse.feature_changes} />
        <ScenarioAssumptions assumptions={sparse.assumptions_used} />
        <ScenarioExplainability response={sparse} />
        <ScenarioComparables comparables={sparse.comparables.comparables} />
      </>,
    );

    expect(screen.getByText(/no unknown scenario assumptions/i)).toBeInTheDocument();
    expect(screen.getByText(/no feature changes were returned/i)).toBeInTheDocument();
    expect(screen.getByText(/no feature drivers returned/i)).toBeInTheDocument();
    expect(screen.getByText(/no scenario comparables were returned/i)).toBeInTheDocument();
  });
});
