import os
# Set DATABASE_URL to use real PostgreSQL instance
os.environ["DATABASE_URL"] = "postgresql+psycopg2://fairprice:fairprice@localhost:5432/fairprice"

import sys
import json
import pandas as pd
from tqdm import tqdm

# Ensure backend app is in pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal
from app.services.valuation_service import price_listing
from app.api.schemas.pricing import RentFairPriceRequest

DATA_DIR = r"c:\Users\mh978\Downloads\mobile computing project\pf_scraper\data_eg"
INPUT_DIR = os.path.join(DATA_DIR, "dataset_v3")
OUTPUT_DIR = os.path.join(DATA_DIR, "dataset_hybrid_v1")
os.makedirs(OUTPUT_DIR, exist_ok=True)

datasets = ["residential_rent.parquet", "residential_sale.parquet"]

def build_request(row, is_sale=False):
    req = {
        "location_mode": "manual_coordinates",
        "lat": float(row.get('latitude', 30.0)) if pd.notna(row.get('latitude')) else 30.0,
        "lng": float(row.get('longitude', 31.0)) if pd.notna(row.get('longitude')) else 31.0,
        "property_category": "residential_sale" if is_sale else "residential_rent", 
        "property_type": row.get('property_type', 'Apartment'),
        "size_sqm": float(row.get('size')) if pd.notna(row.get('size')) else 100.0,
        "furnishing_status": "FURNISHED" if row.get('is_furnished', 0) == 1 else "UNFURNISHED",
    }
    
    bedrooms = row.get('bedrooms')
    if pd.notna(bedrooms):
        req["bedrooms"] = int(bedrooms)
        
    bathrooms = row.get('bathrooms')
    if pd.notna(bathrooms):
        req["bathrooms"] = int(bathrooms)
        
    compound_name = row.get('compound_name')
    if pd.notna(compound_name):
        req["compound_name"] = str(compound_name)
        
    return RentFairPriceRequest(**req)

def generate():
    report = {}
    
    # Try to set DATABASE_URL if not set, for local sqlite fallback
    if "DATABASE_URL" not in os.environ:
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        
    db = SessionLocal()
    
    for filename in datasets:
        print(f"Processing {filename}...")
        input_path = os.path.join(INPUT_DIR, filename)
        if not os.path.exists(input_path):
            print(f"Not found: {input_path}")
            continue
            
        df = pd.read_parquet(input_path)
        
        # For testing speed, we might want to sample if it's too large, but user says "every row"
        # We will do all rows
        det_prices = []
        det_conf_scores = []
        det_conf_labels = []
        tier_used = []
        comps_counts = []
        ranges_low = []
        ranges_high = []
        
        is_sale = "sale" in filename.lower()
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            try:
                req = build_request(row, is_sale=is_sale)
                res = price_listing(req, db)
                conf = res.confidence
                conf_score = conf.score if hasattr(conf, 'score') else (conf.get('score', 0.0) if isinstance(conf, dict) else 0.0)
                conf_label = conf.label if hasattr(conf, 'label') else (conf.get('label', 'LOW') if isinstance(conf, dict) else 'LOW')
                
                det_prices.append(res.fair_price_egp)
                det_conf_scores.append(conf_score)
                det_conf_labels.append(conf_label)
                tier_used.append(res.tier_used)
                comps_counts.append(res.comps_count)
                ranges_low.append(res.range_low_egp)
                ranges_high.append(res.range_high_egp)
            except Exception as e:
                # If an error happens before all variables are extracted, we need to ensure lists stay aligned
                # Since we haven't appended yet, we can safely append None/Error here
                det_prices.append(None)
                det_conf_scores.append(None)
                det_conf_labels.append("ERROR")
                tier_used.append(None)
                comps_counts.append(0)
                ranges_low.append(None)
                ranges_high.append(None)
                
        df['deterministic_price'] = det_prices
        df['confidence_score'] = det_conf_scores
        df['confidence_label'] = det_conf_labels
        df['tier_reached'] = tier_used
        df['comparable_count'] = comps_counts
        df['range_low'] = ranges_low
        df['range_high'] = ranges_high
        
        actual_price = df['price']
        df['residual'] = actual_price - df['deterministic_price']
        df['residual_pct'] = (df['residual'] / actual_price) * 100
        df['abs_residual'] = df['residual'].abs()
        
        output_path = os.path.join(OUTPUT_DIR, filename)
        df.to_parquet(output_path)
        
        total_rows = len(df)
        null_pct = df['deterministic_price'].isnull().sum() / total_rows * 100 if total_rows > 0 else 0
        report[filename] = {
            "row_counts": total_rows,
            "null_percentages": {
                "deterministic_price": float(null_pct)
            },
            "confidence_distribution": df['confidence_label'].value_counts().to_dict(),
            "tier_distribution": df['tier_reached'].value_counts().to_dict(),
            "residual_statistics": {
                "mean_residual": float(df['residual'].mean()),
                "median_abs_residual": float(df['abs_residual'].median()),
                "mean_residual_pct": float(df['residual_pct'].mean())
            }
        }
    
    db.close()
    
    report_path = os.path.join(OUTPUT_DIR, "hybrid_dataset_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print("Done generating hybrid dataset.")

if __name__ == '__main__':
    generate()
