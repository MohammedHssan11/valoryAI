import logging
import time
import os
import json
import numpy as np
import pandas as pd
import h3
from catboost import CatBoostRegressor, Pool
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.api.schemas.pricing import RentFairPriceRequest, RentFairPriceResponse
from app.core.enums import PriceFlag, ConfidenceLevel

logger = logging.getLogger(__name__)

# Load models at startup
ML_DIR = os.getenv("ML_MODEL_DIR", os.path.join(os.path.dirname(__file__), "..", "models"))

class MLModels:
    def __init__(self):
        self.rent_model = CatBoostRegressor()
        self.sale_model = CatBoostRegressor()
        self.rent_schema = {}
        self.sale_schema = {}
        self.loaded = False
        
    def load(self):
        if self.loaded: return
        try:
            self.rent_model.load_model(os.path.join(ML_DIR, "residential_rent.cbm"))
            self.sale_model.load_model(os.path.join(ML_DIR, "residential_sale.cbm"))
            with open(os.path.join(ML_DIR, "residential_rent_schema.json")) as f:
                self.rent_schema = json.load(f)
            with open(os.path.join(ML_DIR, "residential_sale_schema.json")) as f:
                self.sale_schema = json.load(f)
            self.loaded = True
            logger.info("ML Models and Schemas loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load ML models: {e}")

ml_models = MLModels()

def _extract_features(req: RentFairPriceRequest, schema: dict) -> pd.DataFrame:
    features = schema["features"]
    categoricals = schema["categoricals"]
    
    # Initialize zeroed dictionary
    row = {f: 0 for f in features}
    for c in categoricals:
        row[c] = "Missing"
        
    row["latitude"] = req.lat or 0.0
    row["longitude"] = req.lng or 0.0
    row["bedrooms"] = req.bedrooms or 0
    row["bathrooms"] = req.bathrooms or 0
    row["size"] = req.size_sqm
    
    # Text / Enum matching
    if req.property_type:
        row["property_type"] = req.property_type
        
    if req.compound_name:
        row["compound_name"] = req.compound_name
        row["is_known_compound"] = 1
        
    if req.lat and req.lng:
        row["h3_res8"] = h3.latlng_to_cell(req.lat, req.lng, 8)
        row["h3_res9"] = h3.latlng_to_cell(req.lat, req.lng, 9)
        
    # Time
    now = datetime.utcnow()
    row["scraped_year"] = now.year
    row["scraped_month"] = now.month
    row["scraped_quarter"] = (now.month - 1) // 3 + 1
    row["listing_age_days"] = 0
    
    # Basic Boolean matching (heuristics for demo)
    furnish_lower = (req.furnishing_status or "").lower()
    if "furnished" in furnish_lower and "semi" not in furnish_lower:
        row["is_furnished"] = 1
    if "semi" in furnish_lower:
        row["semi_furnished"] = 1
        
    if req.amenities:
        row["amenities_count"] = len(req.amenities)
        joined = " ".join(req.amenities).lower()
        if "ac" in joined or "air cond" in joined: row["has_amenity_ac"] = 1
        if "balcony" in joined: row["has_amenity_ba"] = 1
        if "security" in joined: row["has_amenity_se"] = 1
        if "pool" in joined: row["has_amenity_sp"] = 1
        if "kitchen" in joined: row["has_amenity_bk"] = 1
        if "parking" in joined: row["has_amenity_cp"] = 1
        if "garden" in joined: row["has_garden"] = 1
        
    df = pd.DataFrame([row])
    # Ensure correct column order
    return df[features]

def price_listing_ml(req: RentFairPriceRequest, db: Session) -> RentFairPriceResponse:
    """
    Live inference wrapper for the Pure ML CatBoost engine.
    """
    start = time.perf_counter()
    logger.info("stage=ml_inference_start")
    
    ml_models.load()
    if not ml_models.loaded:
        raise HTTPException(status_code=500, detail="ML Models not loaded")
        
    is_rent = "rent" in req.property_category.lower()
    model = ml_models.rent_model if is_rent else ml_models.sale_model
    schema = ml_models.rent_schema if is_rent else ml_models.sale_schema
    
    # Extract
    df = _extract_features(req, schema)
    
    # Inference
    pred_log = model.predict(df)[0]
    fair = int(np.expm1(pred_log))
    
    # SHAP Explainability
    # CatBoost returns shape (1, num_features + 1)
    shap_values = model.get_feature_importance(Pool(df, cat_features=schema["categoricals"]), type='ShapValues')[0]
    base_value = shap_values[-1]
    feature_contributions = shap_values[:-1]
    
    top_pos_idx = np.argsort(feature_contributions)[-3:][::-1]
    top_neg_idx = np.argsort(feature_contributions)[:3]
    
    # We are in log-space. To get approximate EGP impact, we can use the delta of exp(base + shap)
    # A simpler approximation for small shap is: impact_egp = fair * (exp(shap) - 1)
    top_positive_features = []
    for idx in top_pos_idx:
        shap_val = feature_contributions[idx]
        if shap_val <= 0: continue
        feat_name = schema["features"][idx]
        impact_pct = np.expm1(shap_val)
        impact_egp = fair * impact_pct
        top_positive_features.append({
            "feature_name": feat_name,
            "impact_egp": round(impact_egp, 2),
            "impact_percentage": round(impact_pct * 100, 2)
        })
        
    top_negative_features = []
    for idx in top_neg_idx:
        shap_val = feature_contributions[idx]
        if shap_val >= 0: continue
        feat_name = schema["features"][idx]
        # For negative shap, np.expm1 is negative
        impact_pct = np.expm1(shap_val)
        impact_egp = fair * impact_pct
        top_negative_features.append({
            "feature_name": feat_name,
            "impact_egp": round(impact_egp, 2),
            "impact_percentage": round(impact_pct * 100, 2)
        })
    
    p20 = int(fair * 0.85)
    p80 = int(fair * 1.15)
    
    flag = PriceFlag.NO_TARGET
    if req.target_price_egp is not None:
        if req.target_price_egp > p80:
            flag = PriceFlag.TOO_HIGH
        elif req.target_price_egp < p20:
            flag = PriceFlag.TOO_LOW
        else:
            flag = PriceFlag.OK

    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    
    return RentFairPriceResponse(
        fair_price_egp=fair,
        range_low_egp=p20,
        range_high_egp=p80,
        flag=flag,
        tier_used=0,
        comps_count=0,
        confidence={
            "score": 0.85, # Static for ML currently
            "label": ConfidenceLevel.HIGH,
            "factors": {},
            "dimensions": {}
        },
        explanation=[f"Fair price computed using Pure ML CatBoost engine over {len(schema['features'])} spatial and physical features."],
        explanation_trace=[],
        retrieval_trace=[],
        spatial_diagnostics={},
        evidence_summary={},
        area={"name": "ML Inferred Area"},
        resolved_location={"lat": req.lat, "lng": req.lng},
        property_category=req.property_category,
        valuation_contract={},
        amenity_intelligence={},
        top_comps=[],
        debug={
            "top_positive_features": top_positive_features,
            "top_negative_features": top_negative_features,
        }
    )
