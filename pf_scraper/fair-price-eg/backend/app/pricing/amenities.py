from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from typing import Any

from app.core.enums import PropertyCategory
from app.pricing.contracts import category_contract, normalize_property_category


@dataclass(frozen=True)
class AmenityDefinition:
    symbol: str
    normalized: str
    name: str
    arabic: str
    classification: str
    aliases: tuple[str, ...]
    weight_profile: dict[PropertyCategory, float]

    def weight_for(self, property_category: Any) -> float:
        category = normalize_property_category(property_category)
        return float(self.weight_profile.get(category, 0.01))


def _weights(**values: float) -> dict[PropertyCategory, float]:
    return {PropertyCategory(key): float(value) for key, value in values.items()}


AMENITY_REGISTRY: dict[str, AmenityDefinition] = {
    "AC": AmenityDefinition("AC", "central_ac", "Central AC", "تكييف مركزي", "core", ("central ac", "air conditioning", "ac"), _weights(residential_rent=0.035, residential_sale=0.025, villa_sale=0.025, office_rent=0.040, retail_rent=0.020, commercial_rent=0.025, land_sale=0.000)),
    "BA": AmenityDefinition("BA", "balcony", "Balcony", "بلكونة", "core", ("balcony", "terrace"), _weights(residential_rent=0.040, residential_sale=0.030, villa_sale=0.010, office_rent=0.005, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "BD": AmenityDefinition("BD", "business_district", "Business District", "منطقة أعمال", "location", ("business district", "prime business district", "cbd"), _weights(residential_rent=0.005, residential_sale=0.005, villa_sale=0.000, office_rent=0.065, retail_rent=0.045, commercial_rent=0.035, land_sale=0.020)),
    "BK": AmenityDefinition("BK", "kitchen_appliances", "Kitchen Appliances", "أجهزة مطبخ", "fitout", ("kitchen appliances", "appliances"), _weights(residential_rent=0.025, residential_sale=0.012, villa_sale=0.008, office_rent=0.000, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "BL": AmenityDefinition("BL", "landmark_view", "Landmark View", "إطلالة مميزة", "view", ("landmark view", "view"), _weights(residential_rent=0.018, residential_sale=0.022, villa_sale=0.020, office_rent=0.005, retail_rent=0.015, commercial_rent=0.000, land_sale=0.000)),
    "BW": AmenityDefinition("BW", "built_in_wardrobes", "Built-in Wardrobes", "دواليب مدمجة", "fitout", ("built in wardrobes", "wardrobes", "closets"), _weights(residential_rent=0.018, residential_sale=0.012, villa_sale=0.010, office_rent=0.000, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "CH": AmenityDefinition("CH", "clubhouse", "Clubhouse", "كلوب هاوس", "compound", ("clubhouse", "club house"), _weights(residential_rent=0.025, residential_sale=0.030, villa_sale=0.040, office_rent=0.005, retail_rent=0.010, commercial_rent=0.000, land_sale=0.000)),
    "CM": AmenityDefinition("CM", "compound", "Compound", "كمبوند", "location", ("compound", "gated community"), _weights(residential_rent=0.030, residential_sale=0.045, villa_sale=0.045, office_rent=0.015, retail_rent=0.020, commercial_rent=0.010, land_sale=0.010)),
    "CO": AmenityDefinition("CO", "childrens_pool", "Children's Pool", "حمام سباحة أطفال", "leisure", ("children pool", "kids pool", "childrens pool"), _weights(residential_rent=0.012, residential_sale=0.010, villa_sale=0.010, office_rent=0.000, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "CP": AmenityDefinition("CP", "covered_parking", "Covered Parking", "جراج مغطى", "access", ("covered parking", "parking", "garage", "car park"), _weights(residential_rent=0.030, residential_sale=0.025, villa_sale=0.030, office_rent=0.065, retail_rent=0.035, commercial_rent=0.045, land_sale=0.015)),
    "EL": AmenityDefinition("EL", "elevator", "Elevator", "مصعد", "core", ("elevator", "lift"), _weights(residential_rent=0.045, residential_sale=0.035, villa_sale=0.005, office_rent=0.050, retail_rent=0.020, commercial_rent=0.020, land_sale=0.000)),
    "FN": AmenityDefinition("FN", "finishing", "Finishing", "تشطيب", "fitout", ("finishing", "finished", "super lux", "lux finishing"), _weights(residential_rent=0.020, residential_sale=0.045, villa_sale=0.040, office_rent=0.030, retail_rent=0.035, commercial_rent=0.030, land_sale=0.010)),
    "FR": AmenityDefinition("FR", "frontage", "Frontage", "واجهة", "exposure", ("frontage", "wide frontage", "street frontage"), _weights(residential_rent=0.005, residential_sale=0.010, villa_sale=0.025, office_rent=0.015, retail_rent=0.090, commercial_rent=0.035, land_sale=0.070)),
    "FU": AmenityDefinition("FU", "furnished", "Furnished", "مفروش", "fitout", ("furnished", "fully furnished", "furniture"), _weights(residential_rent=0.050, residential_sale=0.015, villa_sale=0.010, office_rent=0.010, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "GE": AmenityDefinition("GE", "land_geometry", "Land Geometry", "هندسة الأرض", "land", ("geometry", "regular shape", "corner plot", "plot shape"), _weights(residential_rent=0.000, residential_sale=0.000, villa_sale=0.025, office_rent=0.000, retail_rent=0.020, commercial_rent=0.030, land_sale=0.085)),
    "IT": AmenityDefinition("IT", "internet", "Internet", "إنترنت", "infrastructure", ("internet", "fiber", "wifi", "broadband"), _weights(residential_rent=0.015, residential_sale=0.005, villa_sale=0.005, office_rent=0.040, retail_rent=0.015, commercial_rent=0.020, land_sale=0.000)),
    "LB": AmenityDefinition("LB", "lobby_in_building", "Lobby in Building", "لوبي", "core", ("lobby", "lobby in building", "reception"), _weights(residential_rent=0.020, residential_sale=0.018, villa_sale=0.000, office_rent=0.035, retail_rent=0.020, commercial_rent=0.010, land_sale=0.000)),
    "MR": AmenityDefinition("MR", "maids_room", "Maid Room", "غرفة مربية", "layout", ("maid room", "maids room", "nanny room"), _weights(residential_rent=0.020, residential_sale=0.022, villa_sale=0.045, office_rent=0.000, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "OI": AmenityDefinition("OI", "office_infrastructure", "Office Infrastructure", "بنية مكتبية", "infrastructure", ("office infrastructure", "meeting rooms", "data cabling", "fiber ready", "raised floor"), _weights(residential_rent=0.000, residential_sale=0.000, villa_sale=0.000, office_rent=0.075, retail_rent=0.020, commercial_rent=0.035, land_sale=0.000)),
    "PG": AmenityDefinition("PG", "private_garden", "Private Garden", "حديقة خاصة", "outdoor", ("private garden", "garden", "yard"), _weights(residential_rent=0.025, residential_sale=0.035, villa_sale=0.075, office_rent=0.000, retail_rent=0.010, commercial_rent=0.010, land_sale=0.020)),
    "PP": AmenityDefinition("PP", "private_pool", "Private Pool", "حمام سباحة خاص", "leisure", ("private pool", "pool", "swimming pool"), _weights(residential_rent=0.020, residential_sale=0.030, villa_sale=0.070, office_rent=0.000, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "RF": AmenityDefinition("RF", "retail_frontage", "Retail Frontage", "واجهة تجارية", "exposure", ("retail frontage", "shop frontage", "storefront"), _weights(residential_rent=0.000, residential_sale=0.000, villa_sale=0.000, office_rent=0.010, retail_rent=0.100, commercial_rent=0.030, land_sale=0.050)),
    "SE": AmenityDefinition("SE", "security", "Security", "أمن", "core", ("security", "secured", "gated security"), _weights(residential_rent=0.040, residential_sale=0.030, villa_sale=0.030, office_rent=0.035, retail_rent=0.020, commercial_rent=0.030, land_sale=0.005)),
    "SH": AmenityDefinition("SH", "smart_home", "Smart Home", "منزل ذكي", "technology", ("smart home", "home automation", "smart system"), _weights(residential_rent=0.018, residential_sale=0.020, villa_sale=0.025, office_rent=0.015, retail_rent=0.005, commercial_rent=0.005, land_sale=0.000)),
    "SP": AmenityDefinition("SP", "shared_pool", "Shared Pool", "حمام سباحة مشترك", "leisure", ("shared pool", "communal pool"), _weights(residential_rent=0.018, residential_sale=0.020, villa_sale=0.018, office_rent=0.000, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "SS": AmenityDefinition("SS", "shared_spa", "Shared Spa", "سبا مشترك", "leisure", ("shared spa", "spa"), _weights(residential_rent=0.010, residential_sale=0.012, villa_sale=0.012, office_rent=0.000, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "ST": AmenityDefinition("ST", "study", "Study", "غرفة مكتب", "layout", ("study", "home office"), _weights(residential_rent=0.018, residential_sale=0.020, villa_sale=0.025, office_rent=0.010, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "SY": AmenityDefinition("SY", "shared_gym", "Shared Gym", "جيم مشترك", "leisure", ("shared gym", "gym", "fitness"), _weights(residential_rent=0.025, residential_sale=0.020, villa_sale=0.015, office_rent=0.010, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "TR": AmenityDefinition("TR", "traffic_exposure", "Traffic Exposure", "تعرض مروري", "exposure", ("traffic exposure", "high traffic", "footfall", "foot traffic"), _weights(residential_rent=0.000, residential_sale=0.000, villa_sale=0.000, office_rent=0.020, retail_rent=0.090, commercial_rent=0.035, land_sale=0.030)),
    "VI": AmenityDefinition("VI", "visibility", "Visibility", "وضوح الرؤية", "exposure", ("visibility", "high visibility", "visible location"), _weights(residential_rent=0.000, residential_sale=0.000, villa_sale=0.000, office_rent=0.020, retail_rent=0.085, commercial_rent=0.030, land_sale=0.020)),
    "VW": AmenityDefinition("VW", "water_view", "Water View", "إطلالة مائية", "view", ("water view", "waterfront", "river view", "sea view", "lake view"), _weights(residential_rent=0.025, residential_sale=0.040, villa_sale=0.045, office_rent=0.005, retail_rent=0.015, commercial_rent=0.000, land_sale=0.020)),
    "WC": AmenityDefinition("WC", "walk_in_closet", "Walk-in Closet", "غرفة ملابس", "layout", ("walk in closet", "dressing room"), _weights(residential_rent=0.012, residential_sale=0.015, villa_sale=0.025, office_rent=0.000, retail_rent=0.000, commercial_rent=0.000, land_sale=0.000)),
    "WF": AmenityDefinition("WF", "waterfront", "Waterfront", "واجهة مائية", "view", ("waterfront", "on water", "lagoon front"), _weights(residential_rent=0.030, residential_sale=0.045, villa_sale=0.055, office_rent=0.005, retail_rent=0.020, commercial_rent=0.000, land_sale=0.040)),
    "ZO": AmenityDefinition("ZO", "zoning", "Zoning", "تقسيم/ترخيص", "land", ("zoning", "licensed use", "building permit", "permitted use"), _weights(residential_rent=0.000, residential_sale=0.000, villa_sale=0.020, office_rent=0.015, retail_rent=0.040, commercial_rent=0.060, land_sale=0.120)),
}

AMENITY_MAP: dict[str, str] = {symbol: item.normalized for symbol, item in AMENITY_REGISTRY.items()}
KNOWN_AMENITY_NAMES = frozenset(AMENITY_MAP.values())


def _normalize_alias_key(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if not text or text in {"none", "null", "nan"}:
        return None
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_") or None


ALIAS_INDEX: dict[str, str] = {}
for _symbol, _definition in AMENITY_REGISTRY.items():
    ALIAS_INDEX[_symbol.lower()] = _symbol
    ALIAS_INDEX[_definition.normalized] = _symbol
    ALIAS_INDEX[_normalize_alias_key(_definition.name) or _definition.normalized] = _symbol
    for _alias in _definition.aliases:
        _key = _normalize_alias_key(_alias)
        if _key:
            ALIAS_INDEX[_key] = _symbol


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
    return _normalize_alias_key(value)


def amenity_definition(value: Any) -> AmenityDefinition | None:
    if isinstance(value, dict):
        for key in ("symbol", "canonical_symbol", "raw", "normalized", "name"):
            if value.get(key):
                match = amenity_definition(value.get(key))
                if match is not None:
                    return match
        return None

    code = normalize_amenity_code(value)
    if code in AMENITY_REGISTRY:
        return AMENITY_REGISTRY[code]

    name = normalize_amenity_name(value)
    if name and name in ALIAS_INDEX:
        return AMENITY_REGISTRY[ALIAS_INDEX[name]]
    return None


def amenity_weight(value: Any, property_category: Any = PropertyCategory.RESIDENTIAL_RENT) -> float:
    definition = amenity_definition(value)
    return definition.weight_for(property_category) if definition else 0.0


def amenity_metadata(value: Any, property_category: Any = PropertyCategory.RESIDENTIAL_RENT) -> dict[str, Any] | None:
    definition = amenity_definition(value)
    if definition is None:
        return None
    return {
        "symbol": definition.symbol,
        "normalized": definition.normalized,
        "name": definition.name,
        "arabic": definition.arabic,
        "category": definition.classification,
        "valuation_weight": definition.weight_for(property_category),
        "weight_profile": {key.value: value for key, value in sorted(definition.weight_profile.items(), key=lambda item: item[0].value)},
    }


def normalize_amenities(value: Any, property_category: Any = PropertyCategory.RESIDENTIAL_RENT) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    seen: set[str] = set()

    for raw_value in parse_feature_list(value):
        raw = normalize_amenity_code(raw_value)
        if raw is None:
            continue
        definition = amenity_definition(raw_value)
        stable_key = definition.symbol if definition is not None else raw
        if stable_key in seen:
            continue
        seen.add(stable_key)
        if definition is None:
            items.append({"raw": raw, "normalized": None, "known": False})
            continue
        items.append(
            {
                "raw": raw,
                "symbol": definition.symbol,
                "normalized": definition.normalized,
                "name": definition.name,
                "arabic": definition.arabic,
                "category": definition.classification,
                "valuation_weight": definition.weight_for(property_category),
                "known": True,
            }
        )

    known = sorted(item["normalized"] for item in items if item["known"])
    symbols = sorted(item["symbol"] for item in items if item["known"])
    unknown = sorted(item["raw"] for item in items if not item["known"])
    return {
        "items": items,
        "known": known,
        "symbols": symbols,
        "unknown": unknown,
        "raw_codes": [item["raw"] for item in items],
    }


def known_amenity_names(value: Any) -> set[str]:
    names: set[str] = set()
    for item in parse_feature_list(value):
        definition = amenity_definition(item)
        if definition is not None:
            names.add(definition.normalized)
    return names


def known_amenity_symbols(value: Any) -> set[str]:
    symbols: set[str] = set()
    for item in parse_feature_list(value):
        definition = amenity_definition(item)
        if definition is not None:
            symbols.add(definition.symbol)
    return symbols


def unknown_amenity_codes(value: Any) -> list[str]:
    codes: set[str] = set()
    for item in parse_feature_list(value):
        if isinstance(item, dict):
            if item.get("known") is False and item.get("raw"):
                codes.add(str(item["raw"]).upper())
            continue
        code = normalize_amenity_code(item)
        if code and amenity_definition(item) is None:
            codes.add(code)
    return sorted(codes)


def _weighted_amenity_union(symbols: set[str], property_category: Any) -> float:
    total = 0.0
    for symbol in symbols:
        total += max(amenity_weight(symbol, property_category), 0.001)
    return total


def amenity_similarity(
    target: Any,
    comp: Any,
    property_category: Any = PropertyCategory.RESIDENTIAL_RENT,
) -> dict[str, Any]:
    target_symbols = known_amenity_symbols(target)
    comp_symbols = known_amenity_symbols(comp)
    union = target_symbols | comp_symbols
    intersection = target_symbols & comp_symbols
    denominator = _weighted_amenity_union(union, property_category)
    numerator = _weighted_amenity_union(intersection, property_category)
    score = 1.0 if not union else numerator / denominator

    target_names = {AMENITY_REGISTRY[symbol].normalized for symbol in target_symbols}
    comp_names = {AMENITY_REGISTRY[symbol].normalized for symbol in comp_symbols}
    matched_symbols = sorted(intersection)
    return {
        "score": float(max(0.0, min(1.0, score))),
        "matched": sorted(target_names & comp_names),
        "missing": sorted(target_names - comp_names),
        "extra": sorted(comp_names - target_names),
        "matched_symbols": matched_symbols,
        "missing_symbols": sorted(target_symbols - comp_symbols),
        "extra_symbols": sorted(comp_symbols - target_symbols),
        "target_known": sorted(target_names),
        "comp_known": sorted(comp_names),
        "weighted_union": round(denominator, 6),
        "weighted_intersection": round(numerator, 6),
        "category": normalize_property_category(property_category).value,
    }


def amenity_governance_registry(property_category: Any = PropertyCategory.RESIDENTIAL_RENT) -> list[dict[str, Any]]:
    return [
        amenity_metadata(symbol, property_category) or {}
        for symbol in sorted(AMENITY_REGISTRY)
    ]


def important_target_amenities(target_features: dict[str, Any], property_category: Any) -> list[dict[str, Any]]:
    contract = category_contract(property_category)
    symbols = target_features.get("canonical_amenity_symbols") or known_amenity_symbols(
        target_features.get("normalized_amenities") or target_features.get("amenities") or []
    )
    items = []
    for symbol in sorted(symbols):
        metadata = amenity_metadata(symbol, property_category)
        if metadata and metadata["valuation_weight"] >= contract.critical_amenity_weight:
            items.append(metadata)
    return items

