# Sprint 5 Performance Baseline

Date: 2026-06-11

## Scope

Measurement only. No optimization work was performed.

## Built-In Valuation Baseline

Command:

```text
python backend/app/scripts/performance_baseline.py
  --base-url http://localhost:18000
  --frontend-url http://localhost:13000
  --iterations 10
  --warmup 1
  --concurrency 2
  --timeout 20
```

Result:

| Metric | Value |
| --- | --- |
| Successful valuation responses | `10` |
| Failed valuation responses | `0` |
| Deterministic fingerprint | `true` |
| Startup readiness probe | `32.83 ms` |
| Valuation avg | `73.00 ms` |
| Valuation p50 | `59.87 ms` |
| Valuation p95 | `110.49 ms` |
| Valuation max | `115.74 ms` |
| Frontend HTML | `15.98 ms` |
| Nginx-proxied valuation | `45.20 ms` |

Operational health:

- API p95 observed: `347.89 ms`, threshold `1200 ms`, status `ok`
- Valuation p95 observed: `60.98 ms`, threshold `1500 ms`, status `ok`
- Slow requests: `0`

## Protected Route And Intelligence Timings

Three samples per category:

| Category | Statuses | Avg | Min | Max |
| --- | --- | --- | --- | --- |
| Auth protected `/v1/copilot/users/me` | 200, 200, 200 | `20.41 ms` | `19.27 ms` | `21.65 ms` |
| Malformed token exchange | 401, 401, 401 | `17.15 ms` | `13.04 ms` | `20.66 ms` |
| Market insight | 200, 200, 200 | `35.60 ms` | `25.69 ms` | `44.57 ms` |
| Copilot investment | 200, 200, 200 | `385.79 ms` | `207.02 ms` | `720.50 ms` |
| Broker reason | 200, 200, 200 | `167.38 ms` | `138.49 ms` | `213.34 ms` |

Single journey timings:

| Endpoint | Time |
| --- | --- |
| Direct valuation | `191.48 ms` |
| Context-backed valuation tool | `116.13 ms` |
| What-if | `365.25 ms` |
| Negotiation | `170.83 ms` |
| Investment | `167.95 ms` |
| Broker chat | `146.86 ms` |
| Broker stream | `162.97 ms` |

## Performance Verdict

PASS.

All measured responses returned expected statuses and stayed within configured smoke thresholds. Copilot had one higher sample at `720.50 ms`, still below the API SLO threshold.
