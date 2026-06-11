import type { RentFairPriceData, RentFairPriceRequest } from "@/types/valuation";

export type PropertyContextId = number;
export type ScenarioContextId = number | null;

export interface BackendVersionedRecord {
  id: number;
  created_at?: string;
  updated_at?: string;
  version?: number;
  is_deleted?: boolean;
}

export interface BackendWorkspaceContext extends BackendVersionedRecord {
  user_id?: number;
  name: string;
}

export interface BackendPropertyContext extends BackendVersionedRecord {
  user_id?: number;
  workspace_id: PropertyContextId;
  label: string;
  location: string;
  area: number | string;
  bedrooms: number;
  bathrooms: number;
  amenities: Record<string, unknown>;
  property_type: string;
  property_category: string;
  valuation_inputs: Record<string, unknown>;
}

export interface BackendToolEvent extends BackendVersionedRecord {
  user_id?: number;
  workspace_id: PropertyContextId;
  chat_id?: number | null;
  property_state_id?: PropertyContextId | null;
  scenario_state_id?: ScenarioContextId;
  tool_name: string;
  event_type: string;
  payload: Record<string, unknown>;
}

export interface PropertyContextBridgeInput {
  request: RentFairPriceRequest;
  valuation: RentFairPriceData;
  requestId?: string;
  preferredWorkspaceId?: PropertyContextId | null;
  signal?: AbortSignal;
}

export interface PropertyContextBinding {
  activeWorkspaceId: PropertyContextId;
  activePropertyId: PropertyContextId;
  activeScenarioId: ScenarioContextId;
  workspace: BackendWorkspaceContext;
  property: BackendPropertyContext;
  valuationEvent: BackendToolEvent;
  reusedWorkspace: boolean;
  reusedProperty: boolean;
  requestId?: string;
}
