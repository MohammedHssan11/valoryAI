# ValorAI Valuation Evolution Forensic Audit
**Subject:** Hybrid Valuation Model Evolution (V1, V2, and V3)  
**Auditor:** Technical Auditor & Forensic Architect  
**Scope:** Valuation router, pricing engine, machine learning services, training pipelines, and documentation  
**Status Key:** `[VERIFIED]`, `[PARTIALLY VERIFIED]`, `[NOT VERIFIED]`  

---

## 1. Timeline of Valuation Systems Reconstructed
`[VERIFIED]` (Supporting documents: [01_project_evolution.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/01_project_evolution.md), [07_hybrid_evolution.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/07_hybrid_evolution.md), [train_baseline.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/data_eg/train_baseline.py), [generate_hybrid_dataset.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/scripts/generate_hybrid_dataset.py))

Through a forensic sweep of the repository's codebase and documentation, the chronological evolution of the ValorAI pricing layer has been reconstructed:

```
CMT Only (Valuation V1)
  │ (Failed: Insufficient data when comps count = 0)
  ▼
ML Only (Valuation V2)
  │ (Failed: Price fluctuations & cold-start hallucinations)
  ▼
Hybrid V1: Fallback Router & Stacking Model
  │ (Failed: Geofence radius expansion matched 1-2 stale comps; 
  │  stacking failed due to high null rates in sparse regions)
  ▼
Hybrid V2: Simple Density Threshold Router
  │ (Failed: Latency spikes in high-density cells; 
  │  high pricing sensitivity to listing variations)
  ▼
Goldilocks Router (Hybrid V3)
     - Successfully deployed. Routes based on exposure registry and Goldilocks Zone rules
```

---

## 2. Hybrid V1 Audit

### 2.1. Implementation Reality
`[VERIFIED]` (Supporting files: [generate_hybrid_dataset.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/scripts/generate_hybrid_dataset.py), [validate_hybrid_dataset.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/scripts/validate_hybrid_dataset.py))

Two distinct systems were implemented under the "Hybrid V1" label:
1. **The Routing Pipeline:** A basic fallback router. The system ran CMT first; if CMT raised an exception or returned zero comparables ($N = 0$), the router executed the CatBoost ML model.
2. **The Training Pipeline:** A residual-learning stacking model. The team generated a hybrid dataset (`dataset_hybrid_v1`) by running listing points through the database to extract CMT outputs (`deterministic_price`, `confidence_score`, etc.) as training features. They then trained a CatBoost regressor to predict the residual error ($P_{\text{actual}} - P_{\text{deterministic}}$). The final price was calculated as:
   $$P_{\text{final}} = P_{\text{deterministic}} + P_{\text{predicted\_residual}}$$

---

### 2.2. Code Evidence
`[VERIFIED]` (Source: [validate_hybrid_dataset.py:98-117](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/scripts/validate_hybrid_dataset.py#L98-L117), [generate_hybrid_dataset.py:104-115](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/scripts/generate_hybrid_dataset.py#L104-L115))

From `generate_hybrid_dataset.py`:
```python
df['deterministic_price'] = det_prices
df['confidence_score'] = det_conf_scores
...
actual_price = df['price']
df['residual'] = actual_price - df['deterministic_price']
df['abs_residual'] = df['residual'].abs()
```

From `validate_hybrid_dataset.py`:
```python
# Predict the residual using features that retain deterministic pricing features
X = df.drop(columns=[c for c in drop_cols if c in df.columns])
y = df['residual']
...
model = CatBoostRegressor(iterations=100, depth=6, learning_rate=0.1, verbose=0, cat_features=cat_features)
model.fit(X_train, y_train)
pred_residual = model.predict(X_test)

final_pred_price = det_test + pred_residual
```

---

### 2.3. Documentation Evidence
`[VERIFIED]` (Source: [07_hybrid_evolution.md:9-11](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/07_hybrid_evolution.md#L9-L11))

From `07_hybrid_evolution.md`:
> **Hybrid V1 (Direct Fallback)**
> * **Vulnerability:** The router executed CMT first. If CMT failed to find any comparables (count $N=0$), it triggered the CatBoost model.

---

### 2.4. Why It Failed
`[VERIFIED]` (Source: [hybrid_dataset_report.json](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/data_eg/dataset_hybrid_v1/hybrid_dataset_report.json), [07_hybrid_evolution.md:11](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/07_hybrid_evolution.md#L11))

1. **Router Failure Mode:** In sparse areas, the geofencing loop (Tiers 1-5) often succeeded in finding a very small number of highly stale listings (e.g. 1-2 comps at Tier 5, 15km away, >180 days old). The engine proceeded to value the property using this sparse sample, producing distorted pricing estimates instead of falling back to the CatBoost ML model.
2. **Model/Dataset Failure Mode:** The residual-learning model was unstable because of data sparsity. In low-density regions, CMT returned `INSUFFICIENT_DATA` (or null/None price). Thus, the residual could not be calculated, leading to high null percentages for `deterministic_price` (13% in rent, 41.5% in sale) in the dataset. This caused training data corruption and poor generalizability.

---

### 2.5. Deployment/Testing Status
`[VERIFIED]` (Source: [hybrid_dataset_report.json](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/data_eg/dataset_hybrid_v1/hybrid_dataset_report.json), [hybrid_training_results.json](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/data_eg/models_hybrid_v1/hybrid_training_results.json))

Hybrid V1 was tested offline. The parquet outputs, residual statistics (median absolute residual of 15,000 EGP for rent and 1.8M EGP for sale), and performance metrics (R² of 0.41 for rent, 0.67 for sale) are documented in the registry reports. It was not promoted to live production due to the sparse geofencing fallback issue.

---

## 3. Hybrid V2 Audit

### 3.1. Implementation Reality
`[VERIFIED]` (Source: [train_baseline.py:12-18](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/data_eg/train_baseline.py#L12-L18), [router_service.py:21-34](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/router_service.py#L21-L34))

Hybrid V2 was a **routing architecture**, not a stacking architecture:
1. The router evaluated CMT first. If the comps count was $\ge 10$, it used the CMT pricing engine; otherwise, it fell back to ML.
2. The ML engine did *not* consume CMT outputs. During dataset preparation for training, the pipeline explicitly dropped all deterministic outputs from the training features, ensuring that the CatBoost model learned purely from spatial and physical listing features.

---

### 3.2. Code Evidence
`[VERIFIED]` (Source: [train_baseline.py:12-18](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/data_eg/train_baseline.py#L12-L18), [train_baseline.py:50](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/data_eg/train_baseline.py#L50))

From `train_baseline.py`:
```python
# Prohibited deterministic features
DETERMINISTIC_FEATURES = [
    "deterministic_price", "comparable_count", "confidence_score",
    "tier_reached", "retrieval_radius", "median_price_per_sqm",
    "weighted_price_per_sqm", "comparable_price_std", "comparable_price_iqr",
    "median_comparable_age_days"
]
...
# Drop all deterministic features to ensure clean training
cols_to_drop += DETERMINISTIC_FEATURES
df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
```

---

### 3.3. Documentation Evidence
`[VERIFIED]` (Source: [07_hybrid_evolution.md:13-15](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/07_hybrid_evolution.md#L13-L15))

From `07_hybrid_evolution.md`:
> **Hybrid V2 (Simple Density Threshold)**
> * **Vulnerability:** The router evaluated CMT first. If the number of comps found was $\ge 10$, it used CMT; otherwise, it fallback to ML.

---

### 3.4. Why It Failed
`[VERIFIED]` (Source: [07_hybrid_evolution.md:15](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/07_hybrid_evolution.md#L15))

1. **Latency Spikes:** In high-density districts (e.g. Madinaty or Zamalek with $>700$ listings), the PostGIS query returned hundreds of rows. Slicing, scoring, and calculating feature similarities for all rows inside Python took up to 300ms of CPU time, violating FastAPI's latency SLOs.
2. **Pricing Sensitivity:** In dense areas, CMT was overly sensitive to listing price variations, whereas the ML model was more robust at smoothing predictions.

---

## 4. Hybrid V3 (Goldilocks Router) Audit

### 4.1. Implementation Reality
`[VERIFIED]` (Source: [router_service.py:21-34](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/router_service.py#L21-L34), [router_service.py:151-191](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/router_service.py#L151-L191))

The active routing logic resolves the request coordinates to an H3 cell (resolution 9) and evaluates rules based on geographic exposure metrics:
1. **Rule 1 (Goldilocks Zone):** If comps count is between 11 and 50 ($11 \le n \le 50$), use CMT.
2. **Rule 2 (Unseen Geography with Sufficient Comps):** If the compound and H3 cell are unseen but have at least 10 comps, use CMT.
3. **Rule 3 (Default):** If comps count is $<11$ or $>50$, use CatBoost ML.

---

### 4.2. Code Evidence
`[VERIFIED]` (Source: [router_service.py:21-34](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/router_service.py#L21-L34))

From `router_service.py`:
```python
def evaluate_routing_rules(comps_count: int, is_unseen_comp: bool, is_unseen_h3: bool) -> tuple[str, str]:
    """
    Evaluates the Phase 5.1 Optimized Router rules:
    if (11 <= comps <= 50) or ((unseen_compound or unseen_h3) and comps >= 10):
        use CMT
    else:
        use ML
    """
    if 11 <= comps_count <= 50:
        return "CMT", "GoldilocksZone"
    if (is_unseen_comp and is_unseen_h3) and comps_count >= 10:
        return "CMT", "UnseenGeographyWithSufficientComps"
    
    return "ML", "PureMLBaseline"
```

---

### 4.3. Why It Succeeded
`[VERIFIED]` (Source: [07_hybrid_evolution.md:41-44](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/project_deep_analysis/07_hybrid_evolution.md#L41-L44))

1. **CMT Bounded Zone:** CMT is highly accurate and interpretable when it has between 11 and 50 comparable properties, avoiding the CPU processing limits of huge datasets while remaining statistically stable.
2. **ML Scale Invariance:** In high-density districts ($N > 50$), the system routes to CatBoost ML, which processes predictions in under 15ms. In low-density districts ($N < 11$), CatBoost ML interpolates pricing based on regional features and coordinate trends, bypassing sparse CMT estimates.

---

## 5. Discrepancy Analysis

The technical audit identified a major discrepancy between the project's documentation and the codebase:

* **Documentation Claim:**
  In the root master state ([PROJECT_MASTER_STATE.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/docs/PROJECT_MASTER_STATE.md) lines 58-60) and technical audit reviews ([TECHNICAL_AUDIT_REPORT.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/docs/TECHNICAL_AUDIT_REPORT.md) lines 399-403), the project claimed to be developing a "Hybrid AVM" by merging Layer 4 deterministic outputs (comparable count, median price, tier reached) directly into the Layer 5 ML models to form a composite estimator.
* **Code Reality:**
  The actual implementation in `train_baseline.py` (line 50) and `ml_service.py` (lines 45-99) explicitly drops all `DETERMINISTIC_FEATURES` before training the CatBoost model. The backend `router_service.py` uses a routing architecture that selects either CMT or ML dynamically, rather than running a stacked/hybrid model.
* **Conclusion:**
  The planned stacking/blending architecture (Hybrid AVM) was abandoned in favor of a clean routing architecture (Goldilocks Router) because CMT values were missing in sparse areas, making residual learning unstable. The documentation was never updated, resulting in drift.
