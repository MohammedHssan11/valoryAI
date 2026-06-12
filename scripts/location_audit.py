import os
import pandas as pd
import random
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_path = os.path.join(ROOT_DIR, "pf_scraper", "data_eg", "all_egypt.jsonl")

df = pd.read_json(file_path, lines=True)

# get unique locations to avoid massive duplication in the sample
locations = df['location'].dropna().unique().tolist()
random.seed(42)
sampled = random.sample(locations, min(200, len(locations)))

classifications = {
    "1. Governorate only": 0,
    "2. City": 0,
    "3. District / Neighborhood": 0,
    "4. Street name": 0,
    "5. Building / Apartment level": 0,
    "6. Exact private address": 0
}

governorates = ['cairo', 'giza', 'alexandria', 'red sea', 'matrouh']
cities = ['new cairo', '6 october', 'sheikh zayed', 'shorouk', 'obour', 'badr', 'new capital']

detailed_output = []

for loc in sampled:
    loc_lower = loc.lower()
    
    # Check for exact private address / building / appt
    if re.search(r'\b(apt|apartment|bldg|building|villa|unit|house|no\.|#\d+)\b', loc_lower):
        if re.search(r'\d+', loc_lower):
             classifications["6. Exact private address"] += 1
             detailed_output.append(f"[6] {loc}")
        else:
             classifications["5. Building / Apartment level"] += 1
             detailed_output.append(f"[5] {loc}")
    # Check for street name
    elif re.search(r'\b(st|street|rd|road|ave|avenue|axis|corridor|sq|square|axis)\b', loc_lower):
        classifications["4. Street name"] += 1
        detailed_output.append(f"[4] {loc}")
    else:
        # We assume if it has 3+ comma separated parts, it's at least a district
        parts = [p.strip() for p in loc_lower.split(',')]
        if any(g in loc_lower for g in governorates) and len(parts) == 1:
            classifications["1. Governorate only"] += 1
            detailed_output.append(f"[1] {loc}")
        elif any(c in loc_lower for c in cities) and len(parts) <= 2:
            classifications["2. City"] += 1
            detailed_output.append(f"[2] {loc}")
        else:
            classifications["3. District / Neighborhood"] += 1
            detailed_output.append(f"[3] {loc}")

print("--- CLASSIFICATION COUNTS ---")
total = len(sampled)
for k, v in classifications.items():
    print(f"{k}: {v} ({v/total*100:.1f}%)")

print("\n--- SAMPLE OF CLASSIFIED LOCATIONS ---")
for out in detailed_output[:50]:
    print(out)
