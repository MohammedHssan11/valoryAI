import { beforeEach, describe, expect, it } from "vitest";
import { usePropertyContextStore } from "./propertyContextStore";

describe("property context store", () => {
  beforeEach(() => {
    localStorage.clear();
    usePropertyContextStore.getState().clearActivePropertyContext();
  });

  it("stores active backend context ids for future intelligence tools", () => {
    usePropertyContextStore.getState().setActivePropertyContext({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: null,
      requestId: "req-valuation-1",
    });

    const state = usePropertyContextStore.getState();
    expect(state.activeWorkspaceId).toBe(11);
    expect(state.activePropertyId).toBe(22);
    expect(state.activeScenarioId).toBeNull();
    expect(state.bridgeStatus).toBe("ready");
    expect(state.lastBridgeRequestId).toBe("req-valuation-1");
    expect(state.lastBridgeError).toBeUndefined();
  });

  it("records bridge failures without clearing the last successful context", () => {
    usePropertyContextStore.getState().setActivePropertyContext({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: 33,
    });

    usePropertyContextStore.getState().setBridgeError("Backend context unavailable", "req-valuation-2");

    const state = usePropertyContextStore.getState();
    expect(state.activeWorkspaceId).toBe(11);
    expect(state.activePropertyId).toBe(22);
    expect(state.activeScenarioId).toBe(33);
    expect(state.bridgeStatus).toBe("error");
    expect(state.lastBridgeRequestId).toBe("req-valuation-2");
    expect(state.lastBridgeError).toBe("Backend context unavailable");
  });

  it("persists only the active backend ids and ready bridge metadata", () => {
    usePropertyContextStore.getState().setActivePropertyContext({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: null,
      requestId: "req-valuation-1",
    });

    const stored = JSON.parse(localStorage.getItem("valorai-property-context") ?? "{}");
    expect(stored.state).toMatchObject({
      activeWorkspaceId: 11,
      activePropertyId: 22,
      activeScenarioId: null,
      bridgeStatus: "ready",
      lastBridgeRequestId: "req-valuation-1",
    });
    expect(stored.state.lastBridgeError).toBeUndefined();
  });
});
