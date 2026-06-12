from pathlib import Path

p = Path("C:\\Users\\mh978\\Downloads\\mobile computing project\\pf_scraper\\pf_scraper\\next_data_eg.json")  # نفس اسم ملفك الحالي
txt = p.read_text(encoding="utf-8", errors="ignore")

print("File size:", len(txt))
print("__NEXT_DATA__ present?", "__NEXT_DATA__" in txt)

# اطبع حوالين أول ظهور لو موجود
idx = txt.find("__NEXT_DATA__")
if idx != -1:
    start = max(0, idx - 200)
    end = min(len(txt), idx + 400)
    print("\n--- context ---\n")
    print(txt[start:end])
