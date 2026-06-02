from app.core.enums import ConfidenceLevel
from app.pricing.contracts import category_contract
from app.pricing.settings import CONFIDENCE, RADIUS_STEPS_M, WEIGHTING


def _clamp_unit(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def confidence_label(score: float) -> str:
    if score >= CONFIDENCE.high_threshold:
        return ConfidenceLevel.HIGH.value
    if score >= CONFIDENCE.medium_threshold:
        return ConfidenceLevel.MEDIUM.value
    return ConfidenceLevel.LOW.value


def _distance_quality(avg_distance_m: float | None) -> float:
    if avg_distance_m is None:
        return 0.5
    return _clamp_unit(1.0 - (max(float(avg_distance_m), 0.0) / RADIUS_STEPS_M[-1]))


def _recency_quality(avg_age_days: float | None) -> float:
    if avg_age_days is None:
        return 0.5
    return _clamp_unit(1.0 / (1.0 + (max(float(avg_age_days), 0.0) / WEIGHTING.recency_decay_days)))


def compute_confidence(
    comps_count: int,
    tier_used: int,
    kept_ratio: float,
    dispersion_ratio: float,
    avg_distance_m: float | None = None,
    avg_age_days: float | None = None,
    avg_similarity: float | None = None,
    avg_amenity_similarity: float | None = None,
    property_category: str | None = None,
    precision_penalty: float = 0.0,
):
    # score in [0,1]
    base_score = 0.0

    # comps_count
    if comps_count >= CONFIDENCE.count_high:
        count_score = CONFIDENCE.count_high_score
    elif comps_count >= CONFIDENCE.count_medium:
        count_score = CONFIDENCE.count_medium_score
    elif comps_count >= CONFIDENCE.count_low:
        count_score = CONFIDENCE.count_low_score
    else:
        count_score = CONFIDENCE.count_fallback_score
    base_score += count_score

    # tier penalty
    tier_score = CONFIDENCE.tier_scores.get(tier_used, CONFIDENCE.tier_scores[max(CONFIDENCE.tier_scores)])
    base_score += tier_score

    # outlier stability
    kept_score = min(
        CONFIDENCE.kept_ratio_max_score,
        max(0.0, (kept_ratio - CONFIDENCE.kept_ratio_baseline)),
    )
    base_score += kept_score

    # dispersion penalty (lower is better)
    # dispersion_ratio ~ (p80-p20)/median
    if dispersion_ratio <= CONFIDENCE.dispersion_low:
        dispersion_score = CONFIDENCE.dispersion_low_score
    elif dispersion_ratio <= CONFIDENCE.dispersion_medium:
        dispersion_score = CONFIDENCE.dispersion_medium_score
    else:
        dispersion_score = CONFIDENCE.dispersion_fallback_score
    base_score += dispersion_score

    distance_score = _distance_quality(avg_distance_m)
    recency_score = _recency_quality(avg_age_days)
    similarity_score = 0.5 if avg_similarity is None else _clamp_unit(avg_similarity)
    contract = category_contract(property_category)
    if avg_amenity_similarity is None:
        amenity_score = None
        confidence_weights = {"base": 0.85, "distance": 0.05, "recency": 0.05, "similarity": 0.05, "amenity": 0.0}
    else:
        amenity_score = _clamp_unit(avg_amenity_similarity)
        confidence_weights = contract.confidence_weights

    score = (
        (base_score * confidence_weights.get("base", 0.85))
        + (distance_score * confidence_weights.get("distance", 0.05))
        + (recency_score * confidence_weights.get("recency", 0.05))
        + (similarity_score * confidence_weights.get("similarity", 0.05))
        + ((amenity_score or 0.0) * confidence_weights.get("amenity", 0.0))
    )

    score = _clamp_unit(score - precision_penalty)
    factors = {
        "count": _clamp_unit(count_score / max(CONFIDENCE.count_high_score, 1e-9)),
        "tier": _clamp_unit(tier_score / max(CONFIDENCE.tier_scores[1], 1e-9)),
        "kept_ratio": _clamp_unit(kept_score / max(CONFIDENCE.kept_ratio_max_score, 1e-9)),
        "dispersion": _clamp_unit(dispersion_score / max(CONFIDENCE.dispersion_low_score, 1e-9)),
        "distance": distance_score,
        "recency": recency_score,
        "similarity": similarity_score,
        "address_precision": _clamp_unit(1.0 - precision_penalty),
    }
    if amenity_score is not None:
        factors["amenity_similarity"] = amenity_score
    return {
        "score": score,
        "label": confidence_label(score),
        "factors": factors,
        "category": {
            "property_category": contract.category.value,
            "label": contract.label,
            "confidence_weights": dict(confidence_weights),
            "amenity_confidence_applied": avg_amenity_similarity is not None,
        },
    }
