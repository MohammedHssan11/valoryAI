from __future__ import annotations

from typing import Any

from app.core.property_features import (
    amenity_similarity,
    floor_band,
    known_amenity_names,
    normalize_match_text,
    unknown_amenity_codes,
)
from app.pricing.contracts import category_contract


FEATURE_SCORE_WEIGHTS = {
    "amenities": 0.70,
    "furnishing": 0.10,
    "compound": 0.10,
    "floor": 0.05,
    "view": 0.03,
    "building_quality": 0.02,
}


def _feature_score_weights(property_category: str | None) -> dict[str, float]:
    if property_category is None:
        return FEATURE_SCORE_WEIGHTS
    return category_contract(property_category).feature_score_weights


def _same_text_score(target: Any, comp: Any) -> float | None:
    target_text = normalize_match_text(target)
    if target_text is None:
        return None
    comp_text = normalize_match_text(comp)
    if comp_text is None:
        return None
    return 1.0 if target_text == comp_text else 0.0


def _floor_score(target: Any, comp: Any) -> float | None:
    target_band = floor_band(target)
    if target_band is None:
        return None
    comp_band = floor_band(comp)
    if comp_band is None:
        return None
    return 1.0 if target_band == comp_band else 0.0


def _amenities_for_features(features: dict[str, Any]) -> Any:
    return features.get("normalized_amenities") or features.get("amenities") or []


def compute_feature_similarity(
    target: dict[str, Any] | None,
    comp: dict[str, Any],
    property_category: str | None = None,
) -> dict[str, Any]:
    target = target or {}
    score_weights = _feature_score_weights(property_category)
    components: dict[str, float] = {}
    details: dict[str, Any] = {
        "matched_amenities": [],
        "missing_amenities": [],
        "extra_amenities": [],
        "target_unknown_amenity_codes": unknown_amenity_codes(target.get("amenities", [])),
        "comp_unknown_amenity_codes": comp.get("unknown_amenity_codes")
        or unknown_amenity_codes(comp.get("amenities", [])),
    }

    target_amenities = _amenities_for_features(target)
    comp_amenities = _amenities_for_features(comp)
    if known_amenity_names(target_amenities):
        amenity = amenity_similarity(target_amenities, comp_amenities, property_category=property_category)
        components["amenities"] = amenity["score"]
        details.update(
            {
                "matched_amenities": amenity["matched"],
                "missing_amenities": amenity["missing"],
                "extra_amenities": amenity["extra"],
                "matched_amenity_symbols": amenity.get("matched_symbols", []),
                "missing_amenity_symbols": amenity.get("missing_symbols", []),
                "extra_amenity_symbols": amenity.get("extra_symbols", []),
                "amenity_score": amenity["score"],
                "amenity_weighted_union": amenity.get("weighted_union"),
                "amenity_weighted_intersection": amenity.get("weighted_intersection"),
            }
        )

    optional_text_fields = {
        "furnishing": ("furnishing_status", "furnishing_match"),
        "compound": ("compound_name", "compound_match"),
        "view": ("view_type", "view_match"),
        "building_quality": ("building_quality", "building_quality_match"),
    }
    for component_name, (field_name, detail_name) in optional_text_fields.items():
        score = _same_text_score(target.get(field_name), comp.get(field_name))
        if score is not None:
            components[component_name] = score
            details[detail_name] = bool(score)

    score = _floor_score(target.get("floor_number"), comp.get("floor_number"))
    if score is not None:
        components["floor"] = score
        details["floor_band_match"] = bool(score)

    total_component_weight = sum(score_weights.get(name, 0.0) for name in components)
    if total_component_weight <= 0:
        return {
            "score": None,
            "components": components,
            "details": details,
            "applied": False,
        }

    weighted_score = sum(
        components[name] * score_weights.get(name, 0.0)
        for name in components
    ) / total_component_weight
    return {
        "score": max(0.0, min(1.0, float(weighted_score))),
        "components": {name: float(value) for name, value in components.items()},
        "details": {
            **details,
            "property_category": property_category,
            "component_weight_profile": {
                name: float(score_weights.get(name, 0.0))
                for name in components
            },
        },
        "applied": True,
    }
