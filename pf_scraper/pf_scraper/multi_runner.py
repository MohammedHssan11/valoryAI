# pf_scraper/multi_runner.py
from __future__ import annotations

import os
from typing import Any, Dict, Optional

from .config import CATEGORIES, ScraperConfig
from .paginator import paginate_category
from .writer import write_jsonl
from .checkpoint import Checkpoint


def scrape_all_categories(
    cfg: ScraperConfig,
    out_dir: str,
    max_pages: Optional[int] = None,
    extra_filters: Optional[Dict[str, Any]] = None,
    sleep_min: float = 0.8,
    sleep_max: float = 1.8,
    resume: bool = False,
) -> None:
    os.makedirs(out_dir, exist_ok=True)

    for category in CATEGORIES:
        out_path = os.path.join(out_dir, f"{category}.jsonl")
        checkpoint_path = os.path.join(out_dir, f"{category}.checkpoint.json")

        start_page = 1
        if resume:
            cp = Checkpoint.load(checkpoint_path)
            # ✅ فقط نقوم بالاستكمال إذا كانت الدولة متطابقة (لمنع خلط بيانات الإمارات ومصر)
            if cp and (cp.country is None or cp.country == cfg.country) and cp.category == category:
                start_page = max(1, int(cp.next_page))
                print(f"Resuming {category} from page {start_page} ({cfg.country})...")
            else:
                print(f"No valid checkpoint for {category} ({cfg.country}). Starting from scratch.")

        rows_iter = paginate_category(
            cfg=cfg,
            category_name=category,
            extra_filters=extra_filters,
            start_page=start_page,
            max_pages=max_pages,
            sleep_min=sleep_min,
            sleep_max=sleep_max,
            checkpoint_path=checkpoint_path if resume else None,
        )

        # ✅ التعديل المطلوب: تحديد الـ mode بناءً على الـ resume
        # 'a' تعني Append (إضافة) و 'w' تعني Write (مسح الملف والبدء من جديد)
        mode = "a" if resume else "w"
        
        n = write_jsonl(out_path, rows_iter, mode=mode)
        
        print(f"Done ✅ {category}: wrote {n} rows -> {out_path} (mode='{mode}')")