import csv
import json

from app.scripts.load_rent_csv import read_rows


def test_read_rows_normalizes_features_from_raw_scraper_csv(tmp_path):
    csv_path = tmp_path / "rent.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "category",
                "price",
                "price_period",
                "property_type",
                "bedrooms",
                "bathrooms",
                "size",
                "location",
                "latitude",
                "longitude",
                "scraped_at_utc",
                "images",
                "amenities",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "id": "52974566",
                "category": "rent",
                "price": "50000",
                "price_period": "monthly",
                "property_type": "Apartment",
                "bedrooms": "3",
                "bathrooms": "3",
                "size": "189",
                "location": "Villette, 5th Settlement Compounds, The 5th Settlement, New Cairo City, Cairo",
                "latitude": "30.022596",
                "longitude": "31.545814",
                "scraped_at_utc": "2026-02-19T16:31:09+00:00",
                "images": "['a.jpg', 'b.jpg']",
                "amenities": "['BA', 'SE', 'VW', 'XY']",
            }
        )

    rows, skipped, area_stats = read_rows([str(csv_path)])

    assert skipped == {}
    assert len(rows) == 1
    row = rows[0]
    assert row["listing_id"] == "52974566"
    assert row["period"] == "monthly"
    assert row["size_sqm"] == 189.0
    assert row["images_count"] == 2
    assert row["compound_name"] == "Villette"
    assert row["view_type"] == "water"
    assert json.loads(row["normalized_amenities"]) == ["balcony", "security", "water_view"]
    assert json.loads(row["unknown_amenity_codes"]) == ["XY"]
    assert json.loads(row["amenities"])[-1] == {"raw": "XY", "normalized": None, "known": False}
    assert area_stats


def test_read_rows_keeps_clean_csv_without_features_idempotent(tmp_path):
    csv_path = tmp_path / "clean.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "listing_id",
                "category",
                "price_egp",
                "period",
                "property_type",
                "bedrooms",
                "bathrooms",
                "size_sqm",
                "location_text",
                "lat",
                "lng",
                "scraped_at_utc",
                "images_count",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "listing_id": "1",
                "category": "rent",
                "price_egp": "10000",
                "period": "monthly",
                "property_type": "Apartment",
                "bedrooms": "2",
                "bathrooms": "1",
                "size_sqm": "100",
                "location_text": "Maadi, Cairo",
                "lat": "29.96",
                "lng": "31.25",
                "scraped_at_utc": "2026-02-19T16:31:09+00:00",
                "images_count": "1",
            }
        )

    rows, skipped, _ = read_rows([str(csv_path)])

    assert skipped == {}
    assert json.loads(rows[0]["amenities"]) == []
    assert json.loads(rows[0]["normalized_amenities"]) == []
    assert rows[0]["compound_name"] is None
