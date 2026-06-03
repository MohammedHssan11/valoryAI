import json
import time
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode

from pf_egypt_parser import extract_egypt_listings_from_next_data

def extract_next_data_from_html(html: str) -> dict:
    marker = 'id="__NEXT_DATA__"'
    i = html.find(marker)
    if i == -1:
        raise ValueError("__NEXT_DATA__ not found")
    j = html.find(">", i)
    k = html.find("</script>", j)
    if j == -1 or k == -1:
        raise ValueError("Could not locate __NEXT_DATA__ script bounds")
    raw = html[j + 1 : k].strip()
    return json.loads(raw)

def set_page(url: str, page: int) -> str:
    u = urlparse(url)
    qs = parse_qs(u.query, keep_blank_values=True)
    qs["page"] = [str(page)]  # ✅ confirmed for Egypt
    return u._replace(query=urlencode(qs, doseq=True)).geturl()

def scrape_search(
    start_url: str,
    out_jsonl: str = "egypt_all.jsonl",
    max_pages: int = 200,
    sleep_s: float = 1.0,
    stop_after_no_new_pages: int = 2,
):
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )

    seen = set()
    consecutive_no_new = 0

    out_path = Path(out_jsonl)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        for page in range(1, max_pages + 1):
            url = set_page(start_url, page)

            r = s.get(url, timeout=30)
            if r.status_code != 200:
                print(f"Stop: page={page} http={r.status_code}")
                break

            try:
                next_data = extract_next_data_from_html(r.text)
            except Exception as e:
                print(f"Stop: page={page} cannot parse __NEXT_DATA__: {e}")
                break

            rows = extract_egypt_listings_from_next_data(next_data)
            if not rows:
                print(f"Stop: page={page} returned 0 rows")
                break

            new_count = 0
            for row in rows:
                pid = row.get("property_id")
                if pid and pid not in seen:
                    seen.add(pid)
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                    new_count += 1

            print(f"page={page} rows={len(rows)} new={new_count} total_unique={len(seen)} url={url}")

            if new_count == 0:
                consecutive_no_new += 1
                if consecutive_no_new >= stop_after_no_new_pages:
                    print(f"Stop: {consecutive_no_new} consecutive pages with 0 new ids")
                    break
            else:
                consecutive_no_new = 0

            time.sleep(sleep_s)

    print("✅ Done. Output:", out_path, "unique:", len(seen))

if __name__ == "__main__":
    START_URL = "https://www.propertyfinder.eg/en/search?c=1&t=35&bdr[]=3&btr[]=2&fu=0&ob=mr"
    scrape_search(
        start_url=START_URL,
        out_jsonl="data/egypt_villas_3br_2bath.jsonl",
        max_pages=200,
        sleep_s=1.2,
    )
