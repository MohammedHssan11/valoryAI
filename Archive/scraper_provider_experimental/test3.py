import json

with open("next_data_eg_only.json", "r", encoding="utf-8") as f:
    data = json.load(f)

hits = []

def scan(obj, path=""):
    if isinstance(obj, list):
        if len(obj) >= 10 and any(isinstance(x, dict) for x in obj[:5]):
            hits.append((path, len(obj)))
        for i, v in enumerate(obj[:20]):
            scan(v, f"{path}[{i}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            scan(v, p)

scan(data)
hits = sorted(hits, key=lambda x: x[1], reverse=True)[:30]

for p, ln in hits:
    print(p, "len=", ln)
