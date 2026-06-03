import json

with open("next_data_eg_only.json", "r", encoding="utf-8") as f:
    data = json.load(f)

KEYWORDS = {"listings", "results", "properties", "hits", "items", "searchResult", "search_result", "searchResults"}

def walk(obj, path=""):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if k in KEYWORDS:
                out.append((p, v))
            out.extend(walk(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:40]):
            out.extend(walk(v, f"{path}[{i}]"))
    return out

cands = walk(data)
print("Found candidates:", len(cands))
for p, v in cands[:40]:
    t = type(v).__name__
    ln = len(v) if isinstance(v, (list, dict)) else ""
    print(f"- {p} ({t}) len={ln}")
