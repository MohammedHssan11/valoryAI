# 15. Technical Q&A (Architectural Defense)

This document compiles anticipated technical questions regarding the platform's architecture, scaling, security, and modeling decisions, along with code-grounded answers.

---

## 1. Modeling & Core Algorithm Questions

### Q1: Why did you choose Median Absolute Deviation (MAD) over standard standard deviation (Z-score) for outlier filtering?
* **Answer:** Z-score assumes a normal distribution and uses the mean and standard deviation to identify outliers. However, the mean and standard deviation are themselves highly sensitive to extreme values. In real estate data, listing errors (e.g. placeholder prices of 1 EGP or duplicate entries) distort the mean.
* **Code Reference:** `mad_filter` in [filters.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/filters.py).
* **Formula:** We calculate the Modified Z-score using MAD:
  $$MZ_i = 0.6745 \cdot \frac{x_i - \tilde{x}}{\text{MAD}}$$
  Since the median and MAD are highly robust statistics, they remain stable even if up to 50% of the dataset consists of outliers.

### Q2: What happens mathematically in your CMT weights estimator if the Median Absolute Deviation (MAD) is zero?
* **Answer:** If all listings in a search tier have the same price, the MAD becomes `0`. This would cause a division by zero in the Modified Z-score calculation.
* **Code Reference:** [filters.py:56-67](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/pricing/filters.py#L56-L67).
* **Failsafe:** The system checks if `mad == 0`. If true, it falls back to a zero-MAD exception filter: it calculates a tolerance interval equal to $\pm 5\%$ of the median and discards any listings whose price falls outside this range, preventing runtime crashes.

### Q3: Why does your ML engine predict log-prices instead of raw EGP values?
* **Answer:** Real estate listing prices span multiple orders of magnitude. Directly predicting price can cause regressors to over-index on high-priced listings, resulting in high variance.
* **Code Reference:** [ml_service.py:120-121](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/services/ml_service.py#L120-L121).
* **Transformations:** We transform the target variable during training using $y = \ln(price + 1)$ and invert the predicted log-price back to EGP during inference using `np.expm1(pred_log)`. This stabilizes variance and ensures errors are evaluated as percentage deviations rather than absolute values.

---

## 2. Geospatial & Database Scaling Questions

### Q4: How does your geofenced search query prevent performance degradation as the listings database grows?
* **Answer:** As the database scales, spatial radius queries (`ST_DWithin`) can slow down.
* **Code Reference:** `tier_comps.sql` [indexes](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/db/sql/init.sql#L100-L113) and [query structure](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/db/sql/tier_comps.sql).
* **Optimization:**
  1. The listings are indexed using GIST indices on both geometry point coordinates (`geom`) and geographical shapes (`geom::geography`).
  2. The SQL query matches parameters in a composite index (`category`, `period`, `property_type`, `bedrooms`, `area_id`), allowing the query planner to quickly narrow down candidates before executing the spatial distance sort (`dist_m ASC`).

### Q5: How do you handle geocoding API limits and latency during listing resolution?
* **Answer:** Calling external geocoding APIs introduces network latency and usage costs.
* **Code Reference:** [address_resolver.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/geo/address_resolver.py).
* **Caching:** We implement a caching layer in the `address_resolution_cache` table. When an address is resolved, the coordinates and area mappings are saved. Subsequent requests for the same address match on a case-insensitive unique index (`lower(raw_input)`), resolving the location instantly in under 5ms.

---

## 3. Co-pilot & LLM Governance Questions

### Q6: How do you prevent the Conversational Co-pilot from hallucinating valuations or calculations?
* **Answer:** The language model has no authority over calculations or data access.
* **Code Reference:** [NARRATION_CONTRACT_ARCHITECTURE.md](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/docs/NARRATION_CONTRACT_ARCHITECTURE.md).
* **Separation of Concerns:**
  - All mathematical operations (averages, price bands, deltas) are executed in Python by the Response Composer before prompt assembly.
  - The LLM is restricted by prompt instructions to narrating the composed facts.
  - If the generated text includes claims that violate grounding checks or lack citation tokens, the Narration Admission Gate rejects the text and defaults to the deterministic JSON payload (`DETERMINISTIC_FALLBACK`).

### Q7: How is tenant isolation enforced in the multi-user workspace state?
* **Answer:** The co-pilot memory tables hold user workspaces, chats, and scenario assumptions.
* **Code Reference:** `DeterministicMemoryIntegration` in [memory/integration.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/memory/integration.py).
* **Isolation:** Every database lookup and update is filtered by the user's workspace context. The user's user ID and workspace ID are extracted from the bearer JWT token, preventing access to foreign tenant data.
