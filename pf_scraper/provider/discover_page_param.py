import json
from pprint import pprint

with open("next_data_eg_only.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("data['query']:")
pprint(data.get("query"))

print("\npageProps.searchResult keys:")
pprint(list(data["props"]["pageProps"]["searchResult"].keys()))
