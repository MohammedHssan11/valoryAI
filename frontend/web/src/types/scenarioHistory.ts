export const SCENARIO_HISTORY_META_KEY = "__valorai_scenario_history";

export interface ScenarioHistoryMeta {
  saved_at?: string;
  base_valuation?: number;
  scenario_valuation?: number;
  signed_delta_value?: number;
  delta_percentage?: number;
  confidence_level?: string;
  fairness_status?: string;
  base_valuation_id?: string;
  scenario_valuation_id?: string;
  fairness_valuation_id?: string;
  assumptions_count?: number;
  effective_modifications?: Record<string, unknown>;
}

export interface ScenarioState {
  id: number;
  created_at?: string;
  updated_at?: string;
  version?: number;
  is_deleted?: boolean;
  deleted_at?: string | null;
  user_id?: number;
  workspace_id: number;
  property_state_id: number;
  parent_scenario_id: number | null;
  name: string;
  modifications: Record<string, unknown>;
  delta_value: number | null;
}

export interface ScenarioTreeNode extends ScenarioState {
  children: ScenarioTreeNode[];
}

export interface ScenarioStateCreate {
  property_state_id: number;
  parent_scenario_id?: number | null;
  name: string;
  modifications: Record<string, unknown>;
  delta_value?: number | null;
}

export interface ScenarioStateUpdate {
  name?: string;
  modifications?: Record<string, unknown>;
  delta_value?: number | null;
}
