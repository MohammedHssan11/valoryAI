# Sprint 6 Observability Audit

Date: 2026-06-11

## Health Endpoints

| Endpoint | Purpose | Verified |
| --- | --- | --- |
| `/health` | Liveness | Yes |
| `/health/ready` | Database readiness | Yes |
| `/health/metrics` | In-process counters, histograms, recent events | Yes |
| `/health/operational` | SLO checks, distributions, recent diagnostics | Yes |

Docker smoke verified both backend direct and nginx-proxied health/readiness.

## Request Tracing

Status: PASS.

Current behavior:

- Middleware creates or propagates `X-Request-ID`.
- Middleware creates or propagates `X-Correlation-ID`.
- Response headers include both values.
- Error envelopes include request id.
- JSON logs include request id, correlation id, environment, endpoint, method, status, duration, and telemetry.

## Runtime Metrics

Status: PASS FOR PILOT.

Current metrics include:

- API endpoint latency histograms.
- DB query latency histograms.
- Request rejection counters.
- Slow request events.
- Slow query events.
- Valuation and operational summaries.
- Recent event ring buffers.

Staging smoke result:

- metrics check: ok, status 200, histograms present, recent events present.
- operational check: ok, status 200, operational status ok.
- `api_latency_p95`: 319.8ms observed, threshold 1200ms.
- `valuation_latency_p95`: unknown during smoke because valuation metrics were not available in that window.
- slow requests: ok, count 0.

## Error Visibility

Status: PASS.

Observed and tested:

- Validation errors produce stable error envelopes.
- Readiness DB failure has a stable `DATABASE_UNAVAILABLE` error code.
- Rate limit errors produce stable envelopes and `Retry-After`.
- Unhandled exceptions are logged and return generic 500 envelopes.
- Request body oversize and timeout produce structured errors.

## Diagnostic Limits

Limitations:

- Metrics are in-process and reset on restart.
- No external APM, Prometheus endpoint, dashboard, or log aggregation is configured in repo.
- No alerting rules are configured in repo.
- Staging smoke observed a CMT ambiguity fallback path in valuation; route returned 200 via ML fallback, but production diagnostics should monitor fallback rate.

## Observability Verdict

Pilot diagnosability: PASS.

Production diagnosability: PARTIAL. The app can diagnose many local/staging issues from headers, logs, metrics, and health endpoints, but production scale needs external log aggregation, metrics retention, dashboards, and alerts.

