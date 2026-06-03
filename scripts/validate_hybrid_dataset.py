import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_DIR = r"c:\Users\mh978\Downloads\mobile computing project\pf_scraper\data_eg\dataset_hybrid_v1"

def mean_absolute_percentage_error(y_true, y_pred):
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def run_validation():
    for dataset_name in ["residential_rent.parquet", "residential_sale.parquet"]:
        print("="*80)
        print(f"VALIDATING: {dataset_name}")
        path = os.path.join(DATA_DIR, dataset_name)
        df = pd.read_parquet(path)
        
        print("\n--- STEP 1: INSPECT HYBRID DATASET ---")
        print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
        cols_to_check = [
            'deterministic_price', 'confidence_score', 'confidence_label', 
            'tier_reached', 'comparable_count', 'range_low', 'range_high', 
            'residual', 'residual_pct', 'abs_residual'
        ]
        
        for col in cols_to_check:
            if col in df.columns:
                null_pct = df[col].isnull().mean() * 100
                print(f"  {col}: Found | Nulls: {null_pct:.2f}%")
            else:
                print(f"  {col}: MISSING")
                
        print("\n--- STEP 2: RESIDUAL AUDIT ---")
        if 'residual' in df.columns:
            res = df['residual'].dropna()
            if len(res) > 0:
                print(f"Mean:   {res.mean():.2f}")
                print(f"Median: {res.median():.2f}")
                print(f"Std:    {res.std():.2f}")
                print(f"P5:     {res.quantile(0.05):.2f}")
                print(f"P25:    {res.quantile(0.25):.2f}")
                print(f"P50:    {res.quantile(0.50):.2f}")
                print(f"P75:    {res.quantile(0.75):.2f}")
                print(f"P95:    {res.quantile(0.95):.2f}")
                
                plt.figure(figsize=(10,6))
                plt.hist(res, bins=50, alpha=0.7)
                plt.title(f"Residual Distribution - {dataset_name}")
                plt.xlabel("Residual (Actual - Deterministic)")
                plt.savefig(os.path.join(DATA_DIR, f"residual_dist_{dataset_name.replace('.parquet','')}.png"))
                plt.close()
            else:
                print("No valid residuals found.")
            
        print("\n--- STEP 3: BIAS ANALYSIS ---")
        if 'residual' in df.columns:
            for group_col in ['property_type', 'compound_name', 'h3_res8', 'bedrooms']:
                if group_col in df.columns:
                    grouped = df.groupby(group_col)['residual'].mean().dropna().sort_values()
                    if len(grouped) > 0:
                        print(f"\nTop 3 underpriced {group_col} (Actual > Det):")
                        for k, v in grouped.tail(3).items(): print(f"  {k}: {v:.2f}")
                        print(f"\nTop 3 overpriced {group_col} (Actual < Det):")
                        for k, v in grouped.head(3).items(): print(f"  {k}: {v:.2f}")
                    
        print("\n--- STEP 4: CONFIDENCE VALIDATION ---")
        if 'confidence_score' in df.columns and 'abs_residual' in df.columns:
            valid = df.dropna(subset=['confidence_score', 'abs_residual'])
            if len(valid) > 1:
                pearson = valid['confidence_score'].corr(valid['abs_residual'], method='pearson')
                spearman = valid['confidence_score'].corr(valid['abs_residual'], method='spearman')
                print(f"Pearson correlation:  {pearson:.4f}")
                print(f"Spearman correlation: {spearman:.4f}")
            else:
                print("Not enough data to calculate correlation.")
            
        print("\n--- STEP 5: RESIDUAL LEARNABILITY ---")
        if 'residual' in df.columns and 'price' in df.columns:
            drop_cols = [
                'price', 'target_log_price', 'residual', 'residual_pct', 'abs_residual',
                'description', 'url', 'id', 'listing_id', 'latitude', 'longitude', 'scraped_at'
            ]
            X = df.drop(columns=[c for c in drop_cols if c in df.columns])
            y = df['residual']
            
            # Drop datetimes
            datetime_cols = X.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
            X = X.drop(columns=datetime_cols)
            
            # Target features containing NaNs that must be mapped to string for catboost if they're object
            cat_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
            X[cat_features] = X[cat_features].fillna('Unknown').astype(str)
            
            # We must drop rows where 'price' or 'deterministic_price' or 'residual' is NaN
            mask = df['price'].notna() & df['deterministic_price'].notna() & y.notna()
            X = X[mask]
            y = y[mask]
            actual_prices = df['price'][mask]
            det_prices = df['deterministic_price'][mask]
            
            if len(X) > 10:
                # Mock OOT split (e.g. last 15%)
                split_idx = int(len(X) * 0.85)
                X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
                y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
                actual_train, actual_test = actual_prices.iloc[:split_idx], actual_prices.iloc[split_idx:]
                det_train, det_test = det_prices.iloc[:split_idx], det_prices.iloc[split_idx:]
                
                model = CatBoostRegressor(iterations=100, depth=6, learning_rate=0.1, verbose=0, cat_features=cat_features)
                model.fit(X_train, y_train)
                pred_residual = model.predict(X_test)
                
                final_pred_price = det_test + pred_residual
                
                diag_mape = mean_absolute_percentage_error(actual_test, final_pred_price)
                diag_mae = mean_absolute_error(actual_test, final_pred_price)
                diag_rmse = np.sqrt(mean_squared_error(actual_test, final_pred_price))
                diag_r2 = r2_score(actual_test, final_pred_price)
                
                print(f"OOT MAPE: {diag_mape:.2f}%")
                print(f"OOT MAE:  {diag_mae:.2f}")
                print(f"OOT RMSE: {diag_rmse:.2f}")
                print(f"OOT R²:   {diag_r2:.4f}")
                
                det_mape = mean_absolute_percentage_error(actual_test, det_test)
                det_mae = mean_absolute_error(actual_test, det_test)
                det_rmse = np.sqrt(mean_squared_error(actual_test, det_test))
                det_r2 = r2_score(actual_test, det_test)
                
                print("\n--- STEP 6: COMPARE THREE SYSTEMS ---")
                print(f"Deterministic | MAPE: {det_mape:.2f}% | MAE: {det_mae:.0f} | RMSE: {det_rmse:.0f} | R²: {det_r2:.4f}")
                print(f"Diagnostic    | MAPE: {diag_mape:.2f}% | MAE: {diag_mae:.0f} | RMSE: {diag_rmse:.0f} | R²: {diag_r2:.4f}")
            else:
                print("Not enough valid data to train Diagnostic model.")

if __name__ == '__main__':
    run_validation()
