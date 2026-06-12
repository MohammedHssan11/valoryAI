import os
import sys
import random
from sqlalchemy import text

os.environ['DATABASE_URL'] = 'postgresql+psycopg2://fairprice:fairprice@localhost:5432/fairprice'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app.db.session import SessionLocal
from app.comps.selector import fetch_comps
from app.services.valuation_service import price_listing
from app.api.schemas.pricing import RentFairPriceRequest

def run_audit():
    print("=== STEP 1: DATABASE CONTENT AUDIT ===")
    try:
        db = SessionLocal()
        listings_count = db.execute(text("SELECT COUNT(*) FROM listings")).scalar()
        areas_count = db.execute(text("SELECT COUNT(*) FROM areas")).scalar()
        rent_count = db.execute(text("SELECT COUNT(*) FROM listings WHERE category='rent'")).scalar()
        sale_count = db.execute(text("SELECT COUNT(*) FROM listings WHERE category='buy'")).scalar()
        
        print(f"Total listings: {listings_count}")
        print(f"Rent listings: {rent_count}")
        print(f"Sale listings: {sale_count}")
        print(f"Total areas: {areas_count}")
        
        if listings_count == 0:
            print("\nDATABASE CONTENT MISSING")
            return
            
        print("\n=== STEP 2: COMPARABLE ENGINE AUDIT ===")
        subjects = db.execute(text("SELECT lat, lng, area_id, property_type, bedrooms, bathrooms, size_sqm FROM listings WHERE category='rent' AND lat IS NOT NULL LIMIT 20")).fetchall()
        
        for i, sub in enumerate(subjects):
            params = {
                "lat": float(sub[0]),
                "lng": float(sub[1]),
                "area_id": sub[2],
                "property_type": sub[3],
                "property_category": "residential",
                "listing_category": "rent",
                "listing_period": "monthly",
                "bedrooms": sub[4],
                "bathrooms": sub[5],
                "size_sqm": float(sub[6]) if sub[6] else 100.0,
                "target_features": {}
            }
            comps, tier_used, trace = fetch_comps(db, params, include_trace=True)
            avg_dist = sum(c.get('dist_m', 0) for c in comps)/len(comps) if len(comps) > 0 else 0
            print(f"Test {i+1}: comps={len(comps)}, tier={tier_used}, avg_distance={avg_dist:.2f}m")

        print("\n=== STEP 3: VALUATION AUDIT ===")
        completed = 0
        for i, sub in enumerate(subjects):
            if completed >= 10: break
            try:
                req = RentFairPriceRequest(
                    location_mode="manual_coordinates",
                    lat=float(sub[0]),
                    lng=float(sub[1]),
                    property_category="residential",
                    property_type=sub[3] or "Apartment",
                    bedrooms=sub[4],
                    bathrooms=sub[5],
                    size_sqm=float(sub[6]) if sub[6] else 100.0
                )
                res = price_listing(req, db)
                conf_score = res.confidence.get('score', 0) if isinstance(res.confidence, dict) else (res.confidence.score if hasattr(res.confidence, 'score') else 0)
                print(f"Valuation {completed+1}: price={res.fair_price_egp}, conf={conf_score:.2f}, comps={res.comps_count}, range=[{res.range_low_egp}, {res.range_high_egp}]")
                completed += 1
            except Exception as e:
                pass

        print("\nHYBRID DATASET REGENERATION READY")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        print("\nDATABASE CONTENT MISSING")
    finally:
        db.close()

if __name__ == '__main__':
    run_audit()
