# Repository Structure - ValoryAI (ValorAI)

This document explains the organization and folder structure of the sanitized ValoryAI codebase. The structure separates responsibilities cleanly, preparing the project for team development and professional GitHub publication.

---

## Folder Map

```
/
├── .gitignore                   # Hardened git ignore definitions
├── README.md                    # Primary repository overview and developer guide
├── github_readiness_report.md   # Final post-migration readiness scorecard
├── migration_plan.md            # Plan detailing before/after migration paths
├── project_audit.md             # Initial project discovery and audit report
│
├── /Archive                     # Legacy, experimental, mock, or duplicate assets (isolated)
│   ├── archive_reason.md        # Document detailing why each asset was archived
│   ├── /frontend_old            # Legacy unused React frontend dashboard
│   ├── /project_deep_analysis   # Duplicate copy of docs/01_* to docs/18_* files
│   ├── /react_valorai_prototype  # Mock Google AI Studio React UX concept app
│   ├── /reports_legacy          # Placeholders of empty reports
│   └── /scraper_provider_experimental  # Experimental parser and pagination scripts
│
├── /backend                     # Main valuation backends and scraper service
│   ├── /app                     # FastAPI app package (routers, models, logic, database)
│   ├── /alembic                 # Alembic database migration scripts
│   ├── /scraper                 # Active listing crawler package and CLI
│   └── query_villette.py        # Entity resolution query utility
│
├── /data                        # Managed dataset packages and ML inputs
│   ├── /kaggle                  # Packaged datasets formatted for Kaggle publication
│   ├── /scraper_raw             # Raw jsonl scraper output dumps
│   └── /scraper_processed_eg    # Parsed and consolidated Egypt listing data
│
├── /docs                        # Platform-wide documentation files
│   ├── /kaggle_audit_reports    # Reports auditing data quality for Kaggle
│   ├── /notebooks               # Jupyter Notebooks containing EDA (Egypt & UAE)
│   └── /resources               # Design system PDF and static assets
│
├── /frontend                    # Main client applications (Web and Mobile)
│   ├── /mobile                  # Production Flutter mobile application code
│   └── /web                     # Production React TypeScript dashboard application
│
├── /infra                       # Infrastructure and deployment orchestrations
│   └── /docker                  # Dockerfiles and docker-compose configurations
│
├── /scripts                     # Administrative, build, release, and audit automation scripts
│   └── run_real_audit.py        # Database/Model consistency checks
│
└── /tests                       # Verification suites
    ├── run_evaluation.py        # Runs CMT valuation precision metrics
    └── analyze_results.py       # Summarizes results of evaluations
```

---

## Directory Descriptions

### `/backend`
Houses the core python logic. Contains the FastAPI app which implements the deterministic Valuation Layer (CMT & CatBoost ML), Explainability Layer, and the Agentic Orchestration Control Plane. It also contains the listing crawler `/scraper` to query real estate portals.

### `/frontend`
Holds the user interface channels:
- `/mobile`: The Flutter application compiling to iOS and Android, handling map-centric searches and conversational assistant interaction.
- `/web`: The Vite-based React application serving as the manager control panel dashboard.

### `/data`
A centralized location for static data. Separates raw crawling JSONL files, cleaned Parquet/CSV files, and ready-to-publish Kaggle archives. Keeps large binaries out of source paths.

### `/docs`
Contains general markdown guides, diagrams, and historical reports detailing the project evolution. Subfolders include `/notebooks` for exploratory data analysis (EDA) and `/resources` for visual assets.

### `/infra`
Stores DevOps-related orchestrations, specifically Docker containers for the API servers, DB instances, and reverse proxy settings.

### `/scripts`
Holds administrative utility scripts for cleaning datasets, auditing geolocations, running explainability reports, and packaging distribution builds.

### `/tests`
Houses scripts designed to evaluate CMT performance, calculate median error variances, and output quality matrices.
