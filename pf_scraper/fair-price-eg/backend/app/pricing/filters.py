import statistics

from app.pricing.settings import MAD


def _to_float(value):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _price_per_sqm_metric(comp):
    price = _to_float(comp.get("price_egp"))
    size = _to_float(comp.get("size_sqm"))
    if price is None or size is None or size <= 0:
        return None
    return price / size


def _price_metric(comp):
    return _to_float(comp.get("price_egp"))


def _metric_pairs(comps):
    pairs = [(comp, _price_per_sqm_metric(comp)) for comp in comps]
    pairs = [(comp, metric) for comp, metric in pairs if metric is not None]
    if len(pairs) >= MAD.min_sample_size:
        return pairs, "price_per_sqm"

    pairs = [(comp, _price_metric(comp)) for comp in comps]
    pairs = [(comp, metric) for comp, metric in pairs if metric is not None]
    return pairs, "price"


def mad_filter(comps, z=None):
    z = MAD.z_threshold if z is None else z
    pairs, metric_name = _metric_pairs(comps)
    values = [metric for _, metric in pairs]
    if len(values) < MAD.min_sample_size:
        return comps, {
            "kept": len(comps),
            "removed": 0,
            "mad": None,
            "median": None,
            "metric": metric_name,
            "reason": "sample_too_small",
        }

    med = statistics.median(values)
    abs_dev = [abs(value - med) for value in values]
    mad = statistics.median(abs_dev)

    if mad == 0:
        tolerance = abs(med) * MAD.zero_tolerance_ratio
        kept = [comp for comp, value in pairs if abs(value - med) <= tolerance]
        removed = len(pairs) - len(kept)
        return kept, {
            "kept": len(kept),
            "removed": removed,
            "mad": 0,
            "median": med,
            "metric": metric_name,
            "reason": "zero_mad_tolerance",
        }

    # Modified Z-score using MAD
    kept = []
    removed = 0
    for comp, value in pairs:
        mz = MAD.modified_z_scale * (value - med) / mad
        if abs(mz) <= z:
            kept.append(comp)
        else:
            removed += 1

    return kept, {
        "kept": len(kept),
        "removed": removed,
        "mad": mad,
        "median": med,
        "metric": metric_name,
        "reason": "modified_z_score",
    }
