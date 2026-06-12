import { beforeEach, describe, expect, it, vi } from "vitest";
import { http } from "@/api/http";
import { sampleRequest, sampleValuation } from "@/test/fixtures";
import {
  bridgeValuationToPropertyContext,
  isPropertyContextReady,
  preparePropertyContext,
} from "./propertyContextService";

vi.mock("@/api/http", () => ({
  http: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

const getMock = vi.mocked(http.get);
const postMock = vi.mocked(http.post);

const workspace = {
  id: 11,
  user_id: 2,
  name: "ValorAI Active Valuations",
  created_at: "2026-06-09T00:00:00Z",
  updated_at: "2026-06-09T00:00:00Z",
  version: 1,
  is_deleted: false,
};

const property = {
  id: 22,
  user_id: 2,
  workspace_id: workspace.id,
  label: "Apartment - Central Cairo",
  location: "Central Cairo",
  area: 150,
  bedrooms: 3,
  bathrooms: 2,
  amenities: { codes: ["BA", "SE"] },
  property_type: "Apartment",
  property_category: "residential_rent",
  valuation_inputs: sampleRequest,
  created_at: "2026-06-09T00:00:00Z",
  updated_at: "2026-06-09T00:00:00Z",
  version: 1,
  is_deleted: false,
};

const valuationEvent = {
  id: 33,
  user_id: 2,
  workspace_id: workspace.id,
  property_state_id: property.id,
  scenario_state_id: null,
  tool_name: "direct_valuation",
  event_type: "valuation.completed",
  payload: {},
  created_at: "2026-06-09T00:00:00Z",
  updated_at: "2026-06-09T00:00:00Z",
  version: 1,
};

describe("property context service", () => {
  beforeEach(() => {
    getMock.mockReset();
    postMock.mockReset();
  });

  it("creates the default workspace, property context, and valuation context event when none exist", async () => {
    getMock.mockResolvedValueOnce({ data: [] });
    postMock.mockResolvedValueOnce({ data: workspace });
    getMock.mockResolvedValueOnce({ data: [] });
    postMock.mockResolvedValueOnce({ data: property });
    postMock.mockResolvedValueOnce({ data: valuationEvent });

    const binding = await bridgeValuationToPropertyContext({
      request: sampleRequest,
      valuation: sampleValuation,
      requestId: "req-valuation-1",
    });

    expect(getMock).toHaveBeenNthCalledWith(1, "/v1/copilot/workspaces", { signal: undefined });
    expect(postMock).toHaveBeenNthCalledWith(1, "/v1/copilot/workspaces", { name: "ValorAI Active Valuations" }, { signal: undefined });
    expect(getMock).toHaveBeenNthCalledWith(2, "/v1/copilot/workspaces/11/properties", { signal: undefined });
    expect(postMock).toHaveBeenNthCalledWith(
      2,
      "/v1/copilot/properties",
      expect.objectContaining({
        workspace_id: 11,
        label: "Apartment - Nile Quarter",
        location: "Nile Quarter",
        area: 150,
        amenities: { codes: ["BA", "SE"] },
        valuation_inputs: expect.objectContaining({ property_type: "Apartment", size_sqm: 150 }),
      }),
      { signal: undefined },
    );
    expect(postMock).toHaveBeenNthCalledWith(
      3,
      "/v1/copilot/tool-events",
      expect.objectContaining({
        workspace_id: 11,
        property_state_id: 22,
        scenario_state_id: null,
        tool_name: "direct_valuation",
        event_type: "valuation.completed",
        payload: expect.objectContaining({
          request_id: "req-valuation-1",
          valuation_result: expect.objectContaining({
            fair_price_egp: 90000,
            engine_used: "CMT",
            routing_reason: "GoldilocksZone",
            explainability: expect.objectContaining({
              narrative_explanation: expect.objectContaining({
                summary: "The property's fair value is 90,000 EGP.",
              }),
            }),
          }),
        }),
      }),
      { signal: undefined },
    );
    expect(binding.activeWorkspaceId).toBe(11);
    expect(binding.activePropertyId).toBe(22);
    expect(binding.activeScenarioId).toBeNull();
    expect(binding.reusedWorkspace).toBe(false);
    expect(binding.reusedProperty).toBe(false);
  });

  it("reuses the preferred workspace and binds to a matching property context", async () => {
    const preferredWorkspace = { ...workspace, id: 44, name: "Existing Workspace" };
    const matchingProperty = {
      ...property,
      id: 55,
      workspace_id: preferredWorkspace.id,
      valuation_inputs: { ...sampleRequest, target_price_egp: 12345 },
    };
    const event = { ...valuationEvent, id: 66, workspace_id: preferredWorkspace.id, property_state_id: matchingProperty.id };

    getMock.mockResolvedValueOnce({ data: [workspace, preferredWorkspace] });
    getMock.mockResolvedValueOnce({ data: [matchingProperty] });
    postMock.mockResolvedValueOnce({ data: event });

    const binding = await bridgeValuationToPropertyContext({
      request: sampleRequest,
      valuation: sampleValuation,
      requestId: "req-valuation-2",
      preferredWorkspaceId: preferredWorkspace.id,
    });

    expect(getMock).toHaveBeenNthCalledWith(2, "/v1/copilot/workspaces/44/properties", { signal: undefined });
    expect(postMock).toHaveBeenCalledTimes(1);
    expect(binding.activeWorkspaceId).toBe(44);
    expect(binding.activePropertyId).toBe(55);
    expect(binding.reusedWorkspace).toBe(true);
    expect(binding.reusedProperty).toBe(true);
  });

  it("prepares property context without requiring a completed valuation", async () => {
    getMock.mockResolvedValueOnce({ data: [] });
    postMock.mockResolvedValueOnce({ data: workspace });
    getMock.mockResolvedValueOnce({ data: [] });
    postMock.mockResolvedValueOnce({ data: property });

    const binding = await preparePropertyContext({ request: sampleRequest });

    expect(postMock).toHaveBeenCalledTimes(2);
    expect(postMock).toHaveBeenNthCalledWith(
      2,
      "/v1/copilot/properties",
      expect.objectContaining({
        workspace_id: 11,
        valuation_inputs: expect.objectContaining({ property_type: "Apartment", size_sqm: 150 }),
      }),
      { signal: undefined },
    );
    expect(postMock).not.toHaveBeenCalledWith("/v1/copilot/tool-events", expect.any(Object), expect.any(Object));
    expect(binding.activeWorkspaceId).toBe(11);
    expect(binding.activePropertyId).toBe(22);
    expect(binding.valuationEvent).toBeNull();
    expect(binding.contextSource).toBe("property");
  });

  it("requires enough property metadata before automatic context preparation", () => {
    expect(isPropertyContextReady(sampleRequest)).toBe(true);
    expect(isPropertyContextReady({ ...sampleRequest, address: "", compound_name: null, lat: undefined, lng: undefined })).toBe(false);
  });

  it("passes abort signals through each backend context call", async () => {
    const controller = new AbortController();
    getMock.mockResolvedValueOnce({ data: [workspace] });
    getMock.mockResolvedValueOnce({ data: [property] });
    postMock.mockResolvedValueOnce({ data: valuationEvent });

    await bridgeValuationToPropertyContext({
      request: sampleRequest,
      valuation: sampleValuation,
      signal: controller.signal,
    });

    expect(getMock).toHaveBeenNthCalledWith(1, "/v1/copilot/workspaces", { signal: controller.signal });
    expect(getMock).toHaveBeenNthCalledWith(2, "/v1/copilot/workspaces/11/properties", { signal: controller.signal });
    expect(postMock).toHaveBeenCalledWith("/v1/copilot/tool-events", expect.any(Object), { signal: controller.signal });
  });

  it("rejects malformed backend context payloads", async () => {
    getMock.mockResolvedValueOnce({
      data: {
        success: true,
        data: { workspaces: [] },
        meta: { request_id: "bad-context-shape" },
      },
    });

    await expect(
      bridgeValuationToPropertyContext({
        request: sampleRequest,
        valuation: sampleValuation,
      }),
    ).rejects.toMatchObject({
      code: "INVALID_API_RESPONSE",
      requestId: "bad-context-shape",
    });
  });
});
