from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple


def _sorted_pairs(values: Sequence[float], weights: Sequence[float]) -> List[Tuple[float, float]]:
    pairs = [(float(v), float(w)) for v, w in zip(values, weights) if v is not None and w is not None and float(w) > 0]
    pairs.sort(key=lambda x: x[0])
    return pairs


def weighted_quantile(values: Sequence[float], weights: Sequence[float], q: float) -> float:
    """
    q in [0,1]. Returns weighted quantile using cumulative weight.
    """
    if not values or not weights:
        return 0.0
    q = max(0.0, min(1.0, float(q)))

    pairs = _sorted_pairs(values, weights)
    if not pairs:
        return 0.0

    total_w = sum(w for _, w in pairs)
    if total_w <= 0:
        return 0.0

    target = q * total_w
    cum = 0.0
    for v, w in pairs:
        cum += w
        if cum >= target:
            return float(v)
    return float(pairs[-1][0])


def weighted_median(values: Sequence[float], weights: Sequence[float]) -> float:
    return weighted_quantile(values, weights, 0.5)

