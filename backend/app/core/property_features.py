from __future__ import annotations

import ast
import json
import re
from typing import Any, Iterable


# Observed by pairing real PropertyFinder "amenities" and "amenity_names" arrays
# from the scraped Egypt dataset. Do not add meanings here unless the source data
# contains an explicit code/name pair.
AMENITY_MAP: dict[str, str] = {
    "AC": "central_ac",
    "BA": "balcony",
    "BK": "kitchen_appliances",
    "BL": "landmark_view",
    "BW": "built_in_wardrobes",
    "CO": "childrens_pool",
    "CP": "covered_parking",
    "LB": "lobby_in_building",
    "MR": "maids_room",
    "PG": "private_garden",
    "PP": "private_pool",
    "SE": "security",
    "SP": "shared_pool",
    "SS": "shared_spa",
    "ST": "study",
    "SY": "shared_gym",
    "VW": "water_view",
    "WC": "walk_in_closet",
}

KNOWN_AMENITY_NAMES = frozenset(AMENITY_MAP.values())

FURNISHING_MAP = {
    "furnished": "furnished",
    "fully furnished": "furnished",
    "unfurnished": "unfurnished",
    "un furnished": "unfurnished",
    "semi furnished": "semi_furnished",
    "semi-furnished": "semi_furnished",
    "partly furnished": "semi_furnished",
}

BUILDING_QUALITY_VALUES = {
    "standard",
    "premium",
    "luxury",
    "renovated",
    "new",
}


def parse_feature_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple | set):
        return list(value)
    if isinstance(value, str):
        raw = value.strip()
        if not raw or raw.lower() in {"none", "null", "nan"}:
            return []
        if raw.startswith("["):
            for parser in (json.loads, ast.literal_eval):
                try:
                    parsed = parser(raw)
                except (ValueError, SyntaxError, TypeError, json.JSONDecodeError):
                    continue
                if isinstance(parsed, list):
                    return parsed
            return []
        if "," in raw:
            return [item.strip() for item in raw.split(",") if item.strip()]
        return [raw]
    return [value]


def normalize_amenity_code(value: Any) -> str | None:
    if value is None:
        return None
    code = str(value).strip().upper()
    if not code or code.lower() in {"none", "null", "nan"}:
        return None
    return code


def normalize_amenity_name(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if not text:
        return None
    normalized = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return normalized or None


def normalize_amenities(value: Any) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    seen: set[str] = set()

    for raw_value in parse_feature_list(value):
        raw = normalize_amenity_code(raw_value)
        if raw is None or raw in seen:
            continue
        seen.add(raw)
        normalized = AMENITY_MAP.get(raw)
        items.append(
            {
                "raw": raw,
                "normalized": normalized,
                "known": normalized is not None,
            }
        )

    known = sorted(item["normalized"] for item in items if item["known"])
    unknown = sorted(item["raw"] for item in items if not item["known"])
    return {
        "items": items,
        "known": known,
        "unknown": unknown,
        "raw_codes": [item["raw"] for item in items],
    }


def known_amenity_names(value: Any) -> set[str]:
    names: set[str] = set()

    for item in parse_feature_list(value):
        if isinstance(item, dict):
            normalized = item.get("normalized")
            if normalized in KNOWN_AMENITY_NAMES:
                names.add(str(normalized))
            continue

        code = normalize_amenity_code(item)
        if code in AMENITY_MAP:
            names.add(AMENITY_MAP[code])
            continue

        name = normalize_amenity_name(item)
        if name in KNOWN_AMENITY_NAMES:
            names.add(name)

    return names


def unknown_amenity_codes(value: Any) -> list[str]:
    codes: set[str] = set()
    for item in parse_feature_list(value):
        if isinstance(item, dict):
            if item.get("known") is False and item.get("raw"):
                codes.add(str(item["raw"]).upper())
            continue
        code = normalize_amenity_code(item)
        if code and code not in AMENITY_MAP and normalize_amenity_name(item) not in KNOWN_AMENITY_NAMES:
            codes.add(code)
    return sorted(codes)


def amenity_similarity(target: Any, comp: Any) -> dict[str, Any]:
    target_set = known_amenity_names(target)
    comp_set = known_amenity_names(comp)
    union = target_set | comp_set
    intersection = target_set & comp_set
    score = 1.0 if not union else len(intersection) / len(union)
    return {
        "score": float(score),
        "matched": sorted(intersection),
        "missing": sorted(target_set - comp_set),
        "extra": sorted(comp_set - target_set),
        "target_known": sorted(target_set),
        "comp_known": sorted(comp_set),
    }


def normalize_furnishing_status(value: Any) -> str | None:
    if value is None:
        return None
    text = " ".join(str(value).strip().lower().replace("_", " ").split())
    if not text or text in {"none", "null", "nan"}:
        return None
    return FURNISHING_MAP.get(text)


def normalize_floor_number(value: Any) -> int | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if not text or text in {"none", "null", "nan"}:
        return None
    if text in {"ground", "ground floor"}:
        return 0
    match = re.search(r"-?\d+", text)
    if not match:
        return None
    floor = int(match.group(0))
    if floor < -5 or floor > 200:
        return None
    return floor


def floor_band(value: Any) -> str | None:
    floor = normalize_floor_number(value)
    if floor is None:
        return None
    if floor <= 0:
        return "ground"
    if floor <= 3:
        return "low"
    if floor <= 10:
        return "mid"
    return "high"


def normalize_text_value(value: Any) -> str | None:
    if value is None:
        return None
    text = re.sub(r"\s+", " ", str(value).strip())
    if not text or text.lower() in {"none", "null", "nan"}:
        return None
    return text


def normalize_match_text(value: Any) -> str | None:
    text = normalize_text_value(value)
    if text is None:
        return None
    return text.casefold()


def location_parts(location_text: Any) -> list[str]:
    text = normalize_text_value(location_text)
    if text is None:
        return []
    return [part.strip() for part in text.split(",") if part.strip()]


def extract_compound_name(location_text: Any, explicit_compound: Any = None) -> str | None:
    explicit = normalize_text_value(explicit_compound)
    if explicit is not None:
        return explicit

    parts = location_parts(location_text)
    if not parts:
        return None

    for idx, part in enumerate(parts):
        if "compound" not in part.casefold():
            continue
        if idx > 0:
            return parts[idx - 1]
        return part

    return None


def normalize_view_type(value: Any = None, amenities: Any = None) -> str | None:
    text = normalize_match_text(value)
    if text:
        if any(token in text for token in ("water", "sea", "river", "lake", "lagoon")):
            return "water"
        if "landmark" in text:
            return "landmark"
        if text in {"water", "landmark", "water_and_landmark"}:
            return text

    names = known_amenity_names(amenities)
    has_water = "water_view" in names
    has_landmark = "landmark_view" in names
    if has_water and has_landmark:
        return "water_and_landmark"
    if has_water:
        return "water"
    if has_landmark:
        return "landmark"
    return None


def normalize_building_quality(value: Any) -> str | None:
    text = normalize_match_text(value)
    if text in BUILDING_QUALITY_VALUES:
        return text
    return None


def first_present(mapping: dict[str, Any], keys: Iterable[str]) -> Any:
    for key in keys:
        value = mapping.get(key)
        if normalize_text_value(value) is not None:
            return value
    return None


def normalize_property_features(row: dict[str, Any]) -> dict[str, Any]:
    raw_amenities = first_present(row, ("amenities", "amenity_codes", "raw_amenities"))
    amenities = normalize_amenities(raw_amenities)

    raw_furnishing = first_present(row, ("furnishing_status", "furnishing", "furnished"))
    raw_floor = first_present(row, ("floor_number", "floor", "floor_level"))
    raw_compound = first_present(row, ("compound_name", "compound", "project_name"))
    raw_view = first_present(row, ("view_type", "view"))
    raw_quality = first_present(row, ("building_quality", "quality", "finishing"))
    location_text = first_present(row, ("location_text", "location"))

    view_type = normalize_view_type(raw_view, amenities["items"])
    compound_name = extract_compound_name(location_text, raw_compound)

    return {
        "amenities": amenities["items"],
        "normalized_amenities": amenities["known"],
        "canonical_amenity_symbols": amenities.get("symbols", []),
        "unknown_amenity_codes": amenities["unknown"],
        "furnishing_status": normalize_furnishing_status(raw_furnishing),
        "floor_number": normalize_floor_number(raw_floor),
        "compound_name": compound_name,
        "view_type": view_type,
        "building_quality": normalize_building_quality(raw_quality),
        "feature_raw": {
            "amenities": amenities["raw_codes"],
            "furnishing": normalize_text_value(raw_furnishing),
            "floor": normalize_text_value(raw_floor),
            "compound": normalize_text_value(raw_compound),
            "view": normalize_text_value(raw_view),
            "building_quality": normalize_text_value(raw_quality),
        },
    }


# The valuation platform now uses the governed amenity registry in
# app.pricing.amenities while preserving this module as the stable import path
# for scraper/import and feature-similarity code.
from app.pricing.amenities import (  # noqa: E402
    AMENITY_MAP as GOVERNED_AMENITY_MAP,
    KNOWN_AMENITY_NAMES as GOVERNED_KNOWN_AMENITY_NAMES,
    amenity_similarity as governed_amenity_similarity,
    known_amenity_names as governed_known_amenity_names,
    normalize_amenities as governed_normalize_amenities,
    normalize_amenity_code as governed_normalize_amenity_code,
    normalize_amenity_name as governed_normalize_amenity_name,
    parse_feature_list as governed_parse_feature_list,
    unknown_amenity_codes as governed_unknown_amenity_codes,
)

AMENITY_MAP = GOVERNED_AMENITY_MAP
KNOWN_AMENITY_NAMES = GOVERNED_KNOWN_AMENITY_NAMES
parse_feature_list = governed_parse_feature_list
normalize_amenity_code = governed_normalize_amenity_code
normalize_amenity_name = governed_normalize_amenity_name
normalize_amenities = governed_normalize_amenities
known_amenity_names = governed_known_amenity_names
unknown_amenity_codes = governed_unknown_amenity_codes
amenity_similarity = governed_amenity_similarity
