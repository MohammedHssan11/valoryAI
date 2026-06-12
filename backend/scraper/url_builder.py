# pf_scraper/url_builder.py
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Union

from .config import CATEGORY_DEFS


def _merge_params(base: Dict[str, Any], extra: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge params safely:
    - ignore None
    - allow list values for keys like bdr[] / btr[]
    - allow overriding existing keys
    """
    out = dict(base)

    for k, v in extra.items():
        if v is None:
            continue
        # allow passing tuples/sets -> list
        if isinstance(v, (tuple, set)):
            v = list(v)

        # if list -> keep as is (urlencode(doseq=True) in http_client handles it)
        out[k] = v

    return out

def build_request(
    category_name: str,
    page: int,
    extra: Optional[Dict[str, Any]] = None,
    *,
    country: str = "UAE",
) -> Tuple[str, Dict[str, Any]]:

    if category_name not in CATEGORY_DEFS:
        raise ValueError(f"Unknown category '{category_name}'")

    info = CATEGORY_DEFS[category_name]
    page_param = info.get("page_param", "page")

    country = country.upper()

    if country == "EG":
        path = info["eg_path"]
        base_params = dict(info.get("eg_params", {}))
    else:
        path = info["uae_path"]
        base_params = dict(info.get("uae_params", {}))

    base_params[page_param] = page

    if extra:
        base_params.update(extra)

    return path, base_params
