from __future__ import annotations

import argparse
import json
from typing import Any

from sqlalchemy import text

from app.comps.selector import TIER_SQL, _market_as_of, _params_for_tier
from app.db.session import SessionLocal
from app.geo.area_resolver import nearest_area
from app.pricing.settings import TIER_SETTINGS


DEFAULT_TARGET = {
    "lat": 30.0444,
    "lng": 31.2357,
    "property_type": "Apartment",
    "bedrooms": 3,
    "bathrooms": 2,
    "size_sqm": 150.0,
}


def normalize_plan(raw_plan: Any) -> dict[str, Any]:
    if isinstance(raw_plan, str):
        raw_plan = json.loads(raw_plan)
    if isinstance(raw_plan, list):
        return raw_plan[0]
    return raw_plan


def collect_nodes(node: dict[str, Any]) -> list[dict[str, Any]]:
    current = {
        "node_type": node.get("Node Type"),
        "relation": node.get("Relation Name"),
        "index": node.get("Index Name"),
        "actual_rows": node.get("Actual Rows"),
        "actual_total_time_ms": node.get("Actual Total Time"),
    }
    children = []
    for child in node.get("Plans", []) or []:
        children.extend(collect_nodes(child))
    return [current, *children]


def explain_tier(db, params: dict[str, Any], tier: int, radius_m: int) -> dict[str, Any]:
    sql = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)\n{TIER_SQL[tier]}"
    raw_plan = db.execute(text(sql), _params_for_tier(params, tier, radius_m)).scalar_one()
    plan = normalize_plan(raw_plan)
    root = plan["Plan"]
    nodes = collect_nodes(root)
    return {
        "tier": tier,
        "tier_label": TIER_SETTINGS[tier].label,
        "radius_m": radius_m,
        "planning_time_ms": round(float(plan.get("Planning Time", 0.0)), 3),
        "execution_time_ms": round(float(plan.get("Execution Time", 0.0)), 3),
        "indexes": sorted({node["index"] for node in nodes if node.get("index")}),
        "seq_scans": [
            {
                "relation": node.get("relation"),
                "actual_rows": node.get("actual_rows"),
                "actual_total_time_ms": node.get("actual_total_time_ms"),
            }
            for node in nodes
            if node.get("node_type") == "Seq Scan"
        ],
        "node_types": [node["node_type"] for node in nodes if node.get("node_type")],
        "root_actual_rows": root.get("Actual Rows"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit PostGIS comparable retrieval query plans.")
    parser.add_argument("--lat", type=float, default=DEFAULT_TARGET["lat"])
    parser.add_argument("--lng", type=float, default=DEFAULT_TARGET["lng"])
    parser.add_argument("--property-type", default=DEFAULT_TARGET["property_type"])
    parser.add_argument("--bedrooms", type=int, default=DEFAULT_TARGET["bedrooms"])
    parser.add_argument("--bathrooms", type=int, default=DEFAULT_TARGET["bathrooms"])
    parser.add_argument("--size-sqm", type=float, default=DEFAULT_TARGET["size_sqm"])
    args = parser.parse_args()

    with SessionLocal() as db:
        area = nearest_area(db, args.lat, args.lng)
        if not area:
            raise SystemExit("No area resolved for target coordinates.")
        params = {
            "lat": args.lat,
            "lng": args.lng,
            "area_id": area["area_id"],
            "property_type": args.property_type,
            "bedrooms": args.bedrooms,
            "bathrooms": args.bathrooms,
            "size_sqm": args.size_sqm,
            "as_of_utc": _market_as_of(db),
        }

        plans = [
            explain_tier(db, params, tier, TIER_SETTINGS[tier].radius_steps[-1])
            for tier in sorted(TIER_SETTINGS)
        ]

    print(
        json.dumps(
            {
                "target": params | {"area": dict(area)},
                "plans": plans,
            },
            indent=2,
            default=str,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
