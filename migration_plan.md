# Migration Plan - Repository Cleanup and Standardization

This migration plan outlines the steps required to reorganize the **ValoryAI (ValorAI)** project into a professional, production-ready structure for public GitHub release. It adheres strictly to the rule of **never deleting code or permanently removing files**. All unused, duplicated, or experimental files will be relocated to a structured `/Archive` directory.

---

## Proposed Directory Relocations

### 1. Frontend Relocations
| BEFORE Path | AFTER Path | Reason | Risk |
|:---|:---|:---|:---|
| `flutter_valorai/` | `frontend/mobile/` | Group mobile application code under a unified frontend folder. | **Low** |
| `pf_scraper/fair-price-eg/frontend/` | `frontend/web/` | Group React web application code under a unified frontend folder. | **Low** |
| `pf_scraper/fair-price-eg/frontend old/` | `Archive/frontend_old/` | Move legacy, unused React frontend out of the active codebase. | **Low** |
| `react valorai/` | `Archive/react_valorai_prototype/` | Move the mock/experimental Google AI Studio React prototype out of the active workspace. | **Low** |

### 2. Backend Relocations
| BEFORE Path | AFTER Path | Reason | Risk |
|:---|:---|:---|:---|
| `pf_scraper/fair-price-eg/backend/` | `backend/` | Promote backend application (FastAPI) to a top-level directory. | **Medium** (requires fixing internal trace scripts path references) |
| `pf_scraper/pf_scraper/` | `backend/scraper/` | Relocate the scraper package to the backend directory. | **Low** |

### 3. Infrastructure and Docker Relocations
| BEFORE Path | AFTER Path | Reason | Risk |
|:---|:---|:---|:---|
| `pf_scraper/fair-price-eg/docker/` | `infra/docker/` | Group Docker configs and scripts under a unified infra directory. | **Low** |
| `pf_scraper/fair-price-eg/docker-compose.yml` | `infra/docker-compose.yml` | Keep docker-compose file in infra directory. | **Low** |

### 4. Test Suite Relocations
| BEFORE Path | AFTER Path | Reason | Risk |
|:---|:---|:---|:---|
| `cmt_test/` | `tests/` | Promote CMT test suite to the standard top-level `/tests` directory. | **Medium** (requires fixing relative path imports to the backend) |

### 5. Script Relocations (Root and Scraper)
| BEFORE Path | AFTER Path | Reason | Risk |
|:---|:---|:---|:---|
| `audit_uae.py` | `scripts/audit_uae.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `build_kaggle_package.py` | `scripts/build_kaggle_package.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `build_release.py` | `scripts/build_release.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `extract_deep_evidence.py` | `scripts/extract_deep_evidence.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `generate_notebooks.py` | `scripts/generate_notebooks.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `generate_reports.py` | `scripts/generate_reports.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `investigate_buy.py` | `scripts/investigate_buy.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `kaggle_audit_script.py` | `scripts/kaggle_audit_script.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `location_audit.py` | `scripts/location_audit.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `package_uae.py` | `scripts/package_uae.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `parse_results.py` | `scripts/parse_results.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `pii_scan.py` | `scripts/pii_scan.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `reorganize_kaggle.py` | `scripts/reorganize_kaggle.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `run_explainability_audit.py` | `scripts/run_explainability_audit.py` | Move root utility scripts to a structured `/scripts` directory. | **Medium** (requires replacing hardcoded absolute paths with relative paths) |
| `pf_scraper/01_clean_all.py` | `scripts/01_clean_all.py` | Move scraper cleanup script to the central `/scripts` directory. | **Low** |

### 6. Scraper Assets & Helpers
| BEFORE Path | AFTER Path | Reason | Risk |
|:---|:---|:---|:---|
| `pf_scraper/http_client.py` | `backend/scraper/http_client.py` | Group scraper helper code under the backend scraper package. | **Low** |
| `pf_scraper/requirements.txt` | `backend/scraper/requirements.txt` | Relocate scraper dependency requirements. | **Low** |

### 7. Documentation and Presentation Relocations
| BEFORE Path | AFTER Path | Reason | Risk |
|:---|:---|:---|:---|
| `Egypt_EDA.ipynb` | `docs/notebooks/Egypt_EDA.ipynb` | Reorganize notebooks under documentation folder. | **Low** |
| `UAE_EDA.ipynb` | `docs/notebooks/UAE_EDA.ipynb` | Reorganize notebooks under documentation folder. | **Low** |
| `Premium UI_UX Design System.pdf` | `docs/resources/Premium_UI_UX_Design_System.pdf` | Relocate visual assets to documentation resources. | **Low** |
| `VALORAI.md` | `docs/VALORAI.md` | Move documentation files into `/docs`. | **Low** |
| `VALORAI.pdf` | `Archive/VALORAI.pdf` | Archive pre-compiled PDF; markdown source remains in docs. | **Low** |
| `architecture.md` | `docs/architecture.md` | Move documentation files into `/docs`. | **Low** |
| `architecture.pdf` | `Archive/architecture.pdf` | Archive pre-compiled PDF; markdown source remains in docs. | **Low** |
| `ppt.md` | `docs/ppt.md` | Relocate slides document to `/docs`. | **Low** |
| `dean.md` | `docs/dean.md` | Relocate legacy report to `/docs`. | **Low** |
| `frontend.md` | `docs/frontend.md` | Relocate frontend specification document to `/docs`. | **Low** |
| `hybrid_forensics.md` | `docs/hybrid_forensics.md` | Relocate analysis document to `/docs`. | **Low** |
| `DISCOVERY_REPORT.md` | `Archive/DISCOVERY_REPORT.md` | Archive root duplicate of `docs/DISCOVERY_REPORT.md`. | **Low** |
| `project_deep_analysis/` | `Archive/project_deep_analysis/` | Archive folder (18 markdown files) containing exact duplicates of `/docs/01_*` to `/docs/18_*`. | **Low** |
| `kaggle_audit_reports/` | `docs/kaggle_audit_reports/` | Group Kaggle publication audits inside `/docs`. | **Low** |
| `reports/` | `Archive/reports_legacy/` | Move empty/placeholder reports directory to Archive. | **Low** |

### 8. Dataset and ZIP Relocations
| BEFORE Path | AFTER Path | Reason | Risk |
|:---|:---|:---|:---|
| `Egypt_Property_Finder_Kaggle/` | `data/kaggle/Egypt_Property_Finder_Kaggle/` | Relocate Kaggle dataset package. | **Low** |
| `UAE_Property_Finder_Kaggle/` | `data/kaggle/UAE_Property_Finder_Kaggle/` | Relocate Kaggle dataset package. | **Low** |
| `pf_scraper/data/` | `data/scraper_raw/` | Move scraper data folder to unified `/data` directory. | **Low** |
| `pf_scraper/data_eg/` | `data/scraper_processed_eg/` | Move scraper processed data folder to unified `/data` directory. | **Low** |
| `pf_scraper/kaggle_eg/` | `data/kaggle_eg/` | Relocate Kaggle formatted CSV data files. | **Low** |
| `pf_scraper/kaggle_uae/` | `data/kaggle_uae/` | Relocate Kaggle formatted CSV data files. | **Low** |
| `pf_scraper/provider/` | `Archive/scraper_provider_experimental/` | Move experimental scraping scripts to Archive. | **Low** |
| `audit_results.json` | `Archive/audit_results.json` | Move large generated JSON data file to Archive. | **Low** |
| `kaggle_audit_results_data.json` | `Archive/kaggle_audit_results_data.json` | Move large generated JSON data file to Archive. | **Low** |
| `pf_scraper/clean_csv.zip` | `Archive/data_zips/clean_csv.zip` | Archive backup data zip. | **Low** |
| `pf_scraper/csv_output.zip` | `Archive/data_zips/csv_output.zip` | Archive backup data zip. | **Low** |
| `pf_scraper/data_eg.zip` | `Archive/data_zips/data_eg.zip` | Archive backup data zip. | **Low** |
| `pf_scraper/rent_3pages.jsonl` | `Archive/data_jsonl/rent_3pages.jsonl` | Archive temporary sample data. | **Low** |
| `pf_scraper/pf_scraper/rent.jsonl.tmp` | `Archive/pf_scraper/rent.jsonl.tmp` | Archive temporary sample data. | **Low** |
| `pf_scraper/pf_scraper/data_v1.jsonl` | `Archive/pf_scraper/data_v1.jsonl` | Archive temporary data. | **Low** |

---

## File Modifications (Path Updates)

To keep all applications, scripts, and test files running correctly, the following code updates will be performed:

### 1. `backend/query_villette.py`
- **Change**: Replace `sys.path.insert(0, r"c:\Users\mh978\Downloads\mobile computing project\pf_scraper\fair-price-eg\backend")` with `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`.

### 2. `backend/trace_resolution.py`
- **Change**: Replace `sys.path.insert(0, r"c:\Users\mh978\Downloads\mobile computing project\pf_scraper\fair-price-eg\backend")` with `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`.

### 3. `tests/analyze_results.py` and `tests/run_evaluation.py`
- **Change**: Update `load_dotenv` and `sys.path.insert` to target backend relatively:
  ```python
  import os
  import sys
  from dotenv import load_dotenv
  
  backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
  load_dotenv(os.path.join(backend_path, ".env"))
  sys.path.insert(0, backend_path)
  ```

### 4. Relocated Scripts under `scripts/`
- **Change**: Update references to `ROOT_DIR` or hardcoded paths to point dynamically to the parent directory:
  ```python
  ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
  ```

---

## Execution Safety and Reversibility

1. **Atomic File Movements**: All file moves will be executed using git commands (where possible) to maintain commit history.
2. **Reversibility**: A rollback script (`scripts/rollback_migration.py`) will be generated to restore all files to their original directories and revert modified file lines in case of any issues.
3. **Behavioral Integrity**: All backend tests will be run before and after the migration to ensure no functionality is broken.
