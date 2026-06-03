import os
import json
import numpy as np
import pandas as pd
from catboost import CatBoostRegressor, Pool
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, median_absolute_error

DATA_DIR = "c:/Users/mh978/Downloads/mobile computing project/pf_scraper/data_eg"
INPUT_DIR = os.path.join(DATA_DIR, "dataset_v3")
OUTPUT_DIR = os.path.join(DATA_DIR, "dataset_v3")

# Prohibited deterministic features
DETERMINISTIC_FEATURES = [
    "deterministic_price", "comparable_count", "confidence_score",
    "tier_reached", "retrieval_radius", "median_price_per_sqm",
    "weighted_price_per_sqm", "comparable_price_std", "comparable_price_iqr",
    "median_comparable_age_days"
]

def load_and_prep(filename):
    filepath = os.path.join(INPUT_DIR, filename)
    if not os.path.exists(filepath):
        return None
    
    df = pd.read_parquet(filepath)
    
    # 1. Parse dates and engineer time features
    df['scraped_at_utc'] = pd.to_datetime(df['scraped_at_utc'], utc=True)
    df['scraped_year'] = df['scraped_at_utc'].dt.year
    df['scraped_month'] = df['scraped_at_utc'].dt.month
    df['scraped_quarter'] = df['scraped_at_utc'].dt.quarter
    
    # 2. Sort by time
    df = df.sort_values('scraped_at_utc').reset_index(drop=True)
    
    # 3. Calculate listing age days using ONLY train max date
    train_idx = int(len(df) * 0.8)
    if train_idx > 0:
        train_max_date = df['scraped_at_utc'].iloc[:train_idx].max()
    else:
        train_max_date = df['scraped_at_utc'].max()
        
    df['listing_age_days'] = (train_max_date - df['scraped_at_utc']).dt.days
    df['listing_age_days'] = df['listing_age_days'].clip(lower=0)
    
    # 4. Drop unwanted leakage and identifier columns
    cols_to_drop = ['id', 'price', 'share_url', 'images', 'record_type', 'category', 'scraped_at_utc', 'title', 'currency', 'price_period', 'price_type', 'price_raw_value']
    # Phase 5.2A.1: Drop raw scraped location strings so the model learns purely spatial representations
    cols_to_drop += ['location', 'district', 'city', 'governorate', 'geo_validation_status']
    cols_to_drop += DETERMINISTIC_FEATURES
    
    # Drop them if they exist
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    # Target
    target_col = 'target_log_price'
    
    # Ensure target isn't null
    df = df.dropna(subset=[target_col])
    
    # Identify Categoricals
    cat_features = ['property_type', 'compound_name', 'h3_res8', 'h3_res9']
    cat_features = [c for c in cat_features if c in df.columns]
    
    # Fill NaNs in categoricals
    for c in cat_features:
        df[c] = df[c].fillna("Missing").astype(str)
        
    return df, target_col, cat_features

def compute_mape(y_true_real, y_pred_real):
    return np.mean(np.abs((y_true_real - y_pred_real) / y_true_real)) * 100

def compute_metrics(y_true_log, y_pred_log):
    # Reverse log transform to evaluate real-world error
    y_true = np.expm1(y_true_log)
    y_pred = np.expm1(y_pred_log)
    
    # Cap negative predictions just in case
    y_pred = np.maximum(y_pred, 1)
    
    return {
        "MAPE": compute_mape(y_true, y_pred),
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred), # R2 usually better on the log or raw? Let's do raw to show real variance explained.
        "Median_Absolute_Error": median_absolute_error(y_true, y_pred)
    }

def train_and_eval(df, target_col, cat_features):
    # OOT Split 80 / 10 / 10
    n = len(df)
    train_idx = int(n * 0.8)
    val_idx = int(n * 0.9)
    
    train_df = df.iloc[:train_idx]
    val_df = df.iloc[train_idx:val_idx]
    test_df = df.iloc[val_idx:]
    
    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]
    
    X_val = val_df.drop(columns=[target_col])
    y_val = val_df[target_col]
    
    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]
    
    train_pool = Pool(X_train, y_train, cat_features=cat_features)
    val_pool = Pool(X_val, y_val, cat_features=cat_features)
    
    model = CatBoostRegressor(
        iterations=1000,
        learning_rate=0.05,
        depth=6,
        loss_function='RMSE',
        eval_metric='RMSE',
        early_stopping_rounds=50,
        random_seed=42,
        has_time=True,
        verbose=0
    )
    
    model.fit(train_pool, eval_set=val_pool)
    
    # Predict
    test_preds = model.predict(X_test)
    metrics = compute_metrics(y_test, test_preds)
    
    # Feature Importance
    feature_importances = model.get_feature_importance()
    feature_names = X_train.columns
    fi_df = pd.DataFrame({'feature': feature_names, 'importance': feature_importances})
    fi_df = fi_df.sort_values('importance', ascending=False).head(30)
    
    # Error Analysis
    # Let's find top residuals
    y_test_real = np.expm1(y_test)
    y_pred_real = np.expm1(test_preds)
    residuals = np.abs(y_test_real - y_pred_real)
    
    # Get top 5 worst predictions
    worst_idx = residuals.nlargest(5).index
    worst_cases = test_df.loc[worst_idx].copy()
    worst_cases['actual_price'] = y_test_real.loc[worst_idx]
    worst_cases['predicted_price'] = y_pred_real[worst_cases.index.map(lambda i: test_df.index.get_loc(i))]
    worst_cases['error_pct'] = (np.abs(worst_cases['actual_price'] - worst_cases['predicted_price']) / worst_cases['actual_price']) * 100
    
    # Clean up worst cases for JSON serialization
    worst_cases = worst_cases[['actual_price', 'predicted_price', 'error_pct', 'size'] + cat_features].to_dict(orient='records')
    
    return model, metrics, fi_df.to_dict(orient='records'), worst_cases, list(X_train.columns)

def evaluate_valerti_edge_case(model, features_list, cat_features):
    # Apartment A: 180 sqm, 3 bed, 3 bath, basic amenities
    # Apartment B: 188 sqm, 3 bed, 3 bath, richer amenities (AC, Pool View, Fully Finished)
    
    def create_apartment(sqm, beds, baths, has_rich_amenities):
        ap = {f: 0 for f in features_list} # Zero out numericals
        for c in cat_features:
            ap[c] = "Missing" # Default categoricals
            
        ap['size'] = sqm
        ap['bedrooms'] = beds
        ap['bathrooms'] = baths
        ap['compound_name'] = "Valerti" # Or similar mock
        ap['is_known_compound'] = 1
        
        if has_rich_amenities:
            if 'has_amenity_ac' in ap: ap['has_amenity_ac'] = 1
            if 'fully_finished' in ap: ap['fully_finished'] = 1
            if 'pool_view' in ap: ap['pool_view'] = 1
            ap['amenities_count'] = 10
        else:
            if 'core_shell' in ap: ap['core_shell'] = 1
            ap['amenities_count'] = 2
            
        # Convert to DF
        return pd.DataFrame([ap])

    apt_A = create_apartment(180, 3, 3, False)
    apt_B = create_apartment(188, 3, 3, True)
    
    # Predict
    pred_A = np.expm1(model.predict(apt_A))[0]
    pred_B = np.expm1(model.predict(apt_B))[0]
    
    return {
        "Apt_A_Basic_Prediction": float(pred_A),
        "Apt_B_Premium_Prediction": float(pred_B),
        "Premium_Difference": float(pred_B - pred_A),
        "Premium_Percent": float(((pred_B - pred_A) / pred_A) * 100)
    }

def main():
    datasets = [
        "residential_rent.parquet",
        "residential_sale.parquet",
        "commercial_rent.parquet",
        "commercial_sale.parquet"
    ]
    
    results = {}
    
    for filename in datasets:
        print(f"Training on {filename}...")
        parsed = load_and_prep(filename)
        if not parsed:
            print(f"File {filename} not found.")
            continue
            
        df, target_col, cat_features = parsed
        dataset_name = filename.split('.')[0]
        
        # Save shape info
        shape_info = {"total_rows": len(df), "features": len(df.columns) - 1}
        
        model, metrics, fi, worst_cases, feat_list = train_and_eval(df, target_col, cat_features)
        
        results[dataset_name] = {
            "shape": shape_info,
            "metrics": metrics,
            "feature_importance": fi,
            "error_analysis_top5": worst_cases
        }
        
        # Save the model
        model_path = os.path.join(OUTPUT_DIR, f"{dataset_name}.cbm")
        model.save_model(model_path)
        print(f"Saved model to {model_path}")
        
        schema_path = os.path.join(OUTPUT_DIR, f"{dataset_name}_schema.json")
        with open(schema_path, "w") as f:
            json.dump({"features": feat_list, "categoricals": cat_features}, f)
        print(f"Saved feature schema to {schema_path}")
        
        # If residential rent, run the edge case
        if dataset_name == "residential_rent":
            results["valerti_edge_case"] = evaluate_valerti_edge_case(model, feat_list, cat_features)
            
    with open(os.path.join(OUTPUT_DIR, "phase3_6_results.json"), "w") as f:
        json.dump(results, f, indent=2)
        
    print("Training complete. Results saved.")

if __name__ == "__main__":
    main()
