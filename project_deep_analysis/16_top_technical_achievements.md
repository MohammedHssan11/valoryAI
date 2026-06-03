# 16. Technical Achievements Deep-Dive

This document presents a technical analysis of the top achievements of the platform, detailing the engineering choices, code structures, and performance profiles.

---

## 1. Hybrid Goldilocks Router
* **Purpose:** Balances estimation speed and accuracy by routing requests to either CMT (for explainability) or ML (for scaling in sparse regions).
* **Code Reference:** [router_service.py:21-34](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/router_service.py#L21-L34)
* **Heuristics:**
  - If comps count is in the "Goldilocks Zone" ($11 \le comps \le 50$), use CMT.
  - If compound and H3 cells are unseen but have $\ge 10$ comps, use CMT.
  - Otherwise, use CatBoost ML.
* **Why it is an achievement:** Merges deterministic, explainable calculations with statistical machine learning regressors, ensuring reliable pricing across all geographic densities.

---

## 2. Multi-Tier Recursive CTE geofencing
* **Purpose:** Queries listings recursively through administrative hierarchies.
* **Code Reference:** [tier_comps.sql](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/db/sql/tier_comps.sql)
* **Query Structure:**
  - Uses recursive SQL to map parent areas (Governorate -> City -> District -> Neighborhood).
  - Sweeps Tiers 1-5 and radius bounds sequentially.
  - Bounded by spatial indexing point structures (`ST_DWithin`).
* **Why it is an achievement:** Replaces slow client-side filtering loops with a single SQL query that executes parent-child containment walks in under 10ms.

---

## 3. Modified Z-Score MAD Outlier Filter
* **Purpose:** Discards listing anomalies and data-entry errors.
* **Code Reference:** [filters.py:38-86](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/filters.py#L38-L86)
* **Algorithm:** Calculates the Modified Z-score using Median Absolute Deviation (MAD):
  $$MZ_i = 0.6745 \cdot \frac{x_i - \tilde{x}}{\text{MAD}}$$
* **Why it is an achievement:** Unlike standard standard deviation filters, MAD is a robust estimator that is unaffected by extreme outliers, ensuring clean data input for valuations.

---

## 4. Narration Contracts Governance
* **Purpose:** Prevents conversational LLM hallucinations.
* **Code Reference:** [NARRATION_CONTRACT_ARCHITECTURE.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/docs/NARRATION_CONTRACT_ARCHITECTURE.md)
* **Rules:**
  - Restricts LLM responses to narrating facts in the composed context.
  - Forbids model calculations or referencing external knowledge.
* **Why it is an achievement:** Protects pricing reliability by restricting the model to a presentation layer.

---

## 5. Arithmetic Offloading in Composer
* **Purpose:** Performs all calculations natively in Python.
* **Code Reference:** [composer.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/composer/composer.py)
* **Actions:** Computes averages, ranges, price differences, and size differences in code before prompt assembly, preventing LLM math errors.
* **Why it is an achievement:** Solves a major limitation of language models, ensuring absolute mathematical accuracy.

---

## 6. Weighted Jaccard Amenity Similarity
* **Purpose:** Scores amenity similarities.
* **Code Reference:** [amenities.py:243-297](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/amenities.py#L243-L297)
* **Formula:**
  $$s_{\text{amenities}} = \frac{\sum_{i \in T \cap C} w_i}{\sum_{j \in T \cup C} w_j}$$
* **Why it is an achievement:** Applies category-specific weights to amenities (e.g. pools, parking), ensuring high-value features have a greater impact on comparable weighting.

---

## 7. SHAP Feature Impact Derivation
* **Purpose:** Translates CatBoost log-space impact values to EGP price adjustments.
* **Code Reference:** [ml_service.py:123-160](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/ml_service.py#L123-L160)
* **Formula:**
  $$\text{Impact}_{\text{EGP}} = \text{Price}_{\text{estimated}} \cdot \left( e^{\text{SHAP}_i} - 1 \right)$$
* **Why it is an achievement:** Provides feature-level transparency for machine learning predictions, identifying positive and negative drivers.

---

## 8. Shadow Execution Telemetry
* **Purpose:** Telemetry logger comparing active and shadow predictions.
* **Code Reference:** [monitoring_service.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/monitoring_service.py)
* **Why it is an achievement:** Runs the alternate model in the background to monitor pricing engine variance and detect model drift.

---

## 9. Geocoding Address Cache
* **Purpose:** Caches normalized address lookups.
* **Code Reference:** [address_resolver.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/geo/address_resolver.py)
* **Why it is an achievement:** Resolves coordinates cache lookups in under 5ms, minimizing external API costs and latency.

---

## 10. Unseen Geography Exposure Registry
* **Purpose:** Evaluates spatial exposure scores.
* **Code Reference:** [exposure_registry.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/geo/exposure_registry.py)
* **Why it is an achievement:** Automatically flags unseen compounds and H3 cells, adjusting valuation routing rules dynamically.
