import os
import json
import pandas as pd
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
buy_path = os.path.join(ROOT_DIR, "pf_scraper", "data_eg", "buy.jsonl")
all_egypt_path = os.path.join(ROOT_DIR, "pf_scraper", "data_eg", "all_egypt.jsonl")

print("### Step 1 - File Structure Inspection")
with open(buy_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
    
total_lines = len(lines)
print(f"Total lines in file: {total_lines}")
print("\nFirst 3 lines:")
for i in range(min(3, total_lines)):
    print(lines[i][:100] + "...")

print("\nLast 3 lines:")
for i in range(max(0, total_lines-3), total_lines):
    print(lines[i][:100] + "...")

mid = total_lines // 2
print("\nMiddle 3 lines:")
for i in range(mid, min(total_lines, mid+3)):
    print(lines[i][:100] + "...")


print("\n### Step 2 & 3 - Error Localization & Recovery")
valid_records = []
invalid_records = []

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    try:
        record = json.loads(line)
        valid_records.append(record)
    except json.JSONDecodeError as e:
        invalid_records.append({
            "line": i + 1,
            "error": str(e),
            "snippet": line[:50] + "..."
        })

print(f"Total Lines: {total_lines}")
print(f"Valid Records: {len(valid_records)}")
print(f"Invalid Records: {len(invalid_records)}")
recovery_rate = len(valid_records) / (len(valid_records) + len(invalid_records)) * 100 if (len(valid_records) + len(invalid_records)) > 0 else 0
print(f"Recovery Rate: {recovery_rate:.2f}%\n")

if invalid_records:
    print("Sample corrupted lines (up to 5):")
    for inv in invalid_records[:5]:
        print(f"Line {inv['line']}: {inv['error']} | Snippet: {inv['snippet']}")

print("\n### Step 4 - Schema Verification")
if valid_records:
    df_buy = pd.DataFrame(valid_records)
    print(f"Column count: {len(df_buy.columns)}")
    
    total_cells = np.prod(df_buy.shape)
    missing_pct = (df_buy.isna().sum().sum() / total_cells * 100) if total_cells else 0
    print(f"Missing value percentage: {missing_pct:.2f}%")
    
    try:
        dup_pct = (df_buy.astype(str).duplicated().sum() / len(df_buy) * 100) if len(df_buy) else 0
        print(f"Duplicate percentage: {dup_pct:.2f}%")
    except:
        print("Duplicate percentage: Error calculating")
        
print("\n### Step 5 - Master Dataset Relationship")
if valid_records and os.path.exists(all_egypt_path):
    try:
        df_all = pd.read_json(all_egypt_path, lines=True)
        if 'id' in df_buy.columns and 'id' in df_all.columns:
            buy_ids = set(df_buy['id'].astype(str).dropna())
            all_ids = set(df_all['id'].astype(str).dropna())
            
            overlap = len(buy_ids.intersection(all_ids))
            overlap_pct = (overlap / len(buy_ids) * 100) if len(buy_ids) else 0
            unique_records = len(buy_ids) - overlap
            
            print(f"Overlap count: {overlap}")
            print(f"Overlap percentage: {overlap_pct:.2f}%")
            print(f"Unique records not present in all_egypt.jsonl: {unique_records}")
    except Exception as e:
        print(f"Error checking master dataset: {e}")
