# Dubai Real Estate Market Listings & Prices (2026)

## Overview
This dataset contains cleaned, deduplicated, and feature-engineered real estate listings in Dubai, UAE, scraped in early 2026 from Property Finder. It covers residential rentals, residential sales, commercial rentals, commercial sales, and off-plan projects.

It provides deep insights into the Middle East's most dynamic property market, offering rich details on pricing, locations, properties, sizes, and amenities.

## Cleaning and Validation Process
- **Deduplication**: Programmatic consolidation of duplicate listing IDs. Crawler double-scraped records were filtered, keeping the most complete records.
- **Outlier Detection**: Flagged size outliers (< 100 sq ft or > 30,000 sq ft for apartments) and pricing outliers using IQR boundaries.
- **Coordinate Correction**: Corrected Azizi Milan 55 spatial outlier (longitude adjusted to 55.31902).
- **Feature Engineering**: Added calculated features: `price_per_sqft`, `amenity_count`, `location_depth`, `has_coordinates`, `is_size_outlier`, `is_price_outlier`.

## Included CSV Files
- `dubai_residential_rent.csv`: Deduplicated residential apartments for rent.
- `dubai_residential_buy.csv`: Deduplicated residential apartments for sale.
- `dubai_commercial_rent.csv`: Deduplicated commercial spaces (offices, retail) for rent.
- `dubai_commercial_buy.csv`: Deduplicated commercial spaces (offices, warehouses) for sale.
- `dubai_new_projects.csv`: Off-plan developer projects in Dubai.

## Potential Use Cases
1. **Price Regression**: Build machine learning models to predict rent/sale prices.
2. **Geospatial Analysis**: Visualizing pricing density across coordinates.
3. **NLP Marketing Analysis**: Extracting features from descriptive titles.

## License
Open Database License (ODbL) 1.0.
