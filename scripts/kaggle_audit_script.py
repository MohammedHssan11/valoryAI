import os
import json
import pandas as pd
import numpy as np
import re
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_FILE = os.path.join(ROOT_DIR, "kaggle_audit_results_data.json")

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

def get_file_stats(filepath):
    stat = os.stat(filepath)
    return stat.st_size

def analyze_dataset(filepath, ext):
    results = {
        "columns": [],
        "record_count": 0,
        "null_percentage": 0,
        "duplicate_percentage": 0,
        "example_row": None,
        "pii_risk": False,
        "pii_details": []
    }
    
    try:
        # Load sample to save memory if needed, but we need full count.
        # We will try loading the whole thing. If it fails, we catch it.
        if ext == '.csv':
            df = pd.read_csv(filepath, low_memory=False)
        elif ext == '.json':
            df = pd.read_json(filepath)
        elif ext == '.parquet':
            df = pd.read_parquet(filepath)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath)
        elif ext == '.feather':
            df = pd.read_feather(filepath)
        elif ext in ['.pickle', '.pkl', '.joblib']:
            # risky to load arbitrary pickles without knowing what they are, we'll skip full parse for models/pickles
            # unless it's a known dataframe
            if 'model' in filepath.lower() or 'scaler' in filepath.lower():
                 results['record_count'] = "Model/Artifact"
                 return results
            else:
                 df = pd.read_pickle(filepath)
        else:
            return results
            
        results['record_count'] = len(df)
        if len(df) > 0:
            results['columns'] = list(df.columns)
            # Calculate Nulls
            total_cells = np.prod(df.shape)
            total_nulls = df.isna().sum().sum()
            results['null_percentage'] = float(total_nulls / total_cells * 100) if total_cells > 0 else 0
            
            # Calculate Duplicates
            try:
                duplicates = df.duplicated().sum()
                results['duplicate_percentage'] = float(duplicates / len(df) * 100)
            except Exception:
                # sometimes complex types (lists/dicts) break duplicated()
                results['duplicate_percentage'] = "Error calculating (complex types)"
                
            # Example row
            example = df.iloc[0].to_dict()
            # Convert non-serializable to string
            results['example_row'] = {str(k): str(v) for k, v in example.items()}
            
            # PII Check (very basic heuristics)
            pii_cols = []
            pii_patterns = [r'phone', r'email', r'agent', r'contact', r'lat', r'lng', r'coordinate', r'name']
            for col in results['columns']:
                col_lower = str(col).lower()
                for p in pii_patterns:
                    if re.search(p, col_lower):
                        pii_cols.append(col)
                        break
            if pii_cols:
                results['pii_risk'] = True
                results['pii_details'] = f"Potentially sensitive columns found: {', '.join(pii_cols)}"

    except Exception as e:
        results['error'] = str(e)
        
    return results

def main():
    audit_data = {
        "folders": {},
        "datasets": [],
        "ml_artifacts": [],
        "egypt_specific": {}
    }
    
    dataset_exts = {'.json', '.csv', '.parquet', '.xlsx', '.xls', '.feather', '.pickle', '.pkl', '.joblib'}
    
    # We will specifically store the DataFrames of the Egypt datasets if they load, to check overlap
    egypt_dfs = {}
    egypt_files_target = ['all_egypt.json', 'buy.json', 'commercial_buy.json', 'commercial_rent.json']
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip certain dirs
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '.venv', 'venv', '__pycache__']]
        
        rel_dir = os.path.relpath(root, ROOT_DIR)
        
        folder_info = {
            "file_count": 0,
            "total_size_bytes": 0,
            "important_files": []
        }
        
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = get_file_stats(filepath)
            except Exception:
                continue
                
            folder_info["file_count"] += 1
            folder_info["total_size_bytes"] += size
            
            ext = os.path.splitext(file)[1].lower()
            
            # Check if it's a dataset
            if ext in dataset_exts:
                is_ml_artifact = any(kw in file.lower() for kw in ['model', 'weight', 'checkpoint', 'scaler', 'catboost_info']) or ext in ['.pkl', '.joblib', '.pickle']
                
                # If it's a dataset not marked as an artifact (or even if it is, we might want to log it)
                ds_info = {
                    "filename": file,
                    "path": os.path.relpath(filepath, ROOT_DIR),
                    "size_bytes": size,
                    "ext": ext
                }
                
                if not is_ml_artifact:
                    analysis = analyze_dataset(filepath, ext)
                    ds_info.update(analysis)
                    audit_data["datasets"].append(ds_info)
                    folder_info["important_files"].append(file)
                    
                    # Track Egypt files
                    if file in egypt_files_target:
                        try:
                            egypt_dfs[file] = pd.read_json(filepath)
                        except Exception as e:
                            print(f"Could not load {file} for overlap analysis: {e}")
                else:
                    ds_info["framework"] = "Unknown"
                    if 'catboost' in file.lower(): ds_info["framework"] = "CatBoost"
                    elif 'sklearn' in file.lower() or ext in ['.pkl', '.joblib']: ds_info["framework"] = "Scikit-Learn/Pickle"
                    elif ext == '.pt' or ext == '.pth': ds_info["framework"] = "PyTorch"
                    
                    ds_info["purpose"] = "ML Model/Artifact"
                    audit_data["ml_artifacts"].append(ds_info)
                    folder_info["important_files"].append(file)
                    
        # only keep folders with stuff
        if folder_info["file_count"] > 0:
            audit_data["folders"][rel_dir] = folder_info

    # Overlap Analysis for Egypt datasets
    # Find common columns, and if there's an 'id' or 'url', check overlap percentage
    if len(egypt_dfs) > 1:
        # find common ID col
        id_cols = ['id', 'url', 'property_id', 'link']
        
        overlap_stats = {}
        for f1, df1 in egypt_dfs.items():
            overlap_stats[f1] = {}
            for f2, df2 in egypt_dfs.items():
                if f1 == f2: continue
                # try to find a join key
                join_key = None
                for col in id_cols:
                    if col in df1.columns and col in df2.columns:
                        join_key = col
                        break
                
                if join_key:
                    # check intersection
                    set1 = set(df1[join_key].dropna().astype(str))
                    set2 = set(df2[join_key].dropna().astype(str))
                    if len(set1) > 0:
                        intersection = len(set1.intersection(set2))
                        overlap_stats[f1][f2] = {
                            "join_key": join_key,
                            "overlap_count": intersection,
                            "overlap_percentage_of_f1": (intersection / len(set1)) * 100
                        }
        audit_data["egypt_specific"]["overlap_analysis"] = overlap_stats

    # Write output
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(audit_data, f, indent=2)
        
    print(f"Audit completed. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
