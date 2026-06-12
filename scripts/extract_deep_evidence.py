import os
import json
import pandas as pd
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def format_size(size_bytes):
    if size_bytes == 0: return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

# Using the .jsonl files actually found in the repo
egypt_files = ['all_egypt.jsonl', 'buy.jsonl', 'commercial_buy.jsonl', 'commercial_rent.jsonl']
datasets = {}

for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file in egypt_files and 'data_eg' in root: # target the ones in data_eg
            path = os.path.join(root, file)
            datasets[file] = {
                'path': path,
                'size': os.path.getsize(path)
            }

print("--- 1. Dataset Statistics ---")
for name, info in datasets.items():
    try:
        # Load jsonl line by line
        df = pd.read_json(info['path'], lines=True)
        info['df'] = df
        info['rows'] = len(df)
        info['cols'] = len(df.columns)
        
        total_cells = np.prod(df.shape)
        info['missing_pct'] = (df.isna().sum().sum() / total_cells * 100) if total_cells else 0
        
        try:
            info['dup_pct'] = (df.astype(str).duplicated().sum() / len(df) * 100) if len(df) else 0
        except:
            info['dup_pct'] = 0
            
        info['top_20_cols'] = list(df.columns)[:20]
    except Exception as e:
        print(f"Error loading {name}: {e}")

for name, info in datasets.items():
    if 'df' in info:
        print(f"File: {name} | Size: {format_size(info['size'])} | Rows: {info['rows']} | Cols: {info['cols']} | Dups: {info['dup_pct']:.2f}% | Missing: {info['missing_pct']:.2f}%")
        print(f"Top 20 Columns: {', '.join(info['top_20_cols'])}")

print("\n--- 2. Master Dataset Verification ---")
if 'all_egypt.jsonl' in datasets and 'df' in datasets['all_egypt.jsonl']:
    all_df = datasets['all_egypt.jsonl']['df']
    id_col = 'url' if 'url' in all_df.columns else ('id' if 'id' in all_df.columns else None)
    
    if id_col:
        all_ids = set(all_df[id_col].astype(str).dropna())
        print(f"Master Dataset Key: {id_col}")
        
        for name in ['buy.jsonl', 'commercial_buy.jsonl', 'commercial_rent.jsonl']:
            if name in datasets and 'df' in datasets[name]:
                df = datasets[name]['df']
                if id_col in df.columns:
                    sub_ids = set(df[id_col].astype(str).dropna())
                    intersection = len(sub_ids.intersection(all_ids))
                    pct = (intersection / len(sub_ids) * 100) if len(sub_ids) else 0
                    print(f"{name} -> all_egypt.jsonl: {intersection} records overlap ({pct:.2f}%)")
                else:
                    print(f"{name} -> all_egypt.jsonl: No matching {id_col} column.")

print("\n--- 3. PII Verification ---")
pii_patterns = [r'phone', r'email', r'agent', r'contact', r'lat', r'lng', r'coordinate', r'name']
for name, info in datasets.items():
    if 'df' in info:
        df = info['df']
        for col in df.columns:
            col_lower = str(col).lower()
            for p in pii_patterns:
                if pd.Series(col_lower).str.contains(p, regex=True).any():
                    valid_vals = df[col].dropna()
                    if len(valid_vals) > 0:
                        val = str(valid_vals.iloc[0])
                        if len(val) > 4:
                            redacted = val[:2] + "***" + val[-2:]
                        else:
                            redacted = "***"
                        
                        risk = "REVIEW"
                        if "phone" in col_lower or "email" in col_lower:
                            risk = "REMOVE"
                        elif "name" in col_lower and "agent" in col_lower:
                            risk = "REMOVE"
                            
                        print(f"[{risk}] Dataset: {name} | Col: {col} | Pattern: {p} | Example: {redacted}")

print("\n--- 5. Model Audit ---")
targets = ['models_hybrid_v1', 'models_hybrid_v2', 'dataset_hybrid_v1', 'dataset_v2', 'dataset_v3', 'catboost_info']
for root, dirs, files in os.walk(ROOT_DIR):
    for d in dirs:
        if d in targets:
            path = os.path.join(root, d)
            size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, _, filenames in os.walk(path) for filename in filenames)
            print(f"Folder: {d} | Size: {format_size(size)}")
    for f in files:
         if f in targets:
            path = os.path.join(root, f)
            print(f"File: {f} | Size: {format_size(os.path.getsize(path))}")
