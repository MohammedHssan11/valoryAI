from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import requests
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.geo.normalization import canonical_location_key
from app.geo.spatial_authority import (
    confidence_for_entity,
    entity_metadata,
    get_entity_by_id,
    match_hierarchical_entities,
    precision_for_entity,
)

logger = logging.getLogger(__name__)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ResolvedLocation(BaseModel):
    lat: float
    lng: float
    precision_level: str
    matched_name: Optional[str] = None
    source: str
    normalized_input: str = ""
    matched_entity: Optional[dict[str, Any]] = None
    confidence: float = Field(default=0.0, ge=0, le=1)
    ambiguity_status: str = "UNAMBIGUOUS"
    resolver_version: str = settings.ADDRESS_RESOLVER_VERSION
    cache_hit: bool = False
    resolution_strategy: str
    area_distance_m: Optional[float] = None
    timestamp: str = Field(default_factory=_utc_now_iso)
    source_metadata: dict[str, Any] = Field(default_factory=dict)


SQL_CHECK_CACHE = """
SELECT
  raw_input,
  normalized_input,
  matched_name,
  lat,
  lng,
  precision_level,
  source,
  confidence,
  ambiguity_status,
  resolver_version,
  resolution_strategy,
  area_distance_m,
  matched_entity,
  source_metadata,
  created_at_utc
FROM address_resolution_cache
WHERE normalized_input = :normalized_input
  AND resolver_version = :resolver_version
  AND invalidated_at_utc IS NULL
  AND (expires_at_utc IS NULL OR expires_at_utc > NOW())
ORDER BY created_at_utc DESC, id ASC
LIMIT 1;
"""

SQL_INSERT_CACHE = """
INSERT INTO address_resolution_cache (
  raw_input,
  normalized_input,
  matched_name,
  lat,
  lng,
  precision_level,
  source,
  confidence,
  ambiguity_status,
  resolver_version,
  resolution_strategy,
  area_distance_m,
  matched_entity,
  source_metadata,
  expires_at_utc
)
VALUES (
  :raw_input,
  :normalized_input,
  :matched_name,
  :lat,
  :lng,
  :precision_level,
  :source,
  :confidence,
  :ambiguity_status,
  :resolver_version,
  :resolution_strategy,
  :area_distance_m,
  CAST(:matched_entity AS jsonb),
  CAST(:source_metadata AS jsonb),
  :expires_at_utc
)
ON CONFLICT (normalized_input, resolver_version) DO UPDATE
SET
  raw_input = EXCLUDED.raw_input,
  matched_name = EXCLUDED.matched_name,
  lat = EXCLUDED.lat,
  lng = EXCLUDED.lng,
  precision_level = EXCLUDED.precision_level,
  source = EXCLUDED.source,
  confidence = EXCLUDED.confidence,
  ambiguity_status = EXCLUDED.ambiguity_status,
  resolution_strategy = EXCLUDED.resolution_strategy,
  area_distance_m = EXCLUDED.area_distance_m,
  matched_entity = EXCLUDED.matched_entity,
  source_metadata = EXCLUDED.source_metadata,
  expires_at_utc = EXCLUDED.expires_at_utc,
  invalidated_at_utc = NULL,
  updated_at_utc = NOW()
WHERE address_resolution_cache.invalidated_at_utc IS NOT NULL
   OR address_resolution_cache.expires_at_utc < NOW();
"""

SQL_MATCH_AREA_BY_NAME = """
SELECT name, ST_Y(center_geom::geometry) as lat, ST_X(center_geom::geometry) as lng, level
FROM areas
WHERE lower(name) = lower(:raw_input)
ORDER BY level DESC, area_id ASC
LIMIT 2;
"""


def _json_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return decoded if isinstance(decoded, dict) else {}
    return {}


def _cache_row_to_location(row: dict[str, Any]) -> ResolvedLocation:
    return ResolvedLocation(
        lat=float(row["lat"]),
        lng=float(row["lng"]),
        precision_level=row["precision_level"],
        matched_name=row.get("matched_name"),
        source=row["source"],
        normalized_input=row.get("normalized_input") or "",
        matched_entity=_json_dict(row.get("matched_entity")) or None,
        confidence=float(row.get("confidence") or 0.0),
        ambiguity_status=row.get("ambiguity_status") or "UNAMBIGUOUS",
        resolver_version=row.get("resolver_version") or settings.ADDRESS_RESOLVER_VERSION,
        cache_hit=True,
        resolution_strategy=row.get("resolution_strategy") or "CACHE",
        area_distance_m=row.get("area_distance_m"),
        timestamp=_utc_now_iso(),
        source_metadata=_json_dict(row.get("source_metadata")),
    )


def _location_from_entity(raw_input: str, normalized_input: str, entity: dict[str, Any], metadata: dict[str, Any] | None = None) -> ResolvedLocation:
    meta = metadata or {}
    source_meta = {"raw_input": raw_input}
    source_meta.update(meta)
    strategy = meta.get("resolution_strategy", "CANONICAL_ALIAS_MATCH")
    return ResolvedLocation(
        lat=float(entity["centroid_lat"]),
        lng=float(entity["centroid_lng"]),
        precision_level=precision_for_entity(entity),
        matched_name=entity.get("canonical_name"),
        source="CANONICAL_ENTITY",
        normalized_input=normalized_input,
        matched_entity=entity_metadata(entity),
        confidence=confidence_for_entity(entity),
        ambiguity_status="UNAMBIGUOUS",
        resolver_version=settings.ADDRESS_RESOLVER_VERSION,
        cache_hit=False,
        resolution_strategy=strategy,
        source_metadata=source_meta,
    )


def resolve_address(db: Session, address: str) -> ResolvedLocation:
    normalized_input = canonical_location_key(address)
    if not normalized_input:
        raise ValueError("Could not resolve empty address input")

    cache_row = db.execute(
        text(SQL_CHECK_CACHE),
        {
            "normalized_input": normalized_input,
            "resolver_version": settings.ADDRESS_RESOLVER_VERSION,
        },
    ).mappings().first()
    if cache_row:
        logger.info("address_cache_hit", extra={"normalized_input": normalized_input})
        return _cache_row_to_location(dict(cache_row))

    entity, status, metadata = match_hierarchical_entities(db, address)
    if status == "AMBIGUOUS_ALIAS":
        raise ValueError(f"Ambiguous address alias: {address}")
    if status == "HIERARCHY_CONFLICT":
        raise ValueError(f"Ambiguous address alias: conflicting hierarchy in {address}")
    if entity:
        loc = _location_from_entity(address, normalized_input, entity, metadata)
        _cache_location(db, address, loc)
        return loc

    area_rows = [
        dict(row)
        for row in db.execute(text(SQL_MATCH_AREA_BY_NAME), {"raw_input": address}).mappings().all()
    ]
    if len(area_rows) > 1 and area_rows[0]["level"] == area_rows[1]["level"]:
        raise ValueError(f"Ambiguous area name: {address}")
    if area_rows:
        area_row = area_rows[0]
        precision = "DISTRICT" if area_row["level"] >= 3 else "CITY"
        confidence = 0.65 if precision == "DISTRICT" else 0.45
        loc = ResolvedLocation(
            lat=float(area_row["lat"]),
            lng=float(area_row["lng"]),
            precision_level=precision,
            matched_name=area_row["name"],
            source="AREA_NAME_MATCH",
            normalized_input=normalized_input,
            confidence=confidence,
            ambiguity_status="UNAMBIGUOUS",
            resolver_version=settings.ADDRESS_RESOLVER_VERSION,
            cache_hit=False,
            resolution_strategy="AREA_NAME_EXACT_MATCH",
        )
        _cache_location(db, address, loc)
        return loc

    loc = _geocode_google_maps(address, normalized_input)
    if loc:
        _cache_location(db, address, loc)
        return loc

    raise ValueError(f"Could not resolve address: {address}")


def resolve_canonical_entity(db: Session, entity_id: str) -> ResolvedLocation:
    entity = get_entity_by_id(db, entity_id)
    if not entity:
        raise ValueError(f"Could not resolve canonical entity: {entity_id}")
    normalized_input = str(entity.get("normalized_name") or entity_id)
    loc = _location_from_entity(entity_id, normalized_input, entity, {"resolution_strategy": "CANONICAL_ENTITY_ID"})
    return loc


def _google_precision_and_confidence(result: dict[str, Any]) -> tuple[str, float]:
    loc_type = result.get("geometry", {}).get("location_type", "")
    types = result.get("types", [])

    if loc_type == "ROOFTOP" or "premise" in types or "subpremise" in types:
        return "ROOFTOP", 0.72
    if "neighborhood" in types or "sublocality" in types:
        return "DISTRICT", 0.58
    if "locality" in types or "administrative_area_level_2" in types:
        return "CITY", 0.40
    if "administrative_area_level_1" in types:
        return "CITY", 0.32
    return "DISTRICT", 0.45


def _geocode_google_maps(address: str, normalized_input: str | None = None) -> Optional[ResolvedLocation]:
    api_key = getattr(settings, "GOOGLE_MAPS_API_KEY", None)
    if not api_key:
        logger.warning("GOOGLE_MAPS_API_KEY is not set. L3 Geocoding skipped.")
        return None

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key,
        "components": "country:EG",
    }

    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results") or []
        if data.get("status") == "OK" and len(results) == 1:
            result = results[0]
            if result.get("partial_match") is True:
                logger.warning("Google Maps partial match rejected", extra={"address": address})
                return None

            lat = result["geometry"]["location"]["lat"]
            lng = result["geometry"]["location"]["lng"]
            if not (22 <= float(lat) <= 32 and 24 <= float(lng) <= 37):
                logger.warning("Google Maps result outside Egypt bounds", extra={"address": address})
                return None

            precision_level, confidence = _google_precision_and_confidence(result)
            return ResolvedLocation(
                lat=lat,
                lng=lng,
                precision_level=precision_level,
                matched_name=result.get("formatted_address"),
                source="GOOGLE_MAPS",
                normalized_input=normalized_input or canonical_location_key(address),
                confidence=confidence,
                ambiguity_status="UNAMBIGUOUS",
                resolver_version=settings.ADDRESS_RESOLVER_VERSION,
                cache_hit=False,
                resolution_strategy="EXTERNAL_GEOCODER_SINGLE_RESULT",
                source_metadata={
                    "place_id": result.get("place_id"),
                    "location_type": result.get("geometry", {}).get("location_type"),
                    "types": result.get("types", []),
                    "result_count": len(results),
                },
            )
        if data.get("status") == "OK" and len(results) > 1:
            logger.warning("Google Maps ambiguous result rejected", extra={"address": address, "result_count": len(results)})
        else:
            logger.warning("Google Maps API failed to resolve address", extra={"address": address, "status": data.get("status")})
    except Exception as e:
        logger.error("Error calling Google Maps API", extra={"error": str(e)})

    return None


def _cache_expiry_for_source(source: str) -> datetime | None:
    if source == "GOOGLE_MAPS":
        return datetime.now(timezone.utc) + timedelta(days=settings.ADDRESS_CACHE_EXTERNAL_TTL_DAYS)
    return None


def _cache_location(db: Session, address: str, loc: ResolvedLocation):
    try:
        db.execute(
            text(SQL_INSERT_CACHE),
            {
                "raw_input": address,
                "normalized_input": loc.normalized_input,
                "matched_name": loc.matched_name,
                "lat": loc.lat,
                "lng": loc.lng,
                "precision_level": loc.precision_level,
                "source": loc.source,
                "confidence": loc.confidence,
                "ambiguity_status": loc.ambiguity_status,
                "resolver_version": loc.resolver_version,
                "resolution_strategy": loc.resolution_strategy,
                "area_distance_m": loc.area_distance_m,
                "matched_entity": json.dumps(loc.matched_entity or {}, sort_keys=True),
                "source_metadata": json.dumps(loc.source_metadata or {}, sort_keys=True),
                "expires_at_utc": _cache_expiry_for_source(loc.source),
            },
        )
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error("Failed to cache address resolution", extra={"address": address, "error": str(e)})
