# Archive Register - ValoryAI (ValorAI)

This directory houses code, assets, and documentation that are no longer active, have been duplicated, or represent experimental/prototype states. These files are preserved to maintain complete historical records and respect the repository's data integrity rules.

---

## 1. Prototype Web Application

- **Original Path**: `/react valorai/`
- **Archived Path**: `/Archive/react_valorai_prototype/`
- **Archive Date**: 2026-06-13
- **Reason**: An experimental, hardcoded React dashboard prototype designed to demonstrate Gemini API integration. It contains no backend connections and uses mock data. Replaced by the production React web dashboard in `/frontend/web`.
- **Dependency Impact**: None.
- **Recovery Instructions**: Can be restored back to `/react valorai/` and run using `npm install` and `npm run dev`.

---

## 2. Duplicate Project Reports

- **Original Path**: `/project_deep_analysis/`
- **Archived Path**: `/Archive/project_deep_analysis/`
- **Archive Date**: 2026-06-13
- **Reason**: Exact duplicates of reports `01_project_evolution.md` through `18_graduation_presentation_outline.md` already present in the `/docs` directory.
- **Dependency Impact**: None.
- **Recovery Instructions**: Can be copied back to `/project_deep_analysis/` if needed.

---

## 3. Legacy Web Dashboard

- **Original Path**: `/pf_scraper/fair-price-eg/frontend old/`
- **Archived Path**: `/Archive/frontend_old/`
- **Archive Date**: 2026-06-13
- **Reason**: Older iteration of the React web frontend dashboard. Replaced by `/frontend/web`.
- **Dependency Impact**: None.
- **Recovery Instructions**: Move back to `/frontend/web-legacy` and execute `npm install`.

---

## 4. Scraper Experimental Provider Scripts

- **Original Path**: `/pf_scraper/provider/`
- **Archived Path**: `/Archive/scraper_provider_experimental/`
- **Archive Date**: 2026-06-13
- **Reason**: Experimental development scripts used to test geocoders, regex parsing, and pagination patterns. Unused in the active production crawling pipelines.
- **Dependency Impact**: None.
- **Recovery Instructions**: Move back to `/backend/scraper/provider/` to execute.

---

## 5. Duplicate Discovery Report

- **Original Path**: `/DISCOVERY_REPORT.md` (root)
- **Archived Path**: `/Archive/DISCOVERY_REPORT.md`
- **Archive Date**: 2026-06-13
- **Reason**: Duplicate of `docs/DISCOVERY_REPORT.md`.
- **Dependency Impact**: None.
- **Recovery Instructions**: Move back to root directory.

---

## 6. Pre-Compiled PDF Documents

- **Original Path**: `/VALORAI.pdf` and `/architecture.pdf` (root)
- **Archived Path**: `/Archive/VALORAI.pdf` and `/Archive/architecture.pdf`
- **Archive Date**: 2026-06-13
- **Reason**: Generated binary targets. The markdown sources (`VALORAI.md` and `architecture.md`) are the authoritative documentation files maintained inside `/docs`.
- **Dependency Impact**: None.
- **Recovery Instructions**: Restore to root folder.

---

## 7. Large Data and Cache Files

- **Original Path**: `/audit_results.json` and `/kaggle_audit_results_data.json` (root)
- **Archived Path**: `/Archive/audit_results/` (contains files)
- **Archive Date**: 2026-06-13
- **Reason**: Large generated audit output files. Excluded from active source workspace.
- **Dependency Impact**: None.
- **Recovery Instructions**: Move files back to root directory.

---

## 8. Temporary Scraper Outputs and Zips

- **Original Path**:
  - `/pf_scraper/clean_csv.zip`
  - `/pf_scraper/csv_output.zip`
  - `/pf_scraper/data_eg.zip`
  - `/pf_scraper/rent_3pages.jsonl`
  - `/pf_scraper/pf_scraper/rent.jsonl.tmp`
  - `/pf_scraper/pf_scraper/data_v1.jsonl`
- **Archived Path**:
  - `/Archive/data_zips/clean_csv.zip`
  - `/Archive/data_zips/csv_output.zip`
  - `/Archive/data_zips/data_eg.zip`
  - `/Archive/data_jsonl/rent_3pages.jsonl`
  - `/Archive/pf_scraper/rent.jsonl.tmp`
  - `/Archive/pf_scraper/data_v1.jsonl`
- **Archive Date**: 2026-06-13
- **Reason**: Backup archives and large temporary scraping outputs. Removed to keep core repository small and clean.
- **Dependency Impact**: None.
- **Recovery Instructions**: Move files back to their respective scraper directories.

---

## 9. Empty Reports Directory

- **Original Path**: `/reports/` (root)
- **Archived Path**: `/Archive/reports_legacy/`
- **Archive Date**: 2026-06-13
- **Reason**: Empty placeholder directory in project root.
- **Dependency Impact**: None.
- **Recovery Instructions**: Recreate `/reports/` directory if needed.
