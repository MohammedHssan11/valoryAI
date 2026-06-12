from __future__ import annotations
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

BASE_URL = "https://www.propertyfinder.eg"

def extract_egypt_listings_from_next_data(next_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    listings = next_data["props"]["pageProps"]["searchResult"]["listings"]

    out: List[Dict[str, Any]] = []
    for item in listings:
        if item.get("listing_type") != "property":
            continue

        p = item.get("property") or {}
        if not p:
            continue

        # --- core fields ---
        pid = str(p.get("id") or "")
        if not pid:
            continue

        price_obj = p.get("price") or {}
        loc = p.get("location") or {}
        coords = (loc.get("coordinates") or {})
        
        # --- logic update: size validation ---
        size_obj = p.get("size") or {}
        raw_size = size_obj.get("value")
        unit = size_obj.get("unit")
        
        # نعتبر المساحة بالمتر المربع بشكل افتراضي
        size_reported = raw_size if unit == "sqm" else raw_size

        ptype = (p.get("property_type") or "").lower()
        
        # منطق التحقق من الحد الأدنى للمساحة
        min_ok = 25
        if "villa" in ptype or "townhouse" in ptype:
            min_ok = 60
        elif "apartment" in ptype or "flat" in ptype:
            min_ok = 35

        # تعيين القيمة فقط إذا كانت رقمية وتتخطى الحد الأدنى، وإلا تكون None
        size_validated = size_reported if isinstance(size_reported, (int, float)) and size_reported >= min_ok else None

        details_path = p.get("details_path") or ""
        share_url = p.get("share_url") or (urljoin(BASE_URL, details_path) if details_path else "")

        images = p.get("images") or []
        image_urls = []
        for im in images:
            if isinstance(im, dict):
                # prefer medium then small
                u = im.get("medium") or im.get("small")
                if u:
                    image_urls.append(u)

        row = {
            "source": {"provider": "propertyfinder", "country_code": "EG"},
            "property_id": pid,
            "listing_id": p.get("listing_id"),
            "title": p.get("title"),
            "description": p.get("description"),
            "category_id": p.get("category_id"),
            "offering_type": p.get("offering_type"),
            "property_type": p.get("property_type"),
            "property_type_id": p.get("property_type_id"),

            "pricing": {
                "currency": price_obj.get("currency"),
                "period": price_obj.get("period"),
                "value": price_obj.get("value"),
                "is_hidden": price_obj.get("is_hidden"),
            },

            "bedrooms": p.get("bedrooms_value") or p.get("bedrooms"),
            "bathrooms": p.get("bathrooms_value") or p.get("bathrooms"),
            
            # الحقول الجديدة بناءً على التعديل
            "size_sqm_reported": size_reported,
            "size_sqm": size_validated,

            "location": {
                "full_name": loc.get("full_name"),
                "id": loc.get("id"),
                "slug": loc.get("slug"),
                "lat": coords.get("lat"),
                "lon": coords.get("lon"),
                "path": loc.get("path"),
                "path_name": loc.get("path_name"),
                "type": loc.get("type"),
            },

            "amenities": p.get("amenities") or [],
            "amenity_names": p.get("amenity_names") or [],

            "images": image_urls,
            "images_count": p.get("images_count"),

            "share_url": share_url,
            "details_path": details_path,
            "listed_date": p.get("listed_date"),
            "is_premium": p.get("is_premium"),
            "is_verified": p.get("is_verified"),
        }

        out.append(row)

    return out