from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.enums import ListingCategory, PropertyCategory, PropertyType, RentalPeriod


@dataclass(frozen=True)
class CategoryGuardrails:
    min_price_egp: int
    max_price_egp: int
    max_target_price_egp: int
    max_size_sqm: float
    min_price_per_sqm: float
    max_price_per_sqm: float

    def model_dump(self) -> dict[str, Any]:
        return {
            "min_price_egp": self.min_price_egp,
            "max_price_egp": self.max_price_egp,
            "max_target_price_egp": self.max_target_price_egp,
            "max_size_sqm": self.max_size_sqm,
            "min_price_per_sqm": self.min_price_per_sqm,
            "max_price_per_sqm": self.max_price_per_sqm,
        }


@dataclass(frozen=True)
class CategoryValuationContract:
    category: PropertyCategory
    label: str
    listing_category: ListingCategory
    period: RentalPeriod
    value_basis: str
    compatible_property_types: tuple[str, ...]
    guardrails: CategoryGuardrails
    radius_multiplier: float
    stale_days_multiplier: float
    match_threshold: int
    size_tolerance_by_tier: dict[int, tuple[float, float]]
    feature_score_weights: dict[str, float]
    property_type_mismatch_weight: float
    confidence_weights: dict[str, float]
    confidence_min_comps_high: int
    critical_amenity_weight: float
    institutional_notes: tuple[str, ...]

    def size_bounds(self, tier: int, fallback_low: float, fallback_high: float) -> tuple[float, float]:
        return self.size_tolerance_by_tier.get(tier, (fallback_low, fallback_high))

    def radius_m(self, base_radius_m: int) -> int:
        return max(1, min(15000, int(round(base_radius_m * self.radius_multiplier))))

    def stale_days(self, base_stale_days: int) -> int:
        return max(1, int(round(base_stale_days * self.stale_days_multiplier)))

    def public_contract(self) -> dict[str, Any]:
        return {
            "category": self.category.value,
            "label": self.label,
            "listing_category": self.listing_category.value,
            "period": self.period.value,
            "value_basis": self.value_basis,
            "compatible_property_types": list(self.compatible_property_types),
            "valuation_constraints": self.guardrails.model_dump(),
            "retrieval_strategy": {
                "radius_multiplier": self.radius_multiplier,
                "stale_days_multiplier": self.stale_days_multiplier,
                "match_threshold": self.match_threshold,
                "size_tolerance_by_tier": {
                    str(tier): {"low": low, "high": high}
                    for tier, (low, high) in sorted(self.size_tolerance_by_tier.items())
                },
            },
            "feature_score_weights": dict(self.feature_score_weights),
            "confidence_weights": dict(self.confidence_weights),
            "critical_amenity_weight": self.critical_amenity_weight,
            "governance": {
                "deterministic_authority": True,
                "amenities_override_pricing": False,
                "llm_may_override": False,
            },
            "institutional_notes": list(self.institutional_notes),
        }


RESIDENTIAL_TYPES = (
    PropertyType.APARTMENT.value,
    PropertyType.BUNGALOW.value,
    PropertyType.CABIN.value,
    PropertyType.CHALET.value,
    PropertyType.DUPLEX.value,
    PropertyType.HOTEL_APARTMENT.value,
    PropertyType.IVILLA.value,
    PropertyType.PENTHOUSE.value,
    PropertyType.ROOF.value,
    PropertyType.TOWNHOUSE.value,
    PropertyType.TWIN_HOUSE.value,
    PropertyType.VILLA.value,
)

APARTMENT_SALE_TYPES = (
    PropertyType.APARTMENT.value,
    PropertyType.CHALET.value,
    PropertyType.DUPLEX.value,
    PropertyType.HOTEL_APARTMENT.value,
    PropertyType.PENTHOUSE.value,
    PropertyType.ROOF.value,
)

VILLA_TYPES = (
    PropertyType.VILLA.value,
    PropertyType.TOWNHOUSE.value,
    PropertyType.TWIN_HOUSE.value,
    PropertyType.IVILLA.value,
    PropertyType.PALACE.value,
)

OFFICE_TYPES = (
    PropertyType.OFFICE_SPACE.value,
    PropertyType.CO_WORKING_SPACE.value,
    PropertyType.FULL_FLOOR.value,
    PropertyType.HALF_FLOOR.value,
)

RETAIL_TYPES = (
    PropertyType.RETAIL.value,
    PropertyType.SHOP.value,
    PropertyType.SHOW_ROOM.value,
    PropertyType.RESTAURANT.value,
    PropertyType.CAFETERIA.value,
)

COMMERCIAL_TYPES = (
    PropertyType.CLINIC.value,
    PropertyType.FACTORY.value,
    PropertyType.MEDICAL_FACILITY.value,
    PropertyType.STAFF_ACCOMMODATION.value,
    PropertyType.WAREHOUSE.value,
    PropertyType.WHOLE_BUILDING.value,
)

LAND_TYPES = (PropertyType.LAND.value, PropertyType.FARM.value)


CONTRACTS: dict[PropertyCategory, CategoryValuationContract] = {
    PropertyCategory.RESIDENTIAL_RENT: CategoryValuationContract(
        category=PropertyCategory.RESIDENTIAL_RENT,
        label="Residential rent",
        listing_category=ListingCategory.RENT,
        period=RentalPeriod.MONTHLY,
        value_basis="monthly_rent",
        compatible_property_types=RESIDENTIAL_TYPES,
        guardrails=CategoryGuardrails(1000, 500_000, 500_000, 1000.0, 30.0, 20_000.0),
        radius_multiplier=1.0,
        stale_days_multiplier=1.0,
        match_threshold=40,
        size_tolerance_by_tier={
            1: (0.85, 1.15),
            2: (0.80, 1.20),
            3: (0.80, 1.20),
            4: (0.75, 1.25),
            5: (0.70, 1.30),
        },
        feature_score_weights={
            "amenities": 0.55,
            "furnishing": 0.18,
            "compound": 0.10,
            "floor": 0.07,
            "view": 0.05,
            "building_quality": 0.05,
        },
        property_type_mismatch_weight=0.60,
        confidence_weights={"base": 0.84, "distance": 0.05, "recency": 0.05, "similarity": 0.04, "amenity": 0.02},
        confidence_min_comps_high=80,
        critical_amenity_weight=0.04,
        institutional_notes=(
            "Furnishing, elevator, security, and compound signals primarily refine comparable realism.",
            "Amenity signals cannot directly alter the weighted-median rent result.",
        ),
    ),
    PropertyCategory.RESIDENTIAL_SALE: CategoryValuationContract(
        category=PropertyCategory.RESIDENTIAL_SALE,
        label="Residential sale",
        listing_category=ListingCategory.BUY,
        period=RentalPeriod.SALE,
        value_basis="sale_price",
        compatible_property_types=APARTMENT_SALE_TYPES,
        guardrails=CategoryGuardrails(100_000, 250_000_000, 250_000_000, 1500.0, 500.0, 1_500_000.0),
        radius_multiplier=1.10,
        stale_days_multiplier=1.60,
        match_threshold=30,
        size_tolerance_by_tier={
            1: (0.80, 1.20),
            2: (0.75, 1.25),
            3: (0.70, 1.30),
            4: (0.65, 1.35),
            5: (0.60, 1.45),
        },
        feature_score_weights={
            "amenities": 0.45,
            "furnishing": 0.08,
            "compound": 0.16,
            "floor": 0.08,
            "view": 0.10,
            "building_quality": 0.13,
        },
        property_type_mismatch_weight=0.55,
        confidence_weights={"base": 0.82, "distance": 0.05, "recency": 0.04, "similarity": 0.05, "amenity": 0.04},
        confidence_min_comps_high=70,
        critical_amenity_weight=0.04,
        institutional_notes=(
            "Sale contracts increase sensitivity to compound, view, and building-quality evidence.",
            "Sale price remains derived only from deterministic comparable price evidence.",
        ),
    ),
    PropertyCategory.VILLA_SALE: CategoryValuationContract(
        category=PropertyCategory.VILLA_SALE,
        label="Villa sale",
        listing_category=ListingCategory.BUY,
        period=RentalPeriod.SALE,
        value_basis="sale_price",
        compatible_property_types=VILLA_TYPES,
        guardrails=CategoryGuardrails(500_000, 800_000_000, 800_000_000, 5000.0, 250.0, 2_000_000.0),
        radius_multiplier=1.45,
        stale_days_multiplier=2.00,
        match_threshold=22,
        size_tolerance_by_tier={
            1: (0.70, 1.35),
            2: (0.65, 1.45),
            3: (0.60, 1.55),
            4: (0.55, 1.70),
            5: (0.50, 1.90),
        },
        feature_score_weights={
            "amenities": 0.58,
            "furnishing": 0.03,
            "compound": 0.12,
            "floor": 0.02,
            "view": 0.10,
            "building_quality": 0.15,
        },
        property_type_mismatch_weight=0.70,
        confidence_weights={"base": 0.80, "distance": 0.05, "recency": 0.04, "similarity": 0.05, "amenity": 0.06},
        confidence_min_comps_high=45,
        critical_amenity_weight=0.05,
        institutional_notes=(
            "Garden, pool, land, view, and compound evidence are high-salience villa comparability signals.",
            "Amenity differences adjust comparable weighting and confidence only.",
        ),
    ),
    PropertyCategory.OFFICE_RENT: CategoryValuationContract(
        category=PropertyCategory.OFFICE_RENT,
        label="Office rent",
        listing_category=ListingCategory.COMMERCIAL_RENT,
        period=RentalPeriod.MONTHLY,
        value_basis="monthly_rent",
        compatible_property_types=OFFICE_TYPES,
        guardrails=CategoryGuardrails(2000, 1_500_000, 1_500_000, 3000.0, 20.0, 30_000.0),
        radius_multiplier=1.25,
        stale_days_multiplier=1.50,
        match_threshold=25,
        size_tolerance_by_tier={
            1: (0.75, 1.25),
            2: (0.70, 1.35),
            3: (0.65, 1.45),
            4: (0.60, 1.60),
            5: (0.55, 1.80),
        },
        feature_score_weights={
            "amenities": 0.52,
            "furnishing": 0.02,
            "compound": 0.18,
            "floor": 0.14,
            "view": 0.02,
            "building_quality": 0.12,
        },
        property_type_mismatch_weight=0.72,
        confidence_weights={"base": 0.81, "distance": 0.06, "recency": 0.04, "similarity": 0.04, "amenity": 0.05},
        confidence_min_comps_high=50,
        critical_amenity_weight=0.05,
        institutional_notes=(
            "Parking, business-district fit, office infrastructure, and floor level are office weighting signals.",
            "The broker may discuss workplace utility but cannot create a separate office rent premium.",
        ),
    ),
    PropertyCategory.RETAIL_RENT: CategoryValuationContract(
        category=PropertyCategory.RETAIL_RENT,
        label="Retail rent",
        listing_category=ListingCategory.COMMERCIAL_RENT,
        period=RentalPeriod.MONTHLY,
        value_basis="monthly_rent",
        compatible_property_types=RETAIL_TYPES,
        guardrails=CategoryGuardrails(2000, 2_000_000, 2_000_000, 2500.0, 30.0, 60_000.0),
        radius_multiplier=1.15,
        stale_days_multiplier=1.35,
        match_threshold=25,
        size_tolerance_by_tier={
            1: (0.70, 1.35),
            2: (0.65, 1.45),
            3: (0.60, 1.60),
            4: (0.55, 1.75),
            5: (0.50, 2.00),
        },
        feature_score_weights={
            "amenities": 0.68,
            "furnishing": 0.01,
            "compound": 0.08,
            "floor": 0.08,
            "view": 0.08,
            "building_quality": 0.07,
        },
        property_type_mismatch_weight=0.68,
        confidence_weights={"base": 0.79, "distance": 0.06, "recency": 0.04, "similarity": 0.04, "amenity": 0.07},
        confidence_min_comps_high=45,
        critical_amenity_weight=0.06,
        institutional_notes=(
            "Frontage, visibility, and traffic exposure are high-salience retail comparability signals.",
            "Amenity retrieval refinement is allowed only when comparable depth remains sufficient.",
        ),
    ),
    PropertyCategory.COMMERCIAL_RENT: CategoryValuationContract(
        category=PropertyCategory.COMMERCIAL_RENT,
        label="Commercial rent",
        listing_category=ListingCategory.COMMERCIAL_RENT,
        period=RentalPeriod.MONTHLY,
        value_basis="monthly_rent",
        compatible_property_types=COMMERCIAL_TYPES,
        guardrails=CategoryGuardrails(2000, 5_000_000, 5_000_000, 10_000.0, 5.0, 40_000.0),
        radius_multiplier=1.60,
        stale_days_multiplier=2.00,
        match_threshold=20,
        size_tolerance_by_tier={
            1: (0.60, 1.55),
            2: (0.55, 1.70),
            3: (0.50, 1.90),
            4: (0.45, 2.20),
            5: (0.40, 2.50),
        },
        feature_score_weights={
            "amenities": 0.55,
            "furnishing": 0.01,
            "compound": 0.10,
            "floor": 0.04,
            "view": 0.02,
            "building_quality": 0.28,
        },
        property_type_mismatch_weight=0.70,
        confidence_weights={"base": 0.80, "distance": 0.05, "recency": 0.04, "similarity": 0.04, "amenity": 0.07},
        confidence_min_comps_high=40,
        critical_amenity_weight=0.05,
        institutional_notes=(
            "Infrastructure, access, size band, and commercial use class drive comparable weighting.",
            "Commercial evidence often requires wider spatial and stale-day retrieval windows.",
        ),
    ),
    PropertyCategory.LAND_SALE: CategoryValuationContract(
        category=PropertyCategory.LAND_SALE,
        label="Land sale",
        listing_category=ListingCategory.BUY,
        period=RentalPeriod.SALE,
        value_basis="sale_price",
        compatible_property_types=LAND_TYPES,
        guardrails=CategoryGuardrails(100_000, 3_000_000_000, 3_000_000_000, 100_000.0, 5.0, 1_000_000.0),
        radius_multiplier=1.80,
        stale_days_multiplier=2.50,
        match_threshold=18,
        size_tolerance_by_tier={
            1: (0.50, 1.80),
            2: (0.45, 2.10),
            3: (0.40, 2.50),
            4: (0.35, 3.00),
            5: (0.30, 3.50),
        },
        feature_score_weights={
            "amenities": 0.82,
            "furnishing": 0.00,
            "compound": 0.04,
            "floor": 0.00,
            "view": 0.02,
            "building_quality": 0.12,
        },
        property_type_mismatch_weight=0.35,
        confidence_weights={"base": 0.77, "distance": 0.05, "recency": 0.03, "similarity": 0.04, "amenity": 0.11},
        confidence_min_comps_high=35,
        critical_amenity_weight=0.06,
        institutional_notes=(
            "Zoning, frontage, geometry, and access are land comparability signals.",
            "Land valuation remains evidence-backed and does not infer planning upside beyond supplied symbols.",
        ),
    ),
}


def normalize_property_category(value: Any) -> PropertyCategory:
    if isinstance(value, PropertyCategory):
        return value
    if value is None:
        return PropertyCategory.RESIDENTIAL_RENT
    normalized = str(value).strip()
    aliases = {
        "rent": PropertyCategory.RESIDENTIAL_RENT,
        "residential": PropertyCategory.RESIDENTIAL_RENT,
        "residential_rent": PropertyCategory.RESIDENTIAL_RENT,
        "residentialrent": PropertyCategory.RESIDENTIAL_RENT,
        "residentialRent": PropertyCategory.RESIDENTIAL_RENT,
        "sale": PropertyCategory.RESIDENTIAL_SALE,
        "buy": PropertyCategory.RESIDENTIAL_SALE,
        "residential_sale": PropertyCategory.RESIDENTIAL_SALE,
        "residentialsale": PropertyCategory.RESIDENTIAL_SALE,
        "villas": PropertyCategory.VILLA_SALE,
        "villa": PropertyCategory.VILLA_SALE,
        "villa_sale": PropertyCategory.VILLA_SALE,
        "villasale": PropertyCategory.VILLA_SALE,
        "office": PropertyCategory.OFFICE_RENT,
        "offices": PropertyCategory.OFFICE_RENT,
        "office_rent": PropertyCategory.OFFICE_RENT,
        "officerent": PropertyCategory.OFFICE_RENT,
        "officeRent": PropertyCategory.OFFICE_RENT,
        "retail": PropertyCategory.RETAIL_RENT,
        "retail_rent": PropertyCategory.RETAIL_RENT,
        "retailrent": PropertyCategory.RETAIL_RENT,
        "commercial": PropertyCategory.COMMERCIAL_RENT,
        "commercial_rent": PropertyCategory.COMMERCIAL_RENT,
        "commercialrent": PropertyCategory.COMMERCIAL_RENT,
        "land": PropertyCategory.LAND_SALE,
        "land_sale": PropertyCategory.LAND_SALE,
        "landsale": PropertyCategory.LAND_SALE,
    }
    if normalized in aliases:
        return aliases[normalized]
    try:
        return PropertyCategory(normalized)
    except ValueError:
        raise ValueError(f"Invalid category: {normalized}")


def category_contract(value: Any) -> CategoryValuationContract:
    category = normalize_property_category(value)
    return CONTRACTS[category]


def public_category_contract(value: Any) -> dict[str, Any]:
    return category_contract(value).public_contract()

