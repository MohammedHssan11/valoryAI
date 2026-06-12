import logging
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.schemas.pricing import RentFairPriceRequest, RentFairPriceResponse
from app.services.ml_service import price_listing_ml
from app.services.valuation_service import price_listing as price_listing_cmt

logger = logging.getLogger(__name__)

def log_prediction(db: Session, req: RentFairPriceRequest, resp: RentFairPriceResponse, request_id: str):
    """
    Phase 5.3B: Prediction Logging
    Synchronously persist every valuation request.
    """
    try:
        h3_res9 = resp.routing_trace.get("h3_res9") if resp.routing_trace else None
        db.execute(
            text("""
                INSERT INTO prediction_logs (
                    request_id, price, engine, routing_decision, lat, lng,
                    property_type, size_sqm, compound, h3_res9
                ) VALUES (
                    :request_id, :price, :engine, :routing_decision, :lat, :lng,
                    :property_type, :size_sqm, :compound, :h3_res9
                )
            """),
            {
                "request_id": request_id,
                "price": resp.fair_price_egp,
                "engine": resp.engine_used,
                "routing_decision": resp.routing_reason,
                "lat": req.lat,
                "lng": req.lng,
                "property_type": req.property_type,
                "size_sqm": req.size_sqm,
                "compound": req.compound_name,
                "h3_res9": h3_res9
            }
        )
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log prediction to DB: {e}", exc_info=True)
        db.rollback()


def execute_shadow_pipeline(
    req: RentFairPriceRequest, 
    primary_resp: RentFairPriceResponse, 
    request_id: str
):
    """
    Phase 5.3A: Shadow Deployment
    Executes the alternative engine asynchronously and logs the result.
    """
    # Create a fresh db session for the background task
    from app.db.session import SessionLocal
    db = SessionLocal()
    
    try:
        engine_used = primary_resp.engine_used
        ml_prediction = primary_resp.fair_price_egp if engine_used == "ML" else None
        cmt_prediction = primary_resp.fair_price_egp if engine_used == "CMT" else None
        
        # Calculate the missing prediction
        if engine_used == "CMT":
            try:
                ml_resp = price_listing_ml(req, db)
                ml_prediction = ml_resp.fair_price_egp
            except Exception as e:
                logger.error(f"Shadow ML engine failed: {e}")
                ml_prediction = 0 # Mark as failed
        else:
            try:
                ctx = {"stage": "init", "comps_count": 0, "tier_used": 0}
                cmt_resp = price_listing_cmt(req, db, ctx)
                cmt_prediction = cmt_resp.fair_price_egp
            except Exception as e:
                logger.error(f"Shadow CMT engine failed: {e}")
                cmt_prediction = None # Mark as failed
                
        h3_res9 = primary_resp.routing_trace.get("h3_res9") if primary_resp.routing_trace else None
        comps_count = primary_resp.routing_trace.get("comparable_count", 0) if primary_resp.routing_trace else 0
        
        db.execute(
            text("""
                INSERT INTO shadow_logs (
                    request_id, actual_response, router_prediction, ml_prediction, cmt_prediction,
                    engine_used, routing_reason, comparable_count, confidence_score, compound_name, h3_res9
                ) VALUES (
                    :request_id, :actual_response, :router_prediction, :ml_prediction, :cmt_prediction,
                    :engine_used, :routing_reason, :comparable_count, :confidence_score, :compound_name, :h3_res9
                )
            """),
            {
                "request_id": request_id,
                "actual_response": primary_resp.fair_price_egp,
                "router_prediction": primary_resp.fair_price_egp,
                "ml_prediction": ml_prediction,
                "cmt_prediction": cmt_prediction,
                "engine_used": engine_used,
                "routing_reason": primary_resp.routing_reason,
                "comparable_count": comps_count,
                "confidence_score": primary_resp.confidence.score if primary_resp.confidence else None,
                "compound_name": req.compound_name,
                "h3_res9": h3_res9
            }
        )
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log shadow execution to DB: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()
