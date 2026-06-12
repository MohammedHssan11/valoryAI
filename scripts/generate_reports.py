import json
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_FILE = os.path.join(ROOT_DIR, "kaggle_audit_results_data.json")
OUTPUT_DIR = os.path.join(ROOT_DIR, "kaggle_audit_reports")

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(DATA_FILE, 'r') as f:
    data = json.load(f)

folders = data.get("folders", {})
datasets = data.get("datasets", [])
ml_artifacts = data.get("ml_artifacts", [])
egypt_specific = data.get("egypt_specific", {})

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

# 1. Repository Audit Report
with open(os.path.join(OUTPUT_DIR, "1_Repository_Audit_Report.md"), 'w', encoding='utf-8') as f:
    f.write("# Repository Audit Report\n\n")
    for d, info in folders.items():
        if "node_modules" in d or ".git" in d or "build" in d or ".dart_tool" in d:
             continue # skip noisy build folders for summary
        f.write(f"### Folder: `{d}`\n")
        f.write(f"- **Purpose**: To be inferred. Contains {info['file_count']} files.\n")
        f.write(f"- **Total Size**: {format_size(info['total_size_bytes'])}\n")
        f.write(f"- **Important Files**: {', '.join(info['important_files']) if info['important_files'] else 'None'}\n")
        
        # Recommendation
        include = False
        if any(ext in str(info['important_files']) for ext in ['.json', '.csv', '.parquet']) and "test" not in d:
            include = True
        f.write(f"- **Recommendation**: {'INCLUDE' if include else 'EXCLUDE'}\n\n")

# 2. Dataset Quality Report
with open(os.path.join(OUTPUT_DIR, "2_Dataset_Quality_Report.md"), 'w', encoding='utf-8') as f:
    f.write("# Dataset Quality Report\n\n")
    
    # Egypt Dataset Analysis
    f.write("## Egypt Datasets Comparison\n")
    f.write("| Dataset | Records | Columns | Missing % | Duplicates % |\n")
    f.write("|---|---|---|---|---|\n")
    for ds in datasets:
        if ds['filename'] in ['all_egypt.json', 'buy.json', 'commercial_buy.json', 'commercial_rent.json']:
            f.write(f"| {ds['filename']} | {ds.get('record_count', 'N/A')} | {len(ds.get('columns', []))} | {ds.get('null_percentage', 0):.2f}% | {ds.get('duplicate_percentage', 0)}% |\n")
    f.write("\n")
    
    f.write("### Overlap Analysis\n")
    overlap = egypt_specific.get("overlap_analysis", {})
    for f1, f2s in overlap.items():
        for f2, stats in f2s.items():
            f.write(f"- **{f1}** overlaps with **{f2}**: {stats['overlap_count']} records ({stats['overlap_percentage_of_f1']:.2f}% of {f1}) on `{stats['join_key']}`\n")
    
    f.write("\n## All Datasets\n")
    for ds in datasets:
        f.write(f"### {ds['filename']} (`{ds['path']}`)\n")
        f.write(f"- **Size**: {format_size(ds['size_bytes'])}\n")
        f.write(f"- **Records**: {ds.get('record_count', 'Error')}\n")
        f.write(f"- **Columns**: {len(ds.get('columns', []))}\n")
        f.write(f"- **Missing %**: {ds.get('null_percentage', 0):.2f}%\n")
        f.write(f"- **Duplicates %**: {ds.get('duplicate_percentage', 0)}\n")
        if ds.get('example_row'):
            f.write(f"- **Example Row**: `{str(ds['example_row'])[:200]}...`\n")
        f.write("\n")

# 3. Kaggle Publication Report
with open(os.path.join(OUTPUT_DIR, "3_Kaggle_Publication_Report.md"), 'w', encoding='utf-8') as f:
    f.write("# Kaggle Publication Report\n\n")
    f.write("## Strategy Recommendation\n")
    f.write("**Recommended: Option C (Raw + Clean)**\n")
    f.write("Publishing both raw scraped data and the processed/cleaned features provides the most value to the Kaggle community. It allows beginners to use the ready ML data, while experts can practice data engineering on the raw data.\n")

# 4 & 5. Files to Include & Exclude
includes = []
excludes = []
for ds in datasets:
    # exclude small test files
    if "test" in ds['path'].lower() or ds.get('record_count', 0) < 1000:
        excludes.append(ds)
    else:
        includes.append(ds)

for ml in ml_artifacts:
    # Usually exclude huge checkpoints, include only final models
    if "checkpoint" in ml['path'].lower():
        excludes.append(ml)
    else:
        includes.append(ml)

with open(os.path.join(OUTPUT_DIR, "4_Files_To_Include.md"), 'w', encoding='utf-8') as f:
    f.write("# Files To Include\n\n")
    for i in includes: f.write(f"- `{i['path']}`\n")

with open(os.path.join(OUTPUT_DIR, "5_Files_To_Exclude.md"), 'w', encoding='utf-8') as f:
    f.write("# Files To Exclude\n\n")
    for e in excludes: f.write(f"- `{e['path']}`\n")

# 6. Recommended Final Kaggle Upload Structure
with open(os.path.join(OUTPUT_DIR, "6_Kaggle_Structure.md"), 'w', encoding='utf-8') as f:
    f.write("# Recommended Final Kaggle Upload Structure\n\n")
    f.write("```\n")
    f.write("dataset/\n")
    f.write("├── raw/\n")
    f.write("│   └── (Original scraped JSONs: all_egypt.json, etc.)\n")
    f.write("├── processed/\n")
    f.write("│   └── (Cleaned CSV/Parquet files used for training)\n")
    f.write("├── models/\n")
    f.write("│   └── (Final pickled models or CatBoost info, if any)\n")
    f.write("├── docs/\n")
    f.write("│   └── data_dictionary.md\n")
    f.write("├── dataset-metadata.json\n")
    f.write("└── README.md\n")
    f.write("```\n")

# 7 & 8. README and Metadata
with open(os.path.join(OUTPUT_DIR, "7_Dataset_README_Draft.md"), 'w', encoding='utf-8') as f:
    f.write("# Egypt Property Real Estate Dataset\n\n")
    f.write("## About Dataset\n")
    f.write("This dataset contains comprehensive real estate listings from Egypt, including residential and commercial properties for both buy and rent categories.\n")
    f.write("\n## Data Sources\n")
    f.write("Scraped from major property platforms (e.g., Property Finder).\n")
    
with open(os.path.join(OUTPUT_DIR, "8_dataset-metadata_Draft.json"), 'w', encoding='utf-8') as f:
    meta = {
        "title": "Egypt Real Estate Listings & Valuations",
        "id": "username/egypt-real-estate-listings",
        "licenses": [{"name": "CC0-1.0"}]
    }
    json.dump(meta, f, indent=2)

# 9. Publication Risk Assessment
with open(os.path.join(OUTPUT_DIR, "9_Publication_Risk_Assessment.md"), 'w', encoding='utf-8') as f:
    f.write("# Publication Risk Assessment\n\n")
    f.write("## PII Risks\n")
    risks = [ds for ds in datasets if ds.get('pii_risk')]
    if risks:
        for r in risks:
            f.write(f"- **{r['filename']}**: {r.get('pii_details')}\n")
        f.write("\n**Mitigation**: Drop or hash all agent names, phone numbers, and exact contact emails before publishing.\n")
    else:
        f.write("No obvious PII column names found. Manual review of text fields is still recommended.\n")

# 10. Final Verdict
with open(os.path.join(OUTPUT_DIR, "10_Final_Verdict.md"), 'w', encoding='utf-8') as f:
    f.write("# Final Verdict\n\n")
    if risks:
        f.write("**READY AFTER CLEANUP**\n\n")
        f.write("Reason: PII data or sensitive columns were detected and need to be anonymized or dropped before a public Kaggle release.\n")
    else:
        f.write("**READY AFTER CLEANUP**\n\n")
        f.write("Reason: Even without obvious PII, the dataset should be reorganized into the proposed `raw/` and `processed/` structure for clarity, and any proprietary models/checkpoints should be stripped.\n")


print("Reports generated.")
