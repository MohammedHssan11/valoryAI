import json
from pprint import pprint

with open("next_data_eg_only.json", "r", encoding="utf-8") as f:
    data = json.load(f)

listings = data["props"]["pageProps"]["searchResult"]["listings"]

print("Listings count:", len(listings))
first = listings[0]

print("\nTop-level keys of first listing:")
print(list(first.keys()))

print("\nFirst listing (truncated view):")
pprint(first)
