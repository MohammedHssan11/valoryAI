import sys
import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.geo.address_resolver import resolve_address
from app.geo.area_resolver import nearest_area

def trace_query(query):
    print(f"\n{'='*50}\nTRACE FOR: '{query}'\n{'='*50}")
    db = SessionLocal()
    try:
        from app.geo.spatial_authority import extract_candidate_tokens, match_hierarchical_entities
        candidates = extract_candidate_tokens(query)
        print(f"1-5. Candidates: {[c.encode('utf-8').decode('utf-8') for c in candidates]}")
        
        # Test hierarchical entity matching
        entity, status, meta = match_hierarchical_entities(db, query)
        print(f"Hierarchical Entity Status: {status}")
        if entity:
            print(f"Selected Entity ID: {entity.get('entity_id')}")
            print(f"Canonical Area ID: {entity.get('canonical_area_id')}")
            print(f"Entity Type: {entity.get('entity_type')}")
        else:
            print(f"Meta: {meta}")
            
        # Actual resolution
        try:
            loc = resolve_address(db, query)
            print(f"Resolved Lat/Lng: {loc.lat}, {loc.lng}")
            print(f"Resolved Source: {loc.source}")
            
            area = nearest_area(db, loc.lat, loc.lng)
            if area:
                print(f"Nearest Area Name: {area.get('name')}")
                print(f"Nearest Area ID: {area.get('area_id')}")
                print(f"Nearest Area Level: {area.get('level')}")
            else:
                print("Nearest Area: None")
        except Exception as e:
            print(f"Resolution Failed: {e}")
            
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    trace_query("Villette")
    trace_query("Villette, 5th Settlement Compounds")
