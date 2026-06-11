# Cairo Compound Villa Prices (3BR/2Bath - 2026)

## Overview
This dataset contains a specialized, highly target niche dataset of luxury villas for sale in Cairo's compound neighborhoods (Fifth Settlement, New Cairo) featuring 3 bedrooms and 2 bathrooms, scraped in early 2026.

## Cleaning & Compliance Audit
- **PII Redaction**: Programmatically scanned and redacted 159 phone numbers and emails inside descriptions, replacing them with `[REDACTED_PHONE]` or `[REDACTED_EMAIL]` to ensure Kaggle policy compliance.
- **Schema Standardization**: Flattened nested pricing, location, and source objects into flat columns.
- **Feature Engineering**: Added `price_per_sqft` (price divided by sqm size), `amenity_count`, `location_depth`, `has_coordinates`, `is_size_outlier`, `is_price_outlier`.

## Included CSV Files
- `egypt_villas_3br_2bath.csv`: Flattened, PII-redacted luxury villa listings.

## Potential Use Cases
1. **Targeted Price Modeling**: Predict price variations between different compound developers in New Cairo.
2. **Geospatial Asset Location**: Map villa clusters in Cairo's compounds.

## License
Open Database License (ODbL) 1.0.
