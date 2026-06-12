# 02. Data Engineering & Scraping Pipeline

This document details the data ingestion, sanitization, feature engineering, and geocoding validation pipelines of the ValorAI platform. It is reverse-engineered directly from the scraper scripts, CSV cleaning files, and geographic database constraints.

```mermaid
graph LR
    HTML[Raw SSR HTML] -->|NEXT_DATA Extraction| NextData[__NEXT_DATA__ JSON Block]
    NextData -->|JSON Parser| StandardListings[Standardized Fields]
    StandardListings -->|Deduplication| UniqueListings[Unique Listings]
    UniqueListings -->|Filters: Price, Coordinates, Size| CleanCSV[Cleaned CSV Output]
    CleanCSV -->|DB Importer| PostgreSQL[(PostgreSQL + PostGIS)]
    
    subgraph Data Validation
        Filters[Price > 100 EGP]
        Bounds[Egypt Box: Lat 22-32.5, Lng 24-36]
        Sizes[Size: 5-10,000 sqm]
    end
    CleanCSV -.-> Data\ Validation
```

---

## 1. Scraping Architecture & NEXT_DATA Ingestion
The primary data source for the valuation platform is property listings scraped from **PropertyFinder Egypt**. The ingestion architecture is structured to retrieve search payloads dynamically from server-side rendered HTML without the overhead of browser automation (headless chrome).

### NEXT_DATA Extraction
* **Source File:** [egy_scraper.py:9-19](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/pf_scraper/egy_scraper.py#L9-L19)
* **Strategy:** PropertyFinder search pages render listing structures inside a JSON script block `<script id="__NEXT_DATA__" type="application/json">`. The function `extract_next_data_from_html` parses this string block using basic index string searching:
  - Searches for `id="__NEXT_DATA__"` marker.
  - Matches the opening boundary `>` and closing boundary `</script>`.
  - Deserializes the raw text into a Python dictionary via `json.loads`.

### Crawl Loop & Page Control
* **Source File:** [egy_scraper.py:21-86](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/pf_scraper/egy_scraper.py#L21-L86)
* **Paginator:** The query parameters are manipulated (`set_page`) to step through page increments (e.g. `page=1`, `page=2`) up to `max_pages=200`.
* **Sleep Constraints:** To respect target server resource usage and prevent IP rate-limiting blocks, the crawler enforces a sleep interval of `sleep_s = 1.2` seconds between HTTP requests.
* **Stop Criteria:** The crawler halts if:
  1. An HTTP request returns a non-200 status code.
  2. The page parser returns `0` listing rows.
  3. No new (unseen) listing IDs are retrieved across `stop_after_no_new_pages = 2` consecutive page crawls.

---

## 2. In-Memory Parsing & Schema Mapping
Raw dictionaries are parsed and normalized in-memory into typed data structures.
* **Source File:** [parser.py:397-460](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/pf_scraper/parser.py#L397-L460)
* **Function:** `parse_listing`

### The Unified Listings Schema
Parsed properties are mapped to a structured class (`ParsedProperty`) with the following fields:

| Field Name | Type | Description |
|---|---|---|
| `id` | `str` | Listing ID on the source portal. |
| `title` | `str` | Title descriptor of the listing. |
| `price` | `float \| None` | Bounded price value in EGP. |
| `currency` | `str \| None` | Currency code (typically `EGP`). |
| `price_period` | `str \| None` | Extracted price period (e.g. `rent`, `buy`). |
| `price_type` | `str` | Classification (`sale_price`, `rent_price`, `suspicious_low`, `hidden`, `unknown`). |
| `price_raw_value` | `float \| None` | Raw numeric value before filtering. |
| `property_type` | `str \| None` | Flat descriptor (e.g. `Apartment`, `Villa`, `Duplex`). |
| `location` | `str \| None` | Raw location descriptor path. |
| `latitude` | `float \| None` | Latitude coordinate. |
| `longitude` | `float \| None` | Longitude coordinate. |
| `images` | `list[str]` | List of listing image URLs. |
| `bedrooms` | `int \| None` | Numeric bedroom count. |
| `bathrooms` | `int \| None` | Numeric bathroom count. |
| `size` | `float \| None` | Total property area in square meters. |
| `amenities` | `list[str]` | List of amenity codes. |
| `category` | `str` | Ingestion category (`rent`, `buy`, `commercial_rent`, `commercial_buy`, `new_projects`). |
| `page` | `int` | Source page number of the listing. |
| `scraped_at_utc` | `str` | ISO 8601 timestamp of crawler extraction. |

---

## 3. Data Cleaning & Sanitization Filters
Raw crawler outputs are sanitized in a batch process to ensure the pricing engine operates on high-integrity data.
* **Source File:** [01_clean_all.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/01_clean_all.py)
* **Function:** `clean_one`

### Cleaning Steps & Heuristic Rules
1. **Mandatory Fields:** Drops any listings missing `price` or `size` values.
2. **Placeholder Pruning:** Removes listings with placeholder prices ($P_{EGP} \le 100$ EGP), which are typically used by agents to artificially rank listings higher.
3. **Geographic Coordinate Bounding Box:**
   - Listings that are not classified as `new_projects` must have coordinates.
   - Latitude and longitude must fall within Egypt's national geographic boundaries:
     $$\text{Latitude} \in [22.0, 32.5] \quad \text{and} \quad \text{Longitude} \in [24.0, 36.0]$$
4. **Size Sanity Limits:** Sizes must be greater than $5$ sqm and less than $10,000$ sqm.
5. **Studio Classification Override:** If the listing title contains "studio" or "ستوديو" (bilingual), the bedroom count is overridden to `0` to prevent studios from being grouped with 1-bedroom apartments.
6. **Deduplication:** A hash set tracks all seen listing IDs during the crawl loop, discarding duplicates at the parser stage.

---

## 4. Text Normalization & Alias Mapping
Real estate descriptions and location paths from scrapers often contain typos, stop words, and language variations. The platform normalizes strings to support exact matches in spatial registries.
* **Source Files:** [normalization.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/geo/normalization.py)
* **Stop Words & Synonyms:** Mutes common prefixes (e.g. `street`, `road`, `compound`) and folds Arabic character sets (e.g., matching standard alif variations).
* **Furnishing Map:** Maps string values to a structured vocabulary:
  - `furnished` $\rightarrow$ `'furnished'`
  - `unfurnished` $\rightarrow$ `'unfurnished'`
  - `semi-furnished` $\rightarrow$ `'semi-furnished'`
* **Geocoding Alias Table:** Maps typos or common alternative names (e.g. "Zayed City" $\rightarrow$ "Sheikh Zayed") using the `location_aliases` table before calling the Google Maps API.

---

## 5. H3 Spatial Indexing
For the Machine Learning regressor, geographic coordinates are indexed into hexagonal cells using the Uber H3 spatial index system.
* **H3 Resolution 8 (`h3_res8`):** Bounded cells of approximately 0.7 square kilometers. Used for broader district-level feature grouping.
* **H3 Resolution 9 (`h3_res9`):** Bounded cells of approximately 0.1 square kilometers. Used for compound-level coordinate resolution.
* **Calculation:**
  ```python
  # ml_service.py:69-70
  row["h3_res8"] = h3.latlng_to_cell(req.lat, req.lng, 8)
  row["h3_res9"] = h3.latlng_to_cell(req.lat, req.lng, 9)
  ```
* **Exposure Registry:** The system uses these indices to build the `exposure_registry.json`. If a valuation request falls into an H3 index cell that contains fewer than 5 historical listings, it is flagged as `unseen_h3 = True` to adjust valuation routing.

---

## 6. Google Maps Geocoding & Address Resolution Cache
Address-based valuations rely on the Google Maps Geocoding API to resolve coordinates, which introduces network latency and API costs.
* **Geocoding Cache:** [address_resolver.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/geo/address_resolver.py)
* **Table:** `address_resolution_cache`
* **Workflow:**
  1. The normalized string is checked against `address_resolution_cache` using a case-insensitive match on `raw_input`.
  2. **Cache Hit:** Resolves coordinates instantly (under 5ms) and skips the external Google Maps call.
  3. **Cache Miss:** Resolves coordinates via Google Maps, performs a PostGIS area containment check, saves the result to the cache table, and returns coordinates.
* **Tenant Isolation:** Geocoding cache table data is shared globally to minimize API costs, but individual workspace queries remain strictly tenant-isolated via JWT tokens.
