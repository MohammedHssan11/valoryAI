import os
import shutil
import subprocess
import sys

# Define root of project (since script runs in /scripts, parent dir is root)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Directories to ensure exist before moving
DIRS_TO_CREATE = [
    "frontend",
    "backend",
    "docs",
    "docs/notebooks",
    "docs/resources",
    "docs/kaggle_audit_reports",
    "scripts",
    "tests",
    "infra",
    "data",
    "data/kaggle",
    "Archive",
    "Archive/data_zips",
    "Archive/data_jsonl",
    "Archive/pf_scraper",
    "Archive/audit_results"
]

# File movements (src relative to root, dest relative to root)
# Format: (src, dest)
MOVE_MAP = [
    # 1. Frontends
    ("flutter_valorai", "frontend/mobile"),
    ("pf_scraper/fair-price-eg/frontend", "frontend/web"),
    ("pf_scraper/fair-price-eg/frontend old", "Archive/frontend_old"),
    ("react valorai", "Archive/react_valorai_prototype"),
    
    # 2. Backends
    ("pf_scraper/fair-price-eg/backend", "backend"),
    ("pf_scraper/pf_scraper", "backend/scraper"),
    
    # 3. Infra
    ("pf_scraper/fair-price-eg/docker", "infra/docker"),
    ("pf_scraper/fair-price-eg/docker-compose.yml", "infra/docker-compose.yml"),
    
    # 4. Test Suite
    ("cmt_test", "tests"),
    
    # 5. Root utility scripts (moved to /scripts)
    ("audit_uae.py", "scripts/audit_uae.py"),
    ("build_kaggle_package.py", "scripts/build_kaggle_package.py"),
    ("build_release.py", "scripts/build_release.py"),
    ("extract_deep_evidence.py", "scripts/extract_deep_evidence.py"),
    ("generate_notebooks.py", "scripts/generate_notebooks.py"),
    ("generate_reports.py", "scripts/generate_reports.py"),
    ("investigate_buy.py", "scripts/investigate_buy.py"),
    ("kaggle_audit_script.py", "scripts/kaggle_audit_script.py"),
    ("location_audit.py", "scripts/location_audit.py"),
    ("package_uae.py", "scripts/package_uae.py"),
    ("parse_results.py", "scripts/parse_results.py"),
    ("pii_scan.py", "scripts/pii_scan.py"),
    ("reorganize_kaggle.py", "scripts/reorganize_kaggle.py"),
    ("run_explainability_audit.py", "scripts/run_explainability_audit.py"),
    ("pf_scraper/01_clean_all.py", "scripts/01_clean_all.py"),
    
    # 6. Scraper helper files
    ("pf_scraper/http_client.py", "backend/scraper/http_client.py"),
    ("pf_scraper/requirements.txt", "backend/scraper/requirements.txt"),
    
    # 7. Documentation
    ("Egypt_EDA.ipynb", "docs/notebooks/Egypt_EDA.ipynb"),
    ("UAE_EDA.ipynb", "docs/notebooks/UAE_EDA.ipynb"),
    ("Premium UI_UX Design System.pdf", "docs/resources/Premium_UI_UX_Design_System.pdf"),
    ("VALORAI.md", "docs/VALORAI.md"),
    ("VALORAI.pdf", "Archive/VALORAI.pdf"),
    ("architecture.md", "docs/architecture.md"),
    ("architecture.pdf", "Archive/architecture.pdf"),
    ("ppt.md", "docs/ppt.md"),
    ("dean.md", "docs/dean.md"),
    ("frontend.md", "docs/frontend.md"),
    ("hybrid_forensics.md", "docs/hybrid_forensics.md"),
    ("DISCOVERY_REPORT.md", "Archive/DISCOVERY_REPORT.md"),
    ("project_deep_analysis", "Archive/project_deep_analysis"),
    ("kaggle_audit_reports", "docs/kaggle_audit_reports"),
    ("reports", "Archive/reports_legacy"),
    
    # 8. Data
    ("Egypt_Property_Finder_Kaggle", "data/kaggle/Egypt_Property_Finder_Kaggle"),
    ("UAE_Property_Finder_Kaggle", "data/kaggle/UAE_Property_Finder_Kaggle"),
    ("pf_scraper/data", "data/scraper_raw"),
    ("pf_scraper/data_eg", "data/scraper_processed_eg"),
    ("pf_scraper/kaggle_eg", "data/kaggle_eg"),
    ("pf_scraper/kaggle_uae", "data/kaggle_uae"),
    ("pf_scraper/provider", "Archive/scraper_provider_experimental"),
    ("audit_results.json", "Archive/audit_results.json"),
    ("kaggle_audit_results_data.json", "Archive/kaggle_audit_results_data.json"),
    ("pf_scraper/clean_csv.zip", "Archive/data_zips/clean_csv.zip"),
    ("pf_scraper/csv_output.zip", "Archive/data_zips/csv_output.zip"),
    ("pf_scraper/data_eg.zip", "Archive/data_zips/data_eg.zip"),
    ("pf_scraper/rent_3pages.jsonl", "Archive/data_jsonl/rent_3pages.jsonl"),
    ("pf_scraper/pf_scraper/rent.jsonl.tmp", "Archive/pf_scraper/rent.jsonl.tmp"),
    ("pf_scraper/pf_scraper/data_v1.jsonl", "Archive/pf_scraper/data_v1.jsonl"),
]

def is_tracked(path):
    """Checks if a file/dir is tracked in git."""
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

def move_path(src_rel, dest_rel, actions_taken):
    src_abs = os.path.join(ROOT_DIR, src_rel)
    dest_abs = os.path.join(ROOT_DIR, dest_rel)
    
    if not os.path.exists(src_abs):
        print(f"Skipping: {src_rel} (does not exist)")
        return
        
    # Ensure target parent dir exists
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    
    print(f"Moving: {src_rel} -> {dest_rel}")
    
    # If the destination already exists (e.g. empty dir), remove it to avoid nested structures
    if os.path.exists(dest_abs):
        if os.path.isdir(dest_abs) and not os.listdir(dest_abs):
            os.rmdir(dest_abs)
        elif os.path.isfile(dest_abs):
            os.remove(dest_abs)
            
    tracked = is_tracked(src_rel)
    
    if tracked:
        # Move using git mv
        try:
            res = subprocess.run(
                ["git", "mv", src_rel, dest_rel],
                cwd=ROOT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if res.returncode == 0:
                actions_taken.append(("git", dest_rel, src_rel))
                print(f"  [GIT MV] Success")
                return
            else:
                print(f"  [GIT MV] Failed: {res.stderr.decode('utf-8').strip()}. Falling back to standard move.")
        except Exception as e:
            print(f"  [GIT MV] Error: {e}. Falling back to standard move.")
            
    # Standard fallback move
    try:
        shutil.move(src_abs, dest_abs)
        actions_taken.append(("shutil", dest_rel, src_rel))
        print(f"  [STANDARD MOVE] Success")
    except Exception as e:
        print(f"  [MOVE ERROR] Failed to move {src_rel}: {e}")

def update_file_contents():
    print("\n=== Updating File Content References ===")
    
    # 1. backend/query_villette.py & backend/trace_resolution.py
    for fname in ["backend/query_villette.py", "backend/trace_resolution.py"]:
        path = os.path.join(ROOT_DIR, fname)
        if os.path.exists(path):
            print(f"Updating: {fname}")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Replace absolute path insert with relative path
            old_str = 'sys.path.insert(0, r"c:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\fair-price-eg\\backend")'
            new_str = 'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))'
            content = content.replace(old_str, new_str)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(content)
                
    # 2. tests/analyze_results.py & tests/run_evaluation.py
    for fname in ["tests/analyze_results.py", "tests/run_evaluation.py"]:
        path = os.path.join(ROOT_DIR, fname)
        if os.path.exists(path):
            print(f"Updating: {fname}")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            old_sys = 'sys.path.insert(0, r"c:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\fair-price-eg\\backend")'
            new_sys = 'sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))'
            old_env = 'load_dotenv(r"c:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\fair-price-eg\\backend\\.env")'
            new_env = 'load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", ".env")))'
            content = content.replace(old_sys, new_sys).replace(old_env, new_env)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(content)
                
    # 3. scripts/run_real_audit.py
    path = os.path.join(ROOT_DIR, "scripts/run_real_audit.py")
    if os.path.exists(path):
        print(f"Updating: scripts/run_real_audit.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        old_sys = "sys.path.append(os.path.abspath(r'c:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\fair-price-eg\\backend'))"
        new_sys = "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))"
        content = content.replace(old_sys, new_sys)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
            
    # 4. Moved python scripts under scripts/
    scripts_dir = os.path.join(ROOT_DIR, "scripts")
    if os.path.exists(scripts_dir):
        for f in os.listdir(scripts_dir):
            if f.endswith(".py"):
                path = os.path.join(scripts_dir, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as file_obj:
                    content = file_obj.read()
                
                modified = False
                # Replace absolute ROOT_DIR or user folder paths
                if 'ROOT_DIR = r"c:\\Users\\mh978\\Downloads\\mobile computing project"' in content:
                    content = content.replace(
                        'ROOT_DIR = r"c:\\Users\\mh978\\Downloads\\mobile computing project"',
                        'ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))'
                    )
                    modified = True
                elif 'ROOT_DIR = r"c:\\Users\\mh978\\Downloads\\mobile computing project"' in content.replace(' ', ''):
                    # handle spacing differences
                    content = content.replace(
                        'ROOT_DIR = r"c:\\Users\\mh978\\Downloads\\mobile computing project"',
                        'ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))'
                    )
                    modified = True
                    
                if 'DATA_DIR = r"C:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\data"' in content:
                    content = content.replace(
                        'DATA_DIR = r"C:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\data"',
                        'DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "scraper_raw"))'
                    )
                    modified = True
                    
                if 'RELEASE_DIR = r"C:\\Users\\mh978\\Downloads\\mobile computing project\\kaggle_release"' in content:
                    content = content.replace(
                        'RELEASE_DIR = r"C:\\Users\\mh978\\Downloads\\mobile computing project\\kaggle_release"',
                        'RELEASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "kaggle_release"))'
                    )
                    modified = True
                    
                if modified:
                    print(f"Fixed paths in script: scripts/{f}")
                    with open(path, "w", encoding="utf-8", newline="") as file_obj:
                        file_obj.write(content)

def generate_rollback_script(actions_taken):
    print("\n=== Generating Rollback Script ===")
    rollback_path = os.path.join(ROOT_DIR, "scripts/rollback_migration.py")
    
    code = f"""import os
import shutil
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Format: (method, current_path, original_path)
ACTIONS = {repr(actions_taken)}

def rollback():
    print("=== Reverting Migration Executions ===")
    
    # Process actions in reverse order
    for method, current, original in reversed(ACTIONS):
        current_abs = os.path.join(ROOT_DIR, current)
        original_abs = os.path.join(ROOT_DIR, original)
        
        if not os.path.exists(current_abs):
            print(f"Skipping revert of: {{current}} (does not exist)")
            continue
            
        os.makedirs(os.path.dirname(original_abs), exist_ok=True)
        print(f"Reverting: {{current}} -> {{original}}")
        
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
            print(f"  [ROLLBACK ERROR] Failed to revert {{current}}: {{e}}")

    print("\\n=== Restoring File Code Path Settings ===")
    # Restore query_villette.py and trace_resolution.py
    for fname in ["pf_scraper/fair-price-eg/backend/query_villette.py", "pf_scraper/fair-price-eg/backend/trace_resolution.py"]:
        path = os.path.join(ROOT_DIR, fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            old_str = 'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))'
            new_str = 'sys.path.insert(0, r"c:\\\\Users\\\\mh978\\\\Downloads\\\\mobile computing project\\\\pf_scraper\\\\fair-price-eg\\\\backend")'
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
            old_sys = 'sys.path.insert(0, r"c:\\\\Users\\\\mh978\\\\Downloads\\\\mobile computing project\\\\pf_scraper\\\\fair-price-eg\\\\backend")'
            new_env = 'load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", ".env")))'
            old_env = 'load_dotenv(r"c:\\\\Users\\\\mh978\\\\Downloads\\\\mobile computing project\\\\pf_scraper\\\\fair-price-eg\\\\backend\\\\.env")'
            content = content.replace(new_sys, old_sys).replace(new_env, old_env)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(content)

    # Restore run_real_audit.py
    path = os.path.join(ROOT_DIR, "scripts/run_real_audit.py")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        new_sys = "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))"
        old_sys = "sys.path.append(os.path.abspath(r'c:\\\\Users\\\\mh978\\\\Downloads\\\\mobile computing project\\\\pf_scraper\\\\fair-price-eg\\\\backend'))"
        content = content.replace(new_sys, old_sys)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
            
    print("Rollback complete.")

if __name__ == '__main__':
    rollback()
"""
    with open(rollback_path, "w", encoding="utf-8", newline="") as f:
        f.write(code)
    print("Rollback script written to: scripts/rollback_migration.py")

def main():
    print("=== STARTING VALORYAI CODEBASE MIGRATION ===")
    
    # Create target directories
    for d in DIRS_TO_CREATE:
        path = os.path.join(ROOT_DIR, d)
        os.makedirs(path, exist_ok=True)
        
    actions_taken = []
    
    # Execute relocations
    for src, dest in MOVE_MAP:
        move_path(src, dest, actions_taken)
        
    # Update files paths
    update_file_contents()
    
    # Generate safety rollback script
    generate_rollback_script(actions_taken)
    
    # Clean up empty source subdirs under pf_scraper if empty
    pf_scraper_dir = os.path.join(ROOT_DIR, "pf_scraper")
    if os.path.exists(pf_scraper_dir):
        # Clean up fair-price-eg inside pf_scraper
        fpe_dir = os.path.join(pf_scraper_dir, "fair-price-eg")
        if os.path.exists(fpe_dir) and not os.listdir(fpe_dir):
            os.rmdir(fpe_dir)
            print("Cleaned up empty directory: pf_scraper/fair-price-eg")
            
        # Clean up pf_scraper if empty
        if not os.listdir(pf_scraper_dir):
            os.rmdir(pf_scraper_dir)
            print("Cleaned up empty directory: pf_scraper")
            
    print("\n=== MIGRATION COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
