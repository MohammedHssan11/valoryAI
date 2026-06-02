from __future__ import annotations

from dataclasses import dataclass

from app.core.config import settings


@dataclass(frozen=True)
class TierSettings:
    sql_file: str
    scope: str
    label: str
    reason_code: str
    radius_steps: tuple[int, ...]
    size_low: float
    size_high: float
    stale_days: int
    limit: int
    match_threshold: int

    def sql_params(self, radius_m: int) -> dict:
        return {
            "scope": self.scope,
            "tier": self.reason_code,
            "tier_label": self.label,
            "radius_m": radius_m,
            "size_low": self.size_low,
            "size_high": self.size_high,
            "stale_days": self.stale_days,
            "limit": min(self.limit, settings.MAX_COMPS_RETURN),
        }


@dataclass(frozen=True)
class GuardrailSettings:
    min_price_egp: int
    max_price_egp: int
    max_size_sqm: float
    min_price_per_sqm: float
    max_price_per_sqm: float


@dataclass(frozen=True)
class MadSettings:
    z_threshold: float
    min_sample_size: int
    modified_z_scale: float
    zero_tolerance_ratio: float


@dataclass(frozen=True)
class WeightingSettings:
    distance_fallback: float
    distance_decay_m: float
    size_fallback: float
    size_min: float
    recency_fallback: float
    recency_decay_days: float
    bathroom_fallback: float
    bathroom_mismatch: float
    non_same_area: float
    feature_max_delta: float


@dataclass(frozen=True)
class ConfidenceSettings:
    high_threshold: float
    medium_threshold: float
    count_high: int
    count_medium: int
    count_low: int
    count_high_score: float
    count_medium_score: float
    count_low_score: float
    count_fallback_score: float
    tier_scores: dict[int, float]
    kept_ratio_baseline: float
    kept_ratio_max_score: float
    dispersion_low: float
    dispersion_medium: float
    dispersion_low_score: float
    dispersion_medium_score: float
    dispersion_fallback_score: float


RADIUS_STEPS_M = tuple(settings.RADIUS_EXPANSION_STEPS_M)

TIER_SETTINGS = {
    1: TierSettings(
        sql_file="tier_comps.sql",
        scope="same_area",
        label="same compound/neighborhood",
        reason_code="SAME_AREA_MATCH",
        radius_steps=(RADIUS_STEPS_M[0], RADIUS_STEPS_M[1]),
        size_low=settings.TIER1_SIZE_LOW,
        size_high=settings.TIER1_SIZE_HIGH,
        stale_days=settings.TIER1_STALE_DAYS,
        limit=settings.TIER1_LIMIT,
        match_threshold=settings.TIER_MATCH_THRESHOLD,
    ),
    2: TierSettings(
        sql_file="tier_comps.sql",
        scope="same_district",
        label="same district",
        reason_code="SAME_DISTRICT_MATCH",
        radius_steps=(RADIUS_STEPS_M[2],),
        size_low=settings.TIER2_SIZE_LOW,
        size_high=settings.TIER2_SIZE_HIGH,
        stale_days=settings.TIER2_STALE_DAYS,
        limit=settings.TIER2_LIMIT,
        match_threshold=settings.TIER_MATCH_THRESHOLD,
    ),
    3: TierSettings(
        sql_file="tier_comps.sql",
        scope="nearby_districts",
        label="nearby districts",
        reason_code="NEARBY_DISTRICT_MATCH",
        radius_steps=(RADIUS_STEPS_M[3],),
        size_low=settings.TIER3_SIZE_LOW,
        size_high=settings.TIER3_SIZE_HIGH,
        stale_days=settings.TIER3_STALE_DAYS,
        limit=settings.TIER3_LIMIT,
        match_threshold=settings.TIER_MATCH_THRESHOLD,
    ),
    4: TierSettings(
        sql_file="tier_comps.sql",
        scope="same_city",
        label="same city",
        reason_code="SAME_CITY_FALLBACK",
        radius_steps=(RADIUS_STEPS_M[4],),
        size_low=settings.TIER4_SIZE_LOW,
        size_high=settings.TIER4_SIZE_HIGH,
        stale_days=settings.TIER4_STALE_DAYS,
        limit=settings.TIER4_LIMIT,
        match_threshold=settings.TIER_MATCH_THRESHOLD,
    ),
    5: TierSettings(
        sql_file="tier_comps.sql",
        scope="same_governorate",
        label="same governorate fallback",
        reason_code="GOVERNORATE_FALLBACK",
        radius_steps=(RADIUS_STEPS_M[5],),
        size_low=settings.TIER5_SIZE_LOW,
        size_high=settings.TIER5_SIZE_HIGH,
        stale_days=settings.TIER5_STALE_DAYS,
        limit=settings.TIER5_LIMIT,
        match_threshold=settings.TIER_MATCH_THRESHOLD,
    ),
}

GUARDRAILS = GuardrailSettings(
    min_price_egp=settings.MIN_PRICE_EGP,
    max_price_egp=settings.MAX_PRICE_EGP,
    max_size_sqm=settings.MAX_SIZE_SQM,
    min_price_per_sqm=settings.MIN_PRICE_PER_SQM,
    max_price_per_sqm=settings.MAX_PRICE_PER_SQM,
)

MAD = MadSettings(
    z_threshold=settings.MAD_Z_THRESHOLD,
    min_sample_size=settings.MAD_MIN_SAMPLE_SIZE,
    modified_z_scale=settings.MAD_MODIFIED_Z_SCALE,
    zero_tolerance_ratio=settings.MAD_ZERO_TOLERANCE_RATIO,
)

WEIGHTING = WeightingSettings(
    distance_fallback=settings.DISTANCE_WEIGHT_FALLBACK,
    distance_decay_m=settings.DISTANCE_DECAY_M,
    size_fallback=settings.SIZE_WEIGHT_FALLBACK,
    size_min=settings.SIZE_WEIGHT_MIN,
    recency_fallback=settings.RECENCY_WEIGHT_FALLBACK,
    recency_decay_days=settings.RECENCY_DECAY_DAYS,
    bathroom_fallback=settings.BATHROOM_WEIGHT_FALLBACK,
    bathroom_mismatch=settings.BATHROOM_MISMATCH_WEIGHT,
    non_same_area=settings.NON_SAME_AREA_WEIGHT,
    feature_max_delta=settings.FEATURE_WEIGHT_MAX_DELTA,
)

CONFIDENCE = ConfidenceSettings(
    high_threshold=settings.CONFIDENCE_HIGH_THRESHOLD,
    medium_threshold=settings.CONFIDENCE_MEDIUM_THRESHOLD,
    count_high=settings.CONFIDENCE_COUNT_HIGH,
    count_medium=settings.CONFIDENCE_COUNT_MEDIUM,
    count_low=settings.CONFIDENCE_COUNT_LOW,
    count_high_score=settings.CONFIDENCE_COUNT_HIGH_SCORE,
    count_medium_score=settings.CONFIDENCE_COUNT_MEDIUM_SCORE,
    count_low_score=settings.CONFIDENCE_COUNT_LOW_SCORE,
    count_fallback_score=settings.CONFIDENCE_COUNT_FALLBACK_SCORE,
    tier_scores={
        1: settings.CONFIDENCE_TIER1_SCORE,
        2: settings.CONFIDENCE_TIER2_SCORE,
        3: settings.CONFIDENCE_TIER3_SCORE,
        4: settings.CONFIDENCE_TIER4_SCORE,
        5: settings.CONFIDENCE_TIER5_SCORE,
    },
    kept_ratio_baseline=settings.CONFIDENCE_KEPT_RATIO_BASELINE,
    kept_ratio_max_score=settings.CONFIDENCE_KEPT_RATIO_MAX_SCORE,
    dispersion_low=settings.CONFIDENCE_DISPERSION_LOW,
    dispersion_medium=settings.CONFIDENCE_DISPERSION_MEDIUM,
    dispersion_low_score=settings.CONFIDENCE_DISPERSION_LOW_SCORE,
    dispersion_medium_score=settings.CONFIDENCE_DISPERSION_MEDIUM_SCORE,
    dispersion_fallback_score=settings.CONFIDENCE_DISPERSION_FALLBACK_SCORE,
)

PRICE_RANGE_QUANTILES = (
    settings.PRICE_RANGE_LOW_QUANTILE,
    settings.PRICE_RANGE_HIGH_QUANTILE,
)
