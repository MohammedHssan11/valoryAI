import type { BrokerOrchestrationResponse } from "@/types/broker";
import type { CopilotOrchestratorResponse } from "@/types/copilot";
import type { InvestmentToolResponse } from "@/types/investment";
import type { MarketInsightToolResponse } from "@/types/marketInsight";
import type { NegotiationToolResponse } from "@/types/negotiation";
import type { ComparableItem, RentFairPriceData, RentFairPriceRequest } from "@/types/valuation";
import type { WhatIfToolResponse } from "@/types/whatIf";

export const sampleRequest: RentFairPriceRequest = {
  lat: 30.0444,
  lng: 31.2357,
  property_type: "Apartment",
  property_category: "residential_rent",
  bedrooms: 3,
  bathrooms: 2,
  size_sqm: 150,
  target_price_egp: 95000,
  amenities: ["BA", "SE"],
  furnishing_status: "furnished",
  floor_number: 8,
  compound_name: "Nile Quarter",
  view_type: "river",
  building_quality: "premium",
};

export const sampleComparable: ComparableItem = {
  listing_id: "comp-001",
  price_egp: 90000,
  size_sqm: 150,
  price_per_sqm: 600,
  property_type: "Apartment",
  bedrooms: 3,
  bathrooms: 2,
  area_id: 10,
  area_name: "Central Cairo",
  lat: 30.047,
  lng: 31.238,
  location_text: "Central Cairo",
  images_count: 8,
  retrieval_tier: 1,
  tier_label: "same compound/neighborhood",
  reason_code: "SAME_AREA_MATCH",
  radius_m: 500,
  dist_m: 420,
  age_days: 12,
  weight: 0.82,
  weight_components: {
    distance: 0.72,
    size_similarity: 1,
    recency: 0.84,
    feature_similarity: 1,
  },
  weighted_contribution: 0.62,
  confidence_contribution: 0.54,
  similarity_score: 1,
  geographic_similarity: 0.72,
  distance_weight: 0.72,
  recency_weight: 0.84,
  evidence_rank: 1,
  property_category: "residential_rent",
  amenities: [],
  normalized_amenities: ["balcony", "security"],
  canonical_amenity_symbols: ["BA", "SE"],
  unknown_amenity_codes: [],
  furnishing_status: "furnished",
  floor_number: 8,
  compound_name: "Nile Quarter",
  view_type: "river",
  building_quality: "premium",
  feature_similarity: 1,
  feature_similarity_components: {
    amenities: 1,
  },
  feature_explanation: {
    matched_amenities: ["balcony", "security"],
    missing_amenities: [],
  },
  feature_overlap: {
    matched_amenities: ["balcony", "security"],
    missing_amenities: [],
    extra_amenities: [],
  },
  amenity_similarity: 1,
  amenity_explanation: {
    matched_amenities: ["balcony", "security"],
    missing_amenities: [],
    extra_amenities: [],
  },
  amenity_metadata: [
    {
      symbol: "BA",
      name: "Balcony",
      normalized: "balcony",
      valuation_weight: 0.04,
    },
  ],
  filter_status: {
    hard_guardrails: "kept",
    mad_outlier: "kept",
  },
};

export const secondaryComparable: ComparableItem = {
  ...sampleComparable,
  listing_id: "comp-002",
  price_egp: 85000,
  dist_m: 900,
  age_days: 140,
  weight: 0.4,
  weighted_contribution: 0.3,
  confidence_contribution: 0.18,
  similarity_score: 0.55,
  feature_similarity: 0.5,
  evidence_rank: 2,
  building_quality: "standard",
  lat: 30.051,
  lng: 31.242,
};

export const sampleValuation: RentFairPriceData = {
  fair_price_egp: 90000,
  range_low_egp: 82000,
  range_high_egp: 105000,
  flag: "OK",
  tier_used: 1,
  comps_count: 12,
  confidence: {
    score: 0.82,
    label: "High",
    factors: {
      count: 1,
      tier: 1,
      kept_ratio: 1,
      dispersion: 0.9,
      distance: 0.97,
      recency: 0.8,
      similarity: 1,
      amenity_similarity: 1,
      valuation_evidence: 0.84,
      location_resolution: 0.82,
    },
    dimensions: {
      valuation_evidence: {
        score: 0.84,
        label: "High",
        factors: {
          count: 1,
        },
      },
      location_resolution: {
        score: 0.82,
        source: "MANUAL_COORDINATES",
        precision_level: "ROOFTOP",
      },
    },
  },
  engine_used: "CMT",
  routing_reason: "GoldilocksZone",
  explainability: {
    router_explanation: "CMT selected due to optimal comparable density (12 comps).",
    confidence_explanation: {
      confidence_level: "High",
      confidence_reason: "High confidence because 12 similar properties were found.",
    },
    fairness_explanation: {
      estimated_value: 90000,
      asking_price: 95000,
      difference_amount: 5000,
      difference_percentage: 5.56,
      status: "Within Fair Value Range",
    },
    narrative_explanation: {
      summary: "The property's fair value is 90,000 EGP.",
      why_this_price: "This is based on 12 highly similar properties recently listed nearby.",
      strongest_factors: "Prices in this specific compound strongly anchor the valuation.",
      confidence_reason: "High confidence because 12 similar properties were found.",
    },
    comparable_evidence: [
      {
        property_id: "comp-001",
        price: 90000,
        size_sqm: 150,
        bedrooms: 3,
        bathrooms: 2,
        furnishing_status: "furnished",
        compound_name: "Nile Quarter",
        distance_km: 0.42,
        similarity_score: 1,
        similarity_reason: "SAME_AREA_MATCH",
      },
    ],
    feature_drivers: [],
  },
  explanation: [
    "12 similar listings found using same compound/neighborhood around Central Cairo.",
    "Fair price computed using weighted median.",
  ],
  explanation_trace: [
    {
      reason_code: "SAME_AREA_MATCH",
      details: {
        radius_m: 500,
        comps_found: 12,
      },
    },
    {
      reason_code: "CONFIDENCE_FACTORS",
      weight: 0.82,
      details: {
        confidence_score: 0.82,
        tier: 1,
      },
    },
    {
      reason_code: "FEATURE_SIMILARITY_APPLIED",
      weight: 1,
      details: {
        matched_amenities: ["balcony", "security"],
        missing_amenities: [],
      },
    },
  ],
  retrieval_trace: [
    {
      tier: 1,
      tier_label: "same compound/neighborhood",
      reason_code: "SAME_AREA_MATCH",
      scope: "same_area",
      radius_m: 500,
      comps_found: 12,
      threshold: 10,
      shortfall: 0,
      attempt_index: 1,
      status: "selected",
      selected: true,
      radius_expansion_m: null,
    },
  ],
  spatial_diagnostics: {
    subject: {
      lat: 30.0444,
      lng: 31.2357,
      area_id: 10,
      area_name: "Central Cairo",
    },
    retrieval_radius_m: 500,
    distance_band_counts: {
      "0_500m": 1,
      "500_1000m": 0,
    },
    cluster_quality: "high_quality_cluster",
  },
  evidence_summary: {
    authoritative_valuation_frozen: true,
    valuation_mutation_allowed: false,
    property_category: "residential_rent",
    valuation_contract: {
      category: "residential_rent",
      label: "Residential rent",
      value_basis: "monthly_rent",
    },
    amenity_intelligence: {
      average_amenity_similarity: 1,
      comps_scored: 1,
      matched_amenities_observed: ["balcony", "security"],
      missing_amenities_observed: [],
    },
    guardrails: {
      kept: 12,
      removed: 0,
    },
    mad: {
      kept: 12,
      removed: 0,
      metric: "price_per_sqm",
    },
  },
  area: {
    name: "Central Cairo",
    area_id: 10,
  },
  resolved_location: {
    lat: 30.0444,
    lng: 31.2357,
    precision_level: "ROOFTOP",
  },
  property_category: "residential_rent",
  valuation_contract: {
    category: "residential_rent",
    label: "Residential rent",
    value_basis: "monthly_rent",
    governance: {
      amenities_override_pricing: false,
    },
  },
  amenity_intelligence: {
    property_category: "residential_rent",
    contract_label: "Residential rent",
    average_amenity_similarity: 1,
    comps_scored: 1,
    matched_amenities_observed: ["balcony", "security"],
    missing_amenities_observed: [],
  },
  debug: {},
  top_comps: [sampleComparable],
};

export const sampleBrokerResponse: BrokerOrchestrationResponse = {
  session_id: "broker-session-1",
  intent: "valuation_explanation",
  response: {
    executive_summary: "The valuation is supported by a high-confidence comparable cluster.",
    valuation_interpretation: "The fair rent sits inside the returned deterministic range.",
    comparable_reasoning: "Comparable evidence is anchored by nearby listings with strong feature similarity.",
    district_insights: "District context is limited to the resolved valuation area and returned evidence.",
    confidence_explanation: "Confidence is high because comparable depth and similarity are strong.",
    opportunity_risk_notes: ["Monitor spread widening before repricing.", "Do not infer external demand signals."],
    analytical_conclusion: "The target remains aligned with the deterministic valuation evidence.",
    authoritative_values: {
      valuation_id: "val-broker-1",
      fair_price_egp: sampleValuation.fair_price_egp,
      range_low_egp: sampleValuation.range_low_egp,
      range_high_egp: sampleValuation.range_high_egp,
      confidence_label: sampleValuation.confidence.label,
      engine_used: "TruthLayer",
      routing_reason: "Valuation context supplied by Broker contract fixture.",
      source: "TruthLayer",
      flag: sampleValuation.flag,
      tier_used: sampleValuation.tier_used,
      comps_count: sampleValuation.comps_count,
      confidence_score: sampleValuation.confidence.score,
    },
    evidence_ids: ["valuation_summary", "comp-001"],
    referenced_comp_listing_ids: ["comp-001"],
  },
  grounding: {
    status: "passed",
    violations: [],
    checked_values: {},
  },
  context: {
    intent: "valuation_explanation",
    session_id: "broker-session-1",
    user_message: "Explain the valuation",
    valuation_summary: {
      valuation_id: "val-broker-1",
      fair_price_egp: sampleValuation.fair_price_egp,
      range_low_egp: sampleValuation.range_low_egp,
      range_high_egp: sampleValuation.range_high_egp,
      confidence_label: sampleValuation.confidence.label,
      engine_used: "TruthLayer",
      routing_reason: "Valuation context supplied by Broker contract fixture.",
      source: "TruthLayer",
      flag: sampleValuation.flag,
      tier_used: sampleValuation.tier_used,
      comps_count: sampleValuation.comps_count,
      confidence_score: sampleValuation.confidence.score,
      area: sampleValuation.area,
      property_category: sampleValuation.property_category,
      valuation_contract: sampleValuation.valuation_contract,
      amenity_intelligence: sampleValuation.amenity_intelligence,
    },
    comparable_evidence: [
      {
        evidence_id: "comp-001",
        listing_id: sampleComparable.listing_id,
        price_egp: sampleComparable.price_egp,
        size_sqm: sampleComparable.size_sqm,
        bedrooms: sampleComparable.bedrooms,
        bathrooms: sampleComparable.bathrooms,
        area_name: sampleComparable.area_name,
        distance_m: sampleComparable.dist_m,
        age_days: sampleComparable.age_days,
        weight: sampleComparable.weight,
        reason_code: sampleComparable.reason_code,
        amenity_similarity: sampleComparable.amenity_similarity,
        matched_amenities: ["balcony", "security"],
        missing_amenities: [],
      },
    ],
    confidence_factors: sampleValuation.confidence.factors,
    explainability_trace: sampleValuation.explanation_trace.map((item) => ({ ...item })),
    valuation_contract: sampleValuation.valuation_contract ?? {},
    amenity_intelligence: sampleValuation.amenity_intelligence ?? {},
    district_intelligence: {
      active_district: "Central Cairo",
    },
    market_signals: ["Valuation context only"],
    session_state: {},
    evidence: [],
    token_budget: {
      max_context_tokens: 6000,
      estimated_context_tokens: 900,
      truncated: false,
    },
    deterministic_authority: {},
  },
  tool_results: [],
  events: [
    {
      event_id: "event-1",
      stage: "classify_intent",
      event_type: "stage_started",
      message: "Classifying analytical broker intent",
      elapsed_ms: null,
      payload: {},
      created_at: "2026-05-25T00:00:00Z",
    },
  ],
  degraded_mode: false,
  intent_classification: {
    intent: "valuation_explanation",
    confidence: 0.86,
    matched_signals: [],
    fallback: false,
    routing_reason: "Rule-assisted classifier selected the highest-confidence broker intent.",
    has_valuation_request: true,
  },
  reasoning_plan: {
    plan_id: "plan_fixture",
    intent: "valuation_explanation",
    stages: [
      "classify_intent",
      "build_reasoning_plan",
      "execute_tools",
      "assemble_context",
      "generate_narration",
      "validate_grounding",
      "finalize_response",
    ],
    selected_tools: [
      "valuation_analysis",
      "comparable_analysis",
      "explainability",
      "district_intelligence",
      "confidence_analysis",
    ],
    requires_valuation: true,
    evidence_requirements: ["deterministic_authority", "valuation_analysis"],
    narration_mode: "valuation_explainability",
    governance_checks: ["numeric_consistency", "confidence_consistency"],
    degraded_mode_reasons: [],
  },
  narration: {
    provider: "deterministic_formatter",
    model: null,
    used_llm: false,
    latency_ms: 12,
    token_usage: {},
    fallback_reason: null,
  },
  governance: {
    status: "passed",
    checks: [],
    violations: [],
    sanitized: false,
  },
};

export const sampleWhatIfResponse: WhatIfToolResponse = {
  tool_name: "what_if",
  base_valuation: 90000,
  scenario_valuation: 108000,
  base_valuation_id: "val-base-1",
  scenario_valuation_id: "val-scenario-1",
  fairness_valuation_id: "val-fairness-1",
  delta_value: 18000,
  delta_percentage: 20,
  fairness_status: "Above Fair Value",
  confidence_level: "High",
  assumptions_used: ["Parking = Unknown"],
  feature_changes: {
    added: [
      {
        feature: "Parking",
        before: false,
        after: true,
        unit: null,
      },
    ],
    removed: [],
    modified: [
      {
        feature: "Size",
        before: 150,
        after: 180,
        unit: "sqm",
      },
    ],
  },
  explainability: {
    tool_name: "explainability",
    valuation_id: "val-scenario-1",
    summary: "Scenario valuation increased after expanding the property profile.",
    why_this_price: "The scenario is benchmarked against larger high-similarity comparables.",
    strongest_factors: "Size and parking are the strongest scenario drivers.",
    confidence_reason: "Confidence remains high because comparable density is strong.",
    fairness_status: "Above Fair Value",
    feature_drivers: [{ feature: "Size", impact: 18000 }],
    comparable_evidence: [{ comparable_id: "scenario-comp-1" }],
    timestamp: "2026-06-09T00:00:00Z",
    source: "TruthLayer",
  },
  comparables: {
    tool_name: "comparable",
    valuation_id: "val-scenario-1",
    comparable_count: 1,
    comparables: [
      {
        comparable_id: "scenario-comp-1",
        price: 110000,
        size_sqm: 180,
        bedrooms: 3,
        bathrooms: 3,
        compound_name: "Nile Quarter",
        distance_km: 0.42,
        similarity_reason: "Expanded unit with similar finish and location.",
        source: "TruthLayer",
      },
    ],
    timestamp: "2026-06-09T00:00:00Z",
    source: "TruthLayer",
  },
  timestamp: "2026-06-09T00:00:00Z",
  source: "TruthLayer",
};

export const sampleNegotiationResponse: NegotiationToolResponse = {
  tool_name: "negotiation",
  valuation_id: "val-negotiation-1",
  asking_price: 118000,
  fair_price: 90000,
  fairness_status: "Above Fair Value",
  price_gap: 28000,
  price_gap_percentage: 31.1111,
  confidence_level: "High",
  confidence_reason: "Confidence is high because comparable depth and similarity are strong.",
  negotiation_position: "Overpriced",
  negotiation_position_reason: "TruthLayer classifies the asking price as Above Fair Value.",
  negotiation_position_evidence: [
    {
      source_tool: "valuation",
      valuation_id: "val-negotiation-1",
      field: "fair_price",
      comparable_id: null,
    },
    {
      source_tool: "fairness",
      valuation_id: "val-negotiation-1",
      field: "fairness_status",
      comparable_id: null,
    },
  ],
  broker_talking_points: [
    {
      text: "Asking price exceeds the TruthLayer fair price by 28,000 EGP (31.11%).",
      evidence: [
        {
          source_tool: "input",
          valuation_id: null,
          field: "asking_price_egp",
          comparable_id: null,
        },
        {
          source_tool: "valuation",
          valuation_id: "val-negotiation-1",
          field: "fair_price",
          comparable_id: null,
        },
      ],
    },
    {
      text: "TruthLayer valuation rationale: The scenario is benchmarked against nearby high-similarity comparables.",
      evidence: [
        {
          source_tool: "explainability",
          valuation_id: "val-negotiation-1",
          field: "why_this_price",
          comparable_id: null,
        },
      ],
    },
  ],
  evidence_summary: {
    valuation_id: "val-negotiation-1",
    price_range: {
      low: 82000,
      high: 105000,
    },
    explainability_summary: "The valuation is supported by a high-confidence comparable cluster.",
    why_this_price: "The scenario is benchmarked against nearby high-similarity comparables.",
    strongest_factors: "Size, location, and comparable support are the strongest factors.",
    source: "TruthLayer",
  },
  comparable_summary: {
    valuation_id: "val-negotiation-1",
    comparable_count: 2,
    comparable_ids: ["scenario-comp-1", "scenario-comp-2"],
    observed_prices: [88000, 92000],
    lowest_observed_price: 88000,
    highest_observed_price: 92000,
    source: "TruthLayer",
  },
  recommended_offer_band: {
    low: 88000,
    high: 90000,
    derivation:
      "The asking price is Above Fair Value. The low endpoint is the highest returned comparable price at or below fair_price; the high endpoint is the authoritative TruthLayer fair_price.",
    comparable_ids_used: ["scenario-comp-1"],
    evidence: [
      {
        source_tool: "valuation",
        valuation_id: "val-negotiation-1",
        field: "fair_price",
        comparable_id: null,
      },
      {
        source_tool: "comparable",
        valuation_id: "val-negotiation-1",
        field: "comparables[].price",
        comparable_id: "scenario-comp-1",
      },
    ],
    source: "TruthLayer-derived",
  },
  risk_notes: [
    {
      text: "TruthLayer confidence is High: Confidence is high because comparable depth and similarity are strong.",
      evidence: [
        {
          source_tool: "fairness",
          valuation_id: "val-negotiation-1",
          field: "confidence_level",
          comparable_id: null,
        },
      ],
    },
    {
      text: "Comparable support is limited to the 2 properties returned by TruthLayer for this valuation snapshot.",
      evidence: [
        {
          source_tool: "comparable",
          valuation_id: "val-negotiation-1",
          field: "comparable_count",
          comparable_id: null,
        },
      ],
    },
  ],
  what_if_analysis: {
    base_valuation: 90000,
    scenario_valuation: 108000,
    base_valuation_id: "val-base-1",
    scenario_valuation_id: "val-scenario-1",
    delta_value: 18000,
    delta_percentage: 20,
    fairness_status: "Above Fair Value",
    assumptions_used: ["Parking = Unknown"],
    feature_changes: sampleWhatIfResponse.feature_changes,
    source: "TruthLayer",
  },
  timestamp: "2026-06-09T00:00:00Z",
  source: "TruthLayer",
};

export const sampleInvestmentResponse: InvestmentToolResponse = {
  tool_name: "investment",
  valuation_id: "val-investment-1",
  asking_price: 118000,
  fair_price: 90000,
  fairness_status: "Above Fair Value",
  price_gap: 28000,
  price_gap_percentage: 31.1111,
  investment_position: "High Risk",
  investment_position_reason: "TruthLayer classifies the asking price as Above Fair Value.",
  investment_position_evidence: sampleNegotiationResponse.negotiation_position_evidence,
  confidence_level: "High",
  confidence_reason: "Confidence is high because comparable depth and similarity are strong.",
  investment_summary:
    "High Risk: TruthLayer classifies the asking price as Above Fair Value. This is evidence-backed opportunity analysis only; no investment return or forecast is asserted.",
  strengths: [
    {
      text: "TruthLayer valuation confidence is High: Confidence is high because comparable depth and similarity are strong.",
      evidence: [
        {
          source_tool: "fairness",
          valuation_id: "val-investment-1",
          field: "confidence_level",
          comparable_id: null,
        },
      ],
    },
  ],
  risks: [
    {
      text: "Premium asking price: asking price exceeds the TruthLayer fair price by 28,000 EGP (31.11%).",
      evidence: [
        {
          source_tool: "input",
          valuation_id: null,
          field: "asking_price_egp",
          comparable_id: null,
        },
        {
          source_tool: "valuation",
          valuation_id: "val-investment-1",
          field: "fair_price",
          comparable_id: null,
        },
      ],
    },
    {
      text: "Investment assessment is limited to current TruthLayer evidence. ROI, yield, returns, and future-price forecasts are not asserted.",
      evidence: [
        {
          source_tool: "valuation",
          valuation_id: "val-investment-1",
          field: "fair_price",
          comparable_id: null,
        },
      ],
    },
  ],
  evidence_summary: sampleNegotiationResponse.evidence_summary,
  comparable_summary: sampleNegotiationResponse.comparable_summary,
  negotiation_summary: {
    negotiation_position: sampleNegotiationResponse.negotiation_position,
    negotiation_position_reason: sampleNegotiationResponse.negotiation_position_reason,
    recommended_offer_band: sampleNegotiationResponse.recommended_offer_band,
    broker_talking_points: sampleNegotiationResponse.broker_talking_points,
    source: "TruthLayer",
  },
  what_if_summary: {
    status: "Available",
    reason: "Optional What-if Tool sensitivity evidence is available.",
    analysis: sampleNegotiationResponse.what_if_analysis,
    source: "TruthLayer",
  },
  timestamp: "2026-06-09T00:00:00Z",
  source: "TruthLayer",
};

export const sampleMarketInsightResponse: MarketInsightToolResponse = {
  tool_name: "market_insight",
  market_summary:
    "Observed 6 persisted TruthLayer valuations in this workspace history. Median observed fair value is EGP 4,450,000.",
  valuation_volume: 6,
  confidence_distribution: {
    valuation_count: 6,
    counts: {
      High: 4,
      Moderate: 2,
    },
    predominant_level: "High",
  },
  fair_value_distribution: {
    valuation_count: 6,
    minimum_fair_value: 3900000,
    median_fair_value: 4450000,
    maximum_fair_value: 5200000,
  },
  comparable_density: {
    valuation_count: 6,
    minimum_comparable_count: 3,
    median_comparable_count: 6,
    maximum_comparable_count: 9,
    density_level: "High",
    measurement_sources: {
      shadow_logs: 4,
      comparable_evidence: 2,
    },
  },
  active_compounds: [
    {
      name: "Nile Quarter",
      valuation_count: 4,
      median_fair_value: 4520000,
      confidence_distribution: {
        High: 3,
        Moderate: 1,
      },
      comparable_density: "High",
      median_comparable_count: 7,
    },
    {
      name: "Garden Heights",
      valuation_count: 2,
      median_fair_value: 4100000,
      confidence_distribution: {
        High: 1,
        Moderate: 1,
      },
      comparable_density: "Moderate",
      median_comparable_count: 4,
    },
  ],
  active_areas: [
    {
      name: "Central Cairo",
      valuation_count: 3,
      median_fair_value: 4500000,
      confidence_distribution: {
        High: 2,
        Moderate: 1,
      },
      comparable_density: "High",
      median_comparable_count: 6,
    },
    {
      name: "New Cairo",
      valuation_count: 3,
      median_fair_value: 4400000,
      confidence_distribution: {
        High: 2,
        Moderate: 1,
      },
      comparable_density: "Moderate",
      median_comparable_count: 4,
    },
  ],
  evidence_summary: {
    valuation_ids: ["val-001", "val-002", "val-003", "val-004", "val-005", "val-006"],
    source_record_counts: {
      valuation_snapshots: 6,
      prediction_logs: 6,
      shadow_logs: 4,
      comparable_evidence: 2,
      tool_events: 6,
      workspace_history: 6,
      scenario_history: 1,
    },
    filters_used: {
      workspace_id: 11,
      compound_name: "Nile Quarter",
      property_type: "Apartment",
      h3_res9: "89754e64993ffff",
      time_window: "90d",
    },
    statements: [
      {
        text: "Observed 6 persisted TruthLayer valuations matching the selected filters.",
        evidence: ["valuation_snapshots:val-001", "valuation_snapshots:val-002"],
      },
      {
        text: "Median observed fair value is EGP 4,450,000.",
        evidence: ["valuation_snapshots:val-003"],
      },
      {
        text: "Comparable density is High with a median comparable count of 6.",
        evidence: ["shadow_logs:val-001", "comparable_evidence:val-004"],
      },
    ],
    traceability_note:
      "Descriptive analytics only. Every statement is derived from persisted tenant-scoped TruthLayer records.",
  },
  data_sources_used: [
    "valuation_snapshots",
    "prediction_logs",
    "shadow_logs",
    "tool_events",
    "workspace_history",
    "comparable_evidence",
    "scenario_history",
  ],
  timestamp: "2026-06-10T00:00:00Z",
  source: "TruthLayer",
};

export const sampleSparseMarketInsightResponse: MarketInsightToolResponse = {
  ...sampleMarketInsightResponse,
  market_summary: "Observed 1 persisted TruthLayer valuation in this workspace history.",
  valuation_volume: 1,
  confidence_distribution: {
    valuation_count: 1,
    counts: {
      Unknown: 1,
    },
    predominant_level: "Unknown",
  },
  fair_value_distribution: {
    valuation_count: 1,
    minimum_fair_value: 3900000,
    median_fair_value: 3900000,
    maximum_fair_value: 3900000,
  },
  comparable_density: {
    valuation_count: 1,
    minimum_comparable_count: 0,
    median_comparable_count: 0,
    maximum_comparable_count: 0,
    density_level: "Sparse",
    measurement_sources: {
      shadow_logs: 1,
    },
  },
  active_compounds: [
    {
      name: "Nile Quarter",
      valuation_count: 1,
      median_fair_value: 3900000,
      confidence_distribution: {
        Unknown: 1,
      },
      comparable_density: "Sparse",
      median_comparable_count: 0,
    },
  ],
  active_areas: [],
  evidence_summary: {
    ...sampleMarketInsightResponse.evidence_summary,
    valuation_ids: ["val-001"],
    source_record_counts: {
      valuation_snapshots: 1,
      prediction_logs: 1,
      shadow_logs: 1,
      comparable_evidence: 0,
      tool_events: 1,
      workspace_history: 1,
      scenario_history: 0,
    },
    statements: [
      {
        text: "Observed 1 persisted TruthLayer valuation matching the selected filters.",
        evidence: ["valuation_snapshots:val-001"],
      },
      {
        text: "Comparable density is Sparse with a median comparable count of 0.",
        evidence: ["shadow_logs:val-001"],
      },
    ],
  },
  data_sources_used: ["valuation_snapshots", "prediction_logs", "shadow_logs", "tool_events", "workspace_history"],
};

export const sampleEmptyMarketInsightResponse: MarketInsightToolResponse = {
  ...sampleMarketInsightResponse,
  market_summary: "No persisted TruthLayer valuations match these filters.",
  valuation_volume: 0,
  confidence_distribution: {
    valuation_count: 0,
    counts: {},
    predominant_level: null,
  },
  fair_value_distribution: {
    valuation_count: 0,
    minimum_fair_value: null,
    median_fair_value: null,
    maximum_fair_value: null,
  },
  comparable_density: {
    valuation_count: 0,
    minimum_comparable_count: null,
    median_comparable_count: null,
    maximum_comparable_count: null,
    density_level: "Insufficient Evidence",
    measurement_sources: {},
  },
  active_compounds: [],
  active_areas: [],
  evidence_summary: {
    valuation_ids: [],
    source_record_counts: {
      valuation_snapshots: 0,
      prediction_logs: 0,
      shadow_logs: 0,
      comparable_evidence: 0,
      tool_events: 0,
      workspace_history: 0,
      scenario_history: 0,
    },
    filters_used: {
      workspace_id: 11,
      compound_name: "Unknown Compound",
      time_window: "30d",
    },
    statements: [
      {
        text: "No persisted TruthLayer valuations match the selected filters.",
        evidence: ["valuation_snapshots:workspace_id=11"],
      },
    ],
    traceability_note:
      "Descriptive analytics only. Every statement is derived from persisted tenant-scoped TruthLayer records.",
  },
  data_sources_used: ["valuation_snapshots", "prediction_logs", "shadow_logs", "tool_events", "workspace_history"],
};

export const sampleCopilotResponse: CopilotOrchestratorResponse = {
  runtime_id: "COPILOT_ORCHESTRATOR_LLM_V1",
  response_id: "narration_response_fixture",
  intent: "INVESTMENT",
  status: "DETERMINISTIC_ONLY",
  delivery_mode: "DETERMINISTIC_FALLBACK",
  citation_package: {
    valuation_ids: ["val-investment-1"],
    tool_event_ids: [],
    comparable_ids: ["scenario-comp-1"],
    unavailable_optional_citation_types: ["tool_event_id"],
  },
  response: {
    schema_version: "1.0",
    composition_status: "SUCCESS",
    tool_outputs: [
      {
        planned_tool: "INVESTMENT_TOOL",
        tool_name: "investment",
        payload: sampleInvestmentResponse,
        ordering_metadata: {
          order_index: 0,
          parallel_group_index: null,
        },
      },
    ],
    failed_tools: [],
    full_evidence: {
      comparables: [
        {
          planned_tool: "INVESTMENT_TOOL",
          comparable: {
            comparable_id: "scenario-comp-1",
            price: 88000,
          },
        },
      ],
      feature_drivers: [],
      market_insights: [],
    },
    citations: {
      valuation_ids: ["val-investment-1"],
      tool_event_ids: [],
      comparable_ids: ["scenario-comp-1"],
      unavailable_optional_citation_types: ["tool_event_id"],
    },
  },
  audit: {
    plan_id: "plan_fixture",
    execution_id: "exec_fixture",
    composition_status: "SUCCESS",
    memory_id: "memory_fixture",
    memory_status: "SUCCESS",
    narration_status: "DETERMINISTIC_ONLY",
  },
};
