import logging
import time

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.config import settings
from app.core.enums import ConfidenceLevel, PriceFlag
from app.core.property_features import normalize_property_features
from app.geo.area_resolver import nearest_area
from app.geo.address_resolver import resolve_address, resolve_canonical_entity
from app.comps.selector import fetch_comps
from app.comps.outliers import hard_guardrails
from app.pricing.filters import mad_filter
from app.pricing.estimator import compute_weights
from app.pricing.weights import weighted_median, weighted_quantile
from app.pricing.confidence import compute_confidence, confidence_label
from app.pricing.explain import (
    build_amenity_intelligence,
    build_evidence_summary,
    build_explanation,
    build_explanation_trace,
    build_spatial_diagnostics,
    pick_top_comps,
)
from app.pricing.contracts import category_contract, public_category_contract
from app.pricing.settings import PRICE_RANGE_QUANTILES

from app.api.schemas.pricing import LocationMode, RentFairPriceRequest, RentFairPriceResponse
from app.core.observability import get_request_telemetry, metrics, telemetry_snapshot, timed_span

logger = logging.getLogger(__name__)


def _avg(values):
    values = [float(value) for value in values if value is not None]
    if not values:
        return None
    return sum(values) / len(values)


def _avg_feature_similarity(weighted):
    values = []
    for comp in weighted:
        components = comp.get("weight_components", {})
        if not components:
            continue
        values.append(
            components.get("size_similarity", 0.0)
            * components.get("bathrooms", 0.0)
            * components.get("bedrooms", 0.0)
            * components.get("property_type", 0.0)
        )
    return _avg(values)


def _avg_amenity_similarity(weighted):
    return _avg(c.get("amenity_similarity") for c in weighted)


def _manual_location_data(req: RentFairPriceRequest) -> dict:
    return {
        "raw_input": None,
        "normalized_input": f"{req.lat:.6f},{req.lng:.6f}",
        "matched_name": None,
        "matched_entity": None,
        "lat": req.lat,
        "lng": req.lng,
        "precision_level": "ROOFTOP",
        "source": "MANUAL_COORDINATES",
        "confidence": 0.95,
        "ambiguity_status": "UNAMBIGUOUS",
        "resolver_version": settings.ADDRESS_RESOLVER_VERSION,
        "cache_hit": False,
        "resolution_strategy": "EXPLICIT_MANUAL_COORDINATES",
        "area_distance_m": None,
    }


def _resolved_location_data(req: RentFairPriceRequest, db: Session) -> tuple[float, float, dict]:
    mode = LocationMode(req.location_mode)
    if mode == LocationMode.MANUAL_COORDINATES:
        return req.lat, req.lng, _manual_location_data(req)

    try:
        if mode == LocationMode.ADDRESS_RESOLUTION:
            loc = resolve_address(db, req.address)
        else:
            loc = resolve_canonical_entity(db, req.canonical_entity_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"code": "LOCATION_RESOLUTION_FAILED", "message": str(e)}) from e

    return loc.lat, loc.lng, loc.model_dump(mode="json")


def _location_confidence_dimension(resolved_location: dict, area_data: dict | None = None) -> dict:
    score = float(resolved_location.get("confidence") or 0.0)
    if area_data and area_data.get("ambiguity_status") not in {None, "UNAMBIGUOUS"}:
        score = min(score, 0.20)
    if area_data and area_data.get("dist_m") is not None and resolved_location.get("source") != "MANUAL_COORDINATES":
        dist = max(float(area_data["dist_m"]), 0.0)
        if dist > settings.AREA_FALLBACK_RADIUS_DEFAULT_M:
            score = min(score, 0.50)
    return {
        "score": max(0.0, min(1.0, score)),
        "source": resolved_location.get("source"),
        "precision_level": resolved_location.get("precision_level"),
        "ambiguity_status": resolved_location.get("ambiguity_status", "UNAMBIGUOUS"),
        "resolution_strategy": resolved_location.get("resolution_strategy"),
        "cache_hit": bool(resolved_location.get("cache_hit")),
        "resolver_version": resolved_location.get("resolver_version"),
    }


def _combine_confidence(evidence_confidence: dict, location_confidence: dict) -> dict:
    evidence_score = float(evidence_confidence.get("score") or 0.0)
    location_score = float(location_confidence.get("score") or 0.0)
    final_score = min(evidence_score, location_score)
    evidence_factors = evidence_confidence.get("factors", {})
    return {
        "score": final_score,
        "label": confidence_label(final_score),
        "factors": {
            **evidence_factors,
            "valuation_evidence": evidence_score,
            "location_resolution": location_score,
        },
        "dimensions": {
            "valuation_evidence": evidence_confidence,
            "location_resolution": location_confidence,
        },
    }


def _target_features_from_request(req: RentFairPriceRequest) -> dict:
    features = normalize_property_features(
        {
            "amenities": req.amenities,
            "furnishing_status": req.furnishing_status,
            "floor_number": req.floor_number,
            "compound_name": req.compound_name,
            "view_type": req.view_type,
            "building_quality": req.building_quality,
        }
    )
    features["property_category"] = req.property_category
    return features


def _record_valuation_metrics(
    *,
    duration_ms: float,
    comparable_count: int,
    tier_used: int,
    valuation_flag: str,
    confidence: dict | None = None,
) -> None:
    confidence = confidence or {}
    confidence_label_val = confidence.get("label")
    confidence_score = confidence.get("score")
    dimensions = confidence.get("dimensions") or {}
    location_score = (dimensions.get("location_resolution") or {}).get("score")
    evidence_score = (dimensions.get("valuation_evidence") or {}).get("score")

    telemetry = get_request_telemetry()
    if telemetry is not None:
        telemetry.add_timing("valuation_total_ms", duration_ms)
        telemetry.set_attribute("comparable_count", comparable_count)
        telemetry.set_attribute("tier_used", tier_used)
        telemetry.set_attribute("valuation_flag", valuation_flag)
        telemetry.set_attribute("confidence_label", confidence_label_val)
        telemetry.set_attribute("confidence_score", confidence_score)
        telemetry.set_attribute("location_confidence_score", location_score)
        telemetry.set_attribute("valuation_evidence_confidence_score", evidence_score)

    metrics.observe("valuation.duration_ms", duration_ms, {"flag": valuation_flag, "tier": tier_used})
    metrics.observe("valuation.comparable_count", comparable_count, {"tier": tier_used, "flag": valuation_flag})
    metrics.increment("valuation.tier_usage", {"tier": tier_used})
    metrics.increment("valuation.flag", {"flag": valuation_flag})
    if confidence_label_val is not None:
        metrics.increment("valuation.confidence_label", {"label": confidence_label_val})
    if confidence_score is not None:
        metrics.observe("valuation.confidence_score", float(confidence_score), {"label": confidence_label_val or "unknown"})
    if location_score is not None:
        metrics.observe("valuation.location_confidence_score", float(location_score), {"label": confidence_label_val or "unknown"})
    if evidence_score is not None:
        metrics.observe("valuation.evidence_confidence_score", float(evidence_score), {"label": confidence_label_val or "unknown"})
    metrics.record_event(
        "valuation",
        {
            "duration_ms": duration_ms,
            "comparable_count": comparable_count,
            "tier_used": tier_used,
            "valuation_flag": valuation_flag,
            "confidence_label": confidence_label_val,
            "confidence_score": confidence_score,
            "telemetry": telemetry_snapshot(),
        },
    )


def price_listing(req: RentFairPriceRequest, db: Session, ctx: dict | None = None) -> RentFairPriceResponse:
    if ctx is None:
        ctx = {"stage": "contract_resolution", "comps_count": None, "tier_used": None}
    
    start = time.perf_counter()
    contract = category_contract(req.property_category)
    valuation_contract = public_category_contract(contract.category)

    with timed_span("location_resolution_ms"):
        lat, lng, resolved_location_data = _resolved_location_data(req, db)

    # 1) resolve area
    with timed_span("area_resolution_ms"):
        area = nearest_area(db, lat, lng)
    area_data = dict(area) if area else {"name": "Unknown"}
    if area_data.get("ambiguity_status") not in {None, "UNAMBIGUOUS"}:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "AMBIGUOUS_LOCATION",
                "message": f"Ambiguous area resolution: {area_data.get('ambiguity_status')}",
            },
        )
    area_id = area_data.get("area_id")
    if resolved_location_data and area_data.get("dist_m") is not None:
        resolved_location_data["area_distance_m"] = area_data.get("dist_m")
    location_confidence = _location_confidence_dimension(resolved_location_data, area_data)

    # 2) build params for comps
    with timed_span("feature_normalization_ms"):
        target_features = _target_features_from_request(req)
    params = {
        "lat": lat,
        "lng": lng,
        "area_id": area_id,
        "property_type": req.property_type,
        "property_category": contract.category.value,
        "listing_category": contract.listing_category.value,
        "listing_period": contract.period.value,
        "bedrooms": req.bedrooms,
        "bathrooms": req.bathrooms,
        "size_sqm": float(req.size_sqm),
        "target_features": target_features,
    }

    # 3) fetch comps (tiers)
    logger.info("stage=comparable_retrieval_start")
    ctx["stage"] = "comparable_retrieval"
    with timed_span("comparable_retrieval_ms"):
        comps, tier_used, retrieval_trace = fetch_comps(db, params, include_trace=True)
        ctx["comps_count"] = len(comps)
        ctx["tier_used"] = tier_used
    logger.info(f"stage=comparable_retrieval_result comparables_count={len(comps)}")

    if len(comps) < settings.MIN_COMPS_REQUIRED:
        amenity_intelligence = build_amenity_intelligence(
            target_features=target_features,
            weighted_comps=comps,
            property_category=contract.category.value,
        )
        confidence = _combine_confidence(
            {
                "score": 0.0,
                "label": ConfidenceLevel.LOW.value,
                "factors": {
                    "count": 0.0,
                    "tier": 0.0,
                    "kept_ratio": 0.0,
                    "dispersion": 0.0,
                    "distance": 0.0,
                    "recency": 0.0,
                    "similarity": 0.0,
                },
            },
            location_confidence,
        )
        with timed_span("explainability_ms"):
            explanation = [f"Only {len(comps)} comps found (tier {tier_used})."]
            spatial_diagnostics = build_spatial_diagnostics(
                subject_lat=lat,
                subject_lng=lng,
                area=area_data,
                retrieval_trace=retrieval_trace,
                weighted_comps=comps,
                location_confidence=location_confidence,
            )
            evidence_summary = build_evidence_summary(
                comps_count=len(comps),
                tier_used=tier_used,
                retrieval_trace=retrieval_trace,
                fair_price_egp=0,
                range_low_egp=0,
                range_high_egp=0,
                property_category=contract.category.value,
                amenity_intelligence=amenity_intelligence,
            )
            explanation_trace = [
                {
                    "reason_code": "CATEGORY_VALUATION_CONTRACT",
                    "details": valuation_contract,
                },
                {
                    "reason_code": "INSUFFICIENT_COMPARABLES",
                    "details": {
                        "comps_found": len(comps),
                        "minimum_required": settings.MIN_COMPS_REQUIRED,
                        "retrieval_trace": retrieval_trace,
                        "confidence_dimensions": confidence.get("dimensions", {}),
                        "resolved_location": resolved_location_data,
                    },
                }
            ]
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        _record_valuation_metrics(
            duration_ms=duration_ms,
            comparable_count=len(comps),
            tier_used=tier_used,
            valuation_flag=PriceFlag.INSUFFICIENT_DATA.value,
            confidence=confidence,
        )
        logger.info(
            "valuation_completed",
            extra={
                "valuation_duration_ms": duration_ms,
                "comparable_count": len(comps),
                "selected_tier": tier_used,
                "valuation_flag": PriceFlag.INSUFFICIENT_DATA.value,
                "confidence_label": ConfidenceLevel.LOW.value,
                "confidence_score": 0.0,
                "telemetry": telemetry_snapshot(),
            },
        )
        return RentFairPriceResponse(
            fair_price_egp=0,
            range_low_egp=0,
            range_high_egp=0,
            flag=PriceFlag.INSUFFICIENT_DATA,
            tier_used=tier_used,
            comps_count=len(comps),
            confidence=confidence,
            explanation=explanation,
            explanation_trace=explanation_trace,
            retrieval_trace=retrieval_trace,
            spatial_diagnostics=spatial_diagnostics,
            evidence_summary=evidence_summary,
            area=area_data,
            resolved_location=resolved_location_data,
            property_category=contract.category,
            valuation_contract=valuation_contract,
            amenity_intelligence=amenity_intelligence,
        )

    # 4) hard guardrails first (super important)
    with timed_span("guardrail_filter_ms"):
        comps2, guard_stats = hard_guardrails(
            comps,
            min_price=contract.guardrails.min_price_egp,
            max_price=contract.guardrails.max_price_egp,
            max_size_sqm=contract.guardrails.max_size_sqm,
            min_ppsqm=contract.guardrails.min_price_per_sqm,
            max_ppsqm=contract.guardrails.max_price_per_sqm,
        )

    # 5) MAD outliers
    with timed_span("mad_filter_ms"):
        filtered, mad_stats = mad_filter(comps2)
    kept_ratio = (mad_stats["kept"] / max(1, (mad_stats["kept"] + mad_stats["removed"])))

    if len(filtered) < settings.MIN_COMPS_REQUIRED:
        amenity_intelligence = build_amenity_intelligence(
            target_features=target_features,
            weighted_comps=filtered,
            property_category=contract.category.value,
        )
        confidence = _combine_confidence(
            {
                "score": 0.0,
                "label": ConfidenceLevel.LOW.value,
                "factors": {
                    "count": 0.0,
                    "tier": 0.0,
                    "kept_ratio": kept_ratio,
                    "dispersion": 0.0,
                    "distance": 0.0,
                    "recency": 0.0,
                    "similarity": 0.0,
                },
            },
            location_confidence,
        )
        with timed_span("explainability_ms"):
            explanation = build_explanation(
                area=area_data,
                tier_used=tier_used,
                comps_count=len(comps),
                mad_stats=mad_stats,
                guard_stats=guard_stats,
                retrieval_trace=retrieval_trace,
                resolved_location=resolved_location_data,
                property_category=contract.category.value,
            )
            explanation_trace = build_explanation_trace(
                retrieval_trace,
                guard_stats,
                mad_stats,
                confidence,
                resolved_location=resolved_location_data,
                property_category=contract.category.value,
                valuation_contract=valuation_contract,
                amenity_intelligence=amenity_intelligence,
            )
            spatial_diagnostics = build_spatial_diagnostics(
                subject_lat=lat,
                subject_lng=lng,
                area=area_data,
                retrieval_trace=retrieval_trace,
                weighted_comps=filtered,
                location_confidence=location_confidence,
            )
            evidence_summary = build_evidence_summary(
                comps_count=len(filtered),
                tier_used=tier_used,
                retrieval_trace=retrieval_trace,
                guard_stats=guard_stats,
                mad_stats=mad_stats,
                fair_price_egp=0,
                range_low_egp=0,
                range_high_egp=0,
                property_category=contract.category.value,
                amenity_intelligence=amenity_intelligence,
            )
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        _record_valuation_metrics(
            duration_ms=duration_ms,
            comparable_count=len(filtered),
            tier_used=tier_used,
            valuation_flag=PriceFlag.INSUFFICIENT_DATA.value,
            confidence=confidence,
        )
        logger.info(
            "valuation_completed",
            extra={
                "valuation_duration_ms": duration_ms,
                "comparable_count": len(filtered),
                "selected_tier": tier_used,
                "valuation_flag": PriceFlag.INSUFFICIENT_DATA.value,
                "confidence_label": ConfidenceLevel.LOW.value,
                "confidence_score": 0.0,
                "telemetry": telemetry_snapshot(),
            },
        )
        return RentFairPriceResponse(
            fair_price_egp=0,
            range_low_egp=0,
            range_high_egp=0,
            flag=PriceFlag.INSUFFICIENT_DATA,
            tier_used=tier_used,
            comps_count=len(filtered),
            confidence=confidence,
            explanation=explanation,
            explanation_trace=explanation_trace,
            retrieval_trace=retrieval_trace,
            spatial_diagnostics=spatial_diagnostics,
            evidence_summary=evidence_summary,
            area=area_data,
            resolved_location=resolved_location_data,
            property_category=contract.category,
            valuation_contract=valuation_contract,
            amenity_intelligence=amenity_intelligence,
            debug={
                "guardrails": guard_stats,
                "mad": mad_stats,
                "retrieval_trace": retrieval_trace,
                "confidence_dimensions": confidence.get("dimensions", {}),
            } if settings.DEBUG else {},
        )

    # 6) weights
    logger.info("stage=scoring")
    with timed_span("weighting_ms"):
        weighted = compute_weights(
            filtered,
            float(req.size_sqm),
            target_bathrooms=req.bathrooms,
            target_bedrooms=req.bedrooms,
            target_property_type=req.property_type,
            target_features=target_features,
            property_category=contract.category.value,
        )

    prices = [int(c["price_egp"]) for c in weighted]
    weights = [float(c["weight"]) for c in weighted]

    with timed_span("pricing_statistics_ms"):
        fair = int(round(weighted_median(prices, weights)))
        low_quantile, high_quantile = PRICE_RANGE_QUANTILES
        p20 = int(round(weighted_quantile(prices, weights, low_quantile)))
        p80 = int(round(weighted_quantile(prices, weights, high_quantile)))

    dispersion_ratio = (p80 - p20) / max(fair, 1)
    with timed_span("confidence_computation_ms"):
        evidence_conf = compute_confidence(
            len(filtered),
            tier_used,
            kept_ratio,
            dispersion_ratio,
            avg_distance_m=_avg(c.get("dist_m") for c in weighted),
            avg_age_days=_avg(c.get("age_days") for c in weighted),
            avg_similarity=_avg_feature_similarity(weighted),
            avg_amenity_similarity=_avg_amenity_similarity(weighted),
            property_category=contract.category.value,
        )
        conf = _combine_confidence(evidence_conf, location_confidence)

    # 7) flag vs target
    flag = PriceFlag.NO_TARGET
    if req.target_price_egp is not None:
        if req.target_price_egp > p80:
            flag = PriceFlag.TOO_HIGH
        elif req.target_price_egp < p20:
            flag = PriceFlag.TOO_LOW
        else:
            flag = PriceFlag.OK

    # 8) explainability + top comps
    with timed_span("explainability_ms"):
        explanation = build_explanation(
            area=area_data,
            tier_used=tier_used,
            comps_count=len(comps),
            mad_stats=mad_stats,
            guard_stats=guard_stats,
            retrieval_trace=retrieval_trace,
            resolved_location=resolved_location_data,
            property_category=contract.category.value,
        )
        amenity_intelligence = build_amenity_intelligence(
            target_features=target_features,
            weighted_comps=weighted,
            property_category=contract.category.value,
        )
        explanation_trace = build_explanation_trace(
            retrieval_trace,
            guard_stats,
            mad_stats,
            conf,
            target_features=target_features,
            weighted_comps=weighted,
            resolved_location=resolved_location_data,
            property_category=contract.category.value,
            valuation_contract=valuation_contract,
            amenity_intelligence=amenity_intelligence,
        )
        top_comps = pick_top_comps(weighted, n=settings.TOP_COMPS_N)
        spatial_diagnostics = build_spatial_diagnostics(
            subject_lat=lat,
            subject_lng=lng,
            area=area_data,
            retrieval_trace=retrieval_trace,
            weighted_comps=weighted,
            location_confidence=location_confidence,
        )
        evidence_summary = build_evidence_summary(
            comps_count=len(filtered),
            tier_used=tier_used,
            retrieval_trace=retrieval_trace,
            guard_stats=guard_stats,
            mad_stats=mad_stats,
            weighted_comps=weighted,
            fair_price_egp=fair,
            range_low_egp=p20,
            range_high_egp=p80,
            property_category=contract.category.value,
            amenity_intelligence=amenity_intelligence,
        )
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    _record_valuation_metrics(
        duration_ms=duration_ms,
        comparable_count=len(filtered),
        tier_used=tier_used,
        valuation_flag=flag.value,
        confidence=conf,
    )
    logger.info(
        "valuation_completed",
        extra={
            "valuation_duration_ms": duration_ms,
            "comparable_count": len(filtered),
            "selected_tier": tier_used,
            "valuation_flag": flag.value,
            "fair_price_egp": fair,
            "confidence_label": conf.get("label"),
            "confidence_score": conf.get("score"),
            "telemetry": telemetry_snapshot(),
        },
    )

    return RentFairPriceResponse(
        fair_price_egp=fair,
        range_low_egp=p20,
        range_high_egp=p80,
        flag=flag,
        tier_used=tier_used,
        comps_count=len(filtered),
        confidence=conf,
        explanation=explanation,
        explanation_trace=explanation_trace,
        retrieval_trace=retrieval_trace,
        spatial_diagnostics=spatial_diagnostics,
        evidence_summary=evidence_summary,
        area=area_data,
        resolved_location=resolved_location_data,
        property_category=contract.category,
        valuation_contract=valuation_contract,
        amenity_intelligence=amenity_intelligence,
        debug={
            "guardrails": guard_stats,
            "mad": mad_stats,
            "dispersion_ratio": dispersion_ratio,
            "retrieval_trace": retrieval_trace,
            "target_features": target_features,
            "confidence_dimensions": conf.get("dimensions", {}),
        } if settings.DEBUG else {},
        top_comps=top_comps,
    )
