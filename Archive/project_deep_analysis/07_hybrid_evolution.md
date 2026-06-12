# 07. Hybrid Valuation System Evolution

This document traces the development and optimization of the hybrid router that governs how the system routes valuation requests between the deterministic CMT engine and the CatBoost machine learning models.

---

## 1. Failed Designs & Technical Lessons

### Hybrid V1 (Direct Fallback)
* **Vulnerability:** The router executed CMT first. If CMT failed to find any comparables (count $N=0$), it triggered the CatBoost model.
* **Failure Mode:** In sparse areas, the geofencing loop (Tiers 1-5) often succeeded in finding a very small number of stale listings (e.g., $N=1$ or $2$ comps in Tier 5, 15km away, older than 180 days). The engine proceeded to value the property using this sparse sample, resulting in highly distorted estimates instead of falling back to the CatBoost ML model.

### Hybrid V2 (Simple Density Threshold)
* **Vulnerability:** The router evaluated CMT first. If the number of comps found was $\ge 10$, it used CMT; otherwise, it fallback to ML.
* **Failure Mode:** In high-density districts (e.g., Madinaty or Zamalek with $>700$ listings), the PostGIS query returned hundreds of rows. Slicing, scoring, and calculating feature similarities for all rows inside Python took up to 300ms of CPU time. Additionally, in very dense areas, the pricing returned by CMT was overly sensitive to listing price variations, whereas the ML model was more robust at scaling predictions.

---

## 2. Hybrid V3: Exposure-Based Goldilocks System
The active routing logic resolves locations to H3 index cells and evaluates rules based on geographic exposure metrics:
* **Source File:** [router_service.py:21-34](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/router_service.py#L21-L34)
* **Function:** `evaluate_routing_rules`

```
Resolved Location Point (lat, lng)
  │
  ├── 1. Get H3 Cell index (resolution 9) & Compound Name
  │
  ├── 2. Check Exposure Registry (exposure_registry.json)
  │        ├── Compound in seen list?  ──► unseen_comp = False/True
  │        └── H3 Cell in seen list?   ──► unseen_h3 = False/True
  │
  ├── 3. Execute CMT (runs search tiers to resolve comps count)
  │
  └── 4. Evaluate Goldilocks Rules:
           ├── Comp count inside [11, 50]? ───────────────────────► CMT (GoldilocksZone)
           ├── (unseen_comp AND unseen_h3) AND comps >= 10? ───────► CMT (UnseenGeographyWithSufficientComps)
           └── Otherwise (count < 11 OR count > 50)? ──────────────► ML (PureMLBaseline)
```

### Why the Goldilocks Rules Succeeded
1. **CMT Bounded Zone:** CMT is highly accurate and interpretable when it has between 11 and 50 comparable properties. It avoids the CPU processing limits of huge datasets while remaining statistically stable.
2. **ML Scale Invariance:** In high-density districts ($N > 50$), the system routes to CatBoost ML, which processes predictions in under 15ms. In low-density districts ($N < 11$), CatBoost ML interpolates pricing based on regional features and coordinate trends, bypassing sparse CMT estimates.

---

## 3. Telemetry & Shadow Execution Pipelines
* **Source File:** [monitoring_service.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/monitoring_service.py)
* **Shadow Pipeline:** When a valuation request is routed to an active engine, the alternate engine runs in the background via FastAPI's `BackgroundTasks`:
  - If the router selects CMT, CatBoost ML runs in the background.
  - If the router selects ML, CMT runs in the background.
* **Audit Logs:** The results of both runs are logged to the `shadow_logs` table. This allows the engineering team to monitor price divergence and identify model drift without impacting client request latency.

---

## 4. Learnability & Residual Analysis
* **Verification Script:** [validate_hybrid_dataset.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/scripts/validate_hybrid_dataset.py)
* **Residual Analysis:** The script calculates residuals between actual scraped prices and the deterministic CMT output:
  $$\text{Residual} = P_{\text{actual}} - P_{\text{deterministic}}$$
* **Diagnostic Model:** It splits the hybrid dataset (85% train, 15% test) to train a diagnostic model that predicts these residuals.
* **Validation Results:**
  - Evaluates performance metrics (MAPE, MAE, RMSE, $R^2$) to compare:
    1. **Pure Deterministic CMT:** Bounded by local constraints.
    2. **Diagnostic Hybrid:** Uses CatBoost to predict and adjust for CMT residual errors.
  - Pearson and Spearman correlation coefficients are evaluated against `confidence_score` and `abs_residual` to confirm that the confidence score correlates with low valuation errors.
