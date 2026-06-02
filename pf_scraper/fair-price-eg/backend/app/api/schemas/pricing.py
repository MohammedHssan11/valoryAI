from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.config import settings
from enum import Enum

from app.core.enums import ConfidenceLevel, PriceFlag, PropertyCategory, PropertyType
from app.pricing.contracts import category_contract, normalize_property_category


class LocationMode(str, Enum):
    MANUAL_COORDINATES = "manual_coordinates"
    ADDRESS_RESOLUTION = "address_resolution"
    CANONICAL_ENTITY = "canonical_entity"


class RentFairPriceRequest(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "lat": 30.0444,
                    "lng": 31.2357,
                    "property_type": "Apartment",
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "size_sqm": 150,
                    "target_price_egp": 95000,
                    "amenities": ["balcony", "security"],
                    "furnishing_status": "furnished",
                    "floor_number": 8,
                    "compound_name": "Nile Quarter",
                    "view_type": "river",
                    "building_quality": "premium",
                }
            ]
        },
    )

    location_mode: Optional[LocationMode] = Field(default=None, description="Explicit location grounding mode.")
    address: Optional[str] = Field(default=None, description="Natural address string for location resolution.")
    canonical_entity_id: Optional[str] = Field(default=None, description="Stable canonical geospatial entity id.")
    lat: Optional[float] = Field(default=None, ge=-90, le=90, description="Property latitude in WGS84 decimal degrees.")
    lng: Optional[float] = Field(default=None, ge=-180, le=180, description="Property longitude in WGS84 decimal degrees.")
    property_type: PropertyType = Field(description="Stable ValorAI property type enum value.")
    property_category: PropertyCategory = Field(
        default=PropertyCategory.RESIDENTIAL_RENT,
        description="Governed valuation category contract used for retrieval, weighting, confidence, and explainability.",
    )
    bedrooms: Optional[int] = Field(default=None, ge=0, le=settings.MAX_ROOM_COUNT, description="Bedroom count when known.")
    bathrooms: Optional[int] = Field(default=None, ge=0, le=settings.MAX_ROOM_COUNT, description="Bathroom count when known.")
    size_sqm: float = Field(gt=0, description="Usable property size in square meters.")
    target_price_egp: Optional[int] = Field(
        default=None,
        gt=0,
        description="Optional asking price/rent used to flag too-high, too-low, or fair target pricing.",
    )
    amenities: List[str] = Field(default_factory=list, description="Raw amenity names or stable provider codes.")
    furnishing_status: Optional[str] = Field(default=None, description="Structured furnishing signal, when known.")
    floor_number: Optional[int] = Field(default=None, ge=-5, le=200, description="Floor number, including negative parking/basement levels.")
    compound_name: Optional[str] = Field(default=None, description="Compound or project name when applicable.")
    view_type: Optional[str] = Field(default=None, description="View signal such as river, garden, open, or street.")
    building_quality: Optional[str] = Field(default=None, description="Conservative building quality signal.")

    @field_validator("property_type", mode="before")
    @classmethod
    def normalize_property_type(cls, value):
        if isinstance(value, str):
            normalized = " ".join(value.strip().split())
            for item in PropertyType:
                if item.value.lower() == normalized.lower():
                    return item.value
        return value

    @field_validator("property_category", mode="before")
    @classmethod
    def normalize_category(cls, value):
        return normalize_property_category(value).value

    @field_validator("address", "canonical_entity_id", mode="before")
    @classmethod
    def normalize_optional_text(cls, value):
        if isinstance(value, str):
            text = " ".join(value.strip().split())
            return text or None
        return value

    @model_validator(mode="after")
    def validate_location(self):
        contract = category_contract(self.property_category)
        if self.property_type not in contract.compatible_property_types:
            raise ValueError(
                f"Property type '{self.property_type}' is not valid for category '{contract.label}'."
            )
        if self.size_sqm > contract.guardrails.max_size_sqm:
            raise ValueError(
                f"size_sqm exceeds the {contract.label} category maximum of {contract.guardrails.max_size_sqm}."
            )
        if self.target_price_egp is not None and self.target_price_egp > contract.guardrails.max_target_price_egp:
            raise ValueError(
                f"target_price_egp exceeds the {contract.label} category maximum of {contract.guardrails.max_target_price_egp}."
            )

        has_address = bool(self.address)
        has_coords = self.lat is not None or self.lng is not None
        has_complete_coords = self.lat is not None and self.lng is not None
        has_entity = bool(self.canonical_entity_id)

        if self.location_mode is None:
            populated = sum([has_address, has_complete_coords, has_entity])
            if populated == 0:
                raise ValueError("A location input is required.")
            if populated > 1 or has_coords and not has_complete_coords:
                raise ValueError("location_mode is required when location inputs are ambiguous.")
            if has_address:
                self.location_mode = LocationMode.ADDRESS_RESOLUTION
            elif has_entity:
                self.location_mode = LocationMode.CANONICAL_ENTITY
            else:
                self.location_mode = LocationMode.MANUAL_COORDINATES

        mode = LocationMode(self.location_mode)
        if mode == LocationMode.ADDRESS_RESOLUTION:
            if not has_address:
                raise ValueError("address is required for address_resolution mode.")
            if has_coords or has_entity:
                raise ValueError("address_resolution mode cannot include manual coordinates or canonical_entity_id.")
        elif mode == LocationMode.MANUAL_COORDINATES:
            if not has_complete_coords:
                raise ValueError("lat and lng are required for manual_coordinates mode.")
            if has_address or has_entity:
                raise ValueError("manual_coordinates mode cannot include address or canonical_entity_id.")
        elif mode == LocationMode.CANONICAL_ENTITY:
            if not has_entity:
                raise ValueError("canonical_entity_id is required for canonical_entity mode.")
            if has_address or has_coords:
                raise ValueError("canonical_entity mode cannot include address or manual coordinates.")
        return self


class CompItem(BaseModel):
    listing_id: str = Field(description="Stable comparable listing identifier.")
    price_egp: int = Field(description="Comparable monthly rent in EGP.")
    size_sqm: Optional[float] = Field(default=None, description="Comparable size in square meters.")
    price_per_sqm: Optional[float] = Field(default=None, description="Comparable monthly rent per square meter.")
    property_type: Optional[str] = Field(default=None, description="Comparable property type.")
    bedrooms: Optional[int] = Field(default=None, description="Comparable bedroom count.")
    bathrooms: Optional[int] = Field(default=None, description="Comparable bathroom count.")
    area_id: Optional[int] = Field(default=None, description="Resolved comparable area identifier.")
    area_name: Optional[str] = Field(default=None, description="Resolved comparable area name.")
    lat: Optional[float] = Field(default=None, description="Comparable latitude in WGS84 decimal degrees.")
    lng: Optional[float] = Field(default=None, description="Comparable longitude in WGS84 decimal degrees.")
    location_text: Optional[str] = Field(default=None, description="Provider location label.")
    images_count: Optional[int] = Field(default=None, description="Provider image count for evidence quality display.")
    retrieval_tier: Optional[int] = Field(default=None, description="Deterministic retrieval tier that returned this comparable.")
    tier_label: Optional[str] = Field(default=None, description="Human-readable retrieval tier label.")
    reason_code: Optional[str] = Field(default=None, description="Stable explainability reason code for retrieval.")
    radius_m: Optional[int] = Field(default=None, description="Retrieval radius that admitted this comparable.")
    dist_m: Optional[float] = Field(default=None, description="Distance from target in meters.")
    age_days: Optional[float] = Field(default=None, description="Age of listing snapshot in days.")
    weight: Optional[float] = Field(default=None, description="Final deterministic comparable weight.")
    weight_components: Dict[str, float] = Field(default_factory=dict, description="Component-level weight inputs.")
    weighted_contribution: Optional[float] = Field(default=None, description="Share of total deterministic comparable weight.")
    confidence_contribution: Optional[float] = Field(default=None, description="Comparable evidence contribution adjusted by evidence quality.")
    similarity_score: Optional[float] = Field(default=None, description="Composite deterministic similarity score for visual explainability.")
    geographic_similarity: Optional[float] = Field(default=None, description="Distance-derived geographic similarity component.")
    distance_weight: Optional[float] = Field(default=None, description="Distance component used in deterministic weighting.")
    recency_weight: Optional[float] = Field(default=None, description="Recency component used in deterministic weighting.")
    evidence_rank: Optional[int] = Field(default=None, description="Stable evidence rank after deterministic top-comps sorting.")
    property_category: Optional[str] = None
    amenities: List[Dict[str, Any]] = Field(default_factory=list)
    normalized_amenities: List[str] = Field(default_factory=list)
    canonical_amenity_symbols: List[str] = Field(default_factory=list)
    unknown_amenity_codes: List[str] = Field(default_factory=list)
    furnishing_status: Optional[str] = None
    floor_number: Optional[int] = None
    compound_name: Optional[str] = None
    view_type: Optional[str] = None
    building_quality: Optional[str] = None
    feature_similarity: Optional[float] = None
    feature_similarity_components: Dict[str, float] = Field(default_factory=dict)
    feature_explanation: Dict[str, Any] = Field(default_factory=dict)
    feature_overlap: Dict[str, Any] = Field(default_factory=dict)
    amenity_similarity: Optional[float] = None
    amenity_explanation: Dict[str, Any] = Field(default_factory=dict)
    amenity_metadata: List[Dict[str, Any]] = Field(default_factory=list)
    filter_status: Dict[str, Any] = Field(default_factory=dict)


class ExplanationItem(BaseModel):
    reason_code: str = Field(description="Stable machine-readable explanation reason code.")
    weight: Optional[float] = Field(default=None, description="Optional score or weight associated with the reason.")
    details: Dict[str, Any] = Field(default_factory=dict, description="Structured explanation metadata.")


class ConfidenceDTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    score: float = Field(ge=0, le=1, description="Deterministic confidence score in the [0, 1] range.")
    label: ConfidenceLevel = Field(description="Stable confidence label: High, Medium, or Low.")
    factors: Dict[str, float] = Field(default_factory=dict, description="Normalized confidence factor contributions.")
    dimensions: Dict[str, Any] = Field(default_factory=dict, description="Independent confidence dimensions used to cap final score.")


class RetrievalStageItem(BaseModel):
    tier: Optional[int] = Field(default=None, description="Comparable retrieval tier attempted.")
    tier_label: Optional[str] = Field(default=None, description="Human-readable retrieval tier label.")
    reason_code: str = Field(description="Stable reason code for this retrieval stage.")
    scope: Optional[str] = Field(default=None, description="Spatial hierarchy scope attempted.")
    radius_m: Optional[int] = Field(default=None, description="Retrieval radius attempted in meters.")
    comps_found: int = Field(default=0, description="Comparables found at this retrieval stage.")
    threshold: Optional[int] = Field(default=None, description="Minimum comparable threshold for this tier.")
    shortfall: Optional[int] = Field(default=None, description="Threshold shortfall at this stage.")
    attempt_index: Optional[int] = Field(default=None, description="Deterministic retrieval attempt order.")
    status: Optional[str] = Field(default=None, description="Deterministic stage status.")
    selected: bool = Field(default=False, description="Whether this retrieval stage supplied authoritative comps.")
    radius_expansion_m: Optional[int] = Field(default=None, description="Radius expansion relative to the previous attempt.")


class ComparableEvidence(BaseModel):
    property_id: str
    price: int
    size_sqm: float
    bedrooms: int
    bathrooms: int
    furnishing_status: Optional[str]
    compound_name: Optional[str] = None
    distance_km: float
    similarity_score: float
    similarity_reason: Optional[str] = None
    listing_date: Optional[str] = None

class FeatureDriver(BaseModel):
    name: str
    direction: str
    strength: str

class ConfidenceExplanation(BaseModel):
    confidence_level: str
    confidence_reason: str

class FairnessExplanation(BaseModel):
    estimated_value: int
    asking_price: Optional[int]
    difference_amount: Optional[int]
    difference_percentage: Optional[float]
    status: str

class NarrativeExplanation(BaseModel):
    summary: str
    why_this_price: str
    strongest_factors: str
    confidence_reason: str

class ExplainabilityModel(BaseModel):
    router_explanation: str
    confidence_explanation: ConfidenceExplanation
    fairness_explanation: FairnessExplanation
    narrative_explanation: NarrativeExplanation
    comparable_evidence: List[ComparableEvidence]
    feature_drivers: List[FeatureDriver]

class WhatIfRequest(BaseModel):
    base_request_id: str
    size_change_sqm: Optional[float] = None
    bedrooms_change: Optional[int] = None
    furnishing_change: Optional[str] = None
    amenities_added: Optional[List[str]] = None
    amenities_removed: Optional[List[str]] = None

class WhatIfResponse(BaseModel):
    original_price: int
    new_price: int
    price_delta: int
    delta_explanation: str

class RentFairPriceResponse(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "fair_price_egp": 90000,
                    "range_low_egp": 82000,
                    "range_high_egp": 105000,
                    "flag": "OK",
                    "tier_used": 1,
                    "comps_count": 84,
                    "confidence": {
                        "score": 0.82,
                        "label": "High",
                        "factors": {
                            "count": 1.0,
                            "tier": 1.0,
                            "kept_ratio": 0.9,
                            "dispersion": 0.8,
                            "distance": 0.95,
                            "recency": 0.78,
                            "similarity": 0.92,
                        },
                    },
                    "explanation": [
                        "84 similar listings found using same compound/neighborhood around Central Cairo.",
                        "Fair price computed using weighted median (distance, size similarity, recency, and small structured-feature refinement when provided).",
                    ],
                    "explanation_trace": [
                        {
                            "reason_code": "SAME_AREA_MATCH",
                            "weight": None,
                            "details": {"tier": 1, "radius_m": 500, "comps_found": 84},
                        }
                    ],
                    "area": {"area_id": 10, "name": "Central Cairo"},
                    "debug": {},
                    "top_comps": [],
                }
            ]
        },
    )

    fair_price_egp: int = Field(description="Deterministic weighted-median fair monthly rent in EGP.")
    range_low_egp: int = Field(description="Lower deterministic fair-rent band in EGP.")
    range_high_egp: int = Field(description="Upper deterministic fair-rent band in EGP.")
    flag: PriceFlag = Field(description="Stable price flag comparing target rent to the fair band.")
    tier_used: int = Field(description="Comparable retrieval tier selected by the deterministic CMT engine.")
    comps_count: int = Field(description="Comparable count retained after guardrails and outlier filtering.")
    confidence: ConfidenceDTO = Field(description="Deterministic confidence score, label, and factor breakdown.")
    
    # Unified Contract Routing Fields
    engine_used: str = Field(default="UNKNOWN", description="The valuation engine selected by the router (e.g., 'CMT' or 'ML').")
    routing_reason: str = Field(default="UNKNOWN", description="The rule triggered by the router.")
    is_unseen_compound: bool = Field(default=False, description="Whether the compound was missing from the ML training set.")
    is_unseen_h3: bool = Field(default=False, description="Whether the H3 spatial hex was missing from the ML training set.")
    routing_trace: Dict[str, Any] = Field(default_factory=dict, description="Structured routing execution trace.")

    explainability: Optional[ExplainabilityModel] = Field(default=None, description="Detailed explainability model for Phase 5.4")

    explanation: List[str] = Field(description="Human-readable valuation explanation.")
    explanation_trace: List[ExplanationItem] = Field(default_factory=list, description="Structured explainability trace.")
    retrieval_trace: List[RetrievalStageItem] = Field(default_factory=list, description="Deterministic comparable retrieval stage trace.")
    spatial_diagnostics: Dict[str, Any] = Field(default_factory=dict, description="Spatial evidence diagnostics for map rendering.")
    evidence_summary: Dict[str, Any] = Field(default_factory=dict, description="Auditable comparable and filtering evidence summary.")
    property_category: PropertyCategory = Field(
        default=PropertyCategory.RESIDENTIAL_RENT,
        description="Governed property-category contract used for this valuation.",
    )
    valuation_contract: Dict[str, Any] = Field(default_factory=dict, description="Deterministic category valuation contract metadata.")
    amenity_intelligence: Dict[str, Any] = Field(default_factory=dict, description="Governed amenity normalization, weighting, and explainability metadata.")

    area: Dict[str, Any] = Field(default_factory=dict, description="Resolved target area metadata.")
    resolved_location: Dict[str, Any] = Field(default_factory=dict, description="Detailed location resolution metadata including coordinates and precision.")
    debug: Dict[str, Any] = Field(default_factory=dict, description="Debug metadata only populated when DEBUG is enabled.")
    top_comps: List[CompItem] = Field(default_factory=list, description="Top weighted comparable evidence returned to clients.")
