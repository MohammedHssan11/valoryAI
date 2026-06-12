# Phase 1 Task 3 CMT Engine Audit

## Current Valuation Flow

1. `POST /v1/rent/fair-price` resolves the nearest leaf area from request coordinates.
2. Request attributes are passed to comparable selection: coordinates, resolved `area_id`, property type, bedrooms, bathrooms, and target size.
3. Comparable selection tries three SQL tiers in order and stops when a tier reaches the configured threshold.
4. Hard price/size/price-per-sqm guardrails are applied.
5. MAD outlier filtering is applied before weighting.
6. Comparable weights are computed as distance weight * size similarity * recency weight.
7. Fair price is the weighted median. Range is weighted low/high quantiles.
8. Confidence is an additive score from comparable count, selected tier, kept ratio, and price dispersion.
9. Explainability is returned as free-text strings plus the highest-weight top comps.

## Current Tier Behavior

- Tier 1: same `area_id`, exact property type, exact bedrooms, size +/-15%, recent listings.
- Tier 2: radius-only 2 km search, exact property type, exact bedrooms, size +/-20%, recent listings.
- Tier 3: radius-only 5 km search, exact property type, exact bedrooms, size +/-20%, recent listings.

The current engine does not explicitly implement same district, nearby district, city, or governorate fallback.

## Current Weighting Formula

`weight = distance_weight * size_weight * recency_weight`

- Distance: `1 / (1 + dist_m / distance_decay_m)`.
- Size: `max(size_min, 1 - abs(comp_size - target_size) / target_size)`.
- Recency: `1 / (1 + age_days / recency_decay_days)`.

## Current Confidence Methodology

Confidence is a bounded additive score:

- Comparable count bucket.
- Tier score.
- Kept ratio after filtering.
- Dispersion from weighted price range.

## Weaknesses And Inconsistencies

- Tiering is radius-based after tier 1, not hierarchy-based.
- Radius behavior is split across individual tier settings and does not use a single expansion sequence.
- Tier 2 does not apply all SQL guardrails used by tier 3.
- SQL ordering uses distance only, so ties are not fully reproducible.
- Top comparable ordering uses weight only, so ties are not fully reproducible.
- `as_of_utc` defaults to wall-clock time, causing repeated requests to slowly drift as listing ages change.
- Confidence does not directly account for average distance, recency, or feature similarity.
- MAD filtering is price-based instead of price-per-sqm based.
- MAD zero cases can keep obvious anomalies.
- Explanations are free-text only and do not expose structured reason codes.
- Area hierarchy is built and indexed but mostly unused by comparable retrieval.

## Market Realism Concerns

- Radius-only fallback can cross into weakly related markets.
- High comp count can inflate confidence even when comps are far, stale, or geographically weak.
- Bathroom matching is collected but not enforced.
- Missing furnishing, floor, and amenity fields cannot be used without inventing signals.
- No available data supports ML-style explanations; transparency should stay rule-based.
