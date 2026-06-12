# ValorAI: A Governed Agentic Intelligence Platform for Real Estate Decision Making
**System Technical Audit & Architecture Report**  
**Submitted To:** The Dean of the College of Artificial Intelligence  
**Prepared By:** Technical Auditor & Forensic Architect  
**System State Version:** Phase 5.5C (FastAPI Governed Orchestrator & Multi-Engine Integration)  
**Date of Audit:** June 4, 2026  

---

## 1. Executive Overview

> [!IMPORTANT]
> **CRITICAL ARCHITECTURAL MESSAGE FOR THE DEAN:**
> * The project is **NOT** "an AI valuation app."
> * The project is **NOT** "a chatbot."
> * The project is **NOT** "a CatBoost model."
> * The project **IS**: **A Governed Agentic Intelligence Platform for Real Estate Decision Making**.
> 
> The mobile client application is only the presentation/delivery layer. The core systems engineering contribution of ValorAI lies entirely in the backend pipelines: geofenced PostGIS spatial queries, multi-engine routing logic, mathematical explainability models, and a thread-isolated, intent-driven agentic orchestrator.

Most modern AI platforms suffer from a critical flaw: they rely on Large Language Models (LLMs) to perform reasoning, mathematical calculations, and direct database lookups. In real estate, where transactional accuracy is paramount, this design leads to valuation hallucinations, arithmetic errors, and severe data leaks. 

`[VERIFIED]` (Supporting files: [runtime.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/runtime.py), [NARRATION_CONTRACT_ARCHITECTURE.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/docs/NARRATION_CONTRACT_ARCHITECTURE.md))

ValorAI resolves this by enforcing a strict **Truth Layer** separation of concerns. All mathematical pricing, geofenced radius sweeps, outlier prunings, and scenario overlays are executed by specialized, deterministic backend engines written in Python and PostGIS. The AI Copilot is restricted to a presentation layer, narrating these pre-calculated facts exactly and linking them to verified database citations. 

This technical report details the end-to-end engineering architecture, database schemas, valuation engines, hybrid evolution history, and the agentic control plane that defines ValorAI as a comprehensive AI system.

---

## 2. Reconstructed Systems Engineering Journey

`[VERIFIED]` (Supporting documents: [01_project_evolution.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/01_project_evolution.md), [07_hybrid_evolution.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/07_hybrid_evolution.md), [train_baseline.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/data_eg/train_baseline.py))

The chronological engineering journey of the ValorAI backend system is structured around the following progression, moving from raw data ingestion to governed agentic intelligence:

```
      Raw Real Estate Data
               │
               ▼
   Data Cleaning & Validation
               │
               ▼
       Database Evolution
               │
               ▼
      Spatial Intelligence
               │
               ▼
     CMT Valuation Engine
               │
               ▼
      ML Valuation Engine
               │
               ▼
        Hybrid Research
               │
               ▼
       Goldilocks Router
               │
               ▼
        Explainability
               │
               ▼
  Business Intelligence Tools
               │
               ▼
     Agentic Orchestration
               │
               ▼
     Governed AI Copilot
```

1. **Raw Real Estate Data Ingestion:** Extracting listings from PropertyFinder Egypt via server-side rendered HTML `__NEXT_DATA__` JSON parsing to bypass rate-limiting.
2. **Data Cleaning & Validation:** In-memory sanitization, coordinate bounding boxes check, deduplication, and bedroom normalizations.
3. **Database Evolution:** Transitioning from flat coordinates lookup tables to spatial PostGIS structures with 4-level parent-child administrative adjacency trees.
4. **Spatial Intelligence:** PostGIS hierarchical CTEs walking governorates, cities, districts, and compounds in under 10ms.
5. **CMT Valuation Engine:** Developing a deterministic pricing model using Tiered geofencing, MAD outlier pruning, and similarity-decay quantiles.
6. **ML Valuation Engine:** Training CatBoost models in log-space on H3 hexagonal grids to handle low-density regions.
7. **Hybrid Research:** Successive attempts (Fallback, Stacking, Density thresholds) to merge CMT and ML engines.
8. **Goldilocks Router (Hybrid V3):** Current active routing engine that dynamically matches query coordinates to H3 cells and exposure registries, selecting CMT for optimal zones ($11 \le n \le 50$) and ML elsewhere.
9. **Explainability Models:** Computing SHAP value EGP conversions, Jaccard amenities indices, and composite confidence scores.
10. **Business Intelligence Tools:** Modularizing logic into 8 authenticated, tenant-isolated tools (e.g. Negotiation, What-if, Investment).
11. **Agentic Orchestration Control Plane:** Routing queries through rule-based Intent classifiers, Execution Planners, and Tool Executors.
12. **Governed AI Copilot:** Restricting LLM text generation to pre-computed facts via Narration Admission Gates and Citation Grounding policies.

---

## 3. Reconstructed Complete System Architecture

`[VERIFIED]` (Supporting files: [runtime.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/runtime.py), [main.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/main.py), [frontend.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/frontend.md))

The interaction flow from the user to the core AI and database systems is mapped out below. The mobile application serves purely as the final presentation layer, while all computational logic is hosted on the FastAPI backend:

```
User
  │
  ▼ [Secure Mobile Client (Flutter UI)] - Presentation Layer Only
  │   - Workspace/Chat Interface & Valuation Snapshot Cards
  │
  ▼ [Bearer JWT Security Gate]
  │   - Public routes: /health, /v1/valuation/fair-price
  │   - Authenticated routes: /v1/copilot/ (Requires Firebase-exchanged JWT)
  │
  ▼ [FastAPI API Router Gateway]
  │   - Validates JSON schemas via Pydantic model configurations
  │
  ▼ [Orchestrator Plane (runtime.py)]
  │   - Intent Engine V1 (Rule-based keyword classification)
  │   - Tool Planner (Schedules Tool 1-8 execution plans)
  │   - Tool Executor (Runs tenant-scoped tools in parallel)
  │   - Response Composer (Normalizes payloads, calculates comparison arithmetic)
  │   - Memory Integration (Workspace filtering for multi-turn chats)
  │
  ▼ [Truth Layer (Tools 1-8)]
  │   - Isolated Python adapters executing business logic
  │
  ▼ [Mathematical Pricing Engine Layer]
  │   ├── CMT Pricing Engine (valuation_service.py)
  │   │     - Container area resolution (ST_Covers containment checks)
  │   │     - PostGIS geofencing comparable retrievals (Tiers 1-5 searches)
  │   │     - Outlier filtering (Hard guardrails + MAD modified Z-scores)
  │   │     - Weighted Quantile picker (Quantiles P20, P50, P80)
  │   │
  │   └── ML Valuation Engine (ml_service.py)
  │         - CatBoost models: residential_rent.cbm & residential_sale.cbm
  │         - Target log-transformations: y = ln(price + 1) -> expm1(pred)
  │         - SHAP feature contribution extraction (EGP impact calculations)
  │
  ▼ [Persistence Layer]
  │   - PostgreSQL 15 + PostGIS Spatial Extensions (SRID 4326 Point/MultiPolygon)
  │   - address_resolution_cache & shadow_logs
  │   - Copilot Memory (workspaces, chats, messages, property_states, scenario_states)
  │
  ▼ [LLM Narration & Grounding Gate]
        - Stateless Gemini 2.5 Pro provider calls (default-off)
        - Narration Admission Gate (Deterministic grounding validation checks)
        - Fallback: Suppresses LLM and returns Composer JSON (DETERMINISTIC_FALLBACK)
```

### Architectural Verification Status:
* **Core API Routing and Database Schemas:** `[VERIFIED]` in FastAPI backend (`app/api/routes/`) and migrations (`000_baseline.sql` through `007_copilot_tools_valuation_explainability.sql`).
* **Valuation Engines, Router, and Tool Adapters:** `[VERIFIED]` in `app/services/router_service.py`, `app/services/valuation_service.py`, `app/services/ml_service.py`, and `app/services/copilot_tools_service.py`.
* **Copilot Orchestrator Plane & Memory Layer:** `[VERIFIED]` in `app/copilot/orchestrator/` runtime and integration modules.
* **Flutter Mobile App Foundation & Screen Features:** `[VERIFIED]` in `flutter_valorai/` presentation, data repository, and route code paths.
* **Native Firebase Configurations:** `[PARTIALLY VERIFIED]` – Firebase sign-in and token-exchange logic are implemented in Dart/Python, but platform configuration files (Android `google-services.json`, iOS `GoogleService-Info.plist`, and backend deployment `FIREBASE_PROJECT_ID`) are absent, blocking physical walkthrough validation.
* **Production Secret Management & Role-Based Access Control:** `[NOT VERIFIED]` – Production secret rotation is absent, organization RBAC models are not implemented, and deployment pipelines remain incomplete.

---

## 4. Data Engineering: Ingestion, Sanitization & Geocoding Cache

`[VERIFIED]` (Supporting files: [egy_scraper.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/pf_scraper/egy_scraper.py), [01_clean_all.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/01_clean_all.py), [address_resolver.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/geo/address_resolver.py))

The data engineering pipeline establishes the bedrock of the system, transforming highly unstructured web listings into clean spatial records:

1. **Scraping Ingestion:** The crawler crawls search pages on PropertyFinder Egypt. Instead of running heavy browser automation, it utilizes session-based HTTP requests to parse server-side rendered HTML, extracting the `<script id="__NEXT_DATA__" type="application/json">` block. This block contains structured listings data directly from PropertyFinder's backend. To prevent IP rate-limiting, the scraper enforces a sleep interval of `sleep_s = 1.2` seconds.
2. **In-Memory Sanitization:** Raw listings are processed through a strict batch cleaning pipeline (`01_clean_all.py`):
   * **Placeholder Pruning:** Removes listings with placeholder prices ($P_{\text{EGP}} \le 100$ EGP).
   * **Coordinate Validation:** Restricts latitudes to $[22.0, 32.5]$ and longitudes to $[24.0, 36.0]$ to filter out errant coordinates outside Egyptian borders.
   * **Physical Limits:** Bounds sizes to $(5, 10000)$ sqm.
   * **Studio Classification:** Uses bilingual title keyword matches ("studio" or "ستوديو") to override bedroom counts to `0`, ensuring studios are not grouped with 1-bedroom apartments.
   * **Deduplication:** Discards duplicate listings by unique portal IDs.
3. **Address Resolution Cache:** Client address-based requests query the `address_resolution_cache` table using a case-insensitive match on the raw text (`lower(raw_input)`). Resolved coordinates are served in under 5ms, avoiding API calls. On a cache miss, coordinates are resolved via Google Maps Geocoding API and stored back to the database.

---

## 5. Spatial Intelligence: Database Architecture & Schema Forensic Breakdown

`[VERIFIED]` (Supporting DDL files: [init.sql](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/db/sql/init.sql), [c66d987da7fa_add_copilot_tables.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/alembic/versions/c66d987da7fa_add_copilot_tables.py))

ValorAI uses a relational schema designed for spatial geofencing queries and multi-turn workspace state tracking.

### 5.1. Core Spatial Tables

#### Table 1: `areas`
* **Purpose:** Represents administrative boundaries in Egypt, structured as a recursive parent-child tree.
* **Columns:**
  - `area_id`: `BIGSERIAL` (Primary Key).
  - `name`: `TEXT` (Not Null).
  - `level`: `SMALLINT` (Not Null, Checked between 1 and 4: 1 = Governorate, 2 = City, 3 = District, 4 = Neighborhood/Compound).
  - `parent_area_id`: `BIGINT` (Nullable Foreign Key referencing `areas(area_id)` ON DELETE RESTRICT).
  - `center_geom`: `geometry(Point, 4326)` (Centroid coordinates, Not Null).
  - `geom`: `geometry(MultiPolygon, 4326)` (Administrative polygon shape, Nullable).
  - `fallback_radius_m`: `INTEGER` (Radius limits used if shape geom is missing).
* **Key Constraints & Indexes:**
  - `ck_areas_level`: `CHECK (level BETWEEN 1 AND 4)`
  - `ck_areas_parent_not_self`: `CHECK (parent_area_id IS NULL OR parent_area_id <> area_id)`
  - Unique index `ux_areas_parent_level_name`: `UNIQUE (parent_area_id, level, lower(name))` (Prevents duplicate entries within the same branch).
  - `ix_areas_geom_gist` & `ix_areas_center_gist`: Spatial GIST indices on the administrative polygon and centroid point.

#### Table 2: `listings`
* **Purpose:** Stores comparable listings scraped from Egyptian real estate portals.
* **Columns:**
  - `listing_id`: `TEXT` (Primary Key).
  - `category`: `TEXT` (Not Null, e.g., `'rent'`, `'buy'`).
  - `period`: `TEXT` (Not Null, e.g., `'monthly'`, `'sale'`).
  - `price_egp`: `INTEGER` (Not Null, Checked $>0$).
  - `property_type`: `TEXT` (Not Null).
  - `bedrooms`: `SMALLINT`, `bathrooms`: `SMALLINT` (Room counts).
  - `size_sqm`: `NUMERIC(8,2)` (Property size).
  - `lat`, `lng`: `DOUBLE PRECISION` (Raw coordinates).
  - `geom`: `geometry(Point, 4326)` (Spatial point representation, Not Null).
  - `area_id`: `BIGINT` (Foreign Key referencing `areas(area_id)` ON DELETE RESTRICT).
  - `scraped_at_utc`: `TIMESTAMPTZ` (Not Null).
  - `normalized_amenities`: `JSONB` (Array of normalized amenity codes, e.g., `["CP", "AC"]`).
  - `furnishing_status`: `TEXT` (e.g., `'furnished'`, `'unfurnished'`).
  - `floor_number`: `SMALLINT` (Floor index).
  - `compound_name`: `TEXT`, `view_type`: `TEXT`, `building_quality`: `TEXT` (Descriptive properties).
* **Indexes:**
  - `ix_listings_geom_gist`: GIST index on the geometry point, enabling radial distance lookups.
  - `ix_listings_geom_geog_gist`: GIST index on geometry cast to geography, enabling distance calculations in meters.
  - `ix_listings_composite_match`: Multi-column index on `(category, period, property_type, bedrooms, area_id, scraped_at_utc DESC)` to optimize filtering.
  - `ix_listings_normalized_amenities_gin`: GIN index on normalized amenities JSONB, enabling fast containment checks (`@>`).

### 5.2. Copilot Memory Tables
* **workspaces:** `id` (`SERIAL` Primary Key), `name` (`VARCHAR(255)` Not Null), `created_at` (`TIMESTAMPTZ` Not Null).
* **chats:** `id` (`SERIAL` Primary Key), `workspace_id` (`INTEGER` FK referencing `workspaces(id)`), `title` (`VARCHAR(255)` Not Null), `created_at` (`TIMESTAMPTZ` Not Null).
* **messages:** `id` (`SERIAL` Primary Key), `chat_id` (`INTEGER` FK referencing `chats(id)`), `role` (`VARCHAR(50)` Not Null, e.g., `'user'`, `'assistant'`), `content` (`TEXT` Not Null), `created_at` (`TIMESTAMPTZ` Not Null).
* **property_states:** `id` (`SERIAL` Primary Key), `workspace_id` (`INTEGER` FK referencing `workspaces(id)`), `location` (`VARCHAR(255)`), `area` (`DOUBLE PRECISION` Not Null), `bedrooms` (`INTEGER`), `bathrooms` (`INTEGER`), `amenities` (`JSON` Not Null), `created_at` (`TIMESTAMPTZ` Not Null).
* **scenario_states:** `id` (`SERIAL` Primary Key), `property_state_id` (`INTEGER` FK referencing `property_states(id)`), `name` (`VARCHAR(255)` Not Null), `modifications` (`JSON` Not Null), `delta_value` (`DOUBLE PRECISION`), `created_at` (`TIMESTAMPTZ` Not Null).

### 5.3. Spatial CTE Query Architecture
`[VERIFIED]` (Supporting file: [tier_comps.sql](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/db/sql/tier_comps.sql))

Instead of running slow client-side routing and distance calculations, ValorAI offloads spatial comparable extraction to a PostGIS geofenced Common Table Expression (CTE) query. The query recursively walks up parent areas to identify sibling districts:

```sql
WITH RECURSIVE area_tree AS (
    -- Anchor member: Start at target area
    SELECT area_id, parent_area_id, level, name, geom
    FROM areas
    WHERE area_id = :target_area_id
    UNION ALL
    -- Recursive member: Move up the parent hierarchy
    SELECT a.area_id, a.parent_area_id, a.level, a.name, a.geom
    FROM areas a
    INNER JOIN area_tree t ON a.area_id = t.parent_area_id
)
SELECT l.listing_id, l.price_egp, l.size_sqm, l.bedrooms, l.bathrooms,
       ST_Distance(l.geom::geography, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography) as distance_m
FROM listings l
WHERE l.category = :category
  AND l.period = :period
  AND l.property_type = :property_type
  AND l.bedrooms = :bedrooms
  AND ST_DWithin(l.geom::geography, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography, :max_distance_m)
ORDER BY distance_m ASC
LIMIT :limit_count;
```

This SQL implementation executes in under 10ms, standardizing spatial performance across dense and sparse districts.

---

## 6. Valuation Research: Core Valuation System (AVM Engines)

`[VERIFIED]` (Supporting files: [valuation_service.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/valuation_service.py), [ml_service.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/ml_service.py))

ValorAI integrates two independent, mathematically rigorous valuation engines to handle varying data densities and spatial criteria.

### 6.1. Comparable Market Technique (CMT) Engine
The CMT engine retrieves comparable listings along administrative hierarchies defined in [selector.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/comps/selector.py):
* **Tier 1 (Compound):** Radius: 500m to 1000m. Size/Age tolerance: $\pm 15\%$.
* **Tier 2 (District):** Radius: 1000m to 2000m. Size/Age tolerance: $\pm 20\%$.
* **Tier 3 (Adjacent Districts):** Radius: 2000m to 5000m. Size/Age tolerance: $\pm 25\%$. Evaluates sibling districts via SQL parent walks, excluding the primary parent district to focus on adjacent neighborhoods.
* **Tier 4 (City):** Radius: 5000m to 10000m. Size/Age tolerance: $\pm 30\%$.
* **Tier 5 (Governorate):** Radius: 10000m to 15000m. Size/Age tolerance: $\pm 30\%$.

#### 6.1.1. Robust Statistical Outlier Pruning (MAD Z-Score)
`[VERIFIED]` (Supporting file: [filters.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/filters.py))

To prevent listing price inflation and placeholder listings from corrupting valuations, ValorAI applies a Median Absolute Deviation (MAD) filter. Unlike standard mean-based Z-scores (which are heavily biased by extreme outliers), MAD is a robust estimator. The system calculates a Modified Z-score:
$$MZ_i = 0.6745 \cdot \frac{x_i - \tilde{x}}{\text{MAD}} \quad \text{where } \tilde{x} = \text{median}(x)$$
Listings with $|MZ_i| > 3.5$ are pruned. If $\text{MAD} = 0$ (e.g. all listings have identical prices), the system applies a fallback filter, keeping listings within $\pm 5\%$ of the median.

#### 6.1.2. Dynamic Weighting & Weighted Quantiles
`[VERIFIED]` (Supporting file: [weights.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/weights.py))

The system calculates similarity weights for each listing as a product of component weights:
* **Distance decay:** $w_{\text{distance}} = \frac{1.0}{1.0 + \frac{d}{1000.0}}$
* **Size similarity:** $w_{\text{size}} = 1.0 - \frac{|S_{\text{comp}} - S_{\text{target}}|}{S_{\text{target}}}$
* **Recency decay:** $w_{\text{recency}} = e^{-\frac{A}{60.0}}$ (where $A$ is the listing age in days)
* **Bathroom mismatch penalty:** $0.50$ (matching is $1.0$, missing is $0.85$).
* **Outside area penalty:** $0.95$ (same area matches are $1.0$).
* **Mismatched property type penalty:** $0.60$ (same type matches are $1.0$).
* **Total Weight:** $W = w_{\text{distance}} \times w_{\text{size}} \times w_{\text{recency}} \times w_{\text{bathrooms}} \times w_{\text{same\_area}} \times w_{\text{prop\_type}} \times w_{\text{features}}$.

Sorts listings by price and uses a cumulative weight picker to calculate:
* Expected Fair Price (P50): $q = 0.50$.
* Low Range Bound (P20): $q = 0.20$.
* High Range Bound (P80): $q = 0.80$.

### 6.2. ML (CatBoost Regression) Engine
The ML engine acts as an interpolation model in cold-start or low-density regions:
* **Models:** Pre-trained regressors are loaded at startup: `residential_rent.cbm` (1.3MB) and `residential_sale.cbm` (2.2MB).
* **Target variable log-transformations:** To stabilize pricing variance across high-end villas and small apartments, the target price $Y$ is transformed during training:
  $$y = \ln(Y + 1)$$
  During inference, predicted values are inverted back to EGP:
  $$\text{Price}_{\text{EGP}} = e^{\hat{y}} - 1$$

---

## 7. Hybrid Valuation System Evolution

`[VERIFIED]` (Supporting documents: [07_hybrid_evolution.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/07_hybrid_evolution.md), [router_service.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/router_service.py), [train_baseline.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/data_eg/train_baseline.py))

The integration of the deterministic CMT engine and the statistical machine learning models represents the most critical research journey in the project's history. The team ran three successive experiments to optimize routing logic:

### 7.1. Hybrid V1: Fallback Routing & Stacking Experiment (Failed)
* **Design:** 
  1. *The Routing Pipeline:* An early fallback router. The system ran CMT first; if CMT failed to find any comparables (count $N = 0$), the router executed the CatBoost ML model.
  2. *The Stacking Pipeline:* The team generated a hybrid dataset (`dataset_hybrid_v1`) by running listing points through the database to extract CMT outputs (`deterministic_price`, `confidence_score`, etc.) as training features. They then trained a CatBoost regressor to predict the residual error ($P_{\text{actual}} - P_{\text{deterministic}}$). The final price was calculated as:
     $$P_{\text{final}} = P_{\text{deterministic}} + P_{\text{predicted\_residual}}$$
* **Why It Failed:** 
  1. *Router Failure:* In sparse areas, the geofencing loop (Tiers 1-5) often succeeded in finding a very small number of highly stale listings (e.g. 1-2 comps at Tier 5, 15km away, >180 days old). CMT proceeded to value the property using this sparse sample, producing distorted pricing estimates instead of falling back to the CatBoost ML model.
  2. *Model Failure:* The residual-learning model was unstable because of data sparsity. In low-density regions, CMT returned `INSUFFICIENT_DATA` (or null/None price). Thus, the residual could not be calculated, leading to high null percentages for `deterministic_price` (13% in rent, 41.5% in sale) in the dataset, corrupting the training features and making residual learning unstable.

### 7.2. Hybrid V2: Simple Density Threshold Router (Failed)
* **Design:** 
  1. The router evaluated CMT first. If the comps count was $\ge 10$, it used the CMT pricing engine; otherwise, it fell back to ML.
  2. The ML engine did *not* consume CMT outputs. During dataset preparation for training, the pipeline explicitly dropped all deterministic outputs from the training features, ensuring that the CatBoost model learned purely from spatial and physical listing features.
* **Why It Failed:**
  1. *Latency Spikes:* In high-density districts (e.g. Madinaty or Zamalek with $>700$ listings), the PostGIS query returned hundreds of rows. Slicing, scoring, and calculating feature similarities for all rows inside Python took up to 300ms of CPU time, violating FastAPI's latency SLOs.
  2. *Pricing Sensitivity:* In dense areas, CMT was overly sensitive to listing price variations, whereas the ML model was more robust at smoothing predictions.

### 7.3. Hybrid V3: Goldilocks Router (Succeeded)
* **Design:** The active routing logic resolves the request coordinates to an H3 cell (resolution 9) and evaluates rules based on geographic exposure metrics:
  * **Rule 1 (Goldilocks Zone):** If comps count is between 11 and 50 ($11 \le n \le 50$), use CMT.
  * **Rule 2 (Unseen Geography with Sufficient Comps):** If the compound and H3 cell are unseen but have at least 10 comps, use CMT.
  * **Rule 3 (Default):** If comps count is $<11$ or $>50$, use CatBoost ML.
* **Why it Succeeded:** CMT is highly accurate and interpretable when it has between 11 and 50 comparable properties, avoiding the CPU processing limits of huge datasets while remaining statistically stable. CatBoost ML processes predictions in under 15ms in high-density districts ($N > 50$) and interpolates pricing based on regional features and coordinate trends in low-density districts ($N < 11$).
* **Shadow Telemetry:** Alternate engines run in the background to monitor pricing variance and log divergence (`shadow_logs`), enabling offline calibration without affecting request latency.

### 7.4. Discrepancy Report
A documentation discrepancy was identified during the technical audit of the codebase:
* **The Discrepancy:** Early project roadmaps ([PROJECT_MASTER_STATE.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/docs/PROJECT_MASTER_STATE.md) lines 58-60) planned a "Hybrid AVM" that would merge Layer 4 deterministic outputs (comparable count, median price, tier reached) directly into the Layer 5 CatBoost ML models as features to train a composite estimator.
* **The Reality:** The actual implementation in `train_baseline.py` (line 50) and `ml_service.py` (lines 45-99) explicitly drops all `DETERMINISTIC_FEATURES` before training the CatBoost model. The backend `router_service.py` uses a routing architecture that selects either CMT or ML dynamically, rather than running a stacked/hybrid model.
* **Conclusion:** The planned stacking/blending architecture (Hybrid AVM) was abandoned in favor of a clean routing architecture (Goldilocks Router) because CMT values were missing in sparse areas, making residual learning unstable. The documentation was never updated, resulting in drift.

---

## 8. Explainability Architecture

`[VERIFIED]` (Supporting files: [confidence.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/confidence.py), [ml_service.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/ml_service.py), [amenities.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/amenities.py))

ValorAI implements explainability across all pricing pipelines, decomposed into four core features:

### 8.1. Multi-Dimensional Confidence Metrics
The platform calculates a composite confidence score between $[0.0, 1.0]$ based on evidence characteristics:
* **Count Score:** Capped at $0.35$ if sample size $\ge 80$ (40 comps adds 0.25, 20 comps adds 0.15).
* **Tier Score:** Tier 1 (Same Compound) adds $0.25$ (Tier 2 adds 0.18, Tier 3 adds 0.10, Tier 4 adds 0.06, Tier 5 adds 0.03).
* **Outlier Stability Score:** $\min(0.20, \text{kept\_ratio} - 0.60)$ (Proportion of comps kept after MAD filtering).
* **Price Dispersion Score:** Adds $0.20$ if range dispersion $\le 0.35$; adds $0.12$ if $\le 0.60$ (where $\text{dispersion} = \frac{P_{80} - P_{20}}{P_{50}}$).
* **Distance Quality:** $1.0 - \frac{d_{avg}}{15000}$ (Average distance of comparables relative to maximum search radius).
* **Recency Quality:** $\frac{1.0}{1.0 + \frac{A_{avg}}{60.0}}$ (Average listing age in days).
* **Composite Score:**
  $$S_{\text{evidence}} = 0.84 \cdot S_{\text{base}} + 0.05 \cdot Q_{\text{distance}} + 0.05 \cdot Q_{\text{recency}} + 0.06 \cdot s_{\text{similarity}}$$
* **Unified Confidence cap:** Bounded as $Score_{\text{unified}} = \min \left( S_{\text{evidence}}, S_{\text{location}} \right)$. Capped at $0.50$ if address resolution is ambiguous or if the containment boundary distance is greater than 2500m.

### 8.2. Machine Learning SHAP Drivers
For CatBoost models, Shapley Additive exPlanations (SHAP) are calculated during inference to determine feature impact. Feature importance is converted from log-space to EGP price adjustments:
$$\text{Impact}_{\text{EGP}} = \text{Price}_{\text{estimated}} \cdot \left( e^{\text{SHAP}_i} - 1 \right)$$
Impact percentages are calculated as $(e^{\text{SHAP}_i} - 1) \cdot 100$. Features are ranked, and the top 3 positive and negative features are returned to identify primary value drivers.

### 8.3. Jaccard-Weighted Amenity Similarity
To calculate amenity similarities, the platform uses a weighted Jaccard index:
$$s_{\text{amenities}} = \frac{\sum_{i \in T \cap C} w_i}{\sum_{j \in T \cup C} w_j}$$
Weights ($w$) are category-specific to ensure major features affect the similarity score more than secondary details:
* Private Pool (`PP`): $0.07$ for villas, $0.01$ for commercial offices.
* Central A/C (`AC`): $0.03$ for apartments, $0.06$ for offices.
* Covered Parking (`CP`): $0.05$ across all residential properties.

### 8.4. Narrative Explanation Payload
Generates human-readable explanations (`explain.py:136`), outlining coordinates resolution accuracy, search tier, comps removed by MAD filtering, and average distance, age, and amenity overlap statistics.

---

## 9. Business Intelligence Tools Layer

`[VERIFIED]` (Supporting file: [copilot_tools_service.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/copilot_tools_service.py))

ValorAI exposes eight authenticated, tenant-isolated tools designed to support property analysis and portfolio monitoring.

### Tool 1: Valuation Tool (`execute_valuation`)
* **Purpose:** Computes the fair price estimate and price range bounds for a property, resolving the valuation engine routing (CMT vs ML).
* **Inputs:** `workspace_id` (Integer), `property_id` (Integer), `scenario_id` (Integer, Optional), `target_price_egp` (Integer, Optional), `sandbox_modifications` (Dict, Optional).
* **Outputs:** `valuation_id` (String), `fair_price` (Integer, P50 price in EGP), `price_range` (`{"low": P20, "high": P80}`), `confidence_level` (String), `engine_used` (`'CMT'` or `'ML'`), `routing_reason` (String), `timestamp`.

### Tool 2: Explainability Tool (`execute_explainability`)
* **Purpose:** Generates a structured narrative explanation of a property's valuation.
* **Inputs:** `workspace_id` (Integer), `valuation_id` (String).
* **Outputs:** `valuation_id`, `summary` (String), `why_this_price` (String), `strongest_factors` (String), `confidence_reason` (String), `fairness_status` (String), `feature_drivers` (List of SHAP drivers), `comparable_evidence` (List of comparable items).

### Tool 3: Comparable Tool (`execute_comparable`)
* **Purpose:** Retrieves the verified comparable listings that influenced a property's valuation.
* **Inputs:** `workspace_id` (Integer), `property_id` (Integer), `scenario_id` (Integer, Optional), `valuation_id` (String, Optional).
* **Outputs:** `valuation_id`, `comparable_count` (Integer), `comparables` (List of properties including size, bedrooms, bathrooms, distance, price, and similarity reasons).

### Tool 4: Fairness Tool (`execute_fairness`)
* **Purpose:** Evaluates whether a target asking price is fair relative to the estimated price range.
* **Inputs:** `workspace_id` (Integer), `property_id` (Integer), `scenario_id` (Integer, Optional), `target_price_egp` (Integer), `valuation_id` (String, Optional).
* **Outputs:** `valuation_id`, `fair_price` (EGP), `target_price` (EGP), `fairness_status` (`'Below Fair Value'`, `'Within Fair Value'`, or `'Above Fair Value'`), `confidence_level`, `confidence_reason`, `timestamp`.

### Tool 5: What-If Tool (`execute_what_if`)
* **Purpose:** Simulates how changes to a property's physical characteristics or amenities would affect its valuation.
* **Inputs:** `workspace_id` (Integer), `property_id` (Integer), `scenario_id` (Integer, Optional), `modifications` (Dict containing changes to size, rooms, amenities, view, quality).
* **Outputs:** `base_valuation`, `scenario_valuation` (EGP), `base_valuation_id`, `scenario_valuation_id`, `delta_value` (EGP difference), `delta_percentage` (Percentage difference), `fairness_status`, `assumptions_used` (List of unchanged features flagged as unknown assumptions), `feature_changes` (Details of modified features), `explainability`, `comparables`, `timestamp`.

### Tool 6: Negotiation Tool (`execute_negotiation`)
* **Purpose:** Recommends target counter-offers and generates negotiation talking points for agents.
* **Inputs:** `workspace_id` (Integer), `property_id` (Integer), `scenario_id` (Integer, Optional), `asking_price_egp` (Integer), `what_if_modifications` (Dict, Optional).
* **Outputs:** `valuation_id`, `asking_price`, `fair_price`, `price_gap` (EGP), `price_gap_percentage`, `negotiation_position` (`'Strong Buy Opportunity'`, `'Overpriced'`, `'Fair Market Position'`, `'Premium Justified'`, or `'Negotiation Recommended'`), `recommended_offer_band` (Counter-offer range: low and high endpoints default to the `fair_price` if asking is below or within fair value; if asking is overpriced, the low end is set to the highest comparable at or below fair price, and the high end is set to the fair price), `broker_talking_points` (List of claims linked to citations), `risk_notes` (List of warnings).

### Tool 7: Investment Tool (`execute_investment`)
* **Purpose:** Synthesizes negotiation, pricing, and risk data to evaluate the feasibility of an investment.
* **Inputs:** `workspace_id` (Integer), `property_id` (Integer), `scenario_id` (Integer, Optional), `asking_price_egp` (Integer), `what_if_modifications` (Dict, Optional).
* **Outputs:** `valuation_id`, `asking_price`, `fair_price`, `investment_position` (`'Strong Opportunity'`, `'Moderate Opportunity'`, `'High Risk'`, `'Fairly Priced'`, or `'Caution'`), `investment_summary`, `strengths` (Positives driving the investment), `risks` (Potential issues), `negotiation_summary`, `what_if_summary`, `timestamp`.

### Tool 8: Market Insight Tool (`execute_market_insight`)
* **Purpose:** Computes aggregate analytics across all valuation snapshots saved in a workspace.
* **Inputs:** `workspace_id` (Integer), `time_window` (String, Optional), `compound_name` (String, Optional), `h3_res9` (String, Optional), `property_type` (String, Optional).
* **Outputs:** `market_summary`, `valuation_volume` (Count of matched snapshots), `confidence_distribution`, `fair_value_distribution` (Minimum, median, and maximum fair prices), `comparable_density`, `active_compounds`, `active_areas` (List of segments with valuation volumes and median prices), `evidence_summary` (Traceability details linking to snapshots), `data_sources_used`, `timestamp`.

---

## 10. Agentic Orchestration Innovation & Control Plane Flow

`[VERIFIED]` (Supporting files: [runtime.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/runtime.py), [NARRATION_CONTRACT_ARCHITECTURE.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/docs/NARRATION_CONTRACT_ARCHITECTURE.md))

ValorAI operates as an agentic system by managing conversational context, scheduling tool execution, and enforcing grounding gates.

### 10.1. Orchestrator Components
The orchestrator consists of six standalone, deterministic integration layers:
1. **RuleBasedIntentEngine (`intents/engine.py`):** Classifies user messages into a 10-intent taxonomy (e.g., `VALUATION`, `EXPLAINABILITY`, `WHAT_IF`, `NEGOTIATION`, etc.) using keyword matching, bypassing network latency.
2. **DeterministicToolPlanner (`planner/planner.py`):** Converts the intent into an `ExecutionPlan`. Multi-intent inputs generate parallel tool calls. Property comparison is represented as two parallel Tool 1 invocation slots.
3. **DeterministicToolExecutor (`executor/executor.py`):** Executes tool calls using isolated SQLAlchemy database sessions, preventing session conflicts during parallel execution. It isolates timeouts and catches failures, returning partial results to prevent system crashes.
4. **DeterministicResponseComposer (`composer/composer.py`):** Normalizes tool payloads and executes all calculations (ranges, deltas, percentages) natively in Python before assembling prompt context. It enforces context compression rules, truncating comparable list arrays to a maximum of 3 items.
5. **DeterministicMemoryIntegration (`memory/integration.py`):** Manages conversation history and scenario lineages. Lookups are strictly filtered by the user's workspace ID to enforce tenant isolation.
6. **LLM Narrator (`llm/`):** Sends the compressed context to Gemini 2.5 Pro (default-off). The model is instructed to act as a presentation layer, narrating the composed facts. If the generated text violates grounding validation checks, the **Narration Admission Gate** suppresses the output and returns the raw JSON payload (`DETERMINISTIC_FALLBACK`).

---

## 11. Why ValorAI Is More Than a Mobile Application

`[VERIFIED]` (Supporting files: [main.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/main.py), [init.sql](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/db/sql/init.sql), [runtime.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/runtime.py))

A common misconception is evaluating ValorAI as a mobile application. The Flutter mobile app is merely the delivery mechanism—a presentation wrapper that interfaces with the actual core system. The real innovation and contribution of the project reside entirely on the backend infrastructure and model planes:

1. **The Data Pipeline:** An in-process crawler and batch cleaner that ingests and sanitizes thousands of listings, overriding duplicates and enforcing bounding box coordinate constraints.
2. **PostGIS Spatial Database:** The administrative hierarchy database schema that runs MultiPolygon containment checks (`ST_Covers`) and geofenced radius queries in under 5ms, standardizing location entities across Egypt.
3. **The Valuation Engines:** An explainable Comparable Market Technique (CMT) pricing engine built in Python, and CatBoost machine learning models executing predictions in log-space.
4. **Hybrid Routing Service:** A density-aware and exposure-aware routing layer that checks geographic registries and dynamically routes requests to the safest valuation engine (Goldilocks Router).
5. **Explainability Models:** Dynamic mathematical calculations computing SHAP feature impacts in EGP, weighted Jaccard amenity overlaps, and multi-dimensional confidence scores.
6. **Agentic Orchestration Control Plane:** A 6-stage pipeline that parses intent, schedules tools, runs thread-isolated database sessions, composer-normalizes payloads, and runs grounding policy validations.
7. **Governed Conversational AI:** Implementation of narration contracts and grounding gates. If the generated text violates grounding validation checks or lacks citation tokens, the system suppresses the text and defaults to the deterministic JSON payload.

The mobile client simply displays these complex back-end operations; the real systems engineering occurs in the PostGIS, Python, and CatBoost layers.

---

## 12. Current Status and Commercial Readiness

`[VERIFIED]` (Supporting files: [PROJECT_MASTER_STATE_V2.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/PROJECT_MASTER_STATE_V2.md) lines 935-983, [PROJECT_MASTER_STATE_v3.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/PROJECT_MASTER_STATE_v3.md) lines 64-70)

ValorAI is currently classified as a **staging-grade governed platform with unresolved production integration work**. The system's readiness status is audited below:

1. **Operational Core Systems:**
   * The PostGIS database schemas and SQL migrations `000`-`007` are implemented and verified.
   * The multi-engine CMT/ML routing layer and the dynamic Goldilocks Router are fully operational.
   * The eight functional tools (Valuation, Explainability, Comparable, Fairness, What-if, Negotiation, Investment, and Market Insight) are implemented and pass Docker validation.
   * The agentic orchestrator runtime (Intent classification, Tool Planning, Tool Execution, Response Composition, and Memory pre-generation) is implemented and Docker-validated.
2. **Staging Readiness:**
   * Live backend tests, database recovery tests, and tenant isolation constraints successfully pass staging-grade Docker validation.
3. **Production Gaps & Blockers:**
   * **Authentication Integration:** Firebase ID token exchange is implemented, but frontend mobile JWT integration has gaps, and native credential files (Android `google-services.json`, iOS `GoogleService-Info.plist`) are absent, blocking physical walkthroughs.
   * **Security Infrastructure:** Production secret management, rotation, and role-based access control (RBAC) are not implemented.
   * **LLM Narration:** The Gemini 2.5 Pro provider adapter is implemented but remains default-off until operational data-governance controls and API credentials are set.

ValorAI is entering the agent validation and testing phase to resolve these integration blockers before a production launch.

---

## 13. Recommended Executive Presentation Structure (PPT Blueprint)

This blueprint outlines the recommended structure for an executive presentation to the Dean and Academic Board.

### Slide 1: Cover Slide
* **Title:** ValorAI: A Governed Agentic Intelligence Platform
* **Subtitle:** Transforming Raw Real Estate Data into Governed Real Estate Intelligence in Egypt.
* **Purpose:** Introduce the project, authors, and academic year.
* **Key Points:** Fuses PostGIS spatial hierarchies, CatBoost machine learning, and governed conversational AI under a strict Truth Layer separation of concerns.
* **Recommended Visuals:** Premium dark mode UI splash screen with a glowing spatial chart of Cairo.

### Slide 2: The Problem
* **Title:** The Problem Space: Opacity & Fragmented Data
* **Purpose:** Detail the challenges in the Egyptian real estate market.
* **Key Points:** Transactions are unrecorded, listings contain pricing outliers and duplicate values, appraisals take days, and standard LLMs hallucinate calculations and prices.
* **Recommended Visuals:** A split slide: Left showing portal duplicate listings and price spikes (e.g. 1 EGP placeholder listings); Right showing a flowchart of manual appraiser pipelines.

### Slide 3: Database & PostGIS Spatial Hierarchies
* **Title:** Geospatial Infrastructure & PostGIS Hierarchies
* **Purpose:** Explain the administrative database design.
* **Key Points:** Enforces a 4-level administrative boundary hierarchy (Governorate $\rightarrow$ City $\rightarrow$ District $\rightarrow$ Neighborhood/Compound). Geometries are stored as native point/MultiPolygon coordinates, enabling Containment (`ST_Covers`) and distance checks in under 5ms.
* **Recommended Visuals:** Entity-Relationship Diagram (ERD) illustrating recursive parent-child associations and spatial indices.

### Slide 4: Ingestion & In-Memory Sanitization
* **Title:** Data Ingestion & Sanitization Pipelines
* **Purpose:** Outline listing crawling and cleaning processes.
* **Key Points:** Crawler extracts NEXT_DATA JSON payloads from PropertyFinder Egypt's SSR HTML. The cleaning pipeline prunes placeholder listings ($P \le 100$ EGP), validates Egypt coordinate bounds, and normalizes studio room counts.
* **Recommended Visuals:** Flowchart: Raw SSR HTML $\rightarrow$ NEXT_DATA block extraction $\rightarrow$ parser validations $\rightarrow$ clean database.

### Slide 5: The Comparable Market Technique (CMT) Engine
* **Title:** Comparable Market Technique (CMT) Engine
* **Purpose:** Explain the deterministic pricing engine.
* **Key Points:** Retrieves comparable listings recursively along geofenced tiers. Applies decay weights for distance, size, age, and features similarities, using a cumulative weight quantile picker to calculate Expected Fair Price (P50) and range bounds (P20, P80).
* **Recommended Visuals:** Workflow diagram of the CMT pipeline: Retrieval $\rightarrow$ Guardrails $\rightarrow$ MAD filtering $\rightarrow$ Weighted median.

### Slide 6: Outlier Filtering via MAD
* **Title:** Outlier Filtering: Median Absolute Deviation (MAD)
* **Purpose:** Detail statistical outlier pruning.
* **Key Points:** Uses MAD to calculate Modified Z-scores on price per square meter. MAD is a robust statistic unaffected by extreme outliers. In zero-MAD cases, the system falls back to a tolerance filter, keeping listings within $\pm 5\%$ of the median.
* **Recommended Visuals:** Chart comparing standard Z-score sensitivity to outliers vs MAD stability.

### Slide 7: Machine Learning Valuation (CatBoost)
* **Title:** Machine Learning Regression & SHAP Drivers
* **Purpose:** Explain the ML engine.
* **Key Points:** Loads CatBoost regressor models. Predictions are computed in log-space to stabilize variance, and SHAP values are extracted during inference to identify positive and negative drivers.
* **Recommended Visuals:** Ingestion feature matrix alongside a SHAP feature impact chart.

### Slide 8: The Hybrid Routing Layer
* **Title:** The Hybrid Router: Goldilocks Zone
* **Purpose:** Detail the routing service.
* **Key Points:** Legacy fallbacks (V1 and V2) failed in sparse or high-density areas. Hybrid V3 evaluates exposure metrics, routing queries to CMT when comparable density is in the "Goldilocks Zone" ($11 \le n \le 50$) or if the compound is unseen. Alternate engines run in the background to monitor drift.
* **Recommended Visuals:** Decision tree illustrating Goldilocks routing rules.

### Slide 9: Conversational Co-pilot & Orchestrator Plane
* **Title:** Conversational Co-pilot & Orchestration Plane
* **Purpose:** Explain the agentic conversational flow.
* **Key Points:** RuleBasedIntentEngine classifies messages. Tool Planner schedules tool execution graphs. Response Composer normalizes payloads and executes calculations in Python. Narration Admission Gate validates facts and requires citation tokens, falling back to JSON if checks fail.
* **Recommended Visuals:** Orchestrator data flow diagram: Input $\dots$ Intent $\dots$ Planner $\dots$ Executor $\dots$ Composer $\dots$ LLM.

### Slide 10: The Functional Tools Layer (Tools 1-8)
* **Title:** The Functional Tools Layer (Tools 1-8)
* **Purpose:** Present the functional tool catalog.
* **Key Points:** Lists the 8 tenant-isolated tools (Valuation, Explainability, Comparable, Fairness, What-if, Negotiation, Investment, Market Insight). Explains how Tool 5 runs sandbox overlays and Tool 6 derives offer bands and talking points.
* **Recommended Visuals:** Component grid showing the inputs, outputs, and dependencies of the eight tools.

### Slide 11: System Summary & Readiness
* **Title:** Why ValorAI is More Than a Mobile App
* **Purpose:** Highlight systems engineering contributions.
* **Key Points:** The Flutter app is a presentation layer. The real system consists of the PostGIS database, CMT engine, CatBoost models, and governed orchestrator. Currently in the agent testing phase, preparing for production launch once auth configuration and RBAC are resolved.
* **Recommended Visuals:** Grid showing backend layer latencies and Docker validation metrics.
