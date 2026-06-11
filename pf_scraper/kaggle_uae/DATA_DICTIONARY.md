# Data Dictionary - Dubai Real Estate Datasets

| Field Name | Data Type | Description | Null % | Cardinality | Example Value |
| --- | --- | --- | --- | --- | --- |
| `amenities` | list | JSON list of amenity shortcodes | 0.0% | >=100 | `['BA', 'BW', 'AC']` |
| `amenity_count` | int | Calculated value: total amenities listed | 0.0% | 28 | `3` |
| `bathrooms` | int | Number of bathrooms in property | 0.1% | 7 | `3` |
| `bedrooms` | int | Number of bedrooms (0 or null indicates studio) | 11.1% | 6 | `3` |
| `category` | str | Market sector classification (rent, buy, new_projects, etc.) | 0.0% | 1 | `rent` |
| `currency` | str | Currency of transaction (AED or EGP) | 0.0% | 1 | `AED` |
| `has_coordinates` | bool | Boolean feature indicating coordinate completeness | 0.0% | 1 | `True` |
| `id` | str | Unique listing ID from the property finder platform | 0.0% | >=100 | `16295055` |
| `images` | list | JSON list of image URLs | 0.0% | >=100 | `['https://static.shared.propertyfin...` |
| `is_price_outlier` | bool | Heuristic flag indicating IQR price outlier | 0.0% | 2 | `False` |
| `is_size_outlier` | bool | Heuristic flag indicating size outlier | 0.0% | 2 | `False` |
| `latitude` | float | GPS latitude coordinate of the property listing | 0.0% | >=100 | `25.11564064025879` |
| `location` | str | Address string representing hierarchy of locations | 0.0% | >=100 | `Al Liwan Building, Dubai Silicon Oa...` |
| `location_depth` | int | Calculated value: levels of nested address paths | 0.0% | 5 | `3` |
| `longitude` | float | GPS longitude coordinate of the property listing | 0.0% | >=100 | `55.38821029663086` |
| `page` | int | Feature engineered or standardized platform field | 0.0% | >=100 | `8` |
| `price` | float | Listed rental cost (per year) or purchase price | 0.0% | >=100 | `115000.0` |
| `price_per_sqft` | float | Calculated value: listing price divided by area size | 0.0% | >=100 | `63.888888888888886` |
| `property_type` | str | Class of building (Apartment, Villa, Land, Office Space, etc.) | 0.0% | 1 | `Apartment` |
| `record_type` | str | Data row record classification (property or project) | 0.0% | 1 | `property` |
| `scraped_at_utc` | str | Scraping timestamp in UTC (ISO 8601 format) | 0.0% | >=100 | `2026-02-13T13:38:16.242976+00:00` |
| `share_url` | str | Direct sharing link to listing page | 0.0% | >=100 | `https://www.propertyfinder.ae/en/pl...` |
| `size` | float | Property area size in square feet | 0.0% | >=100 | `1800.0` |
| `title` | str | Cleaned property title used for marketing | 0.0% | >=100 | `3BHK Apartment | Closed Kitchen | S...` |
