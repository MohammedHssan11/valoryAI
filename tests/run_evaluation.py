import os
import sys
import argparse
import time
import random
import pandas as pd
from dotenv import load_dotenv

# Load env variables from backend .env file
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", ".env")))

from sqlalchemy import text

# Insert backend directory path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.session import SessionLocal
from app.api.schemas.pricing import RentFairPriceRequest
from app.services.valuation_service import price_listing

def parse_args():
    parser = argparse.ArgumentParser(description="CMT Valuation Engine Empirical Evaluation Runner")
    parser.add_argument("--dry-run", action="store_true", help="Run only on a small test sample of 5 listings")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for sampling reproducibility")
    return parser.parse_args()

def main():
    args = parse_args()
    random.seed(args.seed)
    
    db = SessionLocal()
    try:
        print("Fetching candidate listings from the database...")
        # Get residential rent listings
        query = text("""
            SELECT 
                l.listing_id,
                l.price_egp,
                l.property_type,
                l.compound_name,
                a.name AS area_name,
                l.bedrooms,
                l.bathrooms,
                l.size_sqm,
                l.lat,
                l.lng,
                l.normalized_amenities,
                l.category
            FROM listings l
            JOIN areas a ON l.area_id = a.area_id
            WHERE l.category = 'rent'
              AND l.price_egp > 0
              AND l.size_sqm > 0
              AND l.lat IS NOT NULL
              AND l.lng IS NOT NULL
            ORDER BY l.listing_id
        """)
        all_candidates = [dict(row) for row in db.execute(query).mappings().all()]
        print(f"Total candidate listings found: {len(all_candidates)}")
        
        if not all_candidates:
            print("Error: No candidate listings found in database. Cannot proceed.")
            sys.exit(1)
            
        # Draw random samples
        sample_size = 5 if args.dry_run else 500
        if len(all_candidates) < sample_size:
            print(f"Warning: Only {len(all_candidates)} candidates available. Sampling all of them.")
            sampled_listings = all_candidates
        else:
            sampled_listings = random.sample(all_candidates, sample_size)
            
        print(f"Sampled {len(sampled_listings)} listings for evaluation.")
        
        # Build DataFrame for exporting datasets
        dataset_df = pd.DataFrame([{
            "listing_id": l["listing_id"],
            "price": l["price_egp"],
            "property_type": l["property_type"],
            "compound": l["compound_name"],
            "area": l["area_name"],
            "bedrooms": l["bedrooms"],
            "bathrooms": l["bathrooms"],
            "size_sqm": float(l["size_sqm"]),
            "lat": l["lat"],
            "lng": l["lng"]
        } for l in sampled_listings])
        
        # Save nested sample datasets
        os.makedirs("cmt_test/datasets", exist_ok=True)
        if args.dry_run:
            dataset_df.to_csv("cmt_test/datasets/sample_dry_run.csv", index=False)
            print("Exported cmt_test/datasets/sample_dry_run.csv")
        else:
            dataset_df.head(100).to_csv("cmt_test/datasets/sample_100.csv", index=False)
            dataset_df.head(250).to_csv("cmt_test/datasets/sample_250.csv", index=False)
            dataset_df.to_csv("cmt_test/datasets/sample_500.csv", index=False)
            print("Exported cmt_test/datasets/sample_100.csv, sample_250.csv, sample_500.csv")
            
        # Run Leave-One-Out Valuation Loop
        print("\nStarting Leave-One-Out validation runs...")
        results = []
        
        for idx, listing in enumerate(sampled_listings):
            listing_id = listing["listing_id"]
            actual_price = listing["price_egp"]
            
            t0 = time.perf_counter()
            try:
                # Delete the listing inside the transaction
                db.execute(text("DELETE FROM listings WHERE listing_id = :id"), {"id": listing_id})
                
                # Build RentFairPriceRequest
                req = RentFairPriceRequest(
                    lat=listing["lat"],
                    lng=listing["lng"],
                    property_type=listing["property_type"],
                    property_category="residential_rent",
                    bedrooms=listing["bedrooms"],
                    bathrooms=listing["bathrooms"],
                    size_sqm=float(listing["size_sqm"]),
                    compound_name=listing["compound_name"],
                    amenities=listing["normalized_amenities"] if listing["normalized_amenities"] else []
                )
                
                # Execute CMT engine
                res = price_listing(req, db)
                duration_ms = round((time.perf_counter() - t0) * 1000, 2)
                
                predicted_price = res.fair_price_egp
                confidence = res.confidence.score
                tier_used = res.tier_used
                comps_count = res.comps_count
                
                error_pct = abs(actual_price - predicted_price) / max(actual_price, 1)
                
                results.append({
                    "listing_id": listing_id,
                    "actual_price": actual_price,
                    "predicted_price": predicted_price,
                    "error_pct": error_pct,
                    "confidence": confidence,
                    "tier_used": tier_used,
                    "comps_count": comps_count,
                    "execution_time_ms": duration_ms
                })
                
                # Print progress periodic logs
                if (idx + 1) % 50 == 0 or args.dry_run or (idx + 1) == len(sampled_listings):
                    print(f"Progress: Completed {idx + 1}/{len(sampled_listings)} valuations. (Last listing: {listing_id}, error: {error_pct:.2%})")
                    
            except Exception as e:
                print(f"Error evaluating listing {listing_id}: {str(e)}")
                results.append({
                    "listing_id": listing_id,
                    "actual_price": actual_price,
                    "predicted_price": 0,
                    "error_pct": 1.0,
                    "confidence": 0.0,
                    "tier_used": 5,
                    "comps_count": 0,
                    "execution_time_ms": round((time.perf_counter() - t0) * 1000, 2)
                })
            finally:
                # Rollback transaction to restore the listing
                db.rollback()
                
        # Build Results DataFrame
        results_df = pd.DataFrame(results)
        
        # Save nested raw results
        os.makedirs("cmt_test/raw_results", exist_ok=True)
        if args.dry_run:
            results_df.to_csv("cmt_test/raw_results/results_dry_run.csv", index=False)
            print("Exported cmt_test/raw_results/results_dry_run.csv")
        else:
            results_df.head(100).to_csv("cmt_test/raw_results/results_100.csv", index=False)
            results_df.head(250).to_csv("cmt_test/raw_results/results_250.csv", index=False)
            results_df.to_csv("cmt_test/raw_results/results_500.csv", index=False)
            print("Exported cmt_test/raw_results/results_100.csv, results_250.csv, results_500.csv")
            
        print("\nLeave-One-Out validation completed successfully.")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
