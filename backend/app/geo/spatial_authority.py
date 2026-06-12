from __future__ import annotations

from typing import Any
import re
from math import radians, cos, sin, asin, sqrt

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.geo.normalization import canonical_location_key


SQL_MATCH_ENTITIES_BY_ALIASES = """
SELECT DISTINCT
  e.entity_id,
  e.entity_type,
  e.canonical_name,
  e.normalized_name,
  e.canonical_area_id,
  e.centroid_lat,
  e.centroid_lng,
  e.authority_source,
  e.version,
  a.priority,
  a.normalized_alias,
  ar.level AS area_level
FROM location_aliases a
JOIN location_entities e ON e.entity_id = a.entity_id
LEFT JOIN areas ar ON ar.area_id = e.canonical_area_id
WHERE a.normalized_alias = ANY(:candidate_aliases)
  AND a.active = TRUE
ORDER BY a.priority DESC, e.entity_type ASC, e.entity_id ASC;
"""

SQL_MATCH_ENTITY_BY_ALIAS = """
SELECT DISTINCT
  e.entity_id,
  e.entity_type,
  e.canonical_name,
  e.normalized_name,
  e.canonical_area_id,
  e.centroid_lat,
  e.centroid_lng,
  e.authority_source,
  e.version,
  a.priority,
  ar.level AS area_level
FROM location_aliases a
JOIN location_entities e ON e.entity_id = a.entity_id
LEFT JOIN areas ar ON ar.area_id = e.canonical_area_id
WHERE a.normalized_alias = :normalized_alias
  AND a.active = TRUE
ORDER BY a.priority DESC, e.entity_type ASC, e.entity_id ASC;
"""

SQL_ENTITY_BY_ID = """
SELECT
  e.entity_id,
  e.entity_type,
  e.canonical_name,
  e.normalized_name,
  e.canonical_area_id,
  e.centroid_lat,
  e.centroid_lng,
  e.authority_source,
  e.version,
  ar.level AS area_level
FROM location_entities e
LEFT JOIN areas ar ON ar.area_id = e.canonical_area_id
WHERE e.entity_id = :entity_id;
"""


ENTITY_PRECISION = {
    "compound": "COMPOUND",
    "landmark": "ROOFTOP",
    "neighborhood": "COMPOUND",
    "district": "DISTRICT",
    "city": "CITY",
}

ENTITY_CONFIDENCE = {
    "compound": 0.92,
    "landmark": 0.88,
    "neighborhood": 0.86,
    "district": 0.70,
    "city": 0.50,
}


def _dedupe_entities(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        entity_id = str(row["entity_id"])
        if entity_id in seen:
            continue
        seen.add(entity_id)
        out.append(row)
    return out


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    lon1, lat1, lon2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000 # Radius of earth in meters
    return c * r


def extract_candidate_tokens(raw_input: str) -> set[str]:
    candidates = set()
    
    # Split by explicit delimiters
    parts = re.split(r'[,|/|-]', raw_input)
    for part in parts:
        normalized = canonical_location_key(part)
        if normalized:
            candidates.add(normalized)
            
    full_normalized = canonical_location_key(raw_input)
    if not full_normalized:
        return candidates
        
    candidates.add(full_normalized)
    
    # Generate n-grams (up to 6 words)
    words = full_normalized.split()
    max_len = min(6, len(words))
    for n in range(1, max_len + 1):
        for i in range(len(words) - n + 1):
            ngram = " ".join(words[i:i+n])
            canon_ngram = canonical_location_key(ngram)
            if canon_ngram:
                candidates.add(canon_ngram)
            
    return candidates


def match_hierarchical_entities(db: Session, raw_input: str) -> tuple[dict[str, Any] | None, str, dict[str, Any]]:
    candidates = extract_candidate_tokens(raw_input)
    if not candidates:
        return None, "EMPTY_INPUT", {}

    rows = [
        dict(row)
        for row in db.execute(
            text(SQL_MATCH_ENTITIES_BY_ALIASES),
            {"candidate_aliases": list(candidates)},
        ).mappings().all()
    ]
    
    if not rows:
        return None, "NO_MATCH", {"candidate_tokens": list(candidates)}

    entities_by_id = {}
    for row in rows:
        eid = str(row["entity_id"])
        if eid not in entities_by_id:
            entities_by_id[eid] = row
            
    matched_entities = list(entities_by_id.values())
    
    def type_rank(e: dict[str, Any]) -> tuple[int, int]:
        ranks = {
            "compound": 1,
            "landmark": 2,
            "neighborhood": 3,
            "district": 4,
            "city": 5,
            "governorate": 6,
            "region": 7,
            "state": 8,
            "province": 9,
            "country": 10
        }
        etype = e.get("entity_type")
        val = str(etype).casefold() if etype else ""
        primary_rank = ranks.get(val, 99)
        
        level = e.get("area_level")
        
        # If the type is unknown, derive the primary rank from the PostGIS area.level
        if primary_rank == 99 and level is not None:
            level = int(level)
            if level == 4:
                primary_rank = 1  # Act like a compound
            elif level == 3:
                primary_rank = 3  # Act like a neighborhood
            elif level == 2:
                primary_rank = 5  # Act like a city
            elif level == 1:
                primary_rank = 6  # Act like a governorate
                
        # Secondary specificity tiebreaker
        secondary_rank = (10 - int(level)) if level is not None else 99
        
        return (primary_rank, secondary_rank)
        
    # Sort so the MOST SPECIFIC (lowest rank value) comes first.
    # We also sort by priority as a secondary metric to ensure the best match.
    matched_entities.sort(key=lambda e: (type_rank(e), -e.get("priority", 0)))
    
    top_rank = type_rank(matched_entities[0])
    top_entities = [e for e in matched_entities if type_rank(e) == top_rank]
    
    metadata = {
        "candidate_tokens": list(candidates),
        "matched_entities": [e["entity_id"] for e in matched_entities]
    }
    
    # If there are multiple specific entities, try to use the broader geography to disambiguate!
    # Instead of just failing with AMBIGUOUS_ALIAS, we check which candidate is validated by the parents.
    candidate = None
    if len(top_entities) > 1 and len(matched_entities) > len(top_entities):
        parents = [e for e in matched_entities if type_rank(e) > top_rank]
        for potential_candidate in top_entities:
            # Check if this candidate is consistent with ALL parents
            is_valid = True
            for parent in parents:
                dist = haversine_distance(
                    potential_candidate["centroid_lat"], potential_candidate["centroid_lng"],
                    parent["centroid_lat"], parent["centroid_lng"]
                )
                if dist > 30000:
                    is_valid = False
                    break
            if is_valid:
                candidate = potential_candidate
                break
                
        if not candidate:
            return {"candidates": top_entities}, "AMBIGUOUS_ALIAS", metadata
    elif len(top_entities) > 1:
        return {"candidates": top_entities}, "AMBIGUOUS_ALIAS", metadata
    else:
        candidate = top_entities[0]
    
    # Parent geography SHOULD validate children, SHOULD NOT replace children.
    # Validate the chosen candidate against all other matched entities (parents).
    for other in matched_entities:
        if other["entity_id"] == candidate["entity_id"]:
            continue
        dist = haversine_distance(
            candidate["centroid_lat"], candidate["centroid_lng"],
            other["centroid_lat"], other["centroid_lng"]
        )
        if dist > 30000:
            metadata["conflict_between"] = [candidate["entity_id"], other["entity_id"]]
            metadata["distance_m"] = dist
            return None, "HIERARCHY_CONFLICT", metadata
            
    metadata["resolved_entity"] = candidate["entity_id"]
    metadata["resolution_strategy"] = "HIERARCHICAL_CANONICAL_MATCH" if len(matched_entities) > 1 else "CANONICAL_ALIAS_MATCH"
    
    return candidate, "UNAMBIGUOUS", metadata


def match_entity(db: Session, raw_input: str) -> tuple[dict[str, Any] | None, str]:
    # Delegating to the new hierarchical matcher to ensure backward compatibility
    # while leveraging the new capabilities.
    entity, status, _ = match_hierarchical_entities(db, raw_input)
    return entity, status


def get_entity_by_id(db: Session, entity_id: str) -> dict[str, Any] | None:
    row = db.execute(text(SQL_ENTITY_BY_ID), {"entity_id": entity_id}).mappings().first()
    return dict(row) if row else None


def precision_for_entity(entity: dict[str, Any]) -> str:
    return ENTITY_PRECISION.get(str(entity.get("entity_type") or "").casefold(), "DISTRICT")


def confidence_for_entity(entity: dict[str, Any]) -> float:
    return ENTITY_CONFIDENCE.get(str(entity.get("entity_type") or "").casefold(), 0.60)


def entity_metadata(entity: dict[str, Any]) -> dict[str, Any]:
    return {
        "entity_id": entity.get("entity_id"),
        "entity_type": entity.get("entity_type"),
        "canonical_name": entity.get("canonical_name"),
        "canonical_area_id": entity.get("canonical_area_id"),
        "authority_source": entity.get("authority_source"),
        "version": entity.get("version"),
    }
