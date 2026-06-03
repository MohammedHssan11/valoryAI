# pf_scraper/details_fetcher.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .config import ScraperConfig
from .http_client import PropertyFinderHTTPClient


@dataclass
class DetailsFetchResult:
    url: str
    http_status: int
    next_data: Dict[str, Any]


def fetch_listing_next_data(
    cfg: ScraperConfig,
    url: str,
    client: Optional[PropertyFinderHTTPClient] = None,
    warmup: bool = True,
) -> DetailsFetchResult:
    """
    Fetch listing details SSR HTML and extract __NEXT_DATA__ (country-aware via cfg).

    - Uses same session headers/cookies
    - Optional warmup to set WAF cookies
    - Extraction is delegated to http_client.get_json() for robustness
    """
    client = client or PropertyFinderHTTPClient(cfg=cfg)

    # ✅ Warm-up: hit a known SSR page to seed cookies (country-aware via cfg.base_url)
    if warmup:
        try:
            # works for both EG/UAE (search SSR has __NEXT_DATA__)
            client.get_json(
                path="/en/search",
                params={"c": 2, "t": 1, "l": 1, "fu": 0, "ob": "mr", "page": 1},
            )
        except Exception:
            pass  # warmup is best-effort

    # ✅ Fetch details page and extract __NEXT_DATA__ using the same robust extractor
    # Passing the full URL is supported by http_client.build_url()
    res = client.get_json(path=url, params={})

    return DetailsFetchResult(
        url=res.url,
        http_status=res.status_code,
        next_data=res.json_data,
    )
