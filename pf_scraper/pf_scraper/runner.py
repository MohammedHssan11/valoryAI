# pf_scraper/runner.py
from typing import Any, Dict, Optional

from .config import ScraperConfig
from .http_client import PropertyFinderHTTPClient
from .parser import parse_page, summarize_payload
from .url_builder import build_request


def fetch_one_page(
    cfg: ScraperConfig,
    category_name: str,
    page: int = 1,
    extra_filters: Optional[Dict[str, Any]] = None
) -> None:
    client = PropertyFinderHTTPClient(cfg=cfg)
    path, params = build_request(category_name, page=page, extra=extra_filters)

    result = client.get_json(path=path, params=params)

    parsed, found_path = parse_page(result.json_data, category=category_name, page=page)
    summary = summarize_payload(result.json_data)

    print("OK ✅")
    print(f"Fetched URL: {result.url}")
    print(f"HTTP: {result.status_code}")
    print(f"Content-Type: {result.final_content_type}")

    print("\n--- JSON Debug Summary ---")
    print(f"Top-level keys: {summary['top_level_keys']}")
    print(f"pageProps keys: {summary['pageProps_keys']}")
    print(f"Listings found at: {summary['listings_found_path']}")
    print(f"Listings count: {summary['listings_count']}")

    print("\n--- Parsed Preview (up to 3) ---")
    for row in parsed[:3]:
        d = row.to_dict() if hasattr(row, "to_dict") else dict(row)
        d["images"] = (d.get("images") or [])[:2]
        print(d)

    if not parsed:
        print(f"\n⚠️ Parsed 0 items. (path={found_path})")
