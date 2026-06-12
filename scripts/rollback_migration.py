import os
import shutil
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Format: (method, current_path, original_path)
ACTIONS = [('git', 'frontend/mobile', 'flutter_valorai'), ('git', 'frontend/web', 'pf_scraper/fair-price-eg/frontend'), ('git', 'Archive/frontend_old', 'pf_scraper/fair-price-eg/frontend old'), ('git', 'Archive/react_valorai_prototype', 'react valorai'), ('git', 'backend', 'pf_scraper/fair-price-eg/backend'), ('git', 'backend/scraper', 'pf_scraper/pf_scraper'), ('git', 'infra/docker', 'pf_scraper/fair-price-eg/docker'), ('git', 'infra/docker-compose.yml', 'pf_scraper/fair-price-eg/docker-compose.yml'), ('git', 'tests', 'cmt_test'), ('shutil', 'scripts/audit_uae.py', 'audit_uae.py'), ('shutil', 'scripts/build_kaggle_package.py', 'build_kaggle_package.py'), ('git', 'scripts/build_release.py', 'build_release.py'), ('shutil', 'scripts/extract_deep_evidence.py', 'extract_deep_evidence.py'), ('shutil', 'scripts/generate_notebooks.py', 'generate_notebooks.py'), ('shutil', 'scripts/generate_reports.py', 'generate_reports.py'), ('shutil', 'scripts/investigate_buy.py', 'investigate_buy.py'), ('shutil', 'scripts/kaggle_audit_script.py', 'kaggle_audit_script.py'), ('shutil', 'scripts/location_audit.py', 'location_audit.py'), ('shutil', 'scripts/package_uae.py', 'package_uae.py'), ('shutil', 'scripts/pii_scan.py', 'pii_scan.py'), ('git', 'scripts/reorganize_kaggle.py', 'reorganize_kaggle.py'), ('git', 'scripts/run_explainability_audit.py', 'run_explainability_audit.py'), ('git', 'scripts/01_clean_all.py', 'pf_scraper/01_clean_all.py'), ('git', 'backend/scraper/http_client.py', 'pf_scraper/http_client.py'), ('git', 'backend/scraper/requirements.txt', 'pf_scraper/requirements.txt'), ('shutil', 'docs/notebooks/Egypt_EDA.ipynb', 'Egypt_EDA.ipynb'), ('shutil', 'docs/notebooks/UAE_EDA.ipynb', 'UAE_EDA.ipynb'), ('git', 'docs/resources/Premium_UI_UX_Design_System.pdf', 'Premium UI_UX Design System.pdf'), ('git', 'docs/VALORAI.md', 'VALORAI.md'), ('git', 'Archive/VALORAI.pdf', 'VALORAI.pdf'), ('git', 'docs/architecture.md', 'architecture.md'), ('git', 'Archive/architecture.pdf', 'architecture.pdf'), ('git', 'docs/ppt.md', 'ppt.md'), ('git', 'docs/dean.md', 'dean.md'), ('git', 'docs/frontend.md', 'frontend.md'), ('git', 'docs/hybrid_forensics.md', 'hybrid_forensics.md'), ('git', 'Archive/DISCOVERY_REPORT.md', 'DISCOVERY_REPORT.md'), ('git', 'Archive/project_deep_analysis', 'project_deep_analysis'), ('shutil', 'docs/kaggle_audit_reports', 'kaggle_audit_reports'), ('shutil', 'Archive/reports_legacy', 'reports'), ('shutil', 'data/kaggle/Egypt_Property_Finder_Kaggle', 'Egypt_Property_Finder_Kaggle'), ('shutil', 'data/kaggle/UAE_Property_Finder_Kaggle', 'UAE_Property_Finder_Kaggle'), ('git', 'data/scraper_raw', 'pf_scraper/data'), ('git', 'data/scraper_processed_eg', 'pf_scraper/data_eg'), ('git', 'data/kaggle_eg', 'pf_scraper/kaggle_eg'), ('git', 'data/kaggle_uae', 'pf_scraper/kaggle_uae'), ('git', 'Archive/scraper_provider_experimental', 'pf_scraper/provider'), ('git', 'Archive/audit_results.json', 'audit_results.json'), ('shutil', 'Archive/kaggle_audit_results_data.json', 'kaggle_audit_results_data.json'), ('git', 'Archive/data_zips/clean_csv.zip', 'pf_scraper/clean_csv.zip'), ('git', 'Archive/data_zips/csv_output.zip', 'pf_scraper/csv_output.zip'), ('git', 'Archive/data_zips/data_eg.zip', 'pf_scraper/data_eg.zip'), ('git', 'Archive/data_jsonl/rent_3pages.jsonl', 'pf_scraper/rent_3pages.jsonl')]

def rollback():
    print("=== Reverting Migration Executions ===")
    
    # Process actions in reverse order
    for method, current, original in reversed(ACTIONS):
        current_abs = os.path.join(ROOT_DIR, current)
        original_abs = os.path.join(ROOT_DIR, original)
        
        if not os.path.exists(current_abs):
            print(f"Skipping revert of: {current} (does not exist)")
            continue
            
        os.makedirs(os.path.dirname(original_abs), exist_ok=True)
        print(f"Reverting: {current} -> {original}")
        
        if method == "git":
            try:
                res = subprocess.run(
                    ["git", "mv", current, original],
                    cwd=ROOT_DIR,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                if res.returncode == 0:
                    print("  [GIT MV] Reverted successfully")
                    continue
            except Exception as e:
                pass
                
        try:
            shutil.move(current_abs, original_abs)
            print("  [STANDARD MOVE] Reverted successfully")
        except Exception as e:
            print(f"  [ROLLBACK ERROR] Failed to revert {current}: {e}")

    print("\n=== Restoring File Code Path Settings ===")
    # Restore query_villette.py and trace_resolution.py
    for fname in ["pf_scraper/fair-price-eg/backend/query_villette.py", "pf_scraper/fair-price-eg/backend/trace_resolution.py"]:
        path = os.path.join(ROOT_DIR, fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            old_str = 'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))'
            new_str = 'sys.path.insert(0, r"c:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\fair-price-eg\\backend")'
            content = content.replace(old_str, new_str)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(content)

    # Restore cmt_test/analyze_results.py & cmt_test/run_evaluation.py
    for fname in ["cmt_test/analyze_results.py", "cmt_test/run_evaluation.py"]:
        path = os.path.join(ROOT_DIR, fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            new_sys = 'sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))'
            old_sys = 'sys.path.insert(0, r"c:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\fair-price-eg\\backend")'
            new_env = 'load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", ".env")))'
            old_env = 'load_dotenv(r"c:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\fair-price-eg\\backend\\.env")'
            content = content.replace(new_sys, old_sys).replace(new_env, old_env)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(content)

    # Restore run_real_audit.py
    path = os.path.join(ROOT_DIR, "scripts/run_real_audit.py")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        new_sys = "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))"
        old_sys = "sys.path.append(os.path.abspath(r'c:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\fair-price-eg\\backend'))"
        content = content.replace(new_sys, old_sys)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)

    # Restore docker-compose.yml
    path = os.path.join(ROOT_DIR, "pf_scraper/fair-price-eg/docker-compose.yml")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("build: ../backend", "build: ./backend")
        content = content.replace("- ../data/db_clean:/data:ro", "- ./data:/data:ro")
        content = content.replace("context: ../frontend/web", "context: ./frontend")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
            
    print("Rollback complete.")

if __name__ == '__main__':
    rollback()
