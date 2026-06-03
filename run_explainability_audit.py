import requests
import time
import json

BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/v1/valuation/fair-price"

# Base payload
def make_payload(lat, lng, ptype, size, beds, baths, compound, target, category="residential_rent"):
    return {
        "location_mode": "manual_coordinates",
        "lat": lat,
        "lng": lng,
        "property_type": ptype,
        "property_category": category,
        "bedrooms": beds,
        "bathrooms": baths,
        "size_sqm": size,
        "target_price_egp": target,
        "amenities": ["balcony"],
        "furnishing_status": "furnished",
        "floor_number": 2,
        "compound_name": compound,
        "view_type": "street",
        "building_quality": "premium"
    }

test_cases = [
    # Goldilocks (11-50 comps) - Zamalek Villa 900sqm returned 22 comps
    {"name": "CASE 1: Goldilocks Zone (11-50 comps)", "payload": make_payload(30.0263, 31.4913, "Villa", 900, 6, 6, "Zamalek", 250000)},
    # Dense (50+ comps) - Madinaty Apartment 120sqm returned 704 comps
    {"name": "CASE 2: Dense Geography", "payload": make_payload(30.0263, 31.4913, "Apartment", 120, 2, 2, "Madinaty", 20000)},
    # Sparse (<11 comps for Known Geography) - We will use an extremely specific parameter combination
    {"name": "CASE 3: Sparse Geography (<11 comps)", "payload": make_payload(30.0263, 31.4913, "Villa", 5000, 10, 10, "Madinaty", 1000000)},
    # Unseen Geography + enough comps - UNKNOWN compound, but valid H3 cell with 385 comps
    {"name": "CASE 4: Unseen Geography + Enough Comps", "payload": make_payload(30.0263, 31.4913, "Apartment", 150, 3, 2, "UNKNOWN_COMPOUND_1", 10000)},
    # Unseen Geography + insufficient comps - Desert coordinates, UNKNOWN compound -> 0 comps
    {"name": "CASE 5: Unseen Geography + Insufficient Comps", "payload": make_payload(29.0000, 30.0000, "Villa", 900, 6, 6, "UNKNOWN_COMPOUND_2", 10000)},
]

results = []
latencies = []

print("Starting Explainability Audit...")

for idx, tc in enumerate(test_cases):
    start = time.perf_counter()
    try:
        resp = requests.post(ENDPOINT, json=tc["payload"], timeout=5)
        if resp.status_code == 404:
            # Fallback to /v1/rent/fair-price if /v1/valuation/fair-price 404s
            resp = requests.post(f"{BASE_URL}/v1/rent/fair-price", json=tc["payload"], timeout=5)
        
        elapsed_ms = (time.perf_counter() - start) * 1000
        latencies.append(elapsed_ms)
        
        status = resp.status_code
        data = resp.json() if status == 200 else {"error": resp.text}
        
        results.append({
            "case": tc["name"],
            "payload": tc["payload"],
            "status_code": status,
            "latency_ms": elapsed_ms,
            "response": data
        })
        print(f"[{idx+1}/10] {tc['name']} -> {status} in {elapsed_ms:.2f}ms")
    except Exception as e:
        print(f"[{idx+1}/10] {tc['name']} -> FAILED: {str(e)}")
        results.append({
            "case": tc["name"],
            "payload": tc["payload"],
            "status_code": 500,
            "latency_ms": 0,
            "error": str(e)
        })

print("\n--- PERFORMANCE ---")
avg_lat = sum(latencies)/len(latencies) if latencies else 0
p95_lat = sorted(latencies)[int(len(latencies)*0.95)] if latencies else 0
max_lat = max(latencies) if latencies else 0
print(f"Average: {avg_lat:.2f}ms")
print(f"P95:     {p95_lat:.2f}ms")
print(f"Max:     {max_lat:.2f}ms")

with open("audit_results.json", "w", encoding="utf-8") as f:
    json.dump({"metrics": {"avg": avg_lat, "p95": p95_lat, "max": max_lat}, "results": results}, f, indent=2)

print("\nResults saved to audit_results.json")
