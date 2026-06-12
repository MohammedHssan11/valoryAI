from __future__ import annotations

import argparse
import json
import uuid
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


VALUATION_PAYLOAD = {
    "lat": 30.0444,
    "lng": 31.2357,
    "property_type": "Apartment",
    "bedrooms": 3,
    "bathrooms": 2,
    "size_sqm": 150,
    "target_price_egp": 30000,
    "amenities": ["BA", "SE"],
}


def call_json(method: str, url: str, payload: dict[str, Any] | None = None, timeout: float = 20.0) -> tuple[int, Any, dict[str, str]]:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {
        "Accept": "application/json",
        "X-Request-ID": f"smoke-{uuid.uuid4()}",
        "X-Correlation-ID": "staging-smoke",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url=url, data=body, method=method, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, json.loads(response.read().decode("utf-8")), dict(response.headers.items())
    except HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8")), dict(exc.headers.items())
    except URLError as exc:
        return 0, {"success": False, "error": {"code": "NETWORK_ERROR", "message": str(exc), "details": []}}, {}


def assert_envelope(name: str, status: int, body: Any, expected_success: bool = True) -> dict[str, Any]:
    ok = (
        status > 0
        and isinstance(body, dict)
        and body.get("success") is expected_success
        and isinstance(body.get("meta"), dict)
        and bool(body["meta"].get("request_id"))
    )
    return {
        "name": name,
        "status": status,
        "ok": ok,
        "error_code": (body.get("error") or {}).get("code") if isinstance(body, dict) else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run staging readiness smoke checks against ValorAI APIs.")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Backend API base URL.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")

    checks: list[dict[str, Any]] = []

    ready_status, ready_body, _ = call_json("GET", f"{base_url}/health/ready", timeout=args.timeout)
    checks.append(assert_envelope("readiness", ready_status, ready_body))

    openapi_status, openapi_body, _ = call_json("GET", f"{base_url}/openapi.json", timeout=args.timeout)
    checks.append(
        {
            "name": "openapi",
            "status": openapi_status,
            "ok": openapi_status == 200 and "/v1/rent/fair-price" in openapi_body.get("paths", {}),
        }
    )

    valuation_status, valuation_body, valuation_headers = call_json(
        "POST",
        f"{base_url}/v1/rent/fair-price",
        VALUATION_PAYLOAD,
        timeout=args.timeout,
    )
    valuation_check = assert_envelope("valuation", valuation_status, valuation_body)
    if valuation_check["ok"]:
        data = valuation_body["data"]
        valuation_check.update(
            {
                "flag": data.get("flag"),
                "tier_used": data.get("tier_used"),
                "comps_count": data.get("comps_count"),
                "confidence_label": (data.get("confidence") or {}).get("label"),
                "trace_header_present": bool(valuation_headers.get("x-request-id") or valuation_headers.get("X-Request-ID")),
            }
        )
    checks.append(valuation_check)

    invalid_status, invalid_body, _ = call_json(
        "POST",
        f"{base_url}/v1/rent/fair-price",
        {"lat": 100, "lng": 31.2357, "property_type": "Apartment", "size_sqm": 150},
        timeout=args.timeout,
    )
    checks.append(assert_envelope("invalid_payload", invalid_status, invalid_body, expected_success=False))

    metrics_status, metrics_body, _ = call_json("GET", f"{base_url}/health/metrics", timeout=args.timeout)
    metrics_check = assert_envelope("metrics", metrics_status, metrics_body)
    if metrics_check["ok"]:
        metrics_check["has_histograms"] = bool(metrics_body["data"].get("histograms"))
        metrics_check["has_recent_events"] = "recent_events" in metrics_body["data"]
    checks.append(metrics_check)

    operational_status, operational_body, _ = call_json("GET", f"{base_url}/health/operational", timeout=args.timeout)
    operational_check = assert_envelope("operational", operational_status, operational_body)
    if operational_check["ok"]:
        operational_check["operational_status"] = operational_body["data"].get("status")
        operational_check["checks"] = operational_body["data"].get("checks", [])
    checks.append(operational_check)

    report = {
        "base_url": base_url,
        "ok": all(item.get("ok") for item in checks),
        "checks": checks,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
