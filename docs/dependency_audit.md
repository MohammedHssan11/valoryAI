# Dependency Audit - ValoryAI (ValorAI)

This document classifies dependencies across the frontend applications, the backend API, and scraping modules to identify required, unused, or development-only packages.

---

## 1. Backend Dependencies

Audited from: [requirements.txt](file:///backend/requirements.txt)

| Package Name | Category | Purpose | Recommendation |
|:---|:---|:---|:---|
| `fastapi` | **Required** | Web framework for backend API routing. | Maintain |
| `uvicorn` | **Required** | ASGI web server to run FastAPI. | Maintain |
| `SQLAlchemy` | **Required** | Object-Relational Mapper (ORM) for PostgreSQL database interaction. | Maintain |
| `psycopg` | **Required** | PostgreSQL adapter (PostGIS database integration). | Maintain |
| `python-dotenv` | **Required** | Local environment configuration parser. | Maintain |
| `pydantic-settings` | **Required** | Handles strongly typed configuration settings validation. | Maintain |
| `PyJWT` | **Required** | Handles JWT bearer token creation and validation for session auth. | Maintain |
| `cryptography` | **Required** | Encryption backend for token signatures and security. | Maintain |
| `requests` | **Required** | HTTP client for external integrations and caching geocoder calls. | Maintain |
| `h3` | **Required** | Uber H3 Hexagonal spatial index for mapping listing densities. | Maintain |
| `catboost` | **Required** | Inferences ML regressors for residential rent/sale pricing. | Maintain |
| `pandas` | **Required** | Data manipulation framework for feature arrays and SHAP inputs. | Maintain |
| `numpy` | **Required** | Computes mathematical averages, IQR bounds, and quantiles. | Maintain |
| `alembic` | **Required** | Handles database schema migrations. | Maintain |

---

## 2. Frontend Web Dependencies

Audited from: [package.json](file:///frontend/web/package.json)

### Production Dependencies
| Package Name | Category | Purpose | Recommendation |
|:---|:---|:---|:---|
| `react` | **Required** | Core frontend library. | Maintain |
| `react-dom` | **Required** | DOM rendering engine for React. | Maintain |
| `react-router-dom` | **Required** | Single-page application routing. | Maintain |
| `axios` | **Required** | HTTP requests to FastAPI backend. | Maintain |
| `zustand` | **Required** | Global state store (authentications, workspace filters). | Maintain |
| `@tanstack/react-query` | **Required** | Synchronizes and caches server-side API responses. | Maintain |
| `firebase` | **Required** | Firebase integration (Authentication backend). | Maintain |
| `framer-motion` | **Required** | Premium micro-animations and page transitions. | Maintain |
| `lucide-react` | **Required** | High-quality icons. | Maintain |
| `clsx` / `tailwind-merge` | **Required** | Utility helpers for dynamic tailwind styles. | Maintain |

### Development Dependencies
| Package Name | Category | Purpose | Recommendation |
|:---|:---|:---|:---|
| `vitest` / `jsdom` | **Development** | Component and unit test execution environment. | Keep for CI/CD |
| `typescript` | **Development** | Type check and TS compilation. | Keep |
| `@types/*` | **Development** | Node and testing framework types. | Keep |
| `esbuild` / `vite` | **Development** | Module bundler and dev server. | Keep |
| `tsx` | **Development** | Utility to run typescript files directly (e.g. route validation). | Keep |
| `autoprefixer` | **Development** | Adds vendor prefixes to CSS rules. | Keep |

---

## 3. Frontend Mobile Dependencies

Audited from: [pubspec.yaml](file:///frontend/mobile/pubspec.yaml)

### Production Dependencies
| Dependency Name | Category | Purpose | Recommendation |
|:---|:---|:---|:---|
| `go_router` | **Required** | Declarative navigation routing matching Web views. | Maintain |
| `google_fonts` | **Required** | Premium Outfit/Inter fonts. | Maintain |
| `firebase_core` / `firebase_auth` | **Required** | Mobile tenant auth gateways. | Maintain |
| `cloud_firestore` | **Required** | Realtime telemetry persistence. | Maintain |
| `google_sign_in` | **Required** | SSO sign-in capability. | Maintain |
| `flutter_animate` | **Required** | UI micro-animations and animations. | Maintain |
| `dio` | **Required** | Advanced HTTP client supporting JWT refresh interceptors. | Maintain |
| `flutter_secure_storage` | **Required** | Encrypted key-value store for JWT tokens. | Maintain |
| `geolocator` | **Required** | Fetching user device coordinates. | Maintain |
| `google_maps_flutter` | **Required** | Renders interactive maps and polygon overlays. | Maintain |

### Development Dependencies
| Dependency Name | Category | Purpose | Recommendation |
|:---|:---|:---|:---|
| `flutter_test` | **Development** | Widget and unit tests. | Maintain |
| `flutter_lints` | **Development** | Enforces clean code styles. | Maintain |
