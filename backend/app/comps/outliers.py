from typing import List, Dict, Tuple


def hard_guardrails(
    comps: List[Dict],
    min_price: int,
    max_price: int,
    max_size_sqm: float,
    min_ppsqm: float,
    max_ppsqm: float,
) -> Tuple[List[Dict], Dict]:
    kept = []
    removed = 0
    reasons = {
        "bad_price": 0,
        "bad_size": 0,
        "bad_ppsqm": 0,
    }

    for c in comps:
        price = c.get("price_egp")
        size = c.get("size_sqm")

        if price is None or price < min_price or price > max_price:
            removed += 1
            reasons["bad_price"] += 1
            continue

        if size is not None:
            try:
                size_f = float(size)
            except Exception:
                removed += 1
                reasons["bad_size"] += 1
                continue

            if size_f <= 0 or size_f > max_size_sqm:
                removed += 1
                reasons["bad_size"] += 1
                continue

            ppsqm = price / max(size_f, 1e-9)
            if ppsqm < min_ppsqm or ppsqm > max_ppsqm:
                removed += 1
                reasons["bad_ppsqm"] += 1
                continue

        kept.append(c)

    return kept, {"kept": len(kept), "removed": removed, "reasons": reasons}