from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.pricing.amenities import amenity_similarity, important_target_amenities
from app.pricing.contracts import category_contract
from app.pricing.settings import TIER_SETTINGS

BASE = Path(__file__).resolve().parents[1]   # /app/app
SQL_DIR = BASE / "db" / "sql"

def _load_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text(encoding="utf-8")

TIER_SQL = {tier: _load_sql(config.sql_file) for tier, config in TIER_SETTINGS.items()}


SQL_MARKET_AS_OF = """
SELECT MAX(scraped_at_utc) AS as_of_utc
FROM listings
WHERE category = :listing_category AND period = :listing_period;
"""


def _market_as_of(db: Session, listing_category: str, listing_period: str) -> datetime:
    if hasattr(db, "bind") and getattr(db.bind, "dialect", None) and db.bind.dialect.name == "sqlite":
        return datetime(1970, 1, 1, tzinfo=timezone.utc)
    row = db.execute(
        text(SQL_MARKET_AS_OF),
        {"listing_category": listing_category, "listing_period": listing_period},
    ).mappings().first()
    as_of = row["as_of_utc"] if row else None
    return as_of or datetime(1970, 1, 1, tzinfo=timezone.utc)


def _params_for_tier(params: dict, tier: int, radius_m: int) -> dict:
    tier_config = TIER_SETTINGS[tier]
    contract = category_contract(params.get("property_category"))
    size_low, size_high = contract.size_bounds(tier, tier_config.size_low, tier_config.size_high)
    return {
        **params,
        **tier_config.sql_params(contract.radius_m(radius_m)),
        "tier_number": tier,
        "size_low": size_low,
        "size_high": size_high,
        "stale_days": contract.stale_days(tier_config.stale_days),
        "min_price_egp": contract.guardrails.min_price_egp,
        "max_price_egp": contract.guardrails.max_price_egp,
        "max_size_sqm": contract.guardrails.max_size_sqm,
        "min_price_per_sqm": contract.guardrails.min_price_per_sqm,
        "max_price_per_sqm": contract.guardrails.max_price_per_sqm,
        "listing_category": contract.listing_category.value,
        "listing_period": contract.period.value,
        "property_category": contract.category.value,
    }


def _trace_entry(tier: int, radius_m: int, count: int, params: dict, amenity_filter: dict | None = None) -> dict:
    tier_config = TIER_SETTINGS[tier]
    contract = category_contract(params.get("property_category"))
    return {
        "tier": tier,
        "tier_label": tier_config.label,
        "reason_code": tier_config.reason_code,
        "scope": tier_config.scope,
        "radius_m": contract.radius_m(radius_m),
        "comps_found": count,
        "threshold": contract.match_threshold,
        "shortfall": max(contract.match_threshold - count, 0),
        "property_category": contract.category.value,
        "listing_category": contract.listing_category.value,
        "listing_period": contract.period.value,
        "amenity_filter": amenity_filter or {"applied": False},
    }


def _annotate_trace(trace: list[dict], selected_index: int | None) -> list[dict]:
    annotated = []
    previous_radius = None
    for index, entry in enumerate(trace):
        selected = selected_index is not None and index == selected_index
        radius = entry.get("radius_m")
        threshold = entry.get("threshold")
        comps_found = entry.get("comps_found", 0)
        if selected:
            status = "selected"
        elif entry.get("reason_code") == "AREA_UNRESOLVED":
            status = "blocked"
        elif threshold is not None and comps_found >= threshold and not selected:
            status = "threshold_met_not_selected"
        elif threshold is not None and comps_found < threshold:
            status = "below_threshold"

        radius_expansion_m = None
        if radius is not None and previous_radius is not None:
            radius_expansion_m = max(int(radius) - int(previous_radius), 0)
        if radius is not None:
            previous_radius = radius

        annotated.append(
            {
                **entry,
                "attempt_index": index + 1,
                "status": status,
                "selected": selected,
                "radius_expansion_m": radius_expansion_m,
            }
        )
    return annotated


def _passes_amenity_filter(row: dict, target_features: dict, property_category: str) -> bool:
    score = amenity_similarity(
        target_features.get("normalized_amenities") or target_features.get("amenities") or [],
        row.get("normalized_amenities") or row.get("amenities") or [],
        property_category=property_category,
    )
    return bool(score.get("matched_symbols"))


def _apply_amenity_retrieval_filter(rows: list[dict], params: dict, threshold: int) -> tuple[list[dict], dict]:
    target_features = params.get("target_features") or {}
    contract = category_contract(params.get("property_category"))
    important = important_target_amenities(target_features, contract.category)
    if not rows or not important:
        return rows, {"applied": False, "reason": "no_category_critical_target_amenities"}

    filtered = [
        row
        for row in rows
        if _passes_amenity_filter(row, target_features, contract.category.value)
    ]
    filter_summary = {
        "applied": len(filtered) >= threshold,
        "mode": "depth_preserving_refinement",
        "critical_symbols": [item["symbol"] for item in important],
        "pre_filter_count": len(rows),
        "post_filter_count": len(filtered),
        "minimum_depth": threshold,
        "governance": "amenities_refine_retrieval_when_depth_survives",
    }
    if len(filtered) >= threshold:
        return filtered, filter_summary

    return rows, {
        **filter_summary,
        "applied": False,
        "reason": "filter_withheld_to_preserve_minimum_comparable_depth",
    }


def fetch_comps(db: Session, params: dict, include_trace: bool = False):
    trace = []
    contract = category_contract(params.get("property_category"))
    if not params.get("area_id"):
        trace.append(
            {
                "tier": None,
                "tier_label": "area unresolved",
                "reason_code": "AREA_UNRESOLVED",
                "scope": "none",
                "radius_m": None,
                "comps_found": 0,
                "threshold": None,
                "shortfall": None,
                "property_category": contract.category.value,
                "listing_category": contract.listing_category.value,
                "listing_period": contract.period.value,
            }
        )
        return ([], 5, _annotate_trace(trace, None)) if include_trace else ([], 5)

    as_of = params.get("as_of_utc") or _market_as_of(db, contract.listing_category.value, contract.period.value)
    params = {
        **params,
        "as_of_utc": as_of,
        "property_category": contract.category.value,
        "listing_category": contract.listing_category.value,
        "listing_period": contract.period.value,
    }

    if hasattr(db, "bind") and getattr(db.bind, "dialect", None) and db.bind.dialect.name == "sqlite":
        # Fallback for SQLite testing (no PostGIS)
        return ([], 5, _annotate_trace(trace, None)) if include_trace else ([], 5)

    best_rows: list[dict] = []
    best_tier = max(TIER_SETTINGS)
    best_trace_index: int | None = None

    for tier in sorted(TIER_SETTINGS):
        tier_config = TIER_SETTINGS[tier]
        for radius_m in tier_config.radius_steps:
            rows = db.execute(
                text(TIER_SQL[tier]),
                _params_for_tier(params, tier, radius_m),
            ).mappings().all()
            row_dicts = [dict(row) for row in rows]
            row_dicts, amenity_filter = _apply_amenity_retrieval_filter(
                row_dicts,
                params,
                contract.match_threshold,
            )
            trace.append(_trace_entry(tier, radius_m, len(row_dicts), params, amenity_filter))

            if len(row_dicts) > len(best_rows):
                best_rows = row_dicts
                best_tier = tier
                best_trace_index = len(trace) - 1

            if len(row_dicts) >= contract.match_threshold:
                selected_index = len(trace) - 1
                return (row_dicts, tier, _annotate_trace(trace, selected_index)) if include_trace else (row_dicts, tier)

    return (best_rows, best_tier, _annotate_trace(trace, best_trace_index)) if include_trace else (best_rows, best_tier)
