# Data Dictionary - Egypt Compounds Villa Dataset

| Field Name | Data Type | Description | Null % | Cardinality | Example Value |
| --- | --- | --- | --- | --- | --- |
| `amenities` | list | JSON list of amenity shortcodes | 0.0% | >=100 | `['BA', 'CP', 'PG', 'SP', 'ST', 'VW'...` |
| `amenity_count` | int | Calculated value: total amenities listed | 0.0% | 18 | `11` |
| `amenity_names` | list | JSON list of amenity long descriptions | 0.0% | >=100 | `['Balcony', 'Covered Parking', 'Pri...` |
| `bathrooms` | int | Number of bathrooms in property | 0.0% | 1 | `2` |
| `bedrooms` | int | Number of bedrooms (0 or null indicates studio) | 0.0% | 1 | `3` |
| `category` | str | Market sector classification (rent, buy, new_projects, etc.) | 0.0% | 1 | `buy` |
| `currency` | str | Currency of transaction (AED or EGP) | 0.0% | 1 | `EGP` |
| `description` | str | Full textual description (PII-redacted where applicable) | 0.0% | >=100 | `A prime location villa with a fanta...` |
| `details_path` | str | Platform relative URL snippet for details page | 0.0% | >=100 | `/en/plp/buy/villa-for-sale-cairo-ne...` |
| `has_coordinates` | bool | Boolean feature indicating coordinate completeness | 0.0% | 1 | `True` |
| `id` | str | Unique listing ID from the property finder platform | 0.0% | >=100 | `8514666` |
| `images` | list | JSON list of image URLs | 0.0% | >=100 | `['https://static.shared.propertyfin...` |
| `images_count` | int | Total image count in listing gallery | 0.0% | 27 | `9` |
| `is_premium` | bool | Boolean flag indicating premium advertising option | 0.0% | 2 | `True` |
| `is_price_outlier` | bool | Heuristic flag indicating IQR price outlier | 0.0% | 2 | `False` |
| `is_size_outlier` | bool | Heuristic flag indicating size outlier | 0.0% | 2 | `False` |
| `is_verified` | bool | Boolean flag indicating verified property coordinates/data | 0.0% | 1 | `False` |
| `latitude` | float | GPS latitude coordinate of the property listing | 0.0% | >=100 | `30.037769317626953` |
| `listed_date` | str | Original publication date of listing | 0.0% | >=100 | `2026-01-07T16:32:29Z` |
| `listing_id` | str | Platform specific secondary listing identifier | 0.0% | >=100 | `N1QPZB2MF4V1T1KXTKX02DWB5W` |
| `location_depth` | int | Calculated value: levels of nested address paths | 0.0% | 4 | `5` |
| `location_full_name` | str | Flattened full address location path name | 0.0% | >=100 | `Azzar 2, 5th Settlement Compounds, ...` |
| `location_id` | str | Platform specific location identifier | 0.0% | >=100 | `41137` |
| `location_path_name` | str | Hierarchical address path representation | 0.0% | 58 | `Cairo, New Cairo City, The 5th Sett...` |
| `location_slug` | str | SEO slug for platform location URLs | 0.0% | >=100 | `new-cairo-city-the-5th-settlement-5...` |
| `location_type` | str |  платформы address block category (STREET, BUILDING, etc.) | 0.0% | 6 | `STREET` |
| `longitude` | float | GPS longitude coordinate of the property listing | 0.0% | >=100 | `31.534711837768555` |
| `price` | int | Listed rental cost (per year) or purchase price | 0.0% | >=100 | `13700000` |
| `price_per_sqft` | float | Calculated value: listing price divided by area size | 0.0% | >=100 | `79190.7514450867` |
| `property_type` | str | Class of building (Apartment, Villa, Land, Office Space, etc.) | 0.0% | 1 | `Villa` |
| `record_type` | str | Data row record classification (property or project) | 0.0% | 1 | `property` |
| `scraped_at_utc` | str | Scraping timestamp in UTC (ISO 8601 format) | 0.0% | >=100 | `2026-01-07T16:32:29Z` |
| `share_url` | str | Direct sharing link to listing page | 0.0% | >=100 | `https://www.propertyfinder.eg/en/pl...` |
| `size_sqm` | int | Property area size in square meters | 0.0% | >=100 | `173` |
| `size_sqm_reported` | int | Uncorrected area size in square meters reported by scraper | 0.0% | >=100 | `173` |
| `source_country_code` | str | Scraped site country code (AE or EG) | 0.0% | 1 | `EG` |
| `source_provider` | str | Data source site provider reference | 0.0% | 1 | `propertyfinder` |
| `title` | str | Cleaned property title used for marketing | 0.0% | >=100 | `Luxury villa with the lowest price,...` |
