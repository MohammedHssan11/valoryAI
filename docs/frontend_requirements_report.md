# Frontend Requirements Report — Real-Estate Valuation Platform (Egypt)

**Author:** Senior Data Product Analyst & Senior Frontend Architect

**Date:** June 2, 2026

**Status:** Production Specifications

## Executive Summary

This report outlines the complete frontend requirements for the Egypt Real-Estate Valuation Platform, derived **strictly and solely** from reverse-engineering the provided scraper datasets (`buy.jsonl`, `rent.jsonl`, `commercial_buy.jsonl`, `commercial_rent.jsonl`, and `new_projects.jsonl`).

Through exhaustive data profiling, we have mapped out the property taxonomy, location hierarchy, search filters, amenity classifications, form validation specifications, and enums required for a state-of-the-art web application. Additionally, we have performed a rigorous data quality audit to highlight the limitations and risks of the current data structure to guide robust client-side validation and exception handling.

## Phase 1 — Dataset Discovery

The platform dataset consists of 5 distinct categories representing active listings and real estate projects across Egypt. The dataset characteristics are detailed below:

### Category: Buy
- **Total File Lines**: 19,967
- **Parsed Records**: 19,967
- **Failed Parses (Invalid JSON)**: 0

| Field Name | Missing % | Unique Values |
| :--- | :---: | :---: |
| `amenities` | 0.15% | 18 |
| `bathrooms` | 0.15% | 7 |
| `bedrooms` | 2.83% | 7 |
| `category` | 0.00% | 1 |
| `currency` | 0.00% | 1 |
| `id` | 0.00% | 19,967 |
| `images` | 0.00% | 39,934 |
| `latitude` | 0.00% | 1,368 |
| `location` | 0.00% | 1,503 |
| `longitude` | 0.01% | 1,369 |
| `page` | 0.00% | 800 |
| `price` | 0.01% | 4,291 |
| `price_period` | 0.00% | 1 |
| `price_raw_value` | 0.00% | 4,293 |
| `price_type` | 0.00% | 2 |
| `property_type` | 0.00% | 17 |
| `record_type` | 0.00% | 1 |
| `scraped_at_utc` | 0.00% | 1,039 |
| `share_url` | 0.00% | 19,967 |
| `size` | 0.00% | 681 |
| `title` | 0.00% | 17,459 |

### Category: Rent
- **Total File Lines**: 19,979
- **Parsed Records**: 19,979
- **Failed Parses (Invalid JSON)**: 0

| Field Name | Missing % | Unique Values |
| :--- | :---: | :---: |
| `amenities` | 0.01% | 18 |
| `bathrooms` | 0.00% | 7 |
| `bedrooms` | 3.50% | 7 |
| `category` | 0.00% | 1 |
| `currency` | 0.00% | 1 |
| `id` | 0.00% | 19,979 |
| `images` | 0.00% | 39,958 |
| `latitude` | 0.00% | 936 |
| `location` | 0.00% | 1,019 |
| `longitude` | 0.00% | 940 |
| `page` | 0.00% | 800 |
| `price` | 0.00% | 794 |
| `price_period` | 0.00% | 1 |
| `price_raw_value` | 0.00% | 794 |
| `price_type` | 0.00% | 1 |
| `property_type` | 0.00% | 13 |
| `record_type` | 0.00% | 1 |
| `scraped_at_utc` | 0.00% | 1,033 |
| `share_url` | 0.00% | 19,979 |
| `size` | 0.00% | 491 |
| `title` | 0.00% | 15,683 |

### Category: Commercial Buy
- **Total File Lines**: 8,959
- **Parsed Records**: 8,959
- **Failed Parses (Invalid JSON)**: 0

| Field Name | Missing % | Unique Values |
| :--- | :---: | :---: |
| `amenities` | 2.12% | 10 |
| `bathrooms` | 17.51% | 7 |
| `bedrooms` | 54.41% | 7 |
| `category` | 0.00% | 1 |
| `currency` | 0.00% | 1 |
| `id` | 0.00% | 8,959 |
| `images` | 0.00% | 17,918 |
| `latitude` | 0.00% | 1,168 |
| `location` | 0.00% | 1,284 |
| `longitude` | 0.00% | 1,168 |
| `page` | 0.00% | 359 |
| `price` | 0.07% | 3,126 |
| `price_period` | 0.00% | 1 |
| `price_raw_value` | 0.00% | 3,129 |
| `price_type` | 0.00% | 2 |
| `property_type` | 0.00% | 18 |
| `record_type` | 0.00% | 1 |
| `scraped_at_utc` | 0.00% | 526 |
| `share_url` | 0.00% | 8,959 |
| `size` | 0.00% | 756 |
| `title` | 0.00% | 7,873 |

### Category: Commercial Rent
- **Total File Lines**: 14,080
- **Parsed Records**: 14,080
- **Failed Parses (Invalid JSON)**: 0

| Field Name | Missing % | Unique Values |
| :--- | :---: | :---: |
| `amenities` | 0.45% | 14 |
| `bathrooms` | 8.22% | 7 |
| `bedrooms` | 30.21% | 7 |
| `category` | 0.00% | 1 |
| `currency` | 0.00% | 1 |
| `id` | 0.00% | 14,080 |
| `images` | 0.00% | 28,160 |
| `latitude` | 0.00% | 1,100 |
| `location` | 0.00% | 1,196 |
| `longitude` | 0.00% | 1,100 |
| `page` | 0.00% | 564 |
| `price` | 0.00% | 1,927 |
| `price_period` | 0.00% | 1 |
| `price_raw_value` | 0.00% | 1,927 |
| `price_type` | 0.00% | 1 |
| `property_type` | 0.00% | 19 |
| `record_type` | 0.00% | 1 |
| `scraped_at_utc` | 0.00% | 681 |
| `share_url` | 0.00% | 14,080 |
| `size` | 0.00% | 767 |
| `title` | 0.00% | 11,279 |

### Category: New Projects
- **Total File Lines**: 1,121
- **Parsed Records**: 1,121
- **Failed Parses (Invalid JSON)**: 0

| Field Name | Missing % | Unique Values |
| :--- | :---: | :---: |
| `category` | 0.00% | 1 |
| `currency` | 100.00% | 0 |
| `id` | 0.00% | 1,121 |
| `images` | 0.00% | 5,920 |
| `latitude` | 0.00% | 777 |
| `location` | 100.00% | 0 |
| `longitude` | 0.00% | 777 |
| `max_price` | 100.00% | 0 |
| `min_price` | 100.00% | 0 |
| `page` | 0.00% | 47 |
| `record_type` | 0.00% | 1 |
| `scraped_at_utc` | 0.00% | 55 |
| `title` | 0.00% | 1,119 |

## Phase 2 — Property Taxonomy

Below is the distribution of all property types discovered in the dataset. Property types are classified by category to define validation scopes and frontend select lists.

| Property Type | Category | Count | Percentage |
| :--- | :--- | :---: | :---: |
| Apartment | Buy | 10,277 | 51.47% |
| Apartment | Rent | 14,810 | 74.13% |
| Bulk Rent Unit | Commercial Rent | 34 | 0.24% |
| Bulk Sale Unit | Buy | 1 | 0.01% |
| Bulk Sale Unit | Commercial Buy | 39 | 0.44% |
| Bungalow | Rent | 7 | 0.04% |
| Cabin | Buy | 23 | 0.12% |
| Cabin | Rent | 7 | 0.04% |
| Cafeteria | Commercial Buy | 25 | 0.28% |
| Cafeteria | Commercial Rent | 18 | 0.13% |
| Chalet | Buy | 2,119 | 10.61% |
| Chalet | Rent | 73 | 0.37% |
| Clinic | Commercial Buy | 1,092 | 12.19% |
| Clinic | Commercial Rent | 650 | 4.62% |
| Co-Working Space | Commercial Rent | 188 | 1.34% |
| Duplex | Buy | 631 | 3.16% |
| Duplex | Rent | 936 | 4.68% |
| Factory | Commercial Buy | 105 | 1.17% |
| Factory | Commercial Rent | 104 | 0.74% |
| Farm | Commercial Buy | 20 | 0.22% |
| Full Floor | Buy | 2 | 0.01% |
| Full Floor | Commercial Buy | 60 | 0.67% |
| Full Floor | Commercial Rent | 209 | 1.48% |
| Half Floor | Buy | 1 | 0.01% |
| Half Floor | Commercial Buy | 18 | 0.20% |
| Half Floor | Commercial Rent | 48 | 0.34% |
| Hotel Apartment | Buy | 129 | 0.65% |
| Hotel Apartment | Commercial Buy | 33 | 0.37% |
| Land | Buy | 30 | 0.15% |
| Land | Commercial Buy | 138 | 1.54% |
| Land | Commercial Rent | 13 | 0.09% |
| Medical Facility | Commercial Buy | 167 | 1.86% |
| Medical Facility | Commercial Rent | 31 | 0.22% |
| Office Space | Commercial Buy | 3,966 | 44.27% |
| Office Space | Commercial Rent | 10,320 | 73.30% |
| Palace | Buy | 6 | 0.03% |
| Palace | Rent | 15 | 0.08% |
| Penthouse | Buy | 594 | 2.97% |
| Penthouse | Rent | 619 | 3.10% |
| Restaurant | Commercial Buy | 111 | 1.24% |
| Restaurant | Commercial Rent | 65 | 0.46% |
| Retail | Commercial Buy | 600 | 6.70% |
| Retail | Commercial Rent | 366 | 2.60% |
| Roof | Buy | 6 | 0.03% |
| Roof | Rent | 54 | 0.27% |
| Shop | Commercial Buy | 2,255 | 25.17% |
| Shop | Commercial Rent | 1,199 | 8.52% |
| Show Room | Commercial Buy | 41 | 0.46% |
| Show Room | Commercial Rent | 79 | 0.56% |
| Staff Accommodation | Commercial Rent | 2 | 0.01% |
| Townhouse | Buy | 1,477 | 7.40% |
| Townhouse | Rent | 632 | 3.16% |
| Twin House | Buy | 909 | 4.55% |
| Twin House | Rent | 606 | 3.03% |
| Villa | Buy | 3,458 | 17.32% |
| Villa | Rent | 1,995 | 9.99% |
| Villa | Commercial Buy | 9 | 0.10% |
| Villa | Commercial Rent | 122 | 0.87% |
| Warehouse | Commercial Buy | 33 | 0.37% |
| Warehouse | Commercial Rent | 189 | 1.34% |
| Whole Building | Buy | 15 | 0.08% |
| Whole Building | Rent | 4 | 0.02% |
| Whole Building | Commercial Buy | 247 | 2.76% |
| Whole Building | Commercial Rent | 439 | 3.12% |
| iVilla | Buy | 289 | 1.45% |
| iVilla | Rent | 221 | 1.11% |
| iVilla | Commercial Rent | 4 | 0.03% |

## Phase 3 — Location Discovery

The location structure is hierarchically formatted as a comma-separated text string. By splitting location strings from right to left, we discovered a 4-tier hierarchy: **Governorate (Tier 1) -> City (Tier 2) -> District (Tier 3) -> Compound / Street (Tier 4)**.

- **Total Unique Governorates**: 20
- **Total Unique Cities**: 107
- **Total Unique Districts**: 691
- **Total Unique Compounds**: 1678

### Location Popularity for Buy

| Hierarchy Level | Top Value | Frequency |
| :--- | :--- | :---: |
| Governorate (Tier 1) | Cairo | 9,719 |
| Citie (Tier 2) | New Cairo City | 6,824 |
| District (Tier 3) | The 5th Settlement | 4,823 |
| Compound (Tier 4) | 5th Settlement Compounds | 4,227 |

#### Top 5 Governorates, Cities, Districts, and Compounds
- **Governorates**: **Cairo** (9,719), **Giza** (5,290), **Red Sea** (1,928), **North Coast** (1,740), **Suez** (904)
- **Cities**: **New Cairo City** (6,824), **6 October City** (2,570), **Sheikh Zayed City** (2,547), **Hurghada** (1,928), **Al Ain Al Sokhna** (904)
- **Districts**: **The 5th Settlement** (4,823), **Sheikh Zayed Compounds** (1,573), **6 October Compounds** (1,101), **Mostakbal City Compounds** (880), **New Zayed City** (571)
- **Compounds**: **5th Settlement Compounds** (4,227), **Soma Bay** (411), **O West** (287), **Sarai** (279), **New Giza** (205)

### Location Popularity for Rent

| Hierarchy Level | Top Value | Frequency |
| :--- | :--- | :---: |
| Governorate (Tier 1) | Cairo | 16,046 |
| Citie (Tier 2) | New Cairo City | 12,948 |
| District (Tier 3) | The 5th Settlement | 7,999 |
| Compound (Tier 4) | 5th Settlement Compounds | 7,222 |

#### Top 5 Governorates, Cities, Districts, and Compounds
- **Governorates**: **Cairo** (16,046), **Giza** (3,628), **Alexandria** (160), **North Coast** (114), **Red Sea** (24)
- **Cities**: **New Cairo City** (12,948), **Sheikh Zayed City** (2,221), **6 October City** (1,278), **Madinaty** (970), **Hay El Maadi** (743)
- **Districts**: **The 5th Settlement** (7,999), **Sheikh Zayed Compounds** (1,758), **North Investors Area** (1,075), **Privado** (871), **Al Rehab** (858)
- **Compounds**: **5th Settlement Compounds** (7,222), **Cairo Festival City** (784), **El Katameya Compounds** (736), **El Rehab Extension** (562), **Fifth Square** (435)

### Location Popularity for Commercial Buy

| Hierarchy Level | Top Value | Frequency |
| :--- | :--- | :---: |
| Governorate (Tier 1) | Cairo | 4,849 |
| Citie (Tier 2) | New Cairo City | 3,073 |
| District (Tier 3) | The 5th Settlement | 2,241 |
| Compound (Tier 4) | 5th Settlement Compounds | 1,030 |

#### Top 5 Governorates, Cities, Districts, and Compounds
- **Governorates**: **Cairo** (4,849), **Giza** (2,909), **Alexandria** (794), **Qalyubia** (98), **Al Daqahlya** (66)
- **Cities**: **New Cairo City** (3,073), **6 October City** (1,397), **Sheikh Zayed City** (1,346), **New Capital City** (584), **Hay Sharq** (440)
- **Districts**: **The 5th Settlement** (2,241), **26th of July Corridor** (523), **Sheikh Zayed Compounds** (434), **Waslet Dahshur Road** (224), **Downtown Area** (197)
- **Compounds**: **5th Settlement Compounds** (1,030), **South Teseen St.** (502), **North Teseen St.** (425), **Arkan Palm 205** (158), **El Katameya Compounds** (148)

### Location Popularity for Commercial Rent

| Hierarchy Level | Top Value | Frequency |
| :--- | :--- | :---: |
| Governorate (Tier 1) | Cairo | 10,589 |
| Citie (Tier 2) | New Cairo City | 7,402 |
| District (Tier 3) | The 5th Settlement | 5,563 |
| Compound (Tier 4) | 5th Settlement Compounds | 2,441 |

#### Top 5 Governorates, Cities, Districts, and Compounds
- **Governorates**: **Cairo** (10,589), **Giza** (2,642), **Alexandria** (668), **Sharqia** (61), **Qalyubia** (49)
- **Cities**: **New Cairo City** (7,402), **Hay El Maadi** (1,666), **Sheikh Zayed City** (1,348), **6 October City** (608), **Heliopolis - Masr El Gedida** (437)
- **Districts**: **The 5th Settlement** (5,563), **North Investors Area** (620), **Sheikh Zayed Compounds** (531), **26th of July Corridor** (441), **Degla** (418)
- **Compounds**: **5th Settlement Compounds** (2,441), **North Teseen St.** (1,199), **South Teseen St.** (1,178), **Cairo Festival City** (457), **The Polygon** (241)

### Location Frontend UX Architecture

Based on the cardinality at each level, the following UI component mapping is required to ensure scalability and prevent interface slow-down:

1. **Governorate (20 unique values)**: Use a standard **Dropdown Select**. The low cardinality allows direct selection without overwhelming users.

2. **City (107 unique values)**: Use a **Searchable Select (Dropdown with Search Filter)**. Cities should be dynamically filtered as the user types.

3. **District (691 unique values)**: Use a **Type-ahead Autocomplete Component**. The component should query the backend after 2 characters have been typed, showing suggestions grouped by City.

4. **Compound / Street (1,678 unique values)**: Use a **Search-as-you-type Autocomplete Field**. Suggestion dropdowns should display the full hierarchical path (e.g. *New Giza, Sheikh Zayed Compounds, 6 October City, Giza*).

## Phase 4 — Filter Discovery

We identified the core filter fields and their boundary values in the dataset. This informs the range limits and selection components for search interfaces.

### Search Filters: Buy

| Filter Field | Boundary Min | Boundary Max | Median Value | Unique Values | Recommended UI Component |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Price | 200,000.0 | 1,000,000,000.0 | 10,000,000.0 | 4,291 | Dual Range Slider (Logarithmic scale) |
| Bedrooms | 1.0 | 7.0 | 3.0 | 7 | Button Group / Chips (1, 2, 3, 4, 5, 6, 7+) |
| Bathrooms | 1.0 | 7.0 | 3.0 | 7 | Button Group / Chips (1, 2, 3, 4, 5, 6, 7+) |
| Size | 1.0 | 21,000.0 | 165.0 | 681 | Min-Max Input Fields with Range Slider |

### Search Filters: Rent

| Filter Field | Boundary Min | Boundary Max | Median Value | Unique Values | Recommended UI Component |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Price | 1,300.0 | 550,000,000.0 | 65,000.0 | 794 | Dual Range Slider (Logarithmic scale) |
| Bedrooms | 1.0 | 7.0 | 3.0 | 7 | Button Group / Chips (1, 2, 3, 4, 5, 6, 7+) |
| Bathrooms | 1.0 | 7.0 | 3.0 | 7 | Button Group / Chips (1, 2, 3, 4, 5, 6, 7+) |
| Size | 6.0 | 3,500.0 | 188.0 | 491 | Min-Max Input Fields with Range Slider |

### Search Filters: Commercial Buy

| Filter Field | Boundary Min | Boundary Max | Median Value | Unique Values | Recommended UI Component |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Price | 100,000.0 | 1,000,000,000.0 | 10,700,000.0 | 3,126 | Dual Range Slider (Logarithmic scale) |
| Bedrooms | 1.0 | 7.0 | 2.0 | 7 | Button Group / Chips (1, 2, 3, 4, 5, 6, 7+) |
| Bathrooms | 1.0 | 7.0 | 1.0 | 7 | Button Group / Chips (1, 2, 3, 4, 5, 6, 7+) |
| Size | 1.0 | 2,520,000.0 | 82.0 | 756 | Min-Max Input Fields with Range Slider |

### Search Filters: Commercial Rent

| Filter Field | Boundary Min | Boundary Max | Median Value | Unique Values | Recommended UI Component |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Price | 1,000.0 | 350,000,000.0 | 120,950.0 | 1,927 | Dual Range Slider (Logarithmic scale) |
| Bedrooms | 1.0 | 7.0 | 3.0 | 7 | Button Group / Chips (1, 2, 3, 4, 5, 6, 7+) |
| Bathrooms | 1.0 | 7.0 | 2.0 | 7 | Button Group / Chips (1, 2, 3, 4, 5, 6, 7+) |
| Size | 1.0 | 400,200.0 | 200.0 | 767 | Min-Max Input Fields with Range Slider |

## Phase 5 — Amenities Analysis

Amenities are represented in the raw data as two-letter uppercase codes inside stringified arrays. Using the platform's backend `AMENITY_MAP`, we decoded these symbols to human-readable names and categorizations.

### Amenities Distribution: Buy

| Code | Display Name (English / Arabic) | Frequency | Percentage | Filter Classification |
| :---: | :--- | :---: | :---: | :--- |
| `BA` | Balcony / بلكونة | 18,888 | 94.60% | Core |
| `SE` | Security / أمن | 17,861 | 89.45% | Core |
| `SY` | Shared Gym / جيم مشترك | 13,505 | 67.64% | Leisure |
| `CP` | Covered Parking / جراج مغطى | 12,997 | 65.09% | Access |
| `BL` | Landmark View / إإطلالة مميزة | 12,422 | 62.21% | View |
| `SP` | Shared Pool / حمام سباحة مشترك | 12,375 | 61.98% | Leisure |
| `SS` | Shared Spa / سبا مشترك | 12,284 | 61.52% | Leisure |
| `LB` | Lobby in Building / لوبي | 11,100 | 55.59% | Core |
| `VW` | Water View / إإطلالة مائية | 10,550 | 52.84% | View |
| `WC` | Walk-in Closet / غرفة ملابس | 10,547 | 52.82% | Layout |
| `CO` | Children's Pool / حمام سباحة أطفال | 10,505 | 52.61% | Leisure |
| `ST` | Study / غرفة مكتب | 10,015 | 50.16% | Layout |
| `PG` | Private Garden / حديقة خاصة | 9,850 | 49.33% | Outdoor |
| `BW` | Built-in Wardrobes / دواليب مدمجة | 9,354 | 46.85% | Fitout |
| `MR` | Maid Room / غرفة مربية | 8,697 | 43.56% | Layout |
| `AC` | Central AC / تكييف مركزي | 8,476 | 42.45% | Core |
| `BK` | Kitchen Appliances / أجهزة مطبخ | 7,630 | 38.21% | Fitout |
| `PP` | Private Pool / حمام سباحة خاص | 6,302 | 31.56% | Leisure |

### Amenities Distribution: Rent

| Code | Display Name (English / Arabic) | Frequency | Percentage | Filter Classification |
| :---: | :--- | :---: | :---: | :--- |
| `BA` | Balcony / بلكونة | 18,581 | 93.00% | Core |
| `SE` | Security / أمن | 17,704 | 88.61% | Core |
| `AC` | Central AC / تكييف مركزي | 13,751 | 68.83% | Core |
| `BK` | Kitchen Appliances / أجهزة مطبخ | 13,299 | 66.56% | Fitout |
| `CP` | Covered Parking / جراج مغطى | 12,039 | 60.26% | Access |
| `BW` | Built-in Wardrobes / دواليب مدمجة | 11,235 | 56.23% | Fitout |
| `LB` | Lobby in Building / لوبي | 9,977 | 49.94% | Core |
| `BL` | Landmark View / إإطلالة مميزة | 9,936 | 49.73% | View |
| `SY` | Shared Gym / جيم مشترك | 9,104 | 45.57% | Leisure |
| `WC` | Walk-in Closet / غرفة ملابس | 7,762 | 38.85% | Layout |
| `SS` | Shared Spa / سبا مشترك | 7,123 | 35.65% | Leisure |
| `SP` | Shared Pool / حمام سباحة مشترك | 7,078 | 35.43% | Leisure |
| `ST` | Study / غرفة مكتب | 6,197 | 31.02% | Layout |
| `PG` | Private Garden / حديقة خاصة | 5,654 | 28.30% | Outdoor |
| `MR` | Maid Room / غرفة مربية | 5,489 | 27.47% | Layout |
| `CO` | Children's Pool / حمام سباحة أطفال | 5,187 | 25.96% | Leisure |
| `VW` | Water View / إإطلالة مائية | 4,888 | 24.47% | View |
| `PP` | Private Pool / حمام سباحة خاص | 2,451 | 12.27% | Leisure |

### Amenities Distribution: Commercial Buy

| Code | Display Name (English / Arabic) | Frequency | Percentage | Filter Classification |
| :---: | :--- | :---: | :---: | :--- |
| `AN` | Unknown Code (AN) | 7,595 | 84.78% | General / Unclassified |
| `LB` | Lobby in Building / لوبي | 6,840 | 76.35% | Core |
| `CP` | Covered Parking / جراج مغطى | 6,778 | 75.66% | Access |
| `CR` | Unknown Code (CR) | 5,562 | 62.08% | General / Unclassified |
| `DN` | Unknown Code (DN) | 4,453 | 49.70% | General / Unclassified |
| `SY` | Shared Gym / جيم مشترك | 3,752 | 41.88% | Leisure |
| `BA` | Balcony / بلكونة | 6 | 0.07% | Core |
| `SE` | Security / أمن | 3 | 0.03% | Core |
| `BW` | Built-in Wardrobes / دواليب مدمجة | 2 | 0.02% | Fitout |
| `AC` | Central AC / تكييف مركزي | 2 | 0.02% | Core |

### Amenities Distribution: Commercial Rent

| Code | Display Name (English / Arabic) | Frequency | Percentage | Filter Classification |
| :---: | :--- | :---: | :---: | :--- |
| `AN` | Unknown Code (AN) | 12,686 | 90.10% | General / Unclassified |
| `CP` | Covered Parking / جراج مغطى | 10,035 | 71.27% | Access |
| `CR` | Unknown Code (CR) | 9,466 | 67.23% | General / Unclassified |
| `LB` | Lobby in Building / لوبي | 9,118 | 64.76% | Core |
| `DN` | Unknown Code (DN) | 5,864 | 41.65% | General / Unclassified |
| `SY` | Shared Gym / جيم مشترك | 3,548 | 25.20% | Leisure |
| `SE` | Security / أمن | 6 | 0.04% | Core |
| `BA` | Balcony / بلكونة | 5 | 0.04% | Core |
| `BL` | Landmark View / إإطلالة مميزة | 4 | 0.03% | View |
| `ST` | Study / غرفة مكتب | 2 | 0.01% | Layout |
| `WC` | Walk-in Closet / غرفة ملابس | 2 | 0.01% | Layout |
| `BW` | Built-in Wardrobes / دواليب مدمجة | 2 | 0.01% | Fitout |
| `PG` | Private Garden / حديقة خاصة | 1 | 0.01% | Outdoor |
| `PN` | Unknown Code (PN) | 1 | 0.01% | General / Unclassified |

## Phase 6 — Data Quality Audit

To establish the validity of the data source, a data quality audit was conducted on all records. The following metrics list coordinate issues, missing rooms, missing size, and invalid price listings. A data quality score is assigned to each dataset.

### Data Quality Metrics Table

| Metric | Residential Buy | Residential Rent | Commercial Buy | Commercial Rent | New Projects |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Parsed Rows | 19,967 | 19,979 | 8,959 | 14,080 | 1,121 |
| Duplicate URLs | 0 | 0 | 0 | 0 | 0 |
| Duplicate Coords | 18,592 (93.1%) | 19,039 (95.3%) | 7,787 (86.9%) | 12,977 (92.2%) | 343 (30.6%) |
| Missing Coords | 1 | 0 | 0 | 0 | 0 |
| Invalid Coords | 0 | 0 | 20 | 65 | 48 |
| Missing Bedrooms | 565 (2.8%) | 699 (3.5%) | 4,875 (54.4%) | 4,253 (30.2%) | 1,121 (100.0%) |
| Missing Bathrooms | 30 (0.2%) | 0 (0.0%) | 1,569 (17.5%) | 1,158 (8.2%) | 1,121 (100.0%) |
| Missing Area | 0 | 0 | 0 | 0 | 1,121 (100.0%) |
| Invalid Prices | 2 | 0 | 6 | 0 | 1,121 (100.0%) |
| **Overall Quality Score** | **99.09%** | **98.95%** | **89.13%** | **94.28%** | **0.00%** |

## Phase 7 — Valuation Form Requirements

Validation rules are derived directly from the missingness of variables in each category. Required inputs represent variables that are consistently populated (0% missing) for valid valuation targets. Conditional logic adapts form inputs based on the selected property type.

### 1. Residential Buy Form Specification

- **Required Inputs**:
  - **Property Type**: Dropdown Select (must be one of the Residential Buy types).
  - **Area (Size)**: Numeric input (must be between 20 and 5,000 sqm).
  - **Location**: Searchable select / autocomplete hierarchy (Governorate, City, District).
- **Conditionally Required Inputs**:
  - **Bedrooms / Bathrooms**: Required if `property_type` is NOT `Land`. (For `Land`, these fields are disabled and hidden, as 96.7% of Land listings omit them).
- **Optional Inputs**:
  - **Compound**: Autocomplete select (optional fallback to 'Outside Compound').
  - **Amenities**: Multi-select chips grouped by type (Balcony, Gym, Pool, Security, etc.).
  - **Coordinates**: Pin on Map (optional fallback to District center).

### 2. Residential Rent Form Specification

- **Required Inputs**:
  - **Property Type**: Dropdown Select.
  - **Area (Size)**: Numeric input.
  - **Location**: Searchable select / autocomplete hierarchy.
- **Conditionally Required Inputs**:
  - **Bedrooms / Bathrooms**: Required if `property_type` is NOT `Land` or `Bungalow` (where bedrooms are consistently missing).
- **Optional Inputs**:
  - **Compound**, **Amenities**, **Coordinates**.

### 3. Commercial Buy Form Specification

- **Required Inputs**:
  - **Property Type**: Dropdown Select (must be one of the Commercial Buy types).
  - **Area (Size)**: Numeric input.
  - **Location**: Searchable select / autocomplete hierarchy.
- **Optional Inputs**:
  - **Bathrooms**: Optional field (missing in 17.51% of listings overall, and 28.8% of shops).
  - **Amenities**, **Coordinates**.
- **Disabled / Not Applicable**:
  - **Bedrooms**: Disabled and hidden. Bedrooms are missing in 54.41% of listings overall (and 98.6% of shops, 96.8% of retail), indicating they are irrelevant to commercial valuations.

### 4. Commercial Rent Form Specification

- **Required Inputs**:
  - **Property Type**, **Area (Size)**, **Location**.
- **Optional Inputs**:
  - **Bathrooms**: Optional field (missing in 8.22% of listings overall).
  - **Amenities**, **Coordinates**.
- **Disabled / Not Applicable**:
  - **Bedrooms**: Disabled and hidden. Bedrooms are missing in 30.21% of listings overall (and 98.2% of shops, 97.8% of retail).

## Phase 8 — Frontend Enums

The following JSON enums represent the exact values found in the datasets for property types, commercial types, amenities, cities, and districts, structured for production frontend consumption:

```json
{
  "PROPERTY_TYPES": [
    "Apartment",
    "Bulk Sale Unit",
    "Cabin",
    "Chalet",
    "Duplex",
    "Full Floor",
    "Half Floor",
    "Hotel Apartment",
    "Land",
    "Palace",
    "Penthouse",
    "Roof",
    "Townhouse",
    "Twin House",
    "Villa",
    "Whole Building",
    "iVilla"
  ],
  "COMMERCIAL_TYPES": [
    "Bulk Sale Unit",
    "Cafeteria",
    "Clinic",
    "Factory",
    "Farm",
    "Full Floor",
    "Half Floor",
    "Hotel Apartment",
    "Land",
    "Medical Facility",
    "Office Space",
    "Restaurant",
    "Retail",
    "Shop",
    "Show Room",
    "Villa",
    "Warehouse",
    "Whole Building"
  ],
  "AMENITIES": [
    {
      "code": "AC",
      "normalized": "central_ac",
      "name": "Central AC",
      "arabic": "تكييف مركزي",
      "group": "core"
    },
    {
      "code": "BA",
      "normalized": "balcony",
      "name": "Balcony",
      "arabic": "بلكونة",
      "group": "core"
    },
    {
      "code": "BD",
      "normalized": "business_district",
      "name": "Business District",
      "arabic": "منطقة أعمال",
      "group": "location"
    },
    {
      "code": "BK",
      "normalized": "kitchen_appliances",
      "name": "Kitchen Appliances",
      "arabic": "أجهزة مطبخ",
      "group": "fitout"
    },
    {
      "code": "BL",
      "normalized": "landmark_view",
      "name": "Landmark View",
      "arabic": "إإطلالة مميزة",
      "group": "view"
    },
    {
      "code": "BW",
      "normalized": "built_in_wardrobes",
      "name": "Built-in Wardrobes",
      "arabic": "دواليب مدمجة",
      "group": "fitout"
    },
    {
      "code": "CH",
      "normalized": "clubhouse",
      "name": "Clubhouse",
      "arabic": "كلوب هاوس",
      "group": "compound"
    },
    {
      "code": "CM",
      "normalized": "compound",
      "name": "Compound",
      "arabic": "كمبوند",
      "group": "location"
    },
    {
      "code": "CO",
      "normalized": "childrens_pool",
      "name": "Children's Pool",
      "arabic": "حمام سباحة أطفال",
      "group": "leisure"
    },
    {
      "code": "CP",
      "normalized": "covered_parking",
      "name": "Covered Parking",
      "arabic": "جراج مغطى",
      "group": "access"
    },
    {
      "code": "EL",
      "normalized": "elevator",
      "name": "Elevator",
      "arabic": "مصعد",
      "group": "core"
    },
    {
      "code": "FN",
      "normalized": "finishing",
      "name": "Finishing",
      "arabic": "تشطيب",
      "group": "fitout"
    },
    {
      "code": "FR",
      "normalized": "frontage",
      "name": "Frontage",
      "arabic": "واجهة",
      "group": "exposure"
    },
    {
      "code": "FU",
      "normalized": "furnished",
      "name": "Furnished",
      "arabic": "مفروش",
      "group": "fitout"
    },
    {
      "code": "GE",
      "normalized": "land_geometry",
      "name": "Land Geometry",
      "arabic": "هندسة الأرض",
      "group": "land"
    },
    {
      "code": "IT",
      "normalized": "internet",
      "name": "Internet",
      "arabic": "إنترنت",
      "group": "infrastructure"
    },
    {
      "code": "LB",
      "normalized": "lobby_in_building",
      "name": "Lobby in Building",
      "arabic": "لوبي",
      "group": "core"
    },
    {
      "code": "MR",
      "normalized": "maids_room",
      "name": "Maid Room",
      "arabic": "غرفة مربية",
      "group": "layout"
    },
    {
      "code": "OI",
      "normalized": "office_infrastructure",
      "name": "Office Infrastructure",
      "arabic": "بنية مكتبية",
      "group": "infrastructure"
    },
    {
      "code": "PG",
      "normalized": "private_garden",
      "name": "Private Garden",
      "arabic": "حديقة خاصة",
      "group": "outdoor"
    },
    {
      "code": "PP",
      "normalized": "private_pool",
      "name": "Private Pool",
      "arabic": "حمام سباحة خاص",
      "group": "leisure"
    },
    {
      "code": "RF",
      "normalized": "retail_frontage",
      "name": "Retail Frontage",
      "arabic": "واجهة تجارية",
      "group": "exposure"
    },
    {
      "code": "SE",
      "normalized": "security",
      "name": "Security",
      "arabic": "أمن",
      "group": "core"
    },
    {
      "code": "SH",
      "normalized": "smart_home",
      "name": "Smart Home",
      "arabic": "منزل ذكي",
      "group": "technology"
    },
    {
      "code": "SP",
      "normalized": "shared_pool",
      "name": "Shared Pool",
      "arabic": "حمام سباحة مشترك",
      "group": "leisure"
    },
    {
      "code": "SS",
      "normalized": "shared_spa",
      "name": "Shared Spa",
      "arabic": "سبا مشترك",
      "group": "leisure"
    },
    {
      "code": "ST",
      "normalized": "study",
      "name": "Study",
      "arabic": "غرفة مكتب",
      "group": "layout"
    },
    {
      "code": "SY",
      "normalized": "shared_gym",
      "name": "Shared Gym",
      "arabic": "جيم مشترك",
      "group": "leisure"
    },
    {
      "code": "TR",
      "normalized": "traffic_exposure",
      "name": "Traffic Exposure",
      "arabic": "تعرض مروري",
      "group": "exposure"
    },
    {
      "code": "VI",
      "normalized": "visibility",
      "name": "Visibility",
      "arabic": "وضوح الرؤية",
      "group": "exposure"
    },
    {
      "code": "VW",
      "normalized": "water_view",
      "name": "Water View",
      "arabic": "إإطلالة مائية",
      "group": "view"
    },
    {
      "code": "WC",
      "normalized": "walk_in_closet",
      "name": "Walk-in Closet",
      "arabic": "غرفة ملابس",
      "group": "layout"
    },
    {
      "code": "WF",
      "normalized": "waterfront",
      "name": "Waterfront",
      "arabic": "واجهة مائية",
      "group": "view"
    },
    {
      "code": "ZO",
      "normalized": "zoning",
      "name": "Zoning",
      "arabic": "تقسيم/ترخيص",
      "group": "land"
    }
  ],
  "CITIES": [
    "6 October City",
    "Al Ain Al Sokhna",
    "Al Alamein",
    "El Nozha",
    "Hay El Maadi",
    "Hay Sharq",
    "Hurghada",
    "Madinaty",
    "Mokattam",
    "Mostakbal City - Future City",
    "Nasr City",
    "New Cairo City",
    "New Capital City",
    "New Heliopolis",
    "Qesm Ad Dabaah",
    "Qesm Marsa Matrouh",
    "Ras Al Hekma",
    "Sheikh Zayed City",
    "Shorouk City",
    "Sidi Abdel Rahman",
    "Zamalek"
  ],
  "DISTRICTS": [
    "6 October Compounds",
    "6th District",
    "Al Ahyaa District",
    "Al Rehab",
    "Cairo Alexandria Desert Road",
    "El Gouna",
    "El Katameya",
    "El Shorouk Compounds",
    "Hurghada Resorts",
    "Hyde Park",
    "IL Monte Galala",
    "Marassi",
    "Mostakbal City Compounds",
    "New Capital Compounds",
    "New Zayed City",
    "North Investors Area",
    "Privado",
    "Safaga",
    "Sahl Hasheesh",
    "Sarayat Al Maadi",
    "Sheikh Zayed Compounds",
    "South Investors Area",
    "The 5th Settlement"
  ]
}
```

## Phase 9 — Frontend Pages

The scraped datasets directly support and limit specific pages in the frontend architecture. The page requirements and data boundaries are mapped below:

1. **Valuation Tool Page**:
   - *Required Data*: Form parameter inputs (type, size, location, rooms).
   - *Available Data*: Preprocessed parquets contain local valuation models, H3 cell stats, and compound-specific price per sqm.
   - *Limitations*: Predictions are only valid within the boundaries of the dataset (e.g. sizes between 20 and 5000 sqm, and prices > 10,000 EGP). Off-plan properties and new launches cannot be priced due to 100% missing price/area data in the `new_projects.jsonl` dataset.

2. **Map Search Page**:
   - *Required Data*: Latitude, longitude, price, property type, and size for rendering pins.
   - *Available Data*: 99.9%+ of active listings contain valid, non-null latitude and longitude coordinates.
   - *Limitations*: The coordinate duplicate rate is exceptionally high (up to 95.29% in rent and 93.11% in buy). Multiple listings map to the exact same compound center coordinate. The map frontend MUST implement clustering or spidering to separate overlapping pins at the same location.

3. **Comparable Properties (Comps) Section**:
   - *Required Data*: Neighborhood transaction comparables with H3 coordinates or compound match.
   - *Available Data*: Preprocessed datasets store comparative statistics (e.g. `comparable_count`, `comparable_price_std`, `comparable_price_iqr`).
   - *Limitations*: Many smaller compounds have low density, meaning the application must support a fallback search radius (e.g. retrieving comps from the district level if the compound contains fewer than 3 listings).

4. **Property Details Page**:
   - *Required Data*: Images, price, property type, amenities, location hierarchy, share link.
   - *Available Data*: Raw listings contain lists of image URLs (`images`), amenity codes (`amenities`), and a `share_url` pointing to the source listing.
   - *Limitations*: Images are hosted on PropertyFinder's external CDNs and are subject to expiration or hotlinking blocks. Listing titles are available, but full descriptive texts are missing.

## Phase 10 — Product Requirements & Recommendations

### 1. UX Recommendations

- **Hierarchical Auto-Suggest for Search**: Prevent user input errors by implementing a single unified search field that auto-suggests location paths in order of hierarchy (e.g., typing 'Giza' shows 'New Giza (Compound), Giza' and '6 October City, Giza').

- **Logarithmic Price Range Sliders**: Because price spreads are enormous (ranging from 100k to 1 Billion EGP), a linear range slider will be unusable. The slider controls must use a logarithmic scale.

- **Conditional Layouts for Forms**: Dynamically hide and disable the bedrooms and bathrooms inputs if a user selects commercial property types or 'Land' to streamline the form submission and match raw data models.

- **Map Spidering / Clustering**: Implement coordinate spidering (such as OverlappingMarkerSpiderfier) to handle coordinates sharing the exact same latitude/longitude (93%+ of listings).

### 2. Missing Data Risks

- **Off-plan Valuation Void**: The `new_projects.jsonl` file has 100% missing values for prices, sizes, and property types. Off-plan compounds cannot be valued using standard automated valuation models. The frontend must display an 'Off-Plan / Estimate Not Available' message for these projects.

- **Commercial Feature Gap**: Bedrooms and bathrooms are heavily missing in commercial categories (up to 54.4% bedrooms missing in commercial buy). Automated valuation models must not rely on bedroom counts for commercial properties.

- **External Link Expiration**: Since the application relies on external `share_url` and `images` arrays, there is a significant link-rot risk where external pages expire, leading to broken images or 404 errors on comparable cards.

### 3. Production Readiness Assessment

- **Residential Categories**: **High Readiness (99.09% Buy / 98.95% Rent)**. The residential listing data is dense, clean, and has low missingness for core structural attributes. Once coordinate duplicates are resolved on the map layer, the residential module is ready for launch.

- **Commercial Categories**: **Medium Readiness (89.12% Buy / 94.28% Rent)**. Data is highly complete for size and location, but lacking rooms. The frontend must use a simplified commercial form structure that strips out room counts to be production-ready.

- **New Projects Module**: **Not Ready (0.00%)**. The dataset functions solely as a project directory with titles and coordinates. It cannot support a valuation engine. It should be used exclusively to populate autocomplete lists of compound names, rather than active valuation entities.