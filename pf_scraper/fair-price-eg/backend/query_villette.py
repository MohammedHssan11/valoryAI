import sys
import json
import os

sys.path.insert(0, r"c:\Users\mh978\Downloads\mobile computing project\pf_scraper\fair-price-eg\backend")

from app.db.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    print("--- AREAS ---")
    rows = db.execute(text("SELECT area_id, name, level, parent_area_id FROM areas WHERE name ILIKE '%villette%';")).mappings().all()
    for r in rows:
        print(dict(r))
        
    print("\n--- ENTITIES ---")
    rows = db.execute(text("SELECT entity_id, entity_type, canonical_name FROM location_entities WHERE canonical_name ILIKE '%villette%' OR entity_id ILIKE '%villette%';")).mappings().all()
    for r in rows:
        print(dict(r))

    print("\n--- ALIASES ---")
    rows = db.execute(text("SELECT entity_id, normalized_alias, priority FROM location_aliases WHERE normalized_alias ILIKE '%villette%';")).mappings().all()
    for r in rows:
        print(dict(r))
finally:
    db.close()
