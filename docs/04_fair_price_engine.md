# 04. Fair Price Engine (AVM Architecture)

This document details the Fair Price Engine, the core Automated Valuation Model (AVM) of the platform. It explains the algorithm, inputs, outputs, mathematical structures, outlier filtering, and confidence metrics used to generate property valuations.

---

## 1. Algorithm Overview
The Fair Price Engine runs a multi-stage deterministic pipeline. It resolves coordinate locations, retrieves comparable listings, filters out data-entry errors and outliers, weights each comparable by physical and temporal similarity, and resolves values using a weighted median.

```
                  ┌────────────────────────┐
                  │ Valuation Request API  │
                  └───────────┬────────────┘
                              │ [valuation_service.py: price_listing]
                              ▼
                  ┌────────────────────────┐
                  │ Location & Containment │
                  └───────────┬────────────┘
                              │ nearest_area ST_Covers
                              ▼
                  ┌────────────────────────┐
                  │ Multi-Tier Retrieval   │
                  └───────────┬────────────┘
                              │ fetch_comps (Tiers 1-5)
                              ▼
                  ┌────────────────────────┐
                  │ Hard Guardrails Filter │
                  └───────────┬────────────┘
                              │ outliers.py: hard_guardrails
                              ▼
                  ┌────────────────────────┐
                  │   MAD Outliers Filter  │
                  └───────────┬────────────┘
                              │ filters.py: mad_filter
                              ▼
                  ┌────────────────────────┐
                  │ Dynamic Weights Calc   │
                  └───────────┬────────────┘
                              │ estimator.py: compute_weights
                              ▼
                  ┌────────────────────────┐
                  │ Weighted Quantiles     │
                  └───────────┬────────────┘
                              │ weights.py: weighted_median (P20, P50, P80)
                              ▼
                  ┌────────────────────────┐
                  │ Confidence Assessment  │
                  └───────────┬────────────┘
                              │ confidence.py & location cap
                              ▼
                  ┌────────────────────────┐
                  │ Narrative Generation   │
                  └────────────────────────┘
                              │ explain.py: Explainability payload
```

---

## 2. API Input & Output Contracts
* **Direct Valuation Endpoint:** `POST /v1/valuation/fair-price`
* **Aliases:** `POST /v1/rent/fair-price` (aliased to direct valuation for backward compatibility).

### Inbound Schema (`RentFairPriceRequest`)
Defined in [pricing.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/api/routes/pricing.py#L32-L73).

```json
{
  "location_mode": "manual_coordinates",
  "lat": 30.0125,
  "lng": 31.6248,
  "address": null,
  "canonical_entity_id": null,
  "property_category": "residential_rent",
  "property_type": "Apartment",
  "size_sqm": 140.0,
  "bedrooms": 2,
  "bathrooms": 2,
  "target_price_egp": 35000,
  "amenities": ["AC", "CP"],
  "furnishing_status": "unfurnished",
  "floor_number": 2,
  "compound_name": "Villette",
  "view_type": "garden",
  "building_quality": "premium"
}
```

### Outbound Schema (`RentFairPriceResponse`)
Defined in [pricing.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/api/routes/pricing.py#L76-L84).

```json
{
  "fair_price_egp": 32500,
  "range_low_egp": 28000,
  "range_high_egp": 37000,
  "flag": "ok",
  "tier_used": 2,
  "comps_count": 59,
  "confidence": {
    "score": 0.776,
    "label": "High",
    "factors": {
      "count": 0.73,
      "tier": 0.72,
      "kept_ratio": 0.96,
      "dispersion": 0.60,
      "distance": 0.91,
      "recency": 0.81,
      "similarity": 0.92,
      "address_precision": 1.0
    }
  },
  "explanation": ["Valued based on New Cairo area benchmarks."],
  "explanation_trace": [],
  "retrieval_trace": [],
  "spatial_diagnostics": {},
  "evidence_summary": {},
  "area": { "area_id": 284, "name": "Villette", "level": 4 },
  "resolved_location": { "lat": 30.0125, "lng": 31.6248 },
  "property_category": "residential_rent",
  "valuation_contract": {},
  "amenity_intelligence": {},
  "top_comps": []
}
```

---

## 3. Core Valuation Pipeline Stages

### Stage 1: Location Resolution & Containment
* **Source Files:** [address_resolver.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/geo/address_resolver.py) & [area_resolver.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/geo/area_resolver.py)
* **Actions:**
  1. Validates coordinate bounds. Resolves address strings to lat/lng using geocoding cache lookups.
  2. Resolves containment (`nearest_area`) via a PostGIS SQL query checking which polygon covers the point center:
     ```sql
     ST_Covers(geom, ST_SetSRID(ST_MakePoint(lng, lat), 4326))
     ```
  3. Computes the location distance in meters from the point coordinates to the resolved shape center.

### Stage 2: Recursive Comparable Retrieval
* **Source Files:** [selector.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/comps/selector.py) & [tier_comps.sql](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/db/sql/tier_comps.sql)
* **Actions:** Queries the PostGIS database recursively walking up from the resolved leaf area using Tiers 1-5 (Compound $\rightarrow$ District $\rightarrow$ Adjacent Districts $\rightarrow$ City $\rightarrow$ Governorate) until the number of comparables retrieved meets the contract threshold (typically $\ge 40$ listings).
* **Amenity Filter:** If a search tier returns matching listings, the selector runs `_apply_amenity_retrieval_filter`. If the target property has critical amenities, the listings are filtered to require at least one matching amenity code. If this filter reduces the sample size below the contract threshold, the filter is bypassed to maintain search depth.

### Stage 3: Hard Guardrails Filtering
* **Source File:** [outliers.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/comps/outliers.py)
* **Actions:** Evaluates the candidate listings against category-specific boundaries:
  - Excludes listings with missing sizes, bedroom counts, or bathroom counts.
  - Excludes listings where pricing, size, or price per square meter fall outside contract boundaries:
    - Minimum monthly rent: $1,000$ EGP.
    - Maximum monthly rent: $500,000$ EGP.
    - Maximum residential property size: $1,000$ sqm.

### Stage 4: Statistical Outlier Pruning (MAD Z-Score)
* **Source File:** [filters.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/filters.py)
* **Actions:**
  - Evaluates pricing statistics on the remaining comparables using the Median Absolute Deviation (MAD).
  - If the sample size is $\ge 10$, outlier filtering is computed using the price per square meter; otherwise, raw price is used.
  - For each listing, calculates the Modified Z-score:
    $$MZ_i = 0.6745 \cdot \frac{x_i - \tilde{x}}{\text{MAD}} \quad \text{where } \tilde{x} = \text{median}(x)$$
  - Excludes listings where the absolute Z-score $|MZ_i| > 3.5$.
  - **Zero-MAD Exception:** If $\text{MAD} = 0$, the system switches to a tolerance-based filter, keeping only listings whose price falls within $\pm 5\%$ of the median.

### Stage 5: Dynamic Weighting & Similarity Calculations
* **Source File:** [estimator.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/estimator.py)
* **Actions:** Computes component weights for each comparable listing:
  - **Spatial Decay:** $w_{\text{distance}} = \frac{1.0}{1.0 + \frac{d}{1000.0}}$
  - **Size Similarity:** $w_{\text{size}} = 1.0 - \frac{|S_{\text{comp}} - S_{\text{target}}|}{S_{\text{target}}}$
  - **Recency Decay:** $w_{\text{recency}} = e^{-\frac{A}{60.0}}$
  - **Bathroom Congruency:** 1.0 if match, 0.50 if mismatch, 0.85 if missing.
  - **Same Leaf Area:** 1.0 if same neighborhood/compound, 0.95 if outside.
  - **Property Type:** 1.0 if match, 0.60 if mismatch.
  - **Feature Similarity:** Combines floor, view, and furnishing similarity. Mismatches reduce the feature score but do not discard the listing.
  - **Amenity Similarity:** Mapped via Jaccard index:
    $$s_{\text{amenities}} = \frac{\sum_{i \in T \cap C} w_i}{\sum_{j \in T \cup C} w_j}$$
  - **Total Weight ($W$):** Computed as the product of all active weights. If bedroom counts mismatch, the total weight becomes `0`.

### Stage 6: Weighted Quantile Selection
* **Source File:** [weights.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/weights.py)
* **Actions:**
  - Sorts listings in ascending order of price.
  - Finds the price at which the cumulative weight exceeds the target quantile.
  - **P50 (Weighted Median):** Resolves the target fair price ($q=0.50$).
  - **P20 (Low Bound Range):** Resolves the target low-end price ($q=0.20$).
  - **P80 (High Bound Range):** Resolves the target high-end price ($q=0.80$).

### Stage 7: Evidence-Based Confidence Assessment
* **Source File:** [confidence.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/confidence.py)
* **Actions:** Calculates a composite score based on evidence characteristics:
  - Count score: Cap score at 0.35 if sample size $\ge 80$.
  - Tier score: Tier 1 adds 0.25; Tier 5 adds 0.03.
  - Stability score: Fraction of listings kept after MAD filtering ($\min(0.20, \text{kept\_ratio} - 0.60)$).
  - Dispersion score: Adds 0.20 if range dispersion $\le 35\%$; adds 0.05 if $>60\%$.
  - Quality score: Average distance decay, average listing age, average feature similarity.
  - Unified confidence:
    $$Score_{\text{unified}} = \min \left( S_{\text{evidence}}, S_{\text{location}} \right)$$
    Capped at $0.50$ if address resolution is ambiguous or if the containment boundary distance is greater than 2500m.

---

## 4. Operational Guardrails & Failure Modes
1. **Low Density Fallback:** If the multi-tiered search returns fewer than 10 comps across all 5 tiers, the valuation returns `PriceFlag.INSUFFICIENT_DATA` with a price of `0`. Under the hybrid router, this triggers an emergency fallback to the CatBoost ML model.
2. **Ambiguous containment:** If the PostGIS query returns multiple parent shapes, the area resolver raises an error, which blocks the valuation and returns `AMBIGUOUS_LOCATION`.
3. **Database Connection Dropout:** If query execution throws database exceptions, the router intercepts the error and routes the query directly to the CatBoost model to maintain service availability.
