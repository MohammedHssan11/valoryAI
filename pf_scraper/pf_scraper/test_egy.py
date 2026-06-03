import json
from pathlib import Path

html = Path("C:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\pf_scraper\\next_data_eg.json").read_text(encoding="utf-8", errors="ignore")

marker = 'id="__NEXT_DATA__"'
i = html.find(marker)
if i == -1:
    raise SystemExit("❌ __NEXT_DATA__ not found")

j = html.find(">", i)
k = html.find("</script>", j)
raw = html[j+1:k].strip()

data = json.loads(raw)
out = Path("next_data_eg_only.json")
out.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

print("✅ Saved", out, "size=", out.stat().st_size)
print("Top keys:", list(data.keys()))
