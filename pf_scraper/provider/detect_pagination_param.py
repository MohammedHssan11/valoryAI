import json, time, requests
from urllib.parse import urlparse, parse_qs, urlencode
from pf_egypt_parser import extract_egypt_listings_from_next_data

START_URL = "https://www.propertyfinder.eg/en/search?c=1&t=35&bdr[]=3&btr[]=2&fu=0&ob=mr"
CANDIDATES = ["page", "p", "page_number", "pageNumber"]

def extract_next_data(html: str) -> dict:
    marker = 'id="__NEXT_DATA__"'
    i = html.find(marker)
    if i == -1:
        raise ValueError("__NEXT_DATA__ not found")
    j = html.find(">", i)
    k = html.find("</script>", j)
    return json.loads(html[j+1:k].strip())

def set_param(url: str, k: str, v: str) -> str:
    u = urlparse(url)
    qs = parse_qs(u.query, keep_blank_values=True)
    qs[k] = [v]
    return u._replace(query=urlencode(qs, doseq=True)).geturl()

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})

# page 1 baseline
html1 = s.get(START_URL, timeout=30).text
nd1 = extract_next_data(html1)
rows1 = extract_egypt_listings_from_next_data(nd1)
ids1 = [r["property_id"] for r in rows1[:10]]
print("baseline first10:", ids1)

for key in CANDIDATES:
    url2 = set_param(START_URL, key, "2")
    html2 = s.get(url2, timeout=30).text
    nd2 = extract_next_data(html2)
    rows2 = extract_egypt_listings_from_next_data(nd2)
    ids2 = [r["property_id"] for r in rows2[:10]]
    changed = ids2 != ids1
    print(f"try {key}=2 changed={changed} first10={ids2}")
    time.sleep(1)
