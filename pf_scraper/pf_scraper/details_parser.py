# pf_scraper/details_parser.py
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


def _get_nested(obj: Any, path: list[str]) -> Any:
    cur = obj
    for p in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    return cur


def find_listing_payload(next_data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    On listing detail pages, the property/listing often lives under:
      props.pageProps.property
      props.pageProps.listing
      props.pageProps.data.property
      props.pageProps.data.listing
    We'll try multiple paths + DFS fallback.
    """
    candidates = [
        ["props", "pageProps", "property"],
        ["props", "pageProps", "listing"],
        ["props", "pageProps", "data", "property"],
        ["props", "pageProps", "data", "listing"],
        ["pageProps", "property"],
        ["pageProps", "listing"],
    ]
    for path in candidates:
        v = _get_nested(next_data, path)
        if isinstance(v, dict) and (v.get("id") or v.get("property_id") or v.get("title")):
            return v, ".".join(path)

    # DFS fallback
    def dfs(node: Any, trail: str) -> Optional[Tuple[Dict[str, Any], str]]:
        if isinstance(node, dict):
            # looks like a listing/property dict
            if ("id" in node and "title" in node) or ("property" in node and isinstance(node.get("property"), dict)):
                # prefer direct property-like
                if "id" in node and "title" in node:
                    return node, trail
            for k, v in node.items():
                res = dfs(v, f"{trail}.{k}".strip("."))
                if res:
                    return res
        elif isinstance(node, list):
            for i, item in enumerate(node[:200]):
                res = dfs(item, f"{trail}[{i}]")
                if res:
                    return res
        return None

    found = dfs(next_data, "")
    if found:
        return found[0], found[1]

    return None, "(not found)"


def extract_details(listing_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a clean details dict (no HTML scraping, just structured fields).
    We keep it flexible because PF can change keys.
    """
    # Some pages may wrap data under {"property": {...}}
    if "property" in listing_payload and isinstance(listing_payload["property"], dict):
        p = listing_payload["property"]
    else:
        p = listing_payload

    out: Dict[str, Any] = {}

    out["id"] = str(p.get("id") or p.get("property_id") or "")
    out["title"] = p.get("title")
    out["description"] = p.get("description")
    out["reference"] = p.get("reference")
    out["listed_date"] = p.get("listed_date")

    # location
    loc = p.get("location") or {}
    if isinstance(loc, dict):
        out["location"] = loc.get("full_name") or loc.get("name")
        coords = loc.get("coordinates") or {}
        if isinstance(coords, dict):
            out["latitude"] = coords.get("lat")
            out["longitude"] = coords.get("lon") or coords.get("lng")

    # pricing
    price = p.get("price") or {}
    if isinstance(price, dict):
        out["price"] = (price.get("value") if not isinstance(price.get("value"), dict) else price.get("value", {}).get("value"))
        out["currency"] = price.get("currency") or price.get("currency_code")

    out["property_type"] = p.get("property_type") or p.get("type")
    out["bedrooms"] = p.get("bedrooms")
    out["bathrooms"] = p.get("bathrooms")
    out["size"] = p.get("size")

    out["amenities"] = p.get("amenities")

    # images (keep raw; your parser already extracts urls well)
    out["images"] = p.get("images")

    # agent/broker basic
    out["agent"] = p.get("agent")
    out["broker"] = p.get("broker")

    return out
