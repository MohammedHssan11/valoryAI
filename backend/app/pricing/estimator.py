from decimal import Decimal
import math

from app.pricing.feature_similarity import compute_feature_similarity
from app.pricing.contracts import category_contract
from app.pricing.settings import WEIGHTING


def _to_float(x):
    if x is None:
        return None
    if isinstance(x, Decimal):
        return float(x)
    return float(x)


def _clamp_unit(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _w_distance(dist_m):
    dist_m = _to_float(dist_m)
    if dist_m is None:
        return _clamp_unit(WEIGHTING.distance_fallback)

    dist_m = max(dist_m, 0.0)
    return _clamp_unit(1.0 / (1.0 + (dist_m / WEIGHTING.distance_decay_m)))

def _w_size(size_sqm, target):
    size_sqm = _to_float(size_sqm)
    target = float(target)
    if size_sqm is None or target <= 0:
        return _clamp_unit(WEIGHTING.size_fallback)
    rel = abs(size_sqm - target) / target
    return _clamp_unit(1.0 - rel)

def _w_recency(age_days):
    age_days = _to_float(age_days)
    if age_days is None:
        return _clamp_unit(WEIGHTING.recency_fallback)
    age_days = max(age_days, 0.0)
    return _clamp_unit(math.exp(-age_days / WEIGHTING.recency_decay_days))


def _w_bathrooms(comp_bathrooms, target_bathrooms):
    if target_bathrooms is None:
        return 1.0
    if comp_bathrooms is None:
        return _clamp_unit(WEIGHTING.bathroom_fallback)
    return 1.0 if int(comp_bathrooms) == int(target_bathrooms) else _clamp_unit(WEIGHTING.bathroom_mismatch)


def _w_same_area(is_same_area):
    return 1.0 if bool(is_same_area) else _clamp_unit(WEIGHTING.non_same_area)


def _w_required_match(comp_value, target_value):
    if target_value is None:
        return 1.0
    if comp_value is None:
        return 0.0
    return 1.0 if comp_value == target_value else 0.0


def _w_property_type(comp_value, target_value, property_category):
    if target_value is None:
        return 1.0
    if comp_value is None:
        return 0.0
    if comp_value == target_value:
        return 1.0
    return _clamp_unit(category_contract(property_category).property_type_mismatch_weight)


def _w_features(feature_score):
    if feature_score is None:
        return 1.0
    score = _clamp_unit(feature_score)
    max_delta = _clamp_unit(WEIGHTING.feature_max_delta)
    return _clamp_unit(1.0 - (max_delta * (1.0 - score)))


def compute_weights(
    comps: list[dict],
    target_size: float,
    target_bathrooms: int | None = None,
    target_bedrooms: int | None = None,
    target_property_type: str | None = None,
    target_features: dict | None = None,
    property_category: str | None = None,
) -> list[dict]:
    """
    Returns comps with added deterministic weight and component keys.
    """
    out = []
    category_value = property_category or (target_features or {}).get("property_category")
    for c in comps:
        feature_similarity = compute_feature_similarity(target_features, c, property_category=category_value)
        components = {
            "distance": _w_distance(c.get("dist_m")),
            "size_similarity": _w_size(c.get("size_sqm"), target_size),
            "recency": _w_recency(c.get("age_days")),
            "bathrooms": _w_bathrooms(c.get("bathrooms"), target_bathrooms),
            "bedrooms": _w_required_match(c.get("bedrooms"), target_bedrooms),
            "property_type": _w_property_type(c.get("property_type"), target_property_type, category_value),
            "same_area": _w_same_area(c.get("is_same_area", True)),
            "feature_similarity": _w_features(feature_similarity["score"]),
        }
        w = math.prod(components.values())
        cc = dict(c)
        cc["weight"] = float(w)
        cc["weight_components"] = {key: float(value) for key, value in components.items()}
        cc["feature_similarity"] = feature_similarity["score"]
        cc["feature_similarity_components"] = feature_similarity["components"]
        cc["feature_explanation"] = feature_similarity["details"]
        cc["amenity_similarity"] = feature_similarity["components"].get("amenities")
        cc["amenity_explanation"] = {
            "matched_amenities": feature_similarity["details"].get("matched_amenities", []),
            "missing_amenities": feature_similarity["details"].get("missing_amenities", []),
            "extra_amenities": feature_similarity["details"].get("extra_amenities", []),
            "matched_symbols": feature_similarity["details"].get("matched_amenity_symbols", []),
            "missing_symbols": feature_similarity["details"].get("missing_amenity_symbols", []),
            "extra_symbols": feature_similarity["details"].get("extra_amenity_symbols", []),
            "weighted_union": feature_similarity["details"].get("amenity_weighted_union"),
            "weighted_intersection": feature_similarity["details"].get("amenity_weighted_intersection"),
        }
        cc["property_category"] = category_value
        out.append(cc)
    return out
