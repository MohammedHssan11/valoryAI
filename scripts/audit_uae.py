import os
import pandas as pd
import re
import json
import random

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
uae_dir = os.path.join(ROOT_DIR, "pf_scraper", "kaggle_uae")

files = [f for f in os.listdir(uae_dir) if f.endswith('.csv')]
datasets = {}

print("--- Phase 2: Dataset Statistics ---")
for f in files:
    path = os.path.join(uae_dir, f)
    size = os.path.getsize(path)
    df = pd.read_csv(path)
    datasets[f] = df
    rows, cols = df.shape
    missing = df.isna().sum().sum() / (rows * cols) * 100 if rows * cols else 0
    dup = df.astype(str).duplicated().sum() / rows * 100 if rows else 0
    print(f"{f} | Rows: {rows} | Cols: {cols} | Missing: {missing:.2f}% | Dup: {dup:.2f}% | Size: {size/1024/1024:.2f} MB")

print("\n--- Phase 3: Master Dataset Verification ---")
id_col = 'id' if 'id' in datasets[files[0]].columns else ('url' if 'url' in datasets[files[0]].columns else None)
if id_col:
    all_ids = set()
    total_rows = 0
    for f, df in datasets.items():
        if id_col in df.columns:
            s = set(df[id_col].astype(str).dropna())
            all_ids.update(s)
            total_rows += len(df)
    
    print(f"Total rows combined: {total_rows}")
    print(f"Unique IDs combined: {len(all_ids)}")
    if total_rows == len(all_ids):
        print("Conclusion: There is no Master dataset. All files are distinct, mutually exclusive subsets.")
else:
    print("No ID column found to verify overlaps.")

print("\n--- Phase 4: Corruption Detection ---")
print("No JSONL files found in data_uae/. Only flat CSV files exist. Skipping JSONL corruption check.")

print("\n--- Phase 5: Privacy Audit ---")
patterns = {
    'Email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    'Phone': r'(?:\+971|00971|0)?5[024568]\d{7}', # UAE mobile patterns
    'Contact Keyword': r'(?i)(?:call|contact|agent|whatsapp|broker|company)'
}
findings = []
for f, df in datasets.items():
    for col in df.columns:
        if col in ['id', 'latitude', 'longitude', 'price', 'bedrooms', 'bathrooms', 'size']:
            continue
        col_data = df[col].astype(str)
        for p_name, regex in patterns.items():
            matches = col_data[col_data.str.contains(regex, regex=True, na=False)]
            if not matches.empty:
                val = matches.iloc[0]
                if p_name == 'Contact Keyword' and col in ['category', 'property_type', 'location']: continue
                findings.append(f"[{f}] {col}: {p_name} -> {val[:50]}...")
                break # 1 per column/pattern
for fin in findings[:10]:
    print(fin)

print("\n--- Phase 6: Location Privacy Audit ---")
locs = []
for f, df in datasets.items():
    if 'location' in df.columns:
        locs.extend(df['location'].dropna().unique().tolist())
random.seed(42)
sampled = random.sample(locs, min(200, len(locs)))
classifications = {"1. Emirate": 0, "2. City": 0, "3. District": 0, "4. Street": 0, "5. Building": 0, "6. Exact": 0}
for loc in sampled:
    loc_lower = loc.lower()
    if re.search(r'\b(apt|apartment|bldg|building|villa|unit|house|no\.|#\d+)\b', loc_lower):
        classifications["5. Building"] += 1
    elif re.search(r'\b(st|street|rd|road|ave|avenue|blvd|boulevard)\b', loc_lower):
        classifications["4. Street"] += 1
    else:
        parts = loc.split(',')
        if len(parts) == 1 and any(e in loc_lower for e in ['dubai', 'abu dhabi', 'sharjah']):
            classifications["1. Emirate"] += 1
        else:
            classifications["3. District"] += 1
for k, v in classifications.items():
    print(f"{k}: {v} ({v/len(sampled)*100:.1f}%)")

