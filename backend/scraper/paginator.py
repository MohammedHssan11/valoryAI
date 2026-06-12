# pf_scraper/paginator.py
import random
import time
from typing import Any, Dict, Iterable, Optional, Set, List

from .config import ScraperConfig
from .http_client import PropertyFinderHTTPClient
from .parser import parse_page
from .url_builder import build_request
from .checkpoint import Checkpoint


def paginate_category(
    cfg: ScraperConfig,
    category_name: str,
    extra_filters: Optional[Dict[str, Any]] = None,
    start_page: int = 1,
    max_pages: Optional[int] = None,
    sleep_min: float = 0.8,
    sleep_max: float = 1.8,
    checkpoint_path: Optional[str] = None,
) -> Iterable[Dict[str, Any]]:

    client = PropertyFinderHTTPClient(cfg=cfg)

    # ✅ منع التكرار وإيقاف التصفح عند تشابه النتائج
    seen_ids: Set[str] = set()
    consecutive_no_new = 0

    page = start_page
    pages_done = 0

    while True:
        # ✅ التوقف عند الوصول للحد الأقصى من الصفحات
        if max_pages is not None and pages_done >= max_pages:
            print(f"Stop: reached max_pages={max_pages}.")
            break

        # بناء الرابط بناءً على الدولة المحددة في الإعدادات
        path, params = build_request(
            category_name,
            page=page,
            extra=extra_filters,
            country=client.cfg.country,
        )

        # ✅ موحد: جلب البيانات (يعالج NEXT_DATA داخلياً لمصر والإمارات)
        result = client.get_json(path=path, params=params)

        # تحليل محتوى الصفحة
        parsed, found_path = parse_page(result.json_data, category=category_name, page=page)

        # ✅ التوقف إذا لم توجد نتائج في الصفحة
        if not parsed:
            print(f"Stop: page {page} returned 0 records. (path={found_path})")
            break

        new_rows: List[Dict[str, Any]] = []
        new_count = 0

        for item in parsed:
            d = item.to_dict() if hasattr(item, "to_dict") else item
            
            # ✅ دعم جميع أنواع المعرفات لضمان عدم التكرار (Deduplication)
            pid = d.get("id") or d.get("property_id") or d.get("listing_id")
            
            if pid and pid not in seen_ids:
                seen_ids.add(pid)
                new_rows.append(d)
                new_count += 1

        # ✅ التوقف إذا كانت الصفحة بالكامل مكررة
        if new_count == 0:
            consecutive_no_new += 1
            print(f"Stop: page {page} had 0 new IDs (duplicate pagination). (path={found_path})")
            if consecutive_no_new >= 1:
                break
        else:
            consecutive_no_new = 0

        # إرسال النتائج الجديدة فقط
        for row in new_rows:
            yield row

        # ✅ حفظ نقطة التوقف للسماح باستكمال الكشط لاحقاً
        if checkpoint_path:
            Checkpoint(
                category=category_name,
                next_page=page + 1,
                country=cfg.country, 
            ).save(checkpoint_path)

        page += 1
        pages_done += 1
        
        # وقت انتظار عشوائي لتجنب الحظر
        time.sleep(random.uniform(sleep_min, sleep_max))