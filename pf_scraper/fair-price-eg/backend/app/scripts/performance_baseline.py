from __future__ import annotations

import argparse
import json
import statistics
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_PAYLOAD = {
    "lat": 30.0444,
    "lng": 31.2357,
    "property_type": "Apartment",
    "bedrooms": 3,
    "bathrooms": 2,
    "size_sqm": 150,
    "target_price_egp": 30000,
    "amenities": ["BA", "SE"],
}


def percentile(values: list[float], quantile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = int((len(ordered) - 1) * quantile)
    return round(ordered[index], 2)


def summarize(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "p50": None, "p95": None, "p99": None, "avg": None, "min": None, "max": None}
    return {
        "count": len(values),
        "p50": percentile(values, 0.50),
        "p95": percentile(values, 0.95),
        "p99": percentile(values, 0.99),
        "avg": round(statistics.fmean(values), 2),
        "min": round(min(values), 2),
        "max": round(max(values), 2),
    }


def request_json(method: str, url: str, payload: dict[str, Any] | None = None, timeout: float = 20.0) -> tuple[int, dict[str, str], Any, float]:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {
        "Accept": "application/json",
        "X-Request-ID": f"perf-{uuid.uuid4()}",
        "X-Correlation-ID": "perf-baseline",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url=url, data=body, method=method, headers=headers)
    start = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:
            elapsed_ms = (time.perf_counter() - start) * 1000
            content = response.read().decode("utf-8")
            try:
                decoded = json.loads(content)
            except json.JSONDecodeError:
                decoded = {"raw": content[:500]}
            return response.status, dict(response.headers.items()), decoded, elapsed_ms
    except HTTPError as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000
        content = exc.read().decode("utf-8")
        try:
            decoded = json.loads(content)
        except json.JSONDecodeError:
            decoded = {"raw": content}
        return exc.code, dict(exc.headers.items()), decoded, elapsed_ms
    except URLError as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return 0, {}, {"error": str(exc)}, elapsed_ms


def valuation_fingerprint(body: dict[str, Any]) -> dict[str, Any] | None:
    if not body.get("success"):
        return None
    data = body.get("data", {})
    return {
        "fair_price_egp": data.get("fair_price_egp"),
        "range_low_egp": data.get("range_low_egp"),
        "range_high_egp": data.get("range_high_egp"),
        "flag": data.get("flag"),
        "tier_used": data.get("tier_used"),
        "comps_count": data.get("comps_count"),
        "confidence_label": (data.get("confidence") or {}).get("label"),
        "trace_reason_codes": [item.get("reason_code") for item in data.get("explanation_trace", [])],
    }


def run_valuation(base_url: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
    status, headers, body, elapsed_ms = request_json("POST", f"{base_url.rstrip('/')}/v1/rent/fair-price", payload, timeout)
    return {
        "status": status,
        "elapsed_ms": round(elapsed_ms, 2),
        "request_id": headers.get("x-request-id") or headers.get("X-Request-ID"),
        "success": bool(isinstance(body, dict) and body.get("success")),
        "fingerprint": valuation_fingerprint(body) if isinstance(body, dict) else None,
        "error_code": (body.get("error") or {}).get("code") if isinstance(body, dict) else None,
    }


def timed_get(url: str, timeout: float) -> dict[str, Any]:
    status, headers, body, elapsed_ms = request_json("GET", url, timeout=timeout)
    return {
        "status": status,
        "elapsed_ms": round(elapsed_ms, 2),
        "request_id": headers.get("x-request-id") or headers.get("X-Request-ID"),
        "success": bool(isinstance(body, dict) and body.get("success")),
    }


def load_payload(path: str | None) -> dict[str, Any]:
    if not path:
        return dict(DEFAULT_PAYLOAD)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect lightweight ValorAI staging latency baselines.")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Backend API base URL.")
    parser.add_argument("--frontend-url", default=None, help="Optional frontend base URL for proxied API and HTML timing.")
    parser.add_argument("--payload-file", default=None, help="Optional JSON valuation payload.")
    parser.add_argument("--iterations", type=int, default=20, help="Valuation requests to measure.")
    parser.add_argument("--warmup", type=int, default=2, help="Warmup valuation requests before measurement.")
    parser.add_argument("--concurrency", type=int, default=4, help="Concurrent valuation workers.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--max-p95-ms", type=float, default=None, help="Optional failure threshold for valuation p95.")
    parser.add_argument("--output", default=None, help="Optional JSON output path.")
    args = parser.parse_args()

    payload = load_payload(args.payload_file)
    base_url = args.base_url.rstrip("/")
    startup_probe_start = time.perf_counter()
    ready = timed_get(f"{base_url}/health/ready", args.timeout)
    startup_probe_ms = round((time.perf_counter() - startup_probe_start) * 1000, 2)

    for _ in range(max(args.warmup, 0)):
        run_valuation(base_url, payload, args.timeout)

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(args.concurrency, 1)) as executor:
        futures = [executor.submit(run_valuation, base_url, payload, args.timeout) for _ in range(args.iterations)]
        for future in as_completed(futures):
            results.append(future.result())

    success_latencies = [item["elapsed_ms"] for item in results if item["status"] == 200 and item["success"]]
    fingerprints = [item["fingerprint"] for item in results if item.get("fingerprint") is not None]
    deterministic_consistent = len({json.dumps(item, sort_keys=True) for item in fingerprints}) <= 1

    metrics = request_json("GET", f"{base_url}/health/metrics", timeout=args.timeout)[2]
    operational = request_json("GET", f"{base_url}/health/operational", timeout=args.timeout)[2]

    frontend: dict[str, Any] | None = None
    if args.frontend_url:
        frontend_base = args.frontend_url.rstrip("/")
        frontend = {
            "html": timed_get(frontend_base, args.timeout),
            "proxied_valuation": run_valuation(frontend_base, payload, args.timeout),
        }

    report = {
        "base_url": base_url,
        "frontend_url": args.frontend_url,
        "iterations": args.iterations,
        "concurrency": args.concurrency,
        "startup_probe_ms": startup_probe_ms,
        "readiness": ready,
        "valuation_roundtrip_ms": summarize(success_latencies),
        "deterministic_consistent": deterministic_consistent,
        "successful_responses": len(success_latencies),
        "failed_responses": [item for item in results if item["status"] != 200 or not item["success"]],
        "fingerprint": fingerprints[0] if fingerprints else None,
        "runtime_metrics": metrics.get("data") if isinstance(metrics, dict) else metrics,
        "operational_health": operational.get("data") if isinstance(operational, dict) else operational,
        "frontend": frontend,
    }

    output = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    print(output)

    if args.max_p95_ms is not None:
        p95 = report["valuation_roundtrip_ms"]["p95"]
        if p95 is None or p95 > args.max_p95_ms:
            raise SystemExit(2)
    if not deterministic_consistent:
        raise SystemExit(3)


if __name__ == "__main__":
    main()
