import pandas as pd
import ast
import os
from pathlib import Path

INPUT_DIR = Path("csv_output") 
OUTPUT_DIR = Path("clean_csv")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "rent": "rent.csv",
    "buy": "buy.csv",
    "commercial_rent": "commercial_rent.csv",
    "commercial_buy": "commercial_buy.csv",
    "new_projects": "new_projects.csv",
}

def to_float(x):
    if pd.isna(x): return None
    try:
        return float(str(x).replace(",", "").strip())
    except:
        return None

def to_int(x):
    v = to_float(x)
    return int(round(v)) if v is not None else None

def normalize_period(category, price_period):
    if "rent" in category:
        return "monthly"
    return "sale"

def parse_images_count(x):
    if pd.isna(x): return 0
    try:
        # Safely evaluate string representation of list
        lst = ast.literal_eval(str(x))
        return len(lst) if isinstance(lst, list) else 0
    except:
        return 0

def clean_one(category, filename):
    path = INPUT_DIR / filename
    if not path.exists():
        print(f"Skipping {filename}: File not found.")
        return

    df = pd.read_csv(path)
    out = pd.DataFrame()

    # 1. Basic Identifiers
    out["listing_id"] = df["id"].astype(str) if "id" in df.columns else range(len(df))
    out["category"] = category
    
    # 2. Price & Period
    out["price_egp"] = df["price"].apply(to_float) if "price" in df.columns else None
    out["period"] = normalize_period(category, df.get("price_period"))

    # 3. Property Details
    out["property_type"] = df.get("property_type")
    
    # Bedrooms & Studio logic
    if "bedrooms" in df.columns:
        out["bedrooms"] = df["bedrooms"].apply(to_int)
        if "title" in df.columns:
            is_studio = df["title"].astype(str).str.lower().str.contains("studio|ستوديو")
            out.loc[is_studio, "bedrooms"] = 0
    
    out["bathrooms"] = df["bathrooms"].apply(to_int) if "bathrooms" in df.columns else None
    out["size_sqm"] = df["size"].apply(to_float) if "size" in df.columns else None

    # 4. Location
    out["location_text"] = df.get("location")
    out["lat"] = df["latitude"].apply(to_float) if "latitude" in df.columns else None
    out["lng"] = df["longitude"].apply(to_float) if "longitude" in df.columns else None

    # 5. Metadata
    out["scraped_at_utc"] = df.get("scraped_at_utc")
    out["images_count"] = df["images"].apply(parse_images_count) if "images" in df.columns else 0

    # Preserve raw structured feature fields when the scrape provides them.
    # The backend importer owns conservative normalization.
    for col in [
        "amenities",
        "amenity_names",
        "furnishing_status",
        "furnishing",
        "floor_number",
        "floor",
        "compound_name",
        "compound",
        "view_type",
        "view",
        "building_quality",
        "quality",
        "finishing",
    ]:
        if col in df.columns:
            out[col] = df[col]

    # --- Data Cleaning Filters ---
    before = len(out)
    
    # Mandatory price
    out = out.dropna(subset=["price_egp"])
    out = out[out["price_egp"] > 100] # Filter out placeholder prices like 1 EGP
    
    # Egypt Bounds Filter (Only if coords exist)
    if "lat" in out.columns and "lng" in out.columns:
        # We only drop rows with NaN coords for listings that AREN'T "new_projects"
        if category != "new_projects":
            out = out.dropna(subset=["lat", "lng"])
        
        # Valid Egypt bounds filter for remaining coords
        coord_mask = (out["lat"].between(22.0, 32.5)) & (out["lng"].between(24.0, 36.0))
        # Keep if coords are valid OR if coords are NaN (for new_projects only)
        out = out[coord_mask | (out["lat"].isna())]

    # Size Sanity
    out = out[(out["size_sqm"].isna()) | ((out["size_sqm"] > 5) & (out["size_sqm"] < 10000))]

    after = len(out)
    print(f"✅ {category}: {before} -> {after} rows")

    out_path = OUTPUT_DIR / f"{category}_clean.csv"
    out.to_csv(out_path, index=False, encoding='utf-8-sig')

def main():
    for cat, fname in FILES.items():
        clean_one(cat, fname)
    print("\nAll files processed successfully.")

if __name__ == "__main__":
    main()
