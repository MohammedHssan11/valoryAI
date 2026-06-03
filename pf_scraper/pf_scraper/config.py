# pf_scraper/config.py
from dataclasses import dataclass
from typing import Dict, Any


# =========================================================
# DEFAULT HTTP HEADERS
# =========================================================
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


# =========================================================
# COUNTRY CONFIGURATION
# =========================================================
COUNTRY_BASE_URLS = {
    "UAE": "https://www.propertyfinder.ae",
    "EG": "https://www.propertyfinder.eg",
}


# =========================================================
# CATEGORY DEFINITIONS (Search-based unified system)
# =========================================================
# Works for both UAE and EG (search SSR uses same structure)
#
# Each category defines:
# - path: search endpoint
# - page_param: pagination parameter
# - params: fixed base query parameters
# =========================================================

CATEGORY_DEFS = {

    # =====================================================
    # UAE (uses /en/search SSR endpoint)
    # =====================================================

    "rent": {
        "uae_path": "/en/search",
        "eg_path": "/en/rent/properties-for-rent.html",
        "page_param": "page",
        "uae_params": {
            "c": 2,
            "t": 1,
            "l": 1,
            "fu": 0,
            "ob": "mr",
        },
        "eg_params": {},
    },

    "buy": {
        "uae_path": "/en/search",
        "eg_path": "/en/buy/properties-for-sale.html",
        "page_param": "page",
        "uae_params": {
            "c": 1,
            "t": 1,
            "l": 1,
            "fu": 0,
            "ob": "mr",
        },
        "eg_params": {},
    },

    "commercial_rent": {
        "uae_path": "/en/search",
        "eg_path": "/en/commercial-rent/properties-for-rent.html",
        "page_param": "page",
        "uae_params": {
            "c": 2,
            "t": 2,
            "l": 1,
            "fu": 0,
            "ob": "mr",
        },
        "eg_params": {},
    },

    "commercial_buy": {
        "uae_path": "/en/search",
        "eg_path": "/en/commercial-buy/properties-for-sale.html",
        "page_param": "page",
        "uae_params": {
            "c": 1,
            "t": 2,
            "l": 1,
            "fu": 0,
            "ob": "mr",
        },
        "eg_params": {},
    },

    "new_projects": {
        "uae_path": "/en/new-projects",
        "eg_path": "/en/new-projects",
        "page_param": "page",
        "uae_params": {},
        "eg_params": {},
    },
}



# =========================================================
# CATEGORIES (Used by CLI & multi_runner)
# =========================================================
CATEGORIES = list(CATEGORY_DEFS.keys())


# =========================================================
# GLOBAL SCRAPER CONFIG
# =========================================================
@dataclass
class ScraperConfig:
    country: str = "UAE"      # change to "EG" to switch country
    timeout_s: float = 25.0
    max_retries: int = 6

    @property
    def base_url(self) -> str:
        return COUNTRY_BASE_URLS.get(self.country.upper(), COUNTRY_BASE_URLS["UAE"])
