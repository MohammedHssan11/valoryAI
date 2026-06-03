# 06. Machine Learning Analysis (CatBoost Engine)

This document presents the technical analysis of the Machine Learning (ML) valuation engine, detailing the integration of the CatBoost regressor, target transformations, feature mapping schemas, and SHAP explainability.

---

## 1. Why ML Was Introduced
While the deterministic Comparable Market Technique (CMT) engine is highly accurate in high-density areas, it has limitations in sparse or newly developed regions:
* **Cold-Start Areas:** Newly established compounds (e.g. in East Cairo or new phases of Sheikh Zayed) lack a sufficient density of historical listing comparables.
* **Geographical Contraction:** CMT requires matching parameters (size, bedrooms) within tight bounds. If a property is unique, CMT fails and returns `INSUFFICIENT_DATA`.
* **Data Sparsity:** Walk-out radius fallbacks can expand up to 15km, but at that distance, spatial boundaries are lost.

To solve this, the **CatBoost Regression** pipeline was introduced. It does not replace CMT; rather, it acts as an interpolation engine that analyzes wider regional price signals, coordinate trends, and property features to estimate a baseline price in cold-start regions.

---

## 2. Models & Feature Ingestion Schemas
The platform uses two pre-trained binary models loaded at startup:
* **Rent Model:** `residential_rent.cbm` (1.3MB)
* **Sale Model:** `residential_sale.cbm` (2.2MB)
* **Schemas:** Mapped via JSON configurations (`residential_rent_schema.json`, `residential_sale_schema.json`) to enforce features count and ordering.

### Ingestion Features
Features are grouped into three categories:

#### 1. Core Numerical features
* `latitude`, `longitude`: Raw geographic coordinates.
* `bedrooms`, `bathrooms`: Room counts.
* `size`: Total area in square meters.
* `listing_age_days`: Time delta.

#### 2. Categorical features
* `property_type`: Normalized string (e.g. `'Apartment'`, `'Duplex'`).
* `compound_name`: Target compound (if known).
* `h3_res8`, `h3_res9`: Uber H3 grid hexagonal cell indices.

#### 3. Boolean / Heuristic Flags
* `is_known_compound`: Set to `1` if the compound exists in the location registry.
* `is_furnished`, `semi_furnished`: Furnishing status flags.
* `amenities_count`: Total number of amenities.
* `has_amenity_ac`, `has_amenity_ba`, `has_amenity_se`, `has_amenity_sp`, `has_amenity_bk`, `has_amenity_cp`: Flags for specific amenities (AC, Balcony, Security, Pool, Kitchen, Parking).
* `has_garden`: Garden flag.

---

## 3. Mathematical Target Transformations
Real estate listing prices are highly skewed and span multiple orders of magnitude (e.g., from small studios to luxury villas). Directly predicting price can cause regressors to over-index on high-priced listings, resulting in high variance and unstable predictions.

To solve this, the target price $Y$ is log-transformed during training:
$$y = \ln(Y + 1)$$
This stabilizes variance and ensures errors are evaluated as percentage deviations rather than absolute values.

During inference, the predicted log-price is inverted back to EGP:
$$\text{Fair Price}_{\text{EGP}} = e^{\hat{y}} - 1$$
* **Original Code:**
  ```python
  # ml_service.py:120-121
  pred_log = model.predict(df)[0]
  fair = int(np.expm1(pred_log))
  ```

---

## 4. SHAP Explainability & Feature Drivers
* **Source File:** [ml_service.py:123-160](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/ml_service.py#L123-L160)

Since machine learning models are often seen as "black boxes", the platform extracts SHAP (SHapley Additive exPlanations) values to explain individual predictions.

```
Log-space Prediction (ŷ) = Base Value (E[f(x)]) + Σ SHAP_i
  │
  ├── For each feature, extract SHAP value
  │
  ├── Categorize into:
  │     ├── Positive Drivers (SHAP > 0)
  │     └── Negative Drivers (SHAP < 0)
  │
  ├── Sort drivers to find top 3 positive and negative features
  │
  └── Translate log-space impact to approximate EGP impact:
        Impact_EGP = Fair Price * (e^(SHAP_i) - 1)
```

### Interpretation
* **Positive Drivers:** Features that increased the property's estimated value (e.g., being located in a premium compound or having covered parking).
* **Negative Drivers:** Features that decreased the property's estimated value (e.g., being located on a low floor or in an unindexed H3 cell).
* **Narrative Integration:** These drivers are returned in the explainability payload (`explainability.feature_drivers`), ensuring the co-pilot can explain ML valuations in natural language.
