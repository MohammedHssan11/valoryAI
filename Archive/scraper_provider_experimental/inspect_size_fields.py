import json
from collections import Counter

with open("next_data_eg_only.json", "r", encoding="utf-8") as f:
    data = json.load(f)

listings = data["props"]["pageProps"]["searchResult"]["listings"]

keys_counter = Counter()
examples = []

for item in listings:
    p = (item.get("property") or {})
    for k in p.keys():
        if "size" in k.lower() or "area" in k.lower():
            keys_counter[k] += 1
    # خزن مثالين عشوائيين
    if p and len(examples) < 5:
        ex = {k: p.get(k) for k in p.keys() if ("size" in k.lower() or "area" in k.lower())}
        examples.append(ex)

print("Size/Area-like keys frequency:")
for k,v in keys_counter.most_common():
    print("-", k, v)

print("\nExamples:")
for ex in examples:
    print(ex)
