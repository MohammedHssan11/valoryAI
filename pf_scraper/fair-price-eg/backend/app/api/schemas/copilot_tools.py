from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class ValuationToolRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    property_id: int = Field(gt=0)
    scenario_id: int | None = Field(default=None, gt=0)


class PriceRange(BaseModel):
    low: int
    high: int


class ValuationToolResponse(BaseModel):
    tool_name: Literal["valuation"] = "valuation"
    valuation_id: str
    fair_price: int
    price_range: PriceRange
    confidence_level: str
    engine_used: str
    routing_reason: str
    timestamp: datetime
    source: Literal["TruthLayer"] = "TruthLayer"


class ExplainabilityToolRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    valuation_id: str = Field(min_length=1, max_length=80)


class ExplainabilityToolResponse(BaseModel):
    tool_name: Literal["explainability"] = "explainability"
    valuation_id: str
    summary: str
    why_this_price: str
    strongest_factors: str
    confidence_reason: str
    fairness_status: str
    feature_drivers: list[dict[str, Any]]
    comparable_evidence: list[dict[str, Any]]
    timestamp: datetime
    source: Literal["TruthLayer"] = "TruthLayer"


class ComparableToolRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    property_id: int = Field(gt=0)
    scenario_id: int | None = Field(default=None, gt=0)
    valuation_id: str | None = Field(default=None, min_length=1, max_length=80)


class ComparableToolItem(BaseModel):
    comparable_id: str
    price: int
    size_sqm: float
    bedrooms: int
    bathrooms: int
    compound_name: str | None = None
    distance_km: float
    similarity_reason: str | None = None
    source: Literal["TruthLayer"] = "TruthLayer"


class ComparableToolResponse(BaseModel):
    tool_name: Literal["comparable"] = "comparable"
    valuation_id: str
    comparable_count: int
    comparables: list[ComparableToolItem]
    timestamp: datetime
    source: Literal["TruthLayer"] = "TruthLayer"


class FairnessToolRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    property_id: int = Field(gt=0)
    scenario_id: int | None = Field(default=None, gt=0)
    target_price_egp: int = Field(gt=0)


class FairnessToolResponse(BaseModel):
    tool_name: Literal["fairness"] = "fairness"
    valuation_id: str
    fair_price: int
    target_price: int
    fairness_status: Literal["Below Fair Value", "Within Fair Value", "Above Fair Value"]
    confidence_level: str
    confidence_reason: str
    timestamp: datetime
    source: Literal["TruthLayer"] = "TruthLayer"


class WhatIfToolRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    property_id: int = Field(gt=0)
    scenario_id: int | None = Field(default=None, gt=0)
    modifications: dict[str, Any]

    @model_validator(mode="after")
    def validate_modifications(self):
        if not self.modifications:
            raise ValueError("modifications must include at least one property change")
        return self


class FeatureChange(BaseModel):
    feature: str
    before: Any = None
    after: Any = None
    unit: str | None = None


class FeatureChanges(BaseModel):
    added: list[FeatureChange] = Field(default_factory=list)
    removed: list[FeatureChange] = Field(default_factory=list)
    modified: list[FeatureChange] = Field(default_factory=list)


class WhatIfToolResponse(BaseModel):
    tool_name: Literal["what_if"] = "what_if"
    base_valuation: int
    scenario_valuation: int
    base_valuation_id: str
    scenario_valuation_id: str
    fairness_valuation_id: str
    delta_value: int
    delta_percentage: float
    fairness_status: Literal["Below Fair Value", "Within Fair Value", "Above Fair Value"]
    confidence_level: str
    assumptions_used: list[str]
    feature_changes: FeatureChanges
    explainability: ExplainabilityToolResponse
    comparables: ComparableToolResponse
    timestamp: datetime
    source: Literal["TruthLayer"] = "TruthLayer"


class NegotiationToolRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    property_id: int = Field(gt=0)
    scenario_id: int | None = Field(default=None, gt=0)
    asking_price_egp: int = Field(gt=0)
    what_if_modifications: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_what_if_modifications(self):
        if self.what_if_modifications is not None and not self.what_if_modifications:
            raise ValueError("what_if_modifications must include at least one property change")
        return self


class NegotiationEvidenceReference(BaseModel):
    source_tool: Literal["input", "valuation", "explainability", "comparable", "fairness", "negotiation", "what_if"]
    valuation_id: str | None = None
    field: str
    comparable_id: str | None = None


class BrokerTalkingPoint(BaseModel):
    text: str
    evidence: list[NegotiationEvidenceReference]


class NegotiationEvidenceSummary(BaseModel):
    valuation_id: str
    price_range: PriceRange
    explainability_summary: str
    why_this_price: str
    strongest_factors: str
    source: Literal["TruthLayer"] = "TruthLayer"


class NegotiationComparableSummary(BaseModel):
    valuation_id: str
    comparable_count: int
    comparable_ids: list[str]
    observed_prices: list[int]
    lowest_observed_price: int | None = None
    highest_observed_price: int | None = None
    source: Literal["TruthLayer"] = "TruthLayer"


class RecommendedOfferBand(BaseModel):
    low: int | None = None
    high: int | None = None
    derivation: str
    comparable_ids_used: list[str] = Field(default_factory=list)
    evidence: list[NegotiationEvidenceReference]
    source: Literal["TruthLayer-derived"] = "TruthLayer-derived"


class NegotiationWhatIfSummary(BaseModel):
    base_valuation: int
    scenario_valuation: int
    base_valuation_id: str
    scenario_valuation_id: str
    delta_value: int
    delta_percentage: float
    fairness_status: Literal["Below Fair Value", "Within Fair Value", "Above Fair Value"]
    assumptions_used: list[str]
    feature_changes: FeatureChanges
    source: Literal["TruthLayer"] = "TruthLayer"


class NegotiationToolResponse(BaseModel):
    tool_name: Literal["negotiation"] = "negotiation"
    valuation_id: str
    asking_price: int
    fair_price: int
    fairness_status: Literal["Below Fair Value", "Within Fair Value", "Above Fair Value"]
    price_gap: int
    price_gap_percentage: float
    confidence_level: str
    confidence_reason: str
    negotiation_position: Literal[
        "Strong Buy Opportunity",
        "Negotiation Recommended",
        "Fair Market Position",
        "Premium Justified",
        "Overpriced",
    ]
    negotiation_position_reason: str
    negotiation_position_evidence: list[NegotiationEvidenceReference]
    broker_talking_points: list[BrokerTalkingPoint]
    evidence_summary: NegotiationEvidenceSummary
    comparable_summary: NegotiationComparableSummary
    recommended_offer_band: RecommendedOfferBand
    risk_notes: list[BrokerTalkingPoint]
    what_if_analysis: NegotiationWhatIfSummary | None = None
    timestamp: datetime
    source: Literal["TruthLayer"] = "TruthLayer"


class InvestmentToolRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    property_id: int = Field(gt=0)
    scenario_id: int | None = Field(default=None, gt=0)
    asking_price_egp: int = Field(gt=0)
    what_if_modifications: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_what_if_modifications(self):
        if self.what_if_modifications is not None and not self.what_if_modifications:
            raise ValueError("what_if_modifications must include at least one property change")
        return self


class InvestmentFinding(BaseModel):
    text: str
    evidence: list[NegotiationEvidenceReference]


class InvestmentNegotiationSummary(BaseModel):
    negotiation_position: Literal[
        "Strong Buy Opportunity",
        "Negotiation Recommended",
        "Fair Market Position",
        "Premium Justified",
        "Overpriced",
    ]
    negotiation_position_reason: str
    recommended_offer_band: RecommendedOfferBand
    broker_talking_points: list[BrokerTalkingPoint]
    source: Literal["TruthLayer"] = "TruthLayer"


class InvestmentWhatIfSummary(BaseModel):
    status: Literal["Available", "Insufficient Evidence"]
    reason: str
    analysis: NegotiationWhatIfSummary | None = None
    source: Literal["TruthLayer", "Insufficient Evidence"]


class InvestmentToolResponse(BaseModel):
    tool_name: Literal["investment"] = "investment"
    valuation_id: str
    asking_price: int
    fair_price: int
    fairness_status: Literal["Below Fair Value", "Within Fair Value", "Above Fair Value"]
    price_gap: int
    price_gap_percentage: float
    investment_position: Literal[
        "Strong Opportunity",
        "Moderate Opportunity",
        "Fairly Priced",
        "Caution",
        "High Risk",
    ]
    investment_position_reason: str
    investment_position_evidence: list[NegotiationEvidenceReference]
    confidence_level: str
    confidence_reason: str
    investment_summary: str
    strengths: list[InvestmentFinding]
    risks: list[InvestmentFinding]
    evidence_summary: NegotiationEvidenceSummary
    comparable_summary: NegotiationComparableSummary
    negotiation_summary: InvestmentNegotiationSummary
    what_if_summary: InvestmentWhatIfSummary
    timestamp: datetime
    source: Literal["TruthLayer"] = "TruthLayer"


class MarketInsightToolRequest(BaseModel):
    workspace_id: int = Field(gt=0)
    compound_name: str | None = Field(default=None, min_length=1, max_length=255)
    h3_res9: str | None = Field(default=None, min_length=1, max_length=32)
    property_type: str | None = Field(default=None, min_length=1, max_length=120)
    time_window: str | None = Field(default=None, pattern=r"^(all|[1-9][0-9]*d)$")


class MarketInsightConfidenceDistribution(BaseModel):
    valuation_count: int
    counts: dict[str, int]
    predominant_level: str | None = None


class MarketInsightFairValueDistribution(BaseModel):
    valuation_count: int
    minimum_fair_value: float | None = None
    median_fair_value: float | None = None
    maximum_fair_value: float | None = None


class MarketInsightComparableDensity(BaseModel):
    valuation_count: int
    minimum_comparable_count: int | None = None
    median_comparable_count: float | None = None
    maximum_comparable_count: int | None = None
    density_level: Literal["High", "Moderate", "Sparse", "Insufficient Evidence"]
    measurement_sources: dict[str, int]


class MarketInsightSegment(BaseModel):
    name: str
    valuation_count: int
    median_fair_value: float
    confidence_distribution: dict[str, int]
    comparable_density: Literal["High", "Moderate", "Sparse", "Insufficient Evidence"]
    median_comparable_count: float | None = None


class MarketInsightStatement(BaseModel):
    text: str
    evidence: list[str]


class MarketInsightEvidenceSummary(BaseModel):
    valuation_ids: list[str]
    source_record_counts: dict[str, int]
    filters_used: dict[str, Any]
    statements: list[MarketInsightStatement]
    traceability_note: str


class MarketInsightToolResponse(BaseModel):
    tool_name: Literal["market_insight"] = "market_insight"
    market_summary: str
    valuation_volume: int
    confidence_distribution: MarketInsightConfidenceDistribution
    fair_value_distribution: MarketInsightFairValueDistribution
    comparable_density: MarketInsightComparableDensity
    active_compounds: list[MarketInsightSegment]
    active_areas: list[MarketInsightSegment]
    evidence_summary: MarketInsightEvidenceSummary
    data_sources_used: list[str]
    timestamp: datetime
    source: Literal["TruthLayer"] = "TruthLayer"
