import logging
import time
import h3
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.api.schemas.pricing import RentFairPriceRequest, RentFairPriceResponse
from app.geo.exposure_registry import exposure_registry
from app.services.valuation_service import price_listing as price_listing_cmt
from app.services.ml_service import price_listing_ml
from app.core.observability import get_request_telemetry, metrics, telemetry_snapshot
from fastapi import BackgroundTasks
from app.services.monitoring_service import log_prediction, execute_shadow_pipeline
from app.api.schemas.pricing import (
    ExplainabilityModel, ComparableEvidence, FeatureDriver,
    ConfidenceExplanation, FairnessExplanation, NarrativeExplanation
)

logger = logging.getLogger(__name__)

def evaluate_routing_rules(comps_count: int, is_unseen_comp: bool, is_unseen_h3: bool) -> tuple[str, str]:
    """
    Evaluates the Phase 5.1 Optimized Router rules:
    if (11 <= comps <= 50) or ((unseen_compound or unseen_h3) and comps >= 10):
        use CMT
    else:
        use ML
    """
    if 11 <= comps_count <= 50:
        return "CMT", "GoldilocksZone"
    if (is_unseen_comp and is_unseen_h3) and comps_count >= 10:
        return "CMT", "UnseenGeographyWithSufficientComps"
    
    return "ML", "PureMLBaseline"

def _resolve_h3(lat: float | None, lng: float | None) -> str | None:
    if lat is not None and lng is not None:
        return h3.latlng_to_cell(lat, lng, 9)
    return None

def _generate_explainability(req: RentFairPriceRequest, response: RentFairPriceResponse) -> ExplainabilityModel:
    engine = response.engine_used
    
    # 1. Confidence Explanation
    if response.comps_count >= 11:
        conf_level = "High"
        conf_reason = f"High confidence because {response.comps_count} similar properties were found."
    elif response.comps_count >= 5:
        conf_level = "Medium"
        conf_reason = f"Medium confidence based on {response.comps_count} properties."
    else:
        conf_level = "Low"
        conf_reason = "Low confidence due to sparse market data."
    confidence = ConfidenceExplanation(confidence_level=conf_level, confidence_reason=conf_reason)
    
    # 2. Fairness Explanation
    target_price = req.target_price_egp
    estimated = response.fair_price_egp
    diff_amount = None
    diff_pct = None
    status = "Within Fair Value Range"
    
    if target_price:
        diff_amount = abs(target_price - estimated)
        diff_pct = round((diff_amount / estimated) * 100, 2)
        if target_price > response.range_high_egp:
            status = "Above Fair Value"
        elif target_price < response.range_low_egp:
            status = "Below Fair Value"
            
    fairness = FairnessExplanation(
        estimated_value=estimated,
        asking_price=target_price,
        difference_amount=diff_amount,
        difference_percentage=diff_pct,
        status=status
    )
    
    # 3. Features & Comps
    feature_drivers = []
    comparables_used = []
    
    if engine == "CMT":
        for comp in response.top_comps[:5]:
            comparables_used.append(ComparableEvidence(
                property_id=comp.listing_id,
                price=comp.price_egp,
                size_sqm=comp.size_sqm or 0.0,
                bedrooms=comp.bedrooms or 0,
                bathrooms=comp.bathrooms or 0,
                furnishing_status=comp.furnishing_status,
                compound_name=comp.compound_name,
                distance_km=comp.dist_m / 1000.0 if comp.dist_m else 0,
                similarity_score=comp.similarity_score or 0.0,
                similarity_reason=comp.reason_code,
            ))
            
        routing_logic = f"CMT selected due to optimal comparable density ({response.comps_count} comps)."
        summary = f"The property's fair value is {estimated:,.0f} EGP."
        why = f"This is based on {response.comps_count} highly similar properties recently listed nearby."
        strongest = "Prices in this specific compound strongly anchor the valuation."
    else:
        # ML Engine Feature Drivers
        if "top_positive_features" in response.debug:
            for f in response.debug["top_positive_features"]:
                strength = "High" if f["impact_percentage"] > 10 else "Medium" if f["impact_percentage"] > 5 else "Low"
                feature_drivers.append(FeatureDriver(name=f["feature_name"], direction="Positive", strength=strength))
        if "top_negative_features" in response.debug:
            for f in response.debug["top_negative_features"]:
                strength = "High" if f["impact_percentage"] < -10 else "Medium" if f["impact_percentage"] < -5 else "Low"
                feature_drivers.append(FeatureDriver(name=f["feature_name"], direction="Negative", strength=strength))
                
        routing_logic = "ML Baseline selected to interpolate pricing for this specific area/property."
        summary = f"The property's fair value is {estimated:,.0f} EGP."
        why = "Because this area lacks direct comparables, our AI analyzed broader luxury market trends to determine the price."
        
        pos_names = [f.name for f in feature_drivers if f.direction == "Positive"]
        neg_names = [f.name for f in feature_drivers if f.direction == "Negative"]
        strongest_parts = []
        if pos_names:
            strongest_parts.append(f"boosted by {pos_names[0]}")
        if neg_names:
            strongest_parts.append(f"reduced by {neg_names[0]}")
        strongest = f"The price is {' and '.join(strongest_parts)}." if strongest_parts else "Market location is the primary driver."
        
    narrative = NarrativeExplanation(
        summary=summary,
        why_this_price=why,
        strongest_factors=strongest,
        confidence_reason=conf_reason
    )
    
    return ExplainabilityModel(
        router_explanation=routing_logic,
        confidence_explanation=confidence,
        fairness_explanation=fairness,
        narrative_explanation=narrative,
        comparable_evidence=comparables_used,
        feature_drivers=feature_drivers
    )

def price_listing_router(req: RentFairPriceRequest, db: Session, ctx: dict = None, background_tasks: BackgroundTasks = None, request_id: str = None) -> RentFairPriceResponse:
    """
    The master orchestration router for ValorAI Phase 5.2.
    It evaluates spatial exposure, comparable density, and deterministically
    delegates execution to the safest mathematical engine.
    """
    start_time = time.perf_counter()
    logger.info("stage=router_start compound=%s", req.compound_name)

    # 1. Evaluate Geographic Exposure
    h3_index = _resolve_h3(req.lat, req.lng)
    unseen_comp, unseen_h3, exposure_score = exposure_registry.get_exposure_metrics(req.compound_name, h3_index)

    # 2. Execute CMT (We execute CMT first because we strictly require `comps_count` to route)
    # This also acts as our failsafe: if CMT fails entirely, we fallback immediately.
    ctx = {"stage": "init", "comps_count": 0, "tier_used": 0}
    try:
        cmt_response = price_listing_cmt(req, db, ctx=ctx)
        comps_count = cmt_response.comps_count
    except Exception as e:
        logger.error("CMT engine failed, attempting emergency ML fallback", exc_info=True)
        # Fallback 1: If CMT fails, force ML
        try:
            ml_resp = price_listing_ml(req, db)
            ml_resp.engine_used = "ML"
            ml_resp.routing_reason = "Fallback_CMT_Failure"
            ml_resp.is_unseen_compound = unseen_comp
            ml_resp.is_unseen_h3 = unseen_h3
            ml_resp.explainability = _generate_explainability(req, ml_resp)
            
            if background_tasks and request_id:
                background_tasks.add_task(log_prediction, db, req, ml_resp, request_id)
                background_tasks.add_task(execute_shadow_pipeline, req, ml_resp, request_id)
                
            return ml_resp
        except Exception as ml_e:
            raise HTTPException(status_code=503, detail="Both Valuation Engines Failed") from ml_e

    # 3. Apply the routing logic using the exact retrieved comparable count
    engine_used, routing_reason = evaluate_routing_rules(comps_count, unseen_comp, unseen_h3)

    routing_trace = {
        "decision": engine_used,
        "reason": routing_reason,
        "comparable_count": comps_count,
        "is_unseen_compound": unseen_comp,
        "is_unseen_h3": unseen_h3,
        "exposure_score": exposure_score,
        "h3_res9": h3_index
    }

    # 4. Return appropriate response
    if engine_used == "CMT":
        final_response = cmt_response
    else:
        try:
            ml_response = price_listing_ml(req, db)
            final_response = ml_response
            # Preserve CMT comps retrieval trace for the ML explainability
            final_response.retrieval_trace = cmt_response.retrieval_trace
            final_response.comps_count = comps_count
        except Exception as e:
            logger.error("ML engine failed, attempting emergency CMT fallback", exc_info=True)
            final_response = cmt_response
            engine_used = "CMT"
            routing_reason = "Fallback_ML_Failure"
            routing_trace["decision"] = "CMT"
            routing_trace["reason"] = routing_reason
            routing_trace["error"] = str(e)

    # 5. Populate Unified Contract metadata
    final_response.engine_used = engine_used
    final_response.routing_reason = routing_reason
    final_response.is_unseen_compound = unseen_comp
    final_response.is_unseen_h3 = unseen_h3
    final_response.routing_trace = routing_trace

    # 6. Observability
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
    metrics.increment("router.engine_used", {"engine": engine_used, "reason": routing_reason})
    if unseen_comp or unseen_h3:
        metrics.increment("router.unseen_geography")
    
    logger.info(
        "router_completed",
        extra={
            "router_duration_ms": duration_ms,
            "meta": {
                "engine_used": engine_used,
                "routing_reason": routing_reason,
                "comps_count": comps_count,
                "is_unseen": unseen_comp and unseen_h3,
                "exposure_score": exposure_score
            }
        }
    )

    # 7. Generate Explainability
    final_response.explainability = _generate_explainability(req, final_response)

    if background_tasks and request_id:
        background_tasks.add_task(log_prediction, db, req, final_response, request_id)
        background_tasks.add_task(execute_shadow_pipeline, req, final_response, request_id)

    return final_response
