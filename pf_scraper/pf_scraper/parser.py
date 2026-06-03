# pf_scraper/parser.py
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


# ----------------------------
# Output models
# ----------------------------
@dataclass
class ParsedProperty:
    id: str
    title: str
    price: Optional[float]
    currency: Optional[str]

    # ✅ new (do NOT remove old fields)
    price_period: Optional[str]          # e.g. sell / rent / ...
    price_type: str                      # sale_price / rent_price / suspicious_low / hidden / unknown / ...
    price_raw_value: Optional[float]     # raw value before any filtering

    property_type: Optional[str]
    location: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    images: List[str]

    # ✅ extra fields from search SSR
    share_url: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    size: Optional[float]
    amenities: List[str]

    category: str
    page: int
    scraped_at_utc: str

    record_type: str = "property"  # default must be last

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ParsedProject:
    id: str
    title: str
    location: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    images: List[str]
    min_price: Optional[float]
    max_price: Optional[float]
    currency: Optional[str]

    category: str
    page: int
    scraped_at_utc: str

    record_type: str = "project"  # default must be last

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ----------------------------
# Helpers
# ----------------------------
def _get_nested(obj: Any, path: List[str]) -> Any:
    cur = obj
    for p in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    return cur


def _safe_float(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        s = x.strip().replace(",", "")
        if s.replace(".", "", 1).isdigit():
            try:
                return float(s)
            except Exception:
                return None
    return None


def _safe_int(x: Any) -> Optional[int]:
    if x is None:
        return None
    if isinstance(x, bool):
        return None
    if isinstance(x, int):
        return int(x)
    if isinstance(x, float):
        return int(x)
    if isinstance(x, str):
        s = x.strip()
        if s.isdigit():
            try:
                return int(s)
            except Exception:
                return None
    return None


# ✅ robust numeric extraction helper
_NUM_RE = re.compile(r"(\d+(\.\d+)?)")


def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        m = _NUM_RE.search(value)
        return int(float(m.group(1))) if m else None
    if isinstance(value, dict):
        for k in ("value", "count", "number"):
            if k in value:
                return _to_int(value.get(k))
    return None


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = _NUM_RE.search(value.replace(",", ""))
        return float(m.group(1)) if m else None
    if isinstance(value, dict):
        for k in ("value", "area", "size", "number"):
            if k in value:
                return _to_float(value.get(k))
    return None


# ----------------------------
# Listings discovery (rent/buy/commercial)
# ----------------------------
def find_listings(payload: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], str]:
    candidate_paths = [
        ["props", "pageProps", "searchResult", "listings"],
        ["props", "pageProps", "searchResult", "data", "listings"],
        ["props", "pageProps", "searchResult", "result", "listings"],
        ["pageProps", "searchResult", "listings"],
    ]
    for path in candidate_paths:
        val = _get_nested(payload, path)
        if isinstance(val, list):
            return val, ".".join(path)

    # DFS fallback
    def dfs(node: Any, trail: str) -> Optional[Tuple[List[Dict[str, Any]], str]]:
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "listings" and isinstance(v, list) and (len(v) == 0 or isinstance(v[0], dict)):
                    return v, f"{trail}.{k}".strip(".")
                res = dfs(v, f"{trail}.{k}".strip("."))
                if res:
                    return res
        elif isinstance(node, list):
            for i, item in enumerate(node[:200]):
                res = dfs(item, f"{trail}[{i}]")
                if res:
                    return res
        return None

    found = dfs(payload, "")
    if found:
        return found[0], found[1]

    return [], "(not found)"


# ----------------------------
# Projects discovery (new_projects)
# ----------------------------
def find_projects(payload: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], str]:
    """
    New projects pages often use a different key than listings, typically 'projects'.
    We'll try common paths + DFS fallback.
    """
    candidate_paths = [
        ["props", "pageProps", "projects"],
        ["props", "pageProps", "searchResult", "projects"],
        ["props", "pageProps", "projectsResult", "projects"],
        ["pageProps", "projects"],
        # observed alt paths
        ["props", "pageProps", "searchResult", "data", "projects"],
        ["pageProps", "searchResult", "data", "projects"],
    ]
    for path in candidate_paths:
        val = _get_nested(payload, path)
        if isinstance(val, list):
            return val, ".".join(path)

    def dfs(node: Any, trail: str) -> Optional[Tuple[List[Dict[str, Any]], str]]:
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "projects" and isinstance(v, list) and (len(v) == 0 or isinstance(v[0], dict)):
                    return v, f"{trail}.{k}".strip(".")
                res = dfs(v, f"{trail}.{k}".strip("."))
                if res:
                    return res
        elif isinstance(node, list):
            for i, item in enumerate(node[:200]):
                res = dfs(item, f"{trail}[{i}]")
                if res:
                    return res
        return None

    found = dfs(payload, "")
    if found:
        return found[0], found[1]
    return [], "(not found)"


def _extract_coords(location_obj: Any) -> Tuple[Optional[float], Optional[float]]:
    if not isinstance(location_obj, dict):
        return None, None
    coords = location_obj.get("coordinates") or {}
    if isinstance(coords, dict):
        lat = coords.get("lat")
        lon = coords.get("lon") or coords.get("lng")
        return _to_float(lat), _to_float(lon)
    return None, None


def _extract_price(price_obj: Any) -> Tuple[Optional[float], Optional[str]]:
    if not isinstance(price_obj, dict):
        return None, None

    value = price_obj.get("value")
    currency = price_obj.get("currency") or price_obj.get("currency_code")

    if isinstance(value, dict):
        currency = currency or value.get("currency") or value.get("currency_code")
        value = value.get("value") or value.get("amount")

    if value is None:
        value = price_obj.get("amount")

    value_f = _to_float(value)
    currency_s = str(currency) if currency is not None else None
    return value_f, currency_s


# ✅ price classification / filtering helper (put under _extract_price or above parse_listing)
def _extract_and_classify_price(
    prop: Dict[str, Any],
    category: str,
    size: Optional[float],
) -> Tuple[Optional[float], Optional[str], Optional[str], str, Optional[float]]:
    """
    Returns:
      (final_price, currency, period, price_type, raw_price_value)
    """
    price_obj = prop.get("price") or {}
    period = None
    currency = None

    # PropertyFinder often has: {"value": ..., "currency": "EGP", "period": "sell", "is_hidden": false}
    if isinstance(price_obj, dict):
        period = price_obj.get("period")
        currency = price_obj.get("currency") or price_obj.get("currency_code")

    raw_value, cur2 = _extract_price(price_obj if isinstance(price_obj, dict) else {})
    currency = currency or cur2

    # hidden
    if isinstance(price_obj, dict) and price_obj.get("is_hidden") is True:
        return None, currency, (str(period) if period else None), "hidden", raw_value

    # base type
    price_type = "unknown"
    if category in ("buy", "commercial_buy"):
        price_type = "sale_price"
    elif category in ("rent", "commercial_rent"):
        price_type = "rent_price"

    # --- ✅ sanity rules (EG-focused but safe generally) ---
    # Common issue: some listings show installment/monthly or "starting from" tiny number.
    # If it's a BUY category and price is too low compared to typical market, mark suspicious and null it.
    if raw_value is not None and category in ("buy", "commercial_buy"):
        # rule: very low price with a reasonable size -> likely NOT full sale price
        if raw_value < 200_000 and (size is None or size >= 40):
            return None, currency, (str(period) if period else None), "suspicious_low", raw_value

        # optional extra: if period says it's not sell, also suspicious
        if period and str(period).lower() not in ("sell", "sale"):
            return None, currency, (str(period) if period else None), "non_sell_period", raw_value

    return raw_value, currency, (str(period) if period else None), price_type, raw_value


# ----------------------------
# Images extraction (robust)
# ----------------------------
_IMAGE_EXT_RE = re.compile(r"\.(jpg|jpeg|png|webp)(\?|$)", re.IGNORECASE)


def _looks_like_image_url(s: str) -> bool:
    if not isinstance(s, str) or not s:
        return False
    s2 = s.lower()
    if _IMAGE_EXT_RE.search(s2):
        return True
    if "propertyfinder" in s2 and ("image" in s2 or "media" in s2):
        return True
    return False


def _normalize_url(u: str) -> str:
    if u.startswith("//"):
        return "https:" + u
    if u.startswith("http://") or u.startswith("https://"):
        return u
    if u.startswith("static."):
        return "https://" + u
    if u.startswith("/"):
        return "https://www.propertyfinder.ae" + u
    return u


def _collect_strings_recursive(node: Any, out: List[str]) -> None:
    if isinstance(node, dict):
        for v in node.values():
            _collect_strings_recursive(v, out)
    elif isinstance(node, list):
        for item in node:
            _collect_strings_recursive(item, out)
    elif isinstance(node, str):
        out.append(node)


def _extract_images_generic(obj: Any) -> List[str]:
    """
    Works for both property images and project images.
    Handles:
      - list of urls
      - list of dicts with embedded urls
      - dict containing "images" list
    """
    if obj is None:
        return []

    if isinstance(obj, list):
        imgs = obj
    elif isinstance(obj, dict):
        imgs = obj.get("images")
        if not isinstance(imgs, list):
            imgs = obj.get("gallery") if isinstance(obj.get("gallery"), list) else []
    else:
        return []

    found: List[str] = []
    for item in imgs:
        if isinstance(item, str):
            if _looks_like_image_url(item):
                found.append(_normalize_url(item))
        elif isinstance(item, dict):
            strings: List[str] = []
            _collect_strings_recursive(item, strings)
            for s in strings:
                if _looks_like_image_url(s):
                    found.append(_normalize_url(s))

    seen = set()
    uniq: List[str] = []
    for u in found:
        if u and u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


# ----------------------------
# Parsing: listings
# ----------------------------
def parse_listing(listing_obj: Dict[str, Any], category: str, page: int) -> Optional[ParsedProperty]:
    prop = listing_obj.get("property") if isinstance(listing_obj, dict) else None
    if not isinstance(prop, dict):
        if isinstance(listing_obj, dict) and "id" in listing_obj:
            prop = listing_obj
        else:
            return None

    pid = prop.get("id")
    title = prop.get("title") or prop.get("listing_title") or ""

    loc_obj = prop.get("location") or {}
    location = None
    if isinstance(loc_obj, dict):
        location = loc_obj.get("full_name") or loc_obj.get("name")

    lat, lon = _extract_coords(loc_obj)
    property_type = prop.get("property_type") or prop.get("type")

    images = _extract_images_generic(prop.get("images"))
    share_url = prop.get("share_url")

    # bedrooms/bathrooms/size لازم ييجي قبل السعر عشان نستخدم size في sanity
    bedrooms = _to_int(prop.get("bedrooms") or prop.get("bedroom"))
    bathrooms = _to_int(prop.get("bathrooms") or prop.get("bathroom"))
    size = _to_float(prop.get("size") or prop.get("area"))

    price_val, currency, price_period, price_type, raw_price_val = _extract_and_classify_price(
        prop=prop,
        category=category,
        size=size,
    )

    am = prop.get("amenities")
    amenities = am if isinstance(am, list) else []
    amenities = [str(x) for x in amenities if x is not None]

    scraped_at = datetime.now(timezone.utc).isoformat()

    return ParsedProperty(
        id=str(pid) if pid is not None else "",
        title=str(title) if title is not None else "",
        price=price_val,
        currency=currency,

        price_period=price_period,
        price_type=price_type,
        price_raw_value=raw_price_val,

        property_type=str(property_type) if property_type is not None else None,
        location=str(location) if location is not None else None,
        latitude=lat,
        longitude=lon,
        images=images,
        share_url=str(share_url) if share_url is not None else None,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        size=size,
        amenities=amenities,
        category=category,
        page=page,
        scraped_at_utc=scraped_at,
    )


# ----------------------------
# Parsing: projects
# ----------------------------
def _project_price_range(project: Dict[str, Any]) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    Try common patterns:
    - project['price'] (dict)
    - project['min_price'], project['max_price']
    - project['price_range'] or project['prices']
    """
    currency = None
    min_p = _to_float(project.get("min_price"))
    max_p = _to_float(project.get("max_price"))

    price = project.get("price")
    if isinstance(price, dict):
        v, c = _extract_price(price)
        currency = currency or c
        if v is not None and min_p is None and max_p is None:
            min_p = v
            max_p = v

    pr = project.get("priceRange") or project.get("price_range")
    if isinstance(pr, dict):
        currency = currency or pr.get("currency") or pr.get("currency_code")
        if min_p is None:
            min_p = _to_float(pr.get("min"))
        if max_p is None:
            max_p = _to_float(pr.get("max"))

    return min_p, max_p, (str(currency) if currency is not None else None)


def parse_project(project_obj: Dict[str, Any], category: str, page: int) -> Optional[ParsedProject]:
    if not isinstance(project_obj, dict):
        return None

    pid = project_obj.get("id") or project_obj.get("project_id")
    title = project_obj.get("title") or project_obj.get("name") or project_obj.get("project_name") or ""

    loc_obj = project_obj.get("location") or {}
    location = None
    if isinstance(loc_obj, dict):
        location = loc_obj.get("full_name") or loc_obj.get("name") or loc_obj.get("title")

    lat, lon = _extract_coords(loc_obj)

    images = _extract_images_generic(project_obj.get("images") or project_obj.get("gallery") or project_obj)

    min_p, max_p, currency = _project_price_range(project_obj)

    scraped_at = datetime.now(timezone.utc).isoformat()

    if pid is None and not title:
        return None

    return ParsedProject(
        id=str(pid) if pid is not None else "",
        title=str(title),
        location=str(location) if location is not None else None,
        latitude=lat,
        longitude=lon,
        images=images,
        min_price=min_p,
        max_price=max_p,
        currency=currency,
        category=category,
        page=page,
        scraped_at_utc=scraped_at,
    )


# ----------------------------
# Page parsing entry
# ----------------------------
def parse_page(payload: Dict[str, Any], category: str, page: int) -> Tuple[List[Any], str]:
    """
    Returns list of ParsedProperty OR ParsedProject depending on page content.
    """
    listings, l_path = find_listings(payload)
    if listings:
        parsed: List[Any] = []
        for item in listings:
            if isinstance(item, dict):
                p = parse_listing(item, category=category, page=page)
                if p and p.id:
                    parsed.append(p)
        return parsed, l_path

    projects, p_path = find_projects(payload)
    if projects:
        parsed_p: List[Any] = []
        for item in projects:
            if isinstance(item, dict):
                pr = parse_project(item, category=category, page=page)
                if pr and (pr.id or pr.title):
                    parsed_p.append(pr)
        return parsed_p, p_path

    return [], "(not found)"


def summarize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    top_keys = list(payload.keys()) if isinstance(payload, dict) else []

    page_props_keys: List[str] = []
    if isinstance(payload, dict):
        props = payload.get("props")
        if isinstance(props, dict):
            page_props = props.get("pageProps")
            if isinstance(page_props, dict):
                page_props_keys = list(page_props.keys())

    listings, l_path = find_listings(payload)
    projects, p_path = find_projects(payload)

    found_path = l_path if listings else (p_path if projects else "(not found)")
    count = len(listings) if listings else (len(projects) if projects else 0)

    first_listing_keys = list(listings[0].keys())[:30] if listings else []
    first_property_keys = list((listings[0].get("property") or {}).keys())[:30] if listings else []
    first_project_keys = list(projects[0].keys())[:30] if projects else []

    return {
        "top_level_keys": top_keys[:30],
        "pageProps_keys": page_props_keys[:30],
        "listings_found_path": found_path,
        "listings_count": count,
        "first_listing_keys": first_listing_keys,
        "first_property_keys": first_property_keys,
        "first_project_keys": first_project_keys,
    }
