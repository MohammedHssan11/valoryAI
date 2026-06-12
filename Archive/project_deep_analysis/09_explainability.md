# 09. Explainability Architecture

This document details the explainability and telemetry interfaces of the platform. It explains the confidence scoring parameters, the P20-P80 range check for fairness, SHAP feature drivers, and Jaccard-based amenity overlap scoring.

---

## 1. Multi-Dimensional Confidence Metrics
* **Source File:** [confidence.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/confidence.py)
* **Calculations:** Bounded composite score between $[0.0, 1.0]$. The confidence score combines several factors:
  - **Count Score:** $0.35$ if count $\ge 80$; $0.25$ if $\ge 40$; $0.15$ if $\ge 20$; $0.05$ otherwise.
  - **Tier Score:** Tier 1 (Same Compound) adds $0.25$; Tier 2 adds $0.18$; Tier 3 adds $0.10$; Tier 4 adds $0.06$; Tier 5 adds $0.03$.
  - **Outlier Stability Score:** $\min(0.20, \text{kept\_ratio} - 0.60)$.
  - **Price Dispersion Score:** $0.20$ if dispersion $\le 0.35$; $0.12$ if $\le 0.60$; $0.05$ otherwise. (Where $\text{dispersion} = \frac{P_{80} - P_{20}}{P_{50}}$).
  - **Geographic Distance Quality:** $1.0 - \frac{d_{avg}}{15000}$.
  - **Listing Recency Quality:** $\frac{1.0}{1.0 + \frac{A_{avg}}{60.0}}$.
  - **Composite Formula:**
    $$S_{\text{evidence}} = 0.84 \cdot S_{\text{base}} + 0.05 \cdot Q_{\text{distance}} + 0.05 \cdot Q_{\text{recency}} + 0.06 \cdot s_{\text{similarity}}$$
  - **Unified Confidence Score:**
    $$Score_{\text{unified}} = \min \left( S_{\text{evidence}}, S_{\text{location}} \right)$$
    Capped at $0.50$ if address resolution is ambiguous or if the containment boundary distance is greater than 2500m.

---

## 2. Fairness Analysis (Asking Price Auditing)
* **Source Files:** [router_service.py:56-78](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/router_service.py#L56-L78) & [copilot_tools_service.py:571-626](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/copilot_tools_service.py#L571-L626)

When a target asking price is supplied in a request, the system evaluates it against the resolved price range boundaries ($P_{20}$ and $P_{80}$):
1. **Below Fair Value:** Target price $P_{\text{target}} < P_{20}$. (Indicates a strong buying opportunity).
2. **Within Fair Value:** Target price falls inside the price range:
   $$P_{20} \le P_{\text{target}} \le P_{80}$$
3. **Above Fair Value:** Target price $P_{\text{target}} > P_{80}$. (Indicates the property is overpriced).

* **Business Value:** Provides real-time guidance to buyers and sellers on negotiation leverage.

---

## 3. Machine Learning SHAP Drivers
* **Source File:** [ml_service.py:123-160](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/ml_service.py#L123-L160)

When CatBoost executes a prediction, the service extracts SHAP (SHapley Additive exPlanations) values to identify the primary pricing drivers:
- **Positive Drivers:** Top 3 features with SHAP values $>0$.
- **Negative Drivers:** Top 3 features with SHAP values $<0$.
- **Log-space to EGP conversion:** For each feature, the log-space impact is converted to EGP:
  $$\text{Impact}_{\text{EGP}} = \text{Price}_{\text{estimated}} \cdot \left( e^{\text{SHAP}_i} - 1 \right)$$
- **Impact Percentage:** Calculated as $(e^{\text{SHAP}_i} - 1) \cdot 100$.

---

## 4. Jaccard-Weighted Amenity Similarity
* **Source File:** [amenities.py:243-297](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/amenities.py#L243-L297)

The overlap of property amenities is evaluated using a weighted Jaccard index:
$$s_{\text{amenities}} = \frac{\sum_{i \in T \cap C} w_i}{\sum_{j \in T \cup C} w_j}$$
* **Amenity Weights:** Amenity weights are category-specific:
  - Private Pool (`PP`) weight: $0.07$ for villas, $0.01$ for commercial offices.
  - Central A/C (`AC`) weight: $0.03$ for apartments, $0.06$ for offices.
  - Covered Parking (`CP`) weight: $0.05$ across all residential properties.
* **Interpretation:** Standard Jaccard scores treat all features equally. By applying category-specific weights, the index ensures major features (like pools or gardens) affect the similarity score more than secondary features.

---

## 5. Narrative Explanation Payload
* **Source File:** [explain.py:136-167](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/explain.py#L136-L167)
* **Function:** `build_explanation`

Generates human-readable explanations of the valuation steps:
- Confirms how input coordinates were resolved.
- Lists the selected administrative boundary and search tier.
- Discloses the number of comps removed by hard guardrails and MAD filtering.
- Summarizes average distance, listing age, and amenity overlap.
- These explanations are parsed by the Response Composer to feed natural language responses.
