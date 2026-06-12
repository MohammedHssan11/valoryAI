import os
import shutil
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MOVE_MAP_REMAINING = [
    ("pf_scraper/catboost_info", "Archive/catboost_info"),
    ("pf_scraper/csv_output", "data/scraper_processed_eg/csv_output"),
    ("pf_scraper/fair-price-eg/CMT_TASK3_AUDIT.md", "docs/CMT_TASK3_AUDIT.md"),
    ("pf_scraper/fair-price-eg/FIREBASE_AUTH_ROOT_CAUSE.md", "docs/FIREBASE_AUTH_ROOT_CAUSE.md"),
    ("pf_scraper/fair-price-eg/PROJECT_MASTER_STATE.md", "docs/PROJECT_MASTER_STATE.md"),
    ("pf_scraper/fair-price-eg/README.md", "docs/README_fair_price.md"),
    ("pf_scraper/fair-price-eg/backend.docx", "docs/resources/backend.docx"),
    ("pf_scraper/fair-price-eg/data", "data/db_clean"),
    ("pf_scraper/fair-price-eg/db/seed", "data/db_seed"),
    ("pf_scraper/fair-price-eg/feature_gap_verification.md", "docs/feature_gap_verification.md"),
    ("pf_scraper/fair-price-eg/frontend_product_completion_roadmap.md", "docs/frontend_product_completion_roadmap.md"),
    ("pf_scraper/fair-price-eg/implementation_plan.md", "docs/implementation_plan_fair_price.md"),
    ("pf_scraper/fair-price-eg/next_implementation_plan.md", "docs/next_implementation_plan_fair_price.md"),
    ("pf_scraper/fair-price-eg/property_context_bridge.md", "docs/property_context_bridge.md"),
    ("pf_scraper/fair-price-eg/scripts", "scripts/validation_powershell"),
    ("pf_scraper/fair-price-eg/test_script.py", "Archive/test_script.py"),
    ("pf_scraper/fair-price-eg/valorai-phase3b-valuation-screen.png", "docs/resources/valorai-phase3b-valuation-screen.png"),
    ("pf_scraper/fair-price-eg/walkthrough.md", "docs/walkthrough_fair_price.md"),
    ("pf_scraper/fair-price-eg/zip.zip", "Archive/data_zips/fair_price_zip.zip"),
    ("pf_scraper/fair-price-eg/.env", "Archive/fair_price_env"),
    ("pf_scraper/fair-price-eg/.env.example", "Archive/fair_price_env.example"),
    ("pf_scraper/fair-price-eg/.env.staging.example", "Archive/fair_price_env.staging.example"),
    ("pf_scraper/fair-price-eg/CMT_TASK3_AUDIT.md", "docs/CMT_TASK3_AUDIT.md"),
    ("pf_scraper/fair-price-eg/Image 1.jpeg", "docs/resources/Image_1.jpeg")
]

def is_tracked(path):
    try:
        res = subprocess.run(
            ["git", "ls-files", "--error-unmatch", path],
            cwd=ROOT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return res.returncode == 0
    except Exception:
        return False

def move_path(src_rel, dest_rel):
    src_abs = os.path.join(ROOT_DIR, src_rel)
    dest_abs = os.path.join(ROOT_DIR, dest_rel)
    
    if not os.path.exists(src_abs):
        return
        
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    
    if os.path.exists(dest_abs):
        if os.path.isdir(dest_abs) and not os.listdir(dest_abs):
            os.rmdir(dest_abs)
        elif os.path.isfile(dest_abs):
            os.remove(dest_abs)
            
    tracked = is_tracked(src_rel)
    
    if tracked:
        try:
            res = subprocess.run(
                ["git", "mv", src_rel, dest_rel],
                cwd=ROOT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if res.returncode == 0:
                print(f"Moved via Git: {src_rel} -> {dest_rel}")
                return
        except Exception:
            pass
            
    try:
        shutil.move(src_abs, dest_abs)
        print(f"Moved via Shutil: {src_rel} -> {dest_rel}")
    except Exception as e:
        print(f"Error moving {src_rel}: {e}")

def main():
    # 1. Move the mapped list
    for src, dest in MOVE_MAP_REMAINING:
        move_path(src, dest)
        
    # 2. Move files from pf_scraper/fair-price-eg/docs/ into docs/
    fpe_docs_dir = os.path.join(ROOT_DIR, "pf_scraper/fair-price-eg/docs")
    if os.path.exists(fpe_docs_dir):
        for f in os.listdir(fpe_docs_dir):
            src_f = os.path.join("pf_scraper/fair-price-eg/docs", f)
            dest_f = os.path.join("docs", f)
            move_path(src_f, dest_f)
        try:
            os.rmdir(fpe_docs_dir)
        except Exception:
            pass
            
    # Clean up empty parent directories
    for d in ["pf_scraper/fair-price-eg/db", "pf_scraper/fair-price-eg", "pf_scraper"]:
        path = os.path.join(ROOT_DIR, d)
        if os.path.exists(path):
            try:
                os.rmdir(path)
                print(f"Cleaned up empty folder: {d}")
            except Exception:
                pass

if __name__ == "__main__":
    main()
