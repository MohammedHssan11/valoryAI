import os
import json
import pandas as pd
import numpy as np
import h3
import re
from rapidfuzz import process, fuzz

DATA_DIR = "c:/Users/mh978/Downloads/mobile computing project/pf_scraper/data_eg"
OUTPUT_DIR = os.path.join(DATA_DIR, "dataset_v3")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEDUP_STATS = {}

TEXT_FEATURES = {
    "is_furnished": r"(?i)\b(?<!un)furnished\b|مفروش|فرش",
    "has_garden": r"(?i)\bgarden\b|حديقة|private garden",
    "sea_view": r"(?i)sea view|فيو بحر|مطلة على البحر",
    "pool_view": r"(?i)\bpool\b|حمام سباحة|بيسين",
    "corner_unit": r"(?i)\bcorner\b|ناصية",
    "fully_finished": r"(?i)fully finished|تشطيب كامل|سوبر لوكس|ultra super lux",
    "core_shell": r"(?i)core and shell|core & shell|طوب احمر|بدون تشطيب",
    "semi_furnished": r"(?i)semi furnished|نصف مفروش",
    "hotel_apartment": r"(?i)hotel apartment|شقة فندقية|فندقي",
    "luxury": r"(?i)\bluxury\b|فاخر|vip",
    "prime_location": r"(?i)prime location|موقع مميز",
    "is_duplex": r"(?i)\bduplex\b|دوبلكس",
    "is_penthouse": r"(?i)\bpenthouse\b|بنتهاوس|رووف",
    "is_ground_floor": r"(?i)ground floor|دور ارضي|ارضي",
    "is_clinic": r"(?i)\bclinic\b|عيادة",
    "is_office": r"(?i)\boffice\b|مكتب",
    "is_shop": r"(?i)\bshop\b|محل|تجارى|تجاري",
    "is_admin": r"(?i)\badmin\b|اداري",
    "has_nanny_room": r"(?i)\bnanny\b|\bmaid\b|غرفة مربية|غرفة خادمة",
    "has_driver_room": r"(?i)\bdriver\b|غرفة سائق",
    "has_private_entrance": r"(?i)private entrance|مدخل خاص"
}

DETERMINISTIC_FEATURES = [
    "deterministic_price", "comparable_count", "confidence_score",
    "tier_reached", "retrieval_radius", "median_price_per_sqm",
    "weighted_price_per_sqm", "comparable_price_std", "comparable_price_iqr",
    "median_comparable_age_days"
]

def load_new_projects():
    filepath = os.path.join(DATA_DIR, "new_projects.jsonl")
    projects = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                try:
                    projects.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return pd.DataFrame(projects)

def dump_text_feature_dictionary():
    with open(os.path.join(OUTPUT_DIR, "text_feature_dictionary.json"), "w", encoding="utf-8") as f:
        json.dump(TEXT_FEATURES, f, indent=2, ensure_ascii=False)

def get_train_subset(df):
    if 'scraped_at_utc' not in df.columns:
        return df
    sorted_df = df.sort_values('scraped_at_utc')
    train_size = int(len(sorted_df) * 0.8)
    return sorted_df.iloc[:train_size]

def extract_text_features(df):
    for feat, pattern in TEXT_FEATURES.items():
        # Search in title, fallback to location if needed, but title is priority
        # We can search in title + location combined
        text_corpus = df['title'].fillna('') + " " + df['location'].fillna('')
        df[feat] = text_corpus.str.contains(pattern, na=False).astype(int)
    return df

def expand_amenities(df):
    if 'amenities' not in df.columns:
        return df
    
    train_df = get_train_subset(df)
    all_amenities = train_df['amenities'].dropna().explode()
    if all_amenities.empty:
        return df
        
    top_amenities = all_amenities.value_counts().head(30).index.tolist()
    
    for am in top_amenities:
        col_name = f"has_amenity_{am.lower().replace(' ', '_')}"
        df[col_name] = df['amenities'].apply(lambda x: 1 if isinstance(x, list) and am in x else 0)
        
    df['amenities_count'] = df['amenities'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    return df

def geo_validation(df):
    status = []
    for _, row in df.iterrows():
        lat, lon = row.get('latitude'), row.get('longitude')
        if pd.isna(lat) or pd.isna(lon):
            status.append("missing")
        else:
            try:
                lat_f, lon_f = float(lat), float(lon)
                if (22.0 <= lat_f <= 31.5) and (25.0 <= lon_f <= 35.0):
                    status.append("valid")
                else:
                    status.append("invalid")
            except:
                status.append("invalid")
                
    df['geo_validation_status'] = status
    
    # Nullify coords if not valid
    invalid_mask = df['geo_validation_status'] != "valid"
    df.loc[invalid_mask, 'latitude'] = np.nan
    df.loc[invalid_mask, 'longitude'] = np.nan
    
    return df

def generate_h3_features(df):
    def safe_h3(lat, lon, res):
        try:
            if pd.isna(lat) or pd.isna(lon):
                return None
            return h3.latlng_to_cell(float(lat), float(lon), res)
        except:
            return None
            
    df['h3_res8'] = df.apply(lambda row: safe_h3(row['latitude'], row['longitude'], 8), axis=1)
    df['h3_res9'] = df.apply(lambda row: safe_h3(row['latitude'], row['longitude'], 9), axis=1)
    return df

def normalize_compound_name(name):
    if pd.isna(name): return ""
    name = str(name).lower()
    name = re.sub(r'[^\w\s]', '', name)
    # Remove generic keywords
    stopwords = ["compound", "new cairo", "the", "in", "settlement", "fifth"]
    for word in stopwords:
        name = re.sub(rf'\b{word}\b', '', name)
    return " ".join(name.split())

def apply_compound_features(df, projects_df):
    if projects_df.empty:
        df['compound_name'] = "Unknown"
        df['is_known_compound'] = 0
        df['compound_match_confidence'] = 0.0
        df['compound_frequency'] = 0
        return df
        
    known_titles = projects_df['title'].dropna().unique().tolist()
    norm_to_raw = {normalize_compound_name(t): t for t in known_titles if normalize_compound_name(t)}
    norm_known_titles = list(norm_to_raw.keys())
    
    def match_compound(text):
        if pd.isna(text) or not text.strip(): return ("Unknown", 0.0)
        norm_text = normalize_compound_name(text)
        if not norm_text: return ("Unknown", 0.0)
        
        # Stage 1: Exact normalized match
        for norm_kt in norm_known_titles:
            if norm_kt == norm_text:
                return (norm_to_raw[norm_kt], 1.0)
                
        # Stage 2: Substring of normalized match with word boundaries
        for norm_kt in norm_known_titles:
            if re.search(rf'\b{re.escape(norm_kt)}\b', norm_text):
                return (norm_to_raw[norm_kt], 0.95)
                
        # Stage 3: Fuzzy match
        match = process.extractOne(norm_text, norm_known_titles, scorer=fuzz.token_set_ratio)
        if match:
            best_match, score, _ = match
            if score > 85:
                return (norm_to_raw[best_match], score / 100.0)
                
        return ("Unknown", 0.0)
        
    # Check location first, then title if location fails
    matches = df['location'].apply(match_compound)
    mask_unknown = matches.apply(lambda x: x[0] == "Unknown")
    
    # Try title for unknowns
    if 'title' in df.columns:
        title_matches = df.loc[mask_unknown, 'title'].apply(match_compound)
        matches.loc[mask_unknown] = title_matches
        
    df['compound_name'] = matches.apply(lambda x: x[0])
    df['compound_match_confidence'] = matches.apply(lambda x: x[1])
    df['is_known_compound'] = (df['compound_name'] != "Unknown").astype(int)
    
    train_df = get_train_subset(df)
    freq = train_df['compound_name'].value_counts()
    df['compound_frequency'] = df['compound_name'].map(freq).fillna(0)
    
    return df

def stub_deterministic_features(df):
    for f in DETERMINISTIC_FEATURES:
        df[f] = np.nan
    return df

def validate_and_clean(df):
    # Only drop rows with invalid basic bounds for price and size
    df = df[df['price'] > 10000] # Fake 1 EGP listings
    df = df[(df['size'] >= 20) & (df['size'] <= 5000)]
    
    # MAD filtering aligned with Deterministic Engine
    # Calculated purely on training horizon to prevent leakage
    train_df = get_train_subset(df)
    
    filtered_dfs = []
    for prop_type, group in df.groupby('property_type'):
        train_group = train_df[train_df['property_type'] == prop_type]
        if len(train_group) < 10:
            filtered_dfs.append(group)
            continue
            
        median = train_group['price'].median()
        mad = np.median(np.abs(train_group['price'] - median))
        
        if mad == 0:
            filtered_dfs.append(group)
        else:
            mod_z = 0.6745 * np.abs(group['price'] - median) / mad
            filtered_dfs.append(group[mod_z <= 5.0])
            
    if filtered_dfs:
        df = pd.concat(filtered_dfs)
        
    return df

def process_dataset(name, filename, is_rent, projects_df):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return None
        
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            try:
                data.append(json.loads(line))
            except:
                pass
                
    df = pd.DataFrame(data)
    if df.empty: return None
    
    rows_before = len(df)
    
    if 'scraped_at_utc' in df.columns:
        df['scraped_at_utc'] = pd.to_datetime(df['scraped_at_utc'], utc=True)
        df = df.sort_values('scraped_at_utc')
        
    # Tier 1
    if 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'], keep='last')
        
    # Tier 2
    if 'share_url' in df.columns:
        df = df.drop_duplicates(subset=['share_url'], keep='last')
    
    # Basic numeric conversions
    for col in ['price', 'size', 'bedrooms', 'bathrooms', 'latitude', 'longitude']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Tier 3
    tier3 = ['property_type', 'location', 'size', 'bedrooms', 'bathrooms', 'price']
    ext3 = [c for c in tier3 if c in df.columns]
    if len(ext3) == len(tier3):
        df = df.drop_duplicates(subset=ext3, keep='last')
        
    # Tier 4
    tier4 = ['property_type', 'location', 'size', 'bedrooms', 'bathrooms', 'latitude', 'longitude']
    ext4 = [c for c in tier4 if c in df.columns]
    if len(ext4) == len(tier4):
        df = df.drop_duplicates(subset=ext4, keep='last')
        
    rows_after = len(df)
    DEDUP_STATS[name] = {
        'Rows Before': rows_before,
        'Rows After': rows_after,
        'Duplicates Removed': rows_before - rows_after,
        'Duplicate %': ((rows_before - rows_after) / rows_before) * 100 if rows_before > 0 else 0,
        'Remaining Duplicates': 0
    }
            
    df = validate_and_clean(df)
    
    # Target formulation
    df['target_log_price'] = np.log1p(df['price'])
        
    df = extract_text_features(df)
    df = expand_amenities(df)
    df = geo_validation(df)
    df = generate_h3_features(df)
    df = apply_compound_features(df, projects_df)
    df = stub_deterministic_features(df)
    
    # Drop complex object columns for parquet
    if 'amenities' in df.columns:
        df = df.drop(columns=['amenities'])
    if 'images' in df.columns:
        df = df.drop(columns=['images'])
        
    return df

def generate_profiling_reports(dfs_dict):
    missing_data = []
    cardinality_data = []
    amenity_counts = []
    compound_counts = []
    text_counts = []
    geo_validation_data = []
    
    for name, df in dfs_dict.items():
        if df is None: continue
        
        # Missing values
        missing = df.isna().sum().reset_index()
        missing.columns = ['feature', 'missing_count']
        missing['dataset'] = name
        missing['total_rows'] = len(df)
        missing['missing_percentage'] = (missing['missing_count'] / len(df)) * 100
        missing_data.append(missing)
        
        # Cardinality
        cats = df.select_dtypes(include=['object', 'category']).columns
        card = pd.DataFrame({'feature': cats, 'unique_values': [df[c].nunique() for c in cats]})
        card['dataset'] = name
        cardinality_data.append(card)
        
        # Amenity frequency
        amenity_cols = [c for c in df.columns if c.startswith('has_amenity_')]
        if amenity_cols:
            am_freq = df[amenity_cols].sum().reset_index()
            am_freq.columns = ['amenity', 'count']
            am_freq['dataset'] = name
            amenity_counts.append(am_freq)
            
        # Compound frequency
        cf = df['compound_name'].value_counts().reset_index()
        cf.columns = ['compound_name', 'count']
        cf['dataset'] = name
        compound_counts.append(cf)
        
        # Text feature frequency
        text_cols = list(TEXT_FEATURES.keys())
        exist_text_cols = [c for c in text_cols if c in df.columns]
        if exist_text_cols:
            tf = df[exist_text_cols].sum().reset_index()
            tf.columns = ['text_feature', 'count']
            tf['dataset'] = name
            text_counts.append(tf)
            
        # Geo Validation Status
        geo = df['geo_validation_status'].value_counts().reset_index()
        geo.columns = ['geo_validation_status', 'count']
        geo['dataset'] = name
        geo_validation_data.append(geo)

    def safe_concat(lst, filename):
        if lst:
            res = pd.concat(lst, ignore_index=True)
            res.to_csv(os.path.join(OUTPUT_DIR, filename), index=False)

    safe_concat(missing_data, "missing_values_report.csv")
    safe_concat(cardinality_data, "cardinality_report.csv")
    safe_concat(amenity_counts, "amenity_frequency.csv")
    safe_concat(compound_counts, "compound_frequency.csv")
    safe_concat(text_counts, "text_feature_frequency.csv")
    safe_concat(geo_validation_data, "coordinate_quality_report.csv")
    
def generate_feature_registry(dfs_dict):
    registry = []
    # Just take one valid df for schema
    sample_df = None
    for df in dfs_dict.values():
        if df is not None:
            sample_df = df
            break
            
    if sample_df is None: return
    
    text_feat_keys = list(TEXT_FEATURES.keys())
    
    for col in sample_df.columns:
        cat = "raw"
        if col.startswith("has_amenity_") or col == "amenities_count":
            cat = "amenity"
        elif col in text_feat_keys:
            cat = "text"
        elif "compound" in col:
            cat = "compound"
        elif "h3" in col or col in ["latitude", "longitude", "geo_validation_status"]:
            cat = "geo"
        elif col in DETERMINISTIC_FEATURES:
            cat = "deterministic"
        elif col == "target_log_price":
            cat = "derived"
            
        dtype_str = str(sample_df[col].dtype)
        nullable = sample_df[col].isna().any()
        
        registry.append({
            "feature_name": col,
            "source": cat,
            "datatype": dtype_str,
            "nullable": nullable,
            "description": f"Feature {col} from {cat}",
            "category": cat
        })
        
    pd.DataFrame(registry).to_csv(os.path.join(OUTPUT_DIR, "feature_registry.csv"), index=False)

def main():
    dump_text_feature_dictionary()
    
    print("Loading new projects...")
    projects_df = load_new_projects()
    
    tasks = [
        ("residential_rent", "rent.jsonl", True),
        ("residential_sale", "buy.jsonl", False),
        ("commercial_rent", "commercial_rent.jsonl", True),
        ("commercial_sale", "commercial_buy.jsonl", False)
    ]
    
    dfs_dict = {}
    
    for name, filename, is_rent in tasks:
        print(f"Processing {name}...")
        df = process_dataset(name, filename, is_rent, projects_df)
        if df is not None:
            out_path = os.path.join(OUTPUT_DIR, f"{name}.parquet")
            df.to_parquet(out_path, index=False)
            print(f"Saved {out_path} with {len(df)} rows.")
            dfs_dict[name] = df
            
    with open(os.path.join(OUTPUT_DIR, "dedup_stats.json"), "w") as f:
        json.dump(DEDUP_STATS, f, indent=2)
            
    print("Generating Profiling Reports...")
    generate_profiling_reports(dfs_dict)
    print("Generating Feature Registry...")
    generate_feature_registry(dfs_dict)

if __name__ == "__main__":
    main()
