# 18. Graduation Presentation Outline

This document presents the slide-by-slide graduation project presentation structure, slide contents, talking points, visual layouts, and demo sequences.

---

## Slide 1: Cover Slide
* **Visual:** Dark theme UI, glowing spatial map of Cairo, project logo ("ValorAI").
* **Slide Title:** ValorAI: Explainable Real Estate Intelligence
* **Subtitle:** A Hybrid Automated Valuation Model & Governed Conversational Co-pilot for Egypt.
* **Presenter Info:** Student Name, Department, Academic Year 2025/2026.
* **Talking Points:**
  - Introduce the core vision of ValorAI: addressing opaqueness and data fragmentation in the Egyptian real estate market.
  - State the key contribution: fusing PostGIS, machine learning, and governed conversational AI.

---

## Slide 2: The Problem Space
* **Visual:** A split slide: Left side showing portal listing duplicates and price spikes (e.g. 1 EGP placeholder listings); Right side showing a diagram of manual appraiser pipelines.
* **Talking Points:**
  - Real estate in Egypt is highly unstructured; online listings are filled with duplicate entries and placeholder prices.
  - Appraisals take days and lack transparent mathematical validation.
  - Generative AI tools (LLMs) cannot solve this on their own: they frequently make math errors and hallucinate prices.

---

## Slide 3: Ingestion & Scraping Pipeline
* **Visual:** Flowchart showing: Raw SSR HTML $\rightarrow$ `__NEXT_DATA__` JSON extraction $\rightarrow$ parser data structures.
* **Talking Points:**
  - We built a crawler that parses JSON data blocks from PropertyFinder Egypt's search pages.
  - Show how the parser maps listing configurations to standard fields (price, size, rooms, location).
  - Highlight the clean loop rules: pruning placeholders ($P \le 100$ EGP), filtering Egypt bounding box coordinates, and normalizing studio room counts.

---

## Slide 4: Database & PostGIS Spatial Hierarchies
* **Visual:** Database ERD diagram illustrating the recursive relationship in the `areas` table and spatial indices (`ix_listings_geom_gist`).
* **Talking Points:**
  - To support spatial containment checks, we integrated PostGIS.
  - Explain the 4-level administrative boundary hierarchy: Governorate $\rightarrow$ City $\rightarrow$ District $\rightarrow$ Neighborhood/Compound.
  - Highlight the unique index `ux_areas_parent_level_name` that prevents duplicate labels within the same branch.

---

## Slide 5: The Comparable Market Technique (CMT)
* **Visual:** Workflow of the CMT pipeline: Retrieval $\rightarrow$ Guardrails $\rightarrow$ MAD filtering $\rightarrow$ Weighted median.
* **Talking Points:**
  - Detail how we retrieve candidate listings recursively along administrative boundary tiers.
  - Explain the weight decay formulas for distance, size, age, and features similarities.
  - Highlight the weighted quantile picker that calculates the fair price (P50) and price range bounds (P20, P80).

---

## Slide 6: Outlier Filtering via MAD
* **Visual:** Comparison chart: Left showing standard Z-score sensitivity to outliers; Right showing MAD stability.
* **Talking Points:**
  - Explain why we use the Median Absolute Deviation (MAD) for outlier pruning.
  - Detail the Modified Z-score formula:
    $$MZ_i = 0.6745 \cdot \frac{x_i - \tilde{x}}{\text{MAD}}$$
  - Discuss the failsafe check: if MAD is 0, the engine falls back to a tolerance filter, keeping listings within $\pm 5\%$ of the median.

---

## Slide 7: Machine Learning Regression (CatBoost)
* **Visual:** Features ingestion matrix and SHAP explainability chart.
* **Talking Points:**
  - Explain why we trained CatBoost models: to interpolate pricing in cold-start or low-density regions.
  - Detail target log-transformations: $y = \ln(price + 1)$ and inversion: $price = e^y - 1$ to stabilize variance.
  - Show how SHAP values are extracted during inference to identify positive and negative drivers.

---

## Slide 8: The Hybrid Routing Layer
* **Visual:** Goldilocks routing decision tree.
* **Talking Points:**
  - Discuss the failures of legacy fallbacks (V1 and V2).
  - Explain the active routing rules: routing requests to CMT when comparable density is in the "Goldilocks Zone" ($11 \le comps \le 50$) or if the geography is unseen.
  - Highlight the background shadow pipeline that evaluates alternate models to monitor drift.

---

## Slide 9: Conversational Co-pilot & Orchestrator
* **Visual:** Orchestrator data flow diagram: Input $\rightarrow$ Intent $\rightarrow$ Planner $\rightarrow$ Executor $\rightarrow$ Composer $\rightarrow$ LLM.
* **Talking Points:**
  - Detail the RuleBasedIntentEngine and tool execution boundaries.
  - Explain the Response Composer's role: computing deltas and aggregating stats in Python, and truncating prompt context.
  - Highlight the Narration Admission Gate that validates claims and requires citation tokens, falling back to a JSON payload if checks fail.

---

## Slide 10: Live Demo Cues & Conclusion
* **Visual:** Screenshot of the Flutter mobile client interface.
* **Talking Points:**
  - Demo 1: Direct property valuation showing confidence, price bands, and comparable evidence.
  - Demo 2: Conversational co-pilot running a what-if simulation (e.g. adding covered parking) and generating broker talking points.
  - Conclude: ValorAI brings transparency, speed, and trust to real estate markets.
