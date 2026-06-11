import { beforeEach, describe, expect, it, vi } from "vitest";
import { runWhatIfAnalysis } from "@/services/whatIfService";
import { sampleWhatIfResponse } from "@/test/fixtures";
import { initialWhatIfState, useWhatIfStore } from "./whatIfStore";

vi.mock("@/services/whatIfService", () => ({
  runWhatIfAnalysis: vi.fn(),
}));

const runMock = vi.mocked(runWhatIfAnalysis);

const request = {
  workspace_id: 11,
  property_id: 22,
  scenario_id: null,
  modifications: {
    size_sqm: 180,
  },
};

describe("what-if store", () => {
  beforeEach(() => {
    runMock.mockReset();
    useWhatIfStore.setState(initialWhatIfState);
  });

  it("runs a scenario and stores request, response, and loading state", async () => {
    runMock.mockResolvedValueOnce({ data: sampleWhatIfResponse, meta: { request_id: "what-if-req-1" } });

    const result = await useWhatIfStore.getState().runScenario(request);

    expect(runMock).toHaveBeenCalledWith(request, undefined);
    expect(result.scenario_valuation).toBe(108000);
    expect(useWhatIfStore.getState().lastRequest).toEqual(request);
    expect(useWhatIfStore.getState().lastResponse).toEqual(sampleWhatIfResponse);
    expect(useWhatIfStore.getState().isLoading).toBe(false);
    expect(useWhatIfStore.getState().error).toBeNull();
  });

  it("passes abort signals to the service", async () => {
    const controller = new AbortController();
    runMock.mockResolvedValueOnce({ data: sampleWhatIfResponse, meta: {} });

    await useWhatIfStore.getState().runScenario(request, controller.signal);

    expect(runMock).toHaveBeenCalledWith(request, controller.signal);
  });

  it("captures scenario errors without dropping the last attempted request", async () => {
    runMock.mockRejectedValueOnce(new Error("Scenario failed"));

    await expect(useWhatIfStore.getState().runScenario(request)).rejects.toThrow("Scenario failed");

    expect(useWhatIfStore.getState().lastRequest).toEqual(request);
    expect(useWhatIfStore.getState().lastResponse).toBeNull();
    expect(useWhatIfStore.getState().isLoading).toBe(false);
    expect(useWhatIfStore.getState().error?.message).toBe("Scenario failed");
  });

  it("clears and resets scenario state", () => {
    useWhatIfStore.setState({
      lastRequest: request,
      lastResponse: sampleWhatIfResponse,
      isLoading: false,
      error: new Error("old"),
    });

    useWhatIfStore.getState().clearScenario();
    expect(useWhatIfStore.getState().lastRequest).toBeNull();
    expect(useWhatIfStore.getState().lastResponse).toBeNull();
    expect(useWhatIfStore.getState().error).toBeNull();

    useWhatIfStore.setState({ lastRequest: request, lastResponse: sampleWhatIfResponse, isLoading: true, error: null });
    useWhatIfStore.getState().reset();
    expect(useWhatIfStore.getState()).toMatchObject(initialWhatIfState);
  });
});
