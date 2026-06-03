# pf_scraper/merge.py
import json
import os
from typing import Dict, Iterable, List, Set, Tuple


def iter_jsonl(path: str) -> Iterable[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _dedupe_id(row: Dict) -> str:
    # ✅ supports both old & new formats
    return str(
        row.get("id")
        or row.get("property_id")
        or row.get("listing_id")
        or ""
    ).strip()


def merge_jsonl_files(input_paths: List[str], output_path: str) -> int:
    """
    Merge multiple JSONL files into one JSONL with dedupe.

    Dedupe key:
      (country, record_type, category, id)
    where:
      - country inferred from row['source']['country_code'] or row['country_code'] or ''
      - record_type defaults based on category if missing
      - id supports id/property_id/listing_id
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    seen: Set[Tuple[str, str, str, str]] = set()
    wrote = 0

    with open(output_path, "w", encoding="utf-8") as out:
        for p in input_paths:
            if not os.path.exists(p):
                continue

            for row in iter_jsonl(p):
                # country (optional but important if you mix EG+UAE)
                src = row.get("source") if isinstance(row.get("source"), dict) else {}
                country = str(
                    (src.get("country_code") if isinstance(src, dict) else None)
                    or row.get("country_code")
                    or ""
                ).upper()

                cat = str(row.get("category") or "")
                rt = str(row.get("record_type") or ("project" if cat == "new_projects" else "property"))

                rid = _dedupe_id(row)
                if not rid:
                    continue

                key = (country, rt, cat, rid)
                if key in seen:
                    continue
                seen.add(key)

                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                wrote += 1

    return wrote
