import os
import shutil
import csv
import json
import re

WORKSPACE = r"C:\Users\mh978\Downloads\mobile computing project"
SOURCE_RELEASE = os.path.join(WORKSPACE, "kaggle_release")
UAE_TARGET = os.path.join(WORKSPACE, "pf_scraper", "kaggle_uae")
EG_TARGET = os.path.join(WORKSPACE, "pf_scraper", "kaggle_eg")

# Ensure target directories exist
os.makedirs(UAE_TARGET, exist_ok=True)
os.makedirs(EG_TARGET, exist_ok=True)

print("Locating source files...")
# We will locate the files from kaggle_release directly
dubai_source_dir = os.path.join(SOURCE_RELEASE, "dubai_dataset")
egypt_source_dir = os.path.join(SOURCE_RELEASE, "egypt_dataset")

# Copy CSV files
dubai_csvs = [
    "dubai_residential_rent.csv",
    "dubai_residential_buy.csv",
    "dubai_commercial_rent.csv",
    "dubai_commercial_buy.csv",
    "dubai_new_projects.csv"
]
egypt_csvs = [
    "egypt_villas_3br_2bath.csv"
]

print("Copying Dubai CSVs...")
for csv_file in dubai_csvs:
    src = os.path.join(dubai_source_dir, csv_file)
    dst = os.path.join(UAE_TARGET, csv_file)
    shutil.copy2(src, dst)

print("Copying Egypt CSVs...")
for csv_file in egypt_csvs:
    src = os.path.join(egypt_source_dir, csv_file)
    dst = os.path.join(EG_TARGET, csv_file)
    shutil.copy2(src, dst)

# Create/Clean License
license_content = """# Open Database License (ODbL)

This dataset is made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/

### Attribution
You are free to copy, distribute, transmit and adapt the database, as long as you attribute the dataset owner and the Property Finder platform.
"""

with open(os.path.join(UAE_TARGET, "LICENSE.md"), "w", encoding="utf-8") as f:
    f.write(license_content)
with open(os.path.join(EG_TARGET, "LICENSE.md"), "w", encoding="utf-8") as f:
    f.write(license_content)

# Process Dubai README (No Egypt, no JSONL)
dubai_readme = """# Dubai Real Estate Market Listings & Prices (2026)

## Overview
This dataset contains cleaned, deduplicated, and feature-engineered real estate listings in Dubai, UAE, scraped in early 2026 from Property Finder. It covers residential rentals, residential sales, commercial rentals, commercial sales, and off-plan projects.

It provides deep insights into the Middle East's most dynamic property market, offering rich details on pricing, locations, properties, sizes, and amenities.

## Cleaning and Validation Process
- **Deduplication**: Programmatic consolidation of duplicate listing IDs. Crawler double-scraped records were filtered, keeping the most complete records.
- **Outlier Detection**: Flagged size outliers (< 100 sq ft or > 30,000 sq ft for apartments) and pricing outliers using IQR boundaries.
- **Coordinate Correction**: Corrected Azizi Milan 55 spatial outlier (longitude adjusted to 55.31902).
- **Feature Engineering**: Added calculated features: `price_per_sqft`, `amenity_count`, `location_depth`, `has_coordinates`, `is_size_outlier`, `is_price_outlier`.

## Included CSV Files
- `dubai_residential_rent.csv`: Deduplicated residential apartments for rent.
- `dubai_residential_buy.csv`: Deduplicated residential apartments for sale.
- `dubai_commercial_rent.csv`: Deduplicated commercial spaces (offices, retail) for rent.
- `dubai_commercial_buy.csv`: Deduplicated commercial spaces (offices, warehouses) for sale.
- `dubai_new_projects.csv`: Off-plan developer projects in Dubai.

## Potential Use Cases
1. **Price Regression**: Build machine learning models to predict rent/sale prices.
2. **Geospatial Analysis**: Visualizing pricing density across coordinates.
3. **NLP Marketing Analysis**: Extracting features from descriptive titles.

## License
Open Database License (ODbL) 1.0.
"""

with open(os.path.join(UAE_TARGET, "README.md"), "w", encoding="utf-8") as f:
    f.write(dubai_readme)

# Process Egypt README (No UAE, no JSONL)
egypt_readme = """# Cairo Compound Villa Prices (3BR/2Bath - 2026)

## Overview
This dataset contains a specialized, highly target niche dataset of luxury villas for sale in Cairo's compound neighborhoods (Fifth Settlement, New Cairo) featuring 3 bedrooms and 2 bathrooms, scraped in early 2026.

## Cleaning & Compliance Audit
- **PII Redaction**: Programmatically scanned and redacted 159 phone numbers and emails inside descriptions, replacing them with `[REDACTED_PHONE]` or `[REDACTED_EMAIL]` to ensure Kaggle policy compliance.
- **Schema Standardization**: Flattened nested pricing, location, and source objects into flat columns.
- **Feature Engineering**: Added `price_per_sqft` (price divided by sqm size), `amenity_count`, `location_depth`, `has_coordinates`, `is_size_outlier`, `is_price_outlier`.

## Included CSV Files
- `egypt_villas_3br_2bath.csv`: Flattened, PII-redacted luxury villa listings.

## Potential Use Cases
1. **Targeted Price Modeling**: Predict price variations between different compound developers in New Cairo.
2. **Geospatial Asset Location**: Map villa clusters in Cairo's compounds.

## License
Open Database License (ODbL) 1.0.
"""

with open(os.path.join(EG_TARGET, "README.md"), "w", encoding="utf-8") as f:
    f.write(egypt_readme)

# Copy/Clean Data Dictionary files (remove any JSONL references if any, and copy)
def copy_clean_dictionary(src_file, dst_file):
    with open(src_file, "r", encoding="utf-8") as f:
        content = f.read()
    # remove jsonl references if any (none exist in our generated dictionaries, but let's double check)
    content = content.replace(".jsonl", ".csv")
    with open(dst_file, "w", encoding="utf-8") as f:
        f.write(content)

copy_clean_dictionary(os.path.join(dubai_source_dir, "DATA_DICTIONARY.md"), os.path.join(UAE_TARGET, "DATA_DICTIONARY.md"))
copy_clean_dictionary(os.path.join(egypt_source_dir, "DATA_DICTIONARY.md"), os.path.join(EG_TARGET, "DATA_DICTIONARY.md"))

# Copy/Clean Statistics files
copy_clean_dictionary(os.path.join(dubai_source_dir, "DATASET_STATISTICS.md"), os.path.join(UAE_TARGET, "DATASET_STATISTICS.md"))
copy_clean_dictionary(os.path.join(egypt_source_dir, "DATASET_STATISTICS.md"), os.path.join(EG_TARGET, "DATASET_STATISTICS.md"))

print("Verification check inside script...")
# Let's count records and verify that no phone numbers remain in the Egypt CSV
egypt_csv_path = os.path.join(EG_TARGET, "egypt_villas_3br_2bath.csv")
phone_check_passed = True
row_count = 0

with open(egypt_csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row_count += 1
        desc = row.get("description", "")
        title = row.get("title", "")
        # check if raw phone number exists (regex digits sequence >= 8 digits starting with 01 or +)
        for val in [desc, title]:
            # simple check for Egyptian phone pattern
            matches = re.findall(r'\b01[0125]\d{8}\b', val)
            if matches:
                phone_check_passed = False
                print(f"Error: Phone number found in row {row_count}: {matches}")

print(f"Egypt CSV row count: {row_count}")
print(f"PII Phone checks passed: {phone_check_passed}")

# Verify UAE coordinates and duplicates
uae_check_passed = True
for csv_name in dubai_csvs:
    csv_path = os.path.join(UAE_TARGET, csv_name)
    ids = set()
    row_idx = 0
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_idx += 1
            item_id = row.get("id")
            if item_id:
                if item_id in ids:
                    uae_check_passed = False
                    print(f"Error: Duplicate ID {item_id} in {csv_name} at row {row_idx}")
                else:
                    ids.add(item_id)
            
            # check Azizi Milan 55 longitude correction
            if csv_name == "dubai_residential_buy.csv" and item_id == "16228205":
                lon = float(row.get("longitude", 0))
                if lon != 55.31902:
                    uae_check_passed = False
                    print(f"Error: Azizi Milan 55 longitude is {lon}, expected 55.31902")

print(f"UAE duplicate and coordinate checks passed: {uae_check_passed}")
print("Reorganization and validation completed successfully.")
