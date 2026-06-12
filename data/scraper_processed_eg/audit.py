import json
import os
from collections import defaultdict
import glob

def audit_dataset(filepath):
    stats = {
        "rows": 0,
        "missing": defaultdict(int),
        "duplicates_by_url": 0,
        "duplicates_by_coords": 0,
        "invalid_price": 0,
        "invalid_size": 0,
        "invalid_coords": 0,
    }
    
    urls = set()
    coords = set()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            stats["rows"] += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            
            # Check missing
            for key in ["id", "title", "price", "currency", "price_period", "property_type", "location", "latitude", "longitude", "bedrooms", "bathrooms", "size", "amenities", "category"]:
                if key not in record or record[key] is None or record[key] == "" or record[key] == []:
                    stats["missing"][key] += 1
            
            # Duplicates
            url = record.get("url")
            if url:
                if url in urls:
                    stats["duplicates_by_url"] += 1
                urls.add(url)
                
            lat = record.get("latitude")
            lon = record.get("longitude")
            if lat is not None and lon is not None:
                coord_str = f"{lat},{lon}"
                if coord_str in coords:
                    stats["duplicates_by_coords"] += 1
                else:
                    coords.add(coord_str)
                
                # Invalid coords
                try:
                    if not (-90 <= float(lat) <= 90) or not (-180 <= float(lon) <= 180):
                        stats["invalid_coords"] += 1
                except:
                    stats["invalid_coords"] += 1
            else:
                stats["invalid_coords"] += 1
                
            # Invalid price
            price = record.get("price")
            if price is not None:
                try:
                    if float(price) <= 0:
                        stats["invalid_price"] += 1
                except:
                    stats["invalid_price"] += 1
            else:
                stats["invalid_price"] += 1
                
            # Invalid size
            size = record.get("size")
            if size is not None:
                try:
                    if float(size) <= 0:
                        stats["invalid_size"] += 1
                except:
                    stats["invalid_size"] += 1
            else:
                stats["invalid_size"] += 1
                
    return stats

def main():
    directory = "c:/Users/mh978/Downloads/mobile computing project/pf_scraper/data_eg"
    files = ["new_projects.jsonl", "buy.jsonl", "rent.jsonl", "commercial_rent.jsonl", "commercial_buy.jsonl"]
    
    for f in files:
        filepath = os.path.join(directory, f)
        if os.path.exists(filepath):
            print(f"--- Audit for {f} ---")
            stats = audit_dataset(filepath)
            print(json.dumps(stats, indent=2))
            print()
            
if __name__ == "__main__":
    main()
