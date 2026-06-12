# Project Audit - ValoryAI (ValorAI)

This audit report evaluates the current codebase structure, tech stack, code quality, duplication, security risks, and repository readiness for a professional open-source release on GitHub.

---

## 1. Current Architecture & Tech Stack

### Architecture Overview
ValoryAI is a governed agentic platform for real estate valuation. It separates concerns between:
1. **Presentation Layer**: A mobile Flutter application and a React web dashboard.
2. **Deterministic Truth Layer**: A FastAPI Python service providing geofenced radius sweeps (PostGIS), statisticalComparable Market Technique (CMT) pricing, and CatBoost ML inference.
3. **Agentic Control Plane**: An intent classifier, execution orchestrator, and narration contract grounding gate that enforces facts on LLM outputs to prevent hallucinations.

### Tech Stack
- **Frontend (Web)**: React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7, Zustand, Axios.
- **Frontend (Mobile)**: Flutter SDK (Dart), Go Router, Geolocator, Google Maps Flutter.
- **Backend (API & Engines)**: Python 3.10+, FastAPI, SQLAlchemy 2, Alembic, CatBoost, H3 Spatial Hex Index, Pandas, Numpy.
- **Database**: PostgreSQL 15, PostGIS (GiST spatial indices, JSONB GIN indices).

---

## 2. Audit Findings

### A. Dead / Obsolete Code Candidates
- `react valorai/`: A local, mocked React UI prototype. Not integrated with the backend. Excluded from runtime, purely a design/UX reference.
- `pf_scraper/fair-price-eg/frontend old/`: Legacy React dashboard code replaced by the modern frontend.
- `pf_scraper/provider/`: Contains 11 experimental/temporary scripts used for testing geocoding, pagination, and parsing.

### B. Duplicate Code & Files
- `project_deep_analysis/`: Contains markdown files `01_project_evolution.md` through `18_graduation_presentation_outline.md`. These are exact duplicates of files located in `docs/` with the same names (prefixed by numbers).
- `DISCOVERY_REPORT.md` (root): An exact duplicate of `docs/DISCOVERY_REPORT.md`.

### C. Temporary / Generated Files
- `audit_results.json` & `kaggle_audit_results_data.json`: Large JSON reports containing local file analysis data.
- `pf_scraper/pf_scraper/rent.jsonl.tmp`: Large temporary scrape cache.
- `pf_scraper/pf_scraper/data_v1.jsonl`: Large temporary JSONL data.
- ZIP files: `clean_csv.zip`, `csv_output.zip`, `data_eg.zip` in `pf_scraper/`. These are backup archives of dataset steps.

### D. Security Concerns
- **Hardcoded Local Paths**: Multiple scripts (e.g., `audit_uae.py`, `build_release.py`, `cmt_test/analyze_results.py`, `backend/query_villette.py`) hardcode absolute Windows user paths like `c:\Users\mh978\Downloads\mobile computing project...`. This leaks local system configurations and breaks code portability.
- **Secrets Exposure**: The file `pf_scraper/fair-price-eg/.env` exposes active Firebase Web API keys and project credentials. While `.env` is ignored by `.gitignore` in the root, it must be completely excluded from the Git repository, and only `.env.example` with placeholders should be published.

### E. Missing Documentation
- Setup instructions for the scraper.
- Setup and execution runbook for running tests in `cmt_test`.
- Central developer guide outlining the repository layout.

---

## 3. GitHub Readiness Scorecard

| Category | Current Score (1-10) | Target Score (1-10) | Key Actions Required |
|:---|:---:|:---:|:---|
| **Structure** | 4/10 | 10/10 | Reorganize project root, group components into `/frontend`, `/backend`, `/docs`, `/scripts`, `/tests`, `/infra`. |
| **Security** | 5/10 | 10/10 | Replace hardcoded absolute paths with relative paths. Prevent tracking of `.env` files. |
| **Documentation** | 6/10 | 10/10 | Add structured README, document architecture, folder map, and environment variables. |
| **Maintainability** | 5/10 | 9/10 | Separate data assets/zips from scraper source code. Clean up duplicate markdown files. |
| **CI/CD Readiness** | 3/10 | 8/10 | Group Docker configurations and add standard `.gitignore` rules. |

**Composite GitHub Readiness Score**: **4.6 / 10**
