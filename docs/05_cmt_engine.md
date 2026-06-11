# 05. CMT Engine (Comparable Market Technique)

This document presents the technical specification of the Comparable Market Technique (CMT) engine. The CMT engine is a rule-based spatial valuation engine that calculates property values based on statistical adjustments of comparable neighbors.

---

## 1. Candidate Retrieval Pipeline
* **Source Files:** [selector.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/comps/selector.py) & [tier_comps.sql](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/db/sql/tier_comps.sql)

The retrieval process is implemented as a loop that walks through 5 administrative boundary tiers, expanding the search criteria at each tier until a target sample size is reached.

```
Resolved Location Point (lat, lng)
  │
  ├── Tier 1: Same Compound / Neighborhood (Level 4)
  │     Radius steps: [500m, 1000m]
  │     Size bounds: ±15% size, ±15% age
  │     [If comps < 40: Fallback]
  │
  ├── Tier 2: Same District (Level 3)
  │     Radius steps: [1000m, 2000m]
  │     Size bounds: ±20% size, ±20% age
  │     [If comps < 40: Fallback]
  │
  ├── Tier 3: Adjacent Districts (Level 3 Sibling Walk)
  │     Radius steps: [2000m, 5000m]
  │     Size bounds: ±25% size, ±25% age
  │     [If comps < 40: Fallback]
  │
  ├── Tier 4: Same City (Level 2)
  │     Radius steps: [5000m, 10000m]
  │     Size bounds: ±30% size, ±30% age
  │     [If comps < 40: Fallback]
  │
  └── Tier 5: Same Governorate (Level 1)
        Radius steps: [10000m, 15000m]
        Size bounds: ±30% size, ±30% age
```

### Administrative Scope Resolution
To identify child areas recursively, the selector walks parent-child associations in the `areas` table using PostgreSQL recursive CTEs:
* Walks up from target `area_id` to build the hierarchy:
  - `governorate_id` (Level 1)
  - `city_id` (Level 2)
  - `district_id` (Level 3)
  - `leaf_id` (Level 4)
* Traverses down from the resolved scope root area to identify all child shapes.
* **Exclusion logic:** If the scope is set to `nearby_districts`, the query selects siblings of the parent district but explicitly excludes the primary parent district to focus on adjacent neighborhoods.

---

## 2. Core Mathematical Specifications

### 1. Distance Decay Weight ($w_{\text{distance}}$)
* **Code Implementation:**
  ```python
  # estimator.py:25
  return _clamp_unit(1.0 / (1.0 + (dist_m / WEIGHTING.distance_decay_m)))
  ```
* **Formula:**
  $$w_{\text{distance}} = \frac{1.0}{1.0 + \frac{d}{\lambda_{\text{distance}}}}$$
* **Parameters:**
  - $d$: Spatial distance in meters.
  - $\lambda_{\text{distance}}$: Distance decay denominator ($1000.0$ meters).
  - Fallback: $0.20$ if distance is missing.

### 2. Size Similarity Weight ($w_{\text{size}}$)
* **Code Implementation:**
  ```python
  # estimator.py:31-32
  rel = abs(size_sqm - target) / target
  return _clamp_unit(1.0 - rel)
  ```
* **Formula:**
  $$w_{\text{size}} = 1.0 - \frac{|S_{\text{comp}} - S_{\text{target}}|}{S_{\text{target}}}$$
* **Parameters:**
  - $S_{\text{comp}}$: Comparable size in sqm.
  - $S_{\text{target}}$: Subject property size in sqm.
  - Fallback: $0.60$ if size is missing.
  - Bounded: Clamped to $[0.0, 1.0]$. If size difference is $\ge 100\%$, weight becomes $0.0$.

### 3. Recency Decay Weight ($w_{\text{recency}}$)
* **Code Implementation:**
  ```python
  # estimator.py:42
  return _clamp_unit(math.exp(-age_days / WEIGHTING.recency_decay_days))
  ```
* **Formula:**
  $$w_{\text{recency}} = e^{-\frac{A}{\lambda_{\text{recency}}}}$$
* **Parameters:**
  - $A$: Comparable listing age in days.
  - $\lambda_{\text{recency}}$: Recency decay scale ($60.0$ days).
  - Fallback: $0.60$ if age is missing.

### 4. Bathroom Congruency Weight ($w_{\text{bathrooms}}$)
* **Code Implementation:**
  ```python
  # estimator.py:48-50
  return 1.0 if int(comp_bathrooms) == int(target_bathrooms) else _clamp_unit(WEIGHTING.bathroom_mismatch)
  ```
* **Heuristics:**
  - 1.0 if target bathrooms count is unspecified.
  - 1.0 if count matches exactly.
  - 0.50 if count mismatches (`BATHROOM_MISMATCH_WEIGHT`).
  - 0.85 if comparable bathrooms count is missing (`BATHROOM_WEIGHT_FALLBACK`).

### 5. Same Area Weight ($w_{\text{same\_area}}$)
* **Formula:**
  $$w_{\text{same\_area}} = \begin{cases} 1.0 & \text{if } \text{area\_id}_{\text{comp}} = \text{area\_id}_{\text{target}} \\ 0.95 & \text{otherwise} \end{cases}$$
* **Purpose:** Adds a minor penalty for fallback listings located outside the leaf area boundary.

### 6. Property Type Weight ($w_{\text{prop\_type}}$)
* **Formula:**
  $$w_{\text{prop\_type}} = \begin{cases} 1.0 & \text{if } \text{type}_{\text{comp}} = \text{type}_{\text{target}} \\ 0.60 & \text{otherwise} \end{cases}$$
* **Purpose:** Bypasses or down-weights listings of different property types (e.g. comparing a duplex to an apartment). Mismatch weight is category-specific.

### 7. Feature Similarity Score ($S_{\text{feature}}$)
* **Source File:** [feature_similarity.py:108-133](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/feature_similarity.py#L108-L133)
* **Formula:**
  $$s_{\text{composite}} = \frac{\sum_{k \in F} s_k \cdot W_k}{\sum_{k \in F} W_k}$$
* **Parameters:**
  - $F$: Active features specified in both the target and the comparable (furnishing, floor, compound, view, quality).
  - $s_k$: Score (1.0 for match, 0.0 for mismatch).
  - $W_k$: Weight configuration from the category contract.

### 8. Amenity Jaccard Similarity Score ($S_{\text{amenities}}$)
* **Source File:** [amenities.py:290-297](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/amenities.py#L290-L297)
* **Formula:**
  $$s_{\text{amenities}} = \frac{\sum_{i \in T \cap C} w_i}{\sum_{j \in T \cup C} w_j}$$
* **Parameters:**
  - $T$: Target amenity symbols.
  - $C$: Comparable amenity symbols.
  - $w_k$: Weight of amenity symbol $k$ for the given category.
  - Returns $1.0$ if union is empty.

### Composite Listing Weight ($W$)
$$\text{Total Weight } W = w_{\text{distance}} \times w_{\text{size}} \times w_{\text{recency}} \times w_{\text{bathrooms}} \times w_{\text{same\_area}} \times w_{\text{prop\_type}} \times w_{\text{features}}$$

---

## 3. Statistical Outlier Removal (MAD)
* **Source File:** [filters.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/filters.py)

Before pricing calculation, candidate listings are filtered to remove statistical outliers. Unlike standard Z-scores, which are sensitive to outliers (since mean and standard deviation are themselves affected by extreme values), the engine uses the Median Absolute Deviation (MAD).

```
Candidate Listings (Filtered by guardrails)
  │
  ├── Sample size < 10?
  │     ├── YES: Bypass outlier filtering, return candidates.
  │     └── NO: Use price per square meter.
  │
  ├── Calculate median (M) and absolute deviations: |x_i - M|
  │
  ├── Calculate MAD = median(|x_i - M|)
  │
  ├── MAD = 0?
  │     ├── YES: Apply Zero-MAD Tolerance Filter (Keep listings within ±5% of M).
  │     └── NO: Calculate Modified Z-score:
  │              MZ_i = 0.6745 * (x_i - M) / MAD
  │
  └── Exclude listings where |MZ_i| > 3.5
```

---

## 4. Weighted Median Valuation
* **Source File:** [weights.py:12-38](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/weights.py#L12-L38)

Once weights are calculated and outliers are removed, the valuation is resolved using a weighted quantile picker:
1. Pairs prices and weights: $(P_i, W_i)$.
2. Sorts pairs in ascending order of price: $P_1 \le P_2 \le \dots \le P_n$.
3. Finds the index $k$ at which the cumulative weight exceeds the target quantile:
   $$\sum_{i=1}^k W_i \ge q \sum_{j=1}^n W_j$$
4. **P50 (Weighted Median):** Bounded by $q=0.50$.
5. **P20 (Low Bound Range):** Bounded by $q=0.20$.
6. **P80 (High Bound Range):** Bounded by $q=0.80$.
