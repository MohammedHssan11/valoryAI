import json
from pathlib import Path
from pf_egypt_parser import extract_egypt_listings_from_next_data

inp = Path("next_data_eg_only.json")
data = json.loads(inp.read_text(encoding="utf-8"))

rows = extract_egypt_listings_from_next_data(data)

print("✅ rows:", len(rows))
print("First row keys:", list(rows[0].keys()) if rows else None)
print("First row sample:")
print(json.dumps(rows[0], ensure_ascii=False)[:1200], "...\n")

# optional: write jsonl
out = Path("egypt_sample.jsonl")
with out.open("w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("✅ wrote:", out, "lines:", len(rows))
