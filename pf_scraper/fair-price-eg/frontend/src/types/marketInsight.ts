export type MarketInsightSource = "TruthLayer";

export type MarketInsightTimeWindow = "all" | `${number}d`;

export type MarketInsightDensityLevel = "High" | "Moderate" | "Sparse" | "Insufficient Evidence";

export interface MarketInsightToolRequest {
  workspace_id: number;
  compound_name?: string | null;
  h3_res9?: string | null;
  property_type?: string | null;
  time_window?: MarketInsightTimeWindow | string | null;
}

export interface MarketInsightConfidenceDistribution {
  valuation_count: number;
  counts: Record<string, number>;
  predominant_level: string | null;
}

export interface MarketInsightFairValueDistribution {
  valuation_count: number;
  minimum_fair_value: number | null;
  median_fair_value: number | null;
  maximum_fair_value: number | null;
}

export interface MarketInsightComparableDensity {
  valuation_count: number;
  minimum_comparable_count: number | null;
  median_comparable_count: number | null;
  maximum_comparable_count: number | null;
  density_level: MarketInsightDensityLevel;
  measurement_sources: Record<string, number>;
}

export interface MarketInsightSegment {
  name: string;
  valuation_count: number;
  median_fair_value: number;
  confidence_distribution: Record<string, number>;
  comparable_density: MarketInsightDensityLevel;
  median_comparable_count: number | null;
}

export interface MarketInsightStatement {
  text: string;
  evidence: string[];
}

export interface MarketInsightEvidenceSummary {
  valuation_ids: string[];
  source_record_counts: Record<string, number>;
  filters_used: Record<string, unknown>;
  statements: MarketInsightStatement[];
  traceability_note: string;
}

export interface MarketInsightToolResponse {
  tool_name: "market_insight";
  market_summary: string;
  valuation_volume: number;
  confidence_distribution: MarketInsightConfidenceDistribution;
  fair_value_distribution: MarketInsightFairValueDistribution;
  comparable_density: MarketInsightComparableDensity;
  active_compounds: MarketInsightSegment[];
  active_areas: MarketInsightSegment[];
  evidence_summary: MarketInsightEvidenceSummary;
  data_sources_used: string[];
  timestamp: string;
  source: MarketInsightSource;
}

export interface MarketInsightFilters {
  compound_name?: string;
  h3_res9?: string;
  property_type?: string;
  time_window: MarketInsightTimeWindow | string;
}

export interface MarketInsightRunRecord {
  key: string;
  request: MarketInsightToolRequest;
  response: MarketInsightToolResponse;
  createdAt: string;
}
