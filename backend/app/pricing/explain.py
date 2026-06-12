from typing import List, Dict, Any

from app.core.config import settings
from app.pricing.amenities import amenity_governance_registry, amenity_metadata, known_amenity_symbols
from app.pricing.contracts import category_contract, public_category_contract


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _round_float(value: Any, digits: int = 4) -> float | None:
    number = _safe_float(value)
    if number is None:
        return None
    return round(number, digits)


def _unit_average(values: List[float | None], fallback: float = 0.0) -> float:
    usable = [max(0.0, min(1.0, float(value))) for value in values if value is not None]
    if not usable:
        return fallback
    return sum(usable) / len(usable)


def _selected_retrieval_stage(retrieval_trace: List[Dict[str, Any]] | None) -> Dict[str, Any] | None:
    return next((entry for entry in retrieval_trace or [] if entry.get("selected")), None)


def _distance_band_counts(weighted_comps: List[Dict[str, Any]]) -> Dict[str, int]:
    bands = {"0_500m": 0, "500_1000m": 0, "1000_2000m": 0, "2000m_plus": 0, "unknown": 0}
    for comp in weighted_comps:
        dist = _safe_float(comp.get("dist_m"))
        if dist is None:
            bands["unknown"] += 1
        elif dist <= 500:
            bands["0_500m"] += 1
        elif dist <= 1000:
            bands["500_1000m"] += 1
        elif dist <= 2000:
            bands["1000_2000m"] += 1
        else:
            bands["2000m_plus"] += 1
    return bands


def _cluster_quality(weighted_comps: List[Dict[str, Any]], selected_stage: Dict[str, Any] | None) -> str:
    count = len(weighted_comps)
    max_distance = max((_safe_float(comp.get("dist_m")) or 0.0 for comp in weighted_comps), default=0.0)
    radius = _safe_float((selected_stage or {}).get("radius_m"))
    if count >= settings.MIN_COMPS_REQUIRED * 3 and max_distance <= 1000:
        return "high_quality_cluster"
    if count >= settings.MIN_COMPS_REQUIRED and radius is not None and max_distance <= radius:
        return "supported_cluster"
    if count < settings.MIN_COMPS_REQUIRED:
        return "sparse_evidence"
    return "wide_radius_evidence"


def build_spatial_diagnostics(
    *,
    subject_lat: float | None,
    subject_lng: float | None,
    area: Dict[str, Any] | None,
    retrieval_trace: List[Dict[str, Any]] | None,
    weighted_comps: List[Dict[str, Any]] | None = None,
    location_confidence: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    weighted_comps = weighted_comps or []
    selected_stage = _selected_retrieval_stage(retrieval_trace)
    distances = [_safe_float(comp.get("dist_m")) for comp in weighted_comps]
    distances = [value for value in distances if value is not None]
    return {
        "subject": {
            "lat": _round_float(subject_lat, 6),
            "lng": _round_float(subject_lng, 6),
            "area_id": (area or {}).get("area_id"),
            "area_name": (area or {}).get("name"),
        },
        "selected_retrieval": selected_stage or {},
        "retrieval_radius_m": (selected_stage or {}).get("radius_m"),
        "comp_count": len(weighted_comps),
        "avg_distance_m": _round_float(sum(distances) / len(distances), 2) if distances else None,
        "max_distance_m": _round_float(max(distances), 2) if distances else None,
        "distance_band_counts": _distance_band_counts(weighted_comps),
        "cluster_quality": _cluster_quality(weighted_comps, selected_stage),
        "location_confidence": location_confidence or {},
    }


def build_evidence_summary(
    *,
    comps_count: int,
    tier_used: int,
    retrieval_trace: List[Dict[str, Any]] | None,
    guard_stats: Dict[str, Any] | None = None,
    mad_stats: Dict[str, Any] | None = None,
    weighted_comps: List[Dict[str, Any]] | None = None,
    fair_price_egp: int | None = None,
    range_low_egp: int | None = None,
    range_high_egp: int | None = None,
    property_category: str | None = None,
    amenity_intelligence: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    weighted_comps = weighted_comps or []
    contract = category_contract(property_category)
    total_weight = sum(max(_safe_float(comp.get("weight")) or 0.0, 0.0) for comp in weighted_comps)
    selected_stage = _selected_retrieval_stage(retrieval_trace)
    return {
        "authoritative_valuation_frozen": True,
        "valuation_mutation_allowed": False,
        "comps_retained": comps_count,
        "tier_used": tier_used,
        "selected_retrieval": selected_stage or {},
        "guardrails": guard_stats or {"kept": comps_count, "removed": 0, "reasons": {}},
        "mad": mad_stats or {"kept": comps_count, "removed": 0},
        "weighted_comp_count": len(weighted_comps),
        "total_weight": round(total_weight, 6),
        "price_band": {
            "fair_price_egp": fair_price_egp,
            "range_low_egp": range_low_egp,
            "range_high_egp": range_high_egp,
        },
        "retrieval_attempts": len(retrieval_trace or []),
        "property_category": contract.category.value,
        "valuation_contract": public_category_contract(contract.category),
        "amenity_intelligence": amenity_intelligence or {},
    }


def build_explanation(
    area: Dict | None,
    tier_used: int,
    comps_count: int,
    mad_stats: Dict,
    guard_stats: Dict,
    retrieval_trace: List[Dict[str, Any]] | None = None,
    resolved_location: Dict[str, Any] | None = None,
    property_category: str | None = None,
) -> List[str]:
    area_name = (area or {}).get("name", "Unknown area")
    contract = category_contract(property_category)
    selected = next(
        (entry for entry in retrieval_trace or [] if entry.get("tier") == tier_used and entry.get("comps_found") == comps_count),
        None,
    )
    tier_label = selected.get("tier_label") if selected else f"tier {tier_used}"
    expl = []
    if resolved_location:
        if resolved_location.get("source") == "MANUAL_COORDINATES":
            expl.append("Using explicitly supplied manual coordinates for deterministic spatial grounding.")
        else:
            expl.append(f"Resolved input '{resolved_location.get('raw_input')}' to {resolved_location.get('precision_level')} level via {resolved_location.get('source')}.")

    expl.extend([
        f"Applied the governed {contract.label} valuation contract ({contract.value_basis}).",
        f"{comps_count} similar listings found using {tier_label} around {area_name}.",
        f"Hard guardrails removed {guard_stats.get('removed', 0)} records (price/size/ppsqm).",
        f"Outliers removed using MAD on {mad_stats.get('metric', 'price')}: kept {mad_stats['kept']} / removed {mad_stats['removed']}.",
        "Fair price computed using weighted median; amenities affect comparable weighting, confidence, and traces only.",
    ])
    return expl


def build_amenity_intelligence(
    *,
    target_features: Dict[str, Any] | None,
    weighted_comps: List[Dict[str, Any]] | None,
    property_category: str | None = None,
) -> Dict[str, Any]:
    target_features = target_features or {}
    weighted_comps = weighted_comps or []
    contract = category_contract(property_category)
    target_symbols = sorted(target_features.get("canonical_amenity_symbols") or [])
    target_metadata = [
        metadata
        for symbol in target_symbols
        if (metadata := amenity_metadata(symbol, contract.category)) is not None
    ]
    amenity_scores = [
        float(comp["amenity_similarity"])
        for comp in weighted_comps
        if comp.get("amenity_similarity") is not None
    ]
    matched = sorted(
        {
            item
            for comp in weighted_comps
            for item in (comp.get("amenity_explanation") or {}).get("matched_amenities", [])
        }
    )
    missing = sorted(
        {
            item
            for comp in weighted_comps
            for item in (comp.get("amenity_explanation") or {}).get("missing_amenities", [])
        }
    )
    return {
        "property_category": contract.category.value,
        "contract_label": contract.label,
        "target_amenities": target_metadata,
        "target_unknown_amenity_codes": target_features.get("unknown_amenity_codes", []),
        "average_amenity_similarity": (
            round(sum(amenity_scores) / len(amenity_scores), 6)
            if amenity_scores
            else None
        ),
        "comps_scored": len(amenity_scores),
        "matched_amenities_observed": matched,
        "missing_amenities_observed": missing,
        "registry_size": len(amenity_governance_registry(contract.category)),
        "governance": {
            "canonical_symbol_storage": True,
            "amenities_override_pricing": False,
            "influences": [
                "comparable_similarity",
                "comparable_weighting",
                "confidence",
                "retrieval_refinement",
                "explainability",
            ],
        },
    }


def build_explanation_trace(
    retrieval_trace: List[Dict[str, Any]],
    guard_stats: Dict[str, Any],
    mad_stats: Dict[str, Any],
    confidence: Dict[str, Any],
    target_features: Dict[str, Any] | None = None,
    weighted_comps: List[Dict[str, Any]] | None = None,
    resolved_location: Dict[str, Any] | None = None,
    property_category: str | None = None,
    valuation_contract: Dict[str, Any] | None = None,
    amenity_intelligence: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    trace = []
    contract = category_contract(property_category)
    trace.append(
        {
            "reason_code": "CATEGORY_VALUATION_CONTRACT",
            "weight": None,
            "details": valuation_contract or public_category_contract(contract.category),
        }
    )
    if resolved_location:
        trace.append({
            "reason_code": "ADDRESS_RESOLUTION",
            "weight": None,
            "details": resolved_location,
        })
        
    for entry in retrieval_trace:
        trace.append(
            {
                "reason_code": entry.get("reason_code", "COMPARABLE_SEARCH"),
                "weight": None,
                "details": entry,
            }
        )

    trace.append(
        {
            "reason_code": "HARD_GUARDRAILS_APPLIED",
            "weight": None,
            "details": guard_stats,
        }
    )
    trace.append(
        {
            "reason_code": "MAD_OUTLIER_FILTER_APPLIED",
            "weight": None,
            "details": mad_stats,
        }
    )
    trace.append(
        {
            "reason_code": "CONFIDENCE_FACTORS",
            "weight": confidence.get("score"),
            "details": {
                "factors": confidence.get("factors", {}),
                "dimensions": confidence.get("dimensions", {}),
            },
        }
    )

    feature_scores = [
        float(comp["feature_similarity"])
        for comp in weighted_comps or []
        if comp.get("feature_similarity") is not None
    ]
    if target_features and feature_scores:
        trace.append(
            {
                "reason_code": "FEATURE_SIMILARITY_APPLIED",
                "weight": sum(feature_scores) / len(feature_scores),
                "details": {
                    "target_normalized_amenities": target_features.get("normalized_amenities", []),
                    "target_unknown_amenity_codes": target_features.get("unknown_amenity_codes", []),
                    "target_canonical_amenity_symbols": target_features.get("canonical_amenity_symbols", []),
                    "target_furnishing_status": target_features.get("furnishing_status"),
                    "target_compound_name": target_features.get("compound_name"),
                    "target_floor_number": target_features.get("floor_number"),
                    "target_view_type": target_features.get("view_type"),
                    "target_building_quality": target_features.get("building_quality"),
                    "average_feature_similarity": sum(feature_scores) / len(feature_scores),
                    "comps_scored": len(feature_scores),
                },
            }
        )
    if amenity_intelligence and amenity_intelligence.get("comps_scored"):
        trace.append(
            {
                "reason_code": "AMENITY_INTELLIGENCE_APPLIED",
                "weight": amenity_intelligence.get("average_amenity_similarity"),
                "details": amenity_intelligence,
            }
        )
    if weighted_comps:
        weight_values = [max(_safe_float(comp.get("weight")) or 0.0, 0.0) for comp in weighted_comps]
        total_weight = sum(weight_values)
        trace.append(
            {
                "reason_code": "WEIGHTED_COMPARABLE_EVIDENCE",
                "weight": total_weight,
                "details": {
                    "weighted_comp_count": len(weighted_comps),
                    "total_weight": round(total_weight, 6),
                    "top_listing_ids": [
                        str(comp.get("listing_id"))
                        for comp in sorted(
                            weighted_comps,
                            key=lambda comp: (
                                -(float(comp.get("weight") or 0.0)),
                                float(comp.get("dist_m")) if comp.get("dist_m") is not None else float("inf"),
                                str(comp.get("listing_id")),
                            ),
                        )[: settings.TOP_COMPS_N]
                    ],
                },
            }
        )
    return trace


def pick_top_comps(weighted: List[Dict[str, Any]], n: int | None = None) -> List[Dict[str, Any]]:
    n = settings.TOP_COMPS_N if n is None else n
    total_weight = sum(max(_safe_float(comp.get("weight")) or 0.0, 0.0) for comp in weighted)
    # Choose highest weight comps with stable tie-breakers.
    items = sorted(
        weighted,
        key=lambda x: (
            -float(x.get("weight", 0.0)),
            float(x.get("dist_m")) if x.get("dist_m") is not None else float("inf"),
            float(x.get("age_days")) if x.get("age_days") is not None else float("inf"),
            int(x.get("price_egp")) if x.get("price_egp") is not None else 0,
            str(x.get("listing_id")),
        ),
    )[:n]

    # Return deterministic visual-evidence metadata without changing valuation authority.
    out = []
    for rank, c in enumerate(items, start=1):
        components = c.get("weight_components", {}) or {}
        price = _safe_float(c.get("price_egp"))
        size = _safe_float(c.get("size_sqm"))
        weight = max(_safe_float(c.get("weight")) or 0.0, 0.0)
        weighted_contribution = weight / total_weight if total_weight > 0 else 0.0
        similarity_score = _unit_average(
            [
                _safe_float(components.get("size_similarity")),
                _safe_float(components.get("bathrooms")),
                _safe_float(components.get("bedrooms")),
                _safe_float(components.get("property_type")),
                _safe_float(components.get("feature_similarity")),
            ],
            fallback=0.0,
        )
        evidence_quality = _unit_average(
            [
                _safe_float(components.get("distance")),
                _safe_float(components.get("recency")),
                similarity_score,
            ],
            fallback=0.0,
        )
        feature_explanation = c.get("feature_explanation", {}) or {}
        amenity_symbols = c.get("canonical_amenity_symbols") or sorted(
            known_amenity_symbols(c.get("amenities") or c.get("normalized_amenities") or [])
        )
        out.append({
            "listing_id": str(c.get("listing_id")),
            "price_egp": int(c.get("price_egp")),
            "size_sqm": float(c["size_sqm"]) if c.get("size_sqm") is not None else None,
            "price_per_sqm": round(price / size, 2) if price is not None and size and size > 0 else None,
            "property_type": c.get("property_type"),
            "bedrooms": c.get("bedrooms"),
            "bathrooms": c.get("bathrooms"),
            "area_id": c.get("area_id"),
            "area_name": c.get("area_name"),
            "lat": _round_float(c.get("lat"), 6),
            "lng": _round_float(c.get("lng"), 6),
            "location_text": c.get("location_text"),
            "images_count": c.get("images_count"),
            "retrieval_tier": c.get("retrieval_tier"),
            "tier_label": c.get("tier_label"),
            "reason_code": c.get("reason_code"),
            "radius_m": c.get("radius_m"),
            "dist_m": float(c["dist_m"]) if c.get("dist_m") is not None else None,
            "age_days": float(c["age_days"]) if c.get("age_days") is not None else None,
            "weight": float(c.get("weight", 0.0)),
            "weight_components": components,
            "weighted_contribution": round(weighted_contribution, 6),
            "confidence_contribution": round(weighted_contribution * evidence_quality, 6),
            "similarity_score": round(similarity_score, 6),
            "geographic_similarity": _round_float(components.get("distance")),
            "distance_weight": _round_float(components.get("distance")),
            "recency_weight": _round_float(components.get("recency")),
            "evidence_rank": rank,
            "property_category": c.get("property_category"),
            "amenities": c.get("amenities", []),
            "normalized_amenities": c.get("normalized_amenities", []),
            "canonical_amenity_symbols": amenity_symbols,
            "unknown_amenity_codes": c.get("unknown_amenity_codes", []),
            "furnishing_status": c.get("furnishing_status"),
            "floor_number": c.get("floor_number"),
            "compound_name": c.get("compound_name"),
            "view_type": c.get("view_type"),
            "building_quality": c.get("building_quality"),
            "feature_similarity": (
                float(c["feature_similarity"])
                if c.get("feature_similarity") is not None
                else None
            ),
            "feature_similarity_components": c.get("feature_similarity_components", {}),
            "feature_explanation": feature_explanation,
            "feature_overlap": {
                "matched_amenities": feature_explanation.get("matched_amenities", []),
                "missing_amenities": feature_explanation.get("missing_amenities", []),
                "extra_amenities": feature_explanation.get("extra_amenities", []),
            },
            "amenity_similarity": (
                float(c["amenity_similarity"])
                if c.get("amenity_similarity") is not None
                else None
            ),
            "amenity_explanation": c.get("amenity_explanation", {}),
            "amenity_metadata": [
                metadata
                for symbol in amenity_symbols
                if (metadata := amenity_metadata(symbol, c.get("property_category"))) is not None
            ],
            "filter_status": {
                "hard_guardrails": "kept",
                "mad_outlier": "kept",
                "valuation_pipeline": "authoritative_weighted_comp",
            },
        })
    return out
