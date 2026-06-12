import type { RentFairPriceRequest } from "@/types/valuation";

export type TruthLayerSource = "TruthLayer";
export type FairnessStatus = "Below Fair Value" | "Within Fair Value" | "Above Fair Value";

export interface ToolPriceRange {
  low: number;
  high: number;
}

export interface ValuationToolResponse {
  tool_name: "valuation";
  valuation_id: string;
  fair_price: number;
  price_range: ToolPriceRange;
  confidence_level: string;
  engine_used: string;
  routing_reason: string;
  timestamp: string;
  source: TruthLayerSource;
}

export interface ExplainabilityToolResponse {
  tool_name: "explainability";
  valuation_id: string;
  summary: string;
  why_this_price: string;
  strongest_factors: string;
  confidence_reason: string;
  fairness_status: string;
  feature_drivers: Array<Record<string, unknown>>;
  comparable_evidence: Array<Record<string, unknown>>;
  timestamp: string;
  source: TruthLayerSource;
}

export interface ComparableToolItem {
  comparable_id: string;
  price: number;
  size_sqm: number;
  bedrooms: number;
  bathrooms: number;
  compound_name: string | null;
  distance_km: number;
  similarity_reason: string | null;
  source: TruthLayerSource;
}

export interface ComparableToolResponse {
  tool_name: "comparable";
  valuation_id: string;
  comparable_count: number;
  comparables: ComparableToolItem[];
  timestamp: string;
  source: TruthLayerSource;
}

export interface FeatureChange {
  feature: string;
  before: unknown;
  after: unknown;
  unit: string | null;
}

export interface FeatureChanges {
  added: FeatureChange[];
  removed: FeatureChange[];
  modified: FeatureChange[];
}

export type WhatIfModificationKey =
  | keyof RentFairPriceRequest
  | "area"
  | "size"
  | "location"
  | "furnished"
  | "furnishing"
  | "finishing"
  | "parking"
  | "gym"
  | "clubhouse"
  | "amenities_added"
  | "amenities_removed"
  | "valuation_inputs";

export type WhatIfModificationPrimitive = string | number | boolean | null;
export type WhatIfModificationValue =
  | WhatIfModificationPrimitive
  | WhatIfModificationPrimitive[]
  | Partial<RentFairPriceRequest>
  | Record<string, unknown>;

export type WhatIfModifications = Partial<Record<WhatIfModificationKey, WhatIfModificationValue>>;

export interface WhatIfToolRequest {
  workspace_id: number;
  property_id: number;
  scenario_id?: number | null;
  modifications: WhatIfModifications;
}

export interface WhatIfToolResponse {
  tool_name: "what_if";
  base_valuation: number;
  scenario_valuation: number;
  base_valuation_id: string;
  scenario_valuation_id: string;
  fairness_valuation_id: string;
  delta_value: number;
  delta_percentage: number;
  fairness_status: FairnessStatus;
  confidence_level: string;
  assumptions_used: string[];
  feature_changes: FeatureChanges;
  explainability: ExplainabilityToolResponse;
  comparables: ComparableToolResponse;
  timestamp: string;
  source: TruthLayerSource;
}
