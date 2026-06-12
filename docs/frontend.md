# ValorAI Flutter Frontend Guide

**Last updated:** June 2, 2026  
**Purpose:** Practical implementation guide for the Flutter mobile frontend.  
**Project source of truth:** `PROJECT_MASTER_STATE_v3.md`  
**Detailed discovery:** `DISCOVERY_REPORT.md`

## Frontend Vision

The ValorAI mobile app should be:

- **UX First:** Clear, fast, and easy to trust.
- **Premium:** Polished spacing, restrained motion, and deliberate visual hierarchy.
- **Luxury Technology:** Dark surfaces, cyan accents, and evidence-forward presentation.
- **AI Native:** AI assistance is integrated into workflows, not presented as a detached novelty.
- **Real Estate Intelligence:** Valuation, comparables, confidence, and explainability stay central.

React is a visual reference only. Flutter behavior must be designed from backend contracts and this guide.

## Tech Stack

| Concern | Technology |
| --- | --- |
| Mobile framework | Flutter |
| Language | Dart |
| State management | Riverpod |
| Navigation | GoRouter |
| Authentication | Firebase Auth |
| Secure session storage | Flutter Secure Storage |
| HTTP client | Dio |
| UI system | Material 3 |
| Typography | Google Fonts |
| Device location | Geolocator |
| Map pinning | Google Maps Flutter |

Riverpod remains a planned architecture decision. Shared authenticated Dio is
now used by the integrated backend remote data sources.

## Folder Structure

Current Flutter root: `flutter_valorai/lib/`

```text
lib/
  main.dart
  app/
    router/
      app_router.dart
      route_names.dart
      route_paths.dart
    theme/
      app_colors.dart
      app_radius.dart
      app_spacing.dart
      app_text_styles.dart
      app_theme.dart
  core/
    constants/
    network/
    services/
      firebase/
        firebase_exceptions.dart
        firebase_initializer.dart
    utils/
    widgets/
  features/
    auth/
      data/
      domain/
      presentation/
        screens/
    copilot/
      data/
      domain/
      presentation/
        screens/
    home/
      data/
      domain/
      presentation/
        screens/
    onboarding/
      data/
      domain/
      presentation/
        screens/
    profile/
      data/
      domain/
      presentation/
        screens/
    valuation/
      data/
      domain/
      presentation/
        screens/
    workspace/
      data/
      domain/
      presentation/
```

### Folder Rules

- Keep app-wide router and theme configuration under `app/`.
- Keep reusable networking, Firebase services, and shared widgets under `core/`.
- Keep product behavior grouped by feature.
- Use `data/`, `domain/`, and `presentation/` layers where a feature needs API integration or testable business behavior.
- Do not place direct backend calls inside screen widgets.
- Add portfolio as its own feature when implementation begins.

## Design System

### Colors

Current theme tokens:

| Token | Value | Use |
| --- | --- | --- |
| `backgroundPrimary` | `#050B14` | Primary app background |
| `backgroundSecondary` | `#081423` | Secondary background and navigation |
| `surface` | `#0B1C2E` | Cards and input surfaces |
| `accent` | `#00D8FF` | Primary cyan accent |
| `secondaryAccent` | `#2AE6B8` | Secondary green accent |
| `textPrimary` | `#FFFFFF` | High-emphasis text |
| `textSecondary` | `#D9E1EA` | Body text |
| `textMuted` | `#94A3B8` | Secondary labels |

### Typography

Current typography uses Google Fonts Inter.

| Style | Size | Weight |
| --- | --- | --- |
| `displayLarge` | `57` | Bold |
| `displayMedium` | `45` | Bold |
| `headlineLarge` | `32` | `w700` |
| `headlineMedium` | `28` | `w600` |
| `titleLarge` | `22` | `w600` |
| `titleMedium` | `16` | `w600` |
| `bodyLarge` | `16` | `w400` |
| `bodyMedium` | `14` | `w400` |
| `labelLarge` | `14` | `w500` |
| `labelMedium` | `12` | `w500` |

### Spacing

| Token | Value |
| --- | --- |
| `xs` | `4` |
| `sm` | `8` |
| `md` | `16` |
| `lg` | `24` |
| `xl` | `32` |
| `xxl` | `48` |

### Radius

| Token | Value |
| --- | --- |
| `sm` | `4` |
| `md` | `8` |
| `lg` | `12` |
| `xl` | `20` |
| `pill` | `9999` |

### Theme

- Material 3 dark theme is the default.
- Use cyan as the primary interactive color.
- Use green as a secondary intelligence or positive-signal accent.
- Use shared theme components for app bars, inputs, chips, bottom navigation, cards, and buttons.
- Keep confidence, evidence, and status semantics accessible without relying on color alone.

## Authentication Strategy

### Firebase Auth

Use Firebase Authentication as the mobile identity layer.

Required providers:

- Email/password
- Google Sign-In
- Apple Sign-In

Login implementation status:

- Email/password login is implemented.
- Google Sign-In is implemented with `google_sign_in` and Firebase credentials on native platforms, plus Firebase popup authentication on web.
- Apple Sign-In is implemented through Firebase `AppleAuthProvider`.
- Loading, success routing, and SnackBar failure handling are implemented.
- Signup is implemented with Firebase email/password account creation, display-name update, Google continuation, validation, loading, and SnackBars.
- Forgot Password is implemented with Firebase password-reset email delivery, initial/loading/success/failure states, and SnackBars.
- Successful Firebase login exchanges the Firebase ID token through `POST /v1/auth/token-exchange`.
- The returned ValorAI JWT and user metadata are stored with `flutter_secure_storage`.
- App-launch restore, logout cleanup, expired-session cleanup, and protected-route redirects are implemented.

### Session Flow

```text
App launch
  -> Initialize Firebase
  -> Restore stored ValorAI JWT, or re-exchange through persisted Firebase user
  -> Splash visual sequence
  -> Home when session is valid
  -> Onboarding and Login when session is absent
  -> Successful Firebase sign-in
  -> Firebase ID token
  -> POST /v1/auth/token-exchange
  -> ValorAI JWT stored securely
  -> Home
```

Splash session restore and protected-route redirection are active.

### Firebase To ValorAI Token Exchange

Firebase remains the identity provider. The backend authorizes a separate
ValorAI JWT:

```text
Firebase Login
  -> Firebase ID Token
  -> POST /v1/auth/token-exchange
  -> Firebase RS256 signature, issuer, audience, and project validation
  -> User provisioning
  -> ValorAI HS256 JWT
  -> Secure mobile storage
```

### Auth Interceptor

`ApiClient.instance.authenticatedDio` attaches `Authorization: Bearer
<ValorAI JWT>` to integrated API calls. On `401`, it attempts one Firebase
re-exchange and retries the request once. A second `401` clears secure session
state and redirects protected routes to Login. `403` is surfaced as a
permission failure without replacing the backend authorization boundary.

## Navigation

### Current Registered Routes

| Route Name | Path | Screen | Status |
| --- | --- | --- | --- |
| `splash` | `/` | Splash | Scaffold registered |
| `onboarding` | `/onboarding` | Onboarding | Scaffold registered |
| `login` | `/login` | Login | Scaffold registered |
| `signup` | `/signup` | Signup | Completed |
| `forgotPassword` | `/forgot-password` | Forgot Password | Completed |
| `home` | `/home` | Home | Completed backend-owned dashboard slice |
| `valuationInput` | `/valuation-input` | Valuation Input | Completed backend-ready flow |
| `valuationResult` | `/valuation-result` | Valuation Result | Completed flagship response-backed experience |
| `comparableExplorer` | `/comparable-explorer` | Comparable Explorer | Completed response-backed explainability explorer |
| `copilot` | `/copilot` | Copilot | Completed authenticated orchestrator transport |
| `workspace` | `/workspace` | Workspace | Completed backend CRUD and active selection |
| `profile` | `/profile` | Profile | Scaffold registered |

### Current Entry Flow

```text
Splash
  -> Onboarding Page 1
  -> Onboarding Page 2
  -> Login
  -> Home after successful Firebase sign-in
```

`Skip` opens Login from either onboarding page. `Next` advances to Page 2. `Get Started` opens Login.

### Planned Routes

| Suggested Route Name | Suggested Path | Screen |
| --- | --- | --- |
| `portfolio` | `/portfolio` | Tracked-property list |
| `portfolioDetail` | `/portfolio/:propertyId` | Tracked-property detail |

Protected-route redirection is implemented with `AuthSessionManager`.

## Screen Inventory

### Splash

| Field | Value |
| --- | --- |
| Purpose | Initialize Firebase, resolve session state, and route the user correctly. |
| Status | Completed. Displays the startup sequence, restores the secure session during bootstrap, and routes valid sessions to Home after 2.8 seconds. |
| Backend Dependencies | `POST /v1/auth/token-exchange` when a stored ValorAI JWT must be renewed. |
| Priority | P0 |

### Onboarding

| Field | Value |
| --- | --- |
| Purpose | Introduce valuation, evidence, and AI-assisted intelligence before sign-in. |
| Status | Completed. Two-page `PageView` with animated indicator, Skip, Next, and Get Started behavior. |
| Backend Dependencies | None. |
| Priority | P0 |

### Login

| Field | Value |
| --- | --- |
| Purpose | Sign in with email/password, Google, or Apple. |
| Status | Completed. Premium dark UI with Firebase email/password, Google, and Apple login, loading state, success routing, and SnackBar error handling. |
| Backend Dependencies | Firebase Auth and `POST /v1/auth/token-exchange`. |
| Priority | P0 |

### Signup

| Field | Value |
| --- | --- |
| Purpose | Create a Firebase-backed user account. |
| Status | Completed. Validates full name, email, password, and confirmation; creates a Firebase account, updates display name, supports Google continuation, displays SnackBars, and returns to Login after success. |
| Backend Dependencies | Firebase Auth; later backend session bootstrap. |
| Priority | P0 |

### Forgot Password

| Field | Value |
| --- | --- |
| Purpose | Send a Firebase password-reset email. |
| Status | Completed. Supports initial, loading, success, and failure states with SnackBars and Back To Login navigation. |
| Backend Dependencies | Firebase Auth. |
| Priority | P0 |

### Home

| Field | Value |
| --- | --- |
| Purpose | Provide navigation, valuation entry, portfolio summary, and honest intelligence summaries. |
| Status | Completed backend-owned slice. Shows returned user identity, active workspace, property count, Copilot session count, and returned recent Copilot chats. Unsupported AI insight, market signal, saved valuation, and recent valuation sections are hidden. |
| Backend Dependencies | `GET /v1/copilot/users/me`, `GET /v1/copilot/workspaces`, `GET /v1/copilot/workspaces/{workspace_id}/properties`, and `GET /v1/copilot/workspaces/{workspace_id}/chats`. |
| Priority | P1 |

### Valuation Input

| Field | Value |
| --- | --- |
| Purpose | Collect category-aware property inputs and submit a fair-price request. |
| Status | Completed. Six-step premium flow: Category, Property Type, Location, Property Details, Amenities, and Final Review. Includes edit links, conditional residential/commercial details, land handling, grouped real amenity codes, GPS, Google Maps pinning, hierarchical address resolution, validation, loading state, error SnackBars, and real Dio submission. |
| Backend Dependencies | `POST /v1/valuation/fair-price`; future location autocomplete API. |
| Priority | P1 |

### Valuation Result

| Field | Value |
| --- | --- |
| Purpose | Display EGP fair value, range, confidence, explainability, evidence, comparables, optional market context, map context, and next actions. |
| Status | Completed flagship experience. Displays the dominant animated valuation hero, confidence badge and fill, low / expected / high spectrum, response-backed explainability cards, truth-layer AI summary, evidence grid, top-three comparable cards, graceful optional market context, compact map, sticky actions, and navigation into Comparable Explorer. |
| Backend Dependencies | Valuation response from `POST /v1/valuation/fair-price`. |
| Priority | P1 |

### Valuation Result Backend Mapping

| UI Section | Backend Response Fields |
| --- | --- |
| Hero | `fair_price_egp`, `confidence.score`, `confidence.label`, `comps_count`, `flag`, `valuation_contract.value_basis` |
| Fair Value Range | `range_low_egp`, `fair_price_egp`, `range_high_egp` |
| Why This Value? | ML `debug.top_positive_features` / `debug.top_negative_features` impact percentages when returned; otherwise CMT `confidence.factors` evidence scores |
| AI Summary | `explainability.narrative_explanation.why_this_price`, `strongest_factors`, `confidence_reason`; falls back to backend `explanation[]` only |
| Evidence | `area`, `resolved_location`, `spatial_diagnostics.retrieval_radius_m`, `evidence_summary.selected_retrieval`, `confidence.label`, `comps_count` |
| Top Comparables | `top_comps[]`: `price_egp`, `dist_m`, `similarity_score`, `size_sqm`, `property_type`, `area_name`, `evidence_rank`, plus optional room, amenity, retrieval, component-similarity, and contribution values |
| Market Context | Optional `market_context` or `market_insights` values only; entire section is hidden when unavailable |
| Mini Map | `resolved_location.lat`, `resolved_location.lng`, optional comparable `lat` / `lng`, optional retrieval radius |

No client-side price estimation, percentage fabrication, or market inference is
used. The screen hides unsupported optional fields rather than filling them with
mock values.

### Valuation Input Flow

```text
Category
  -> Category-aware Property Type
  -> Location: hierarchy, GPS, or Google Maps pin
  -> Conditional Property Details
  -> Grouped Dataset Amenities
  -> Editable Final Review
  -> POST /v1/valuation/fair-price
  -> Response-backed Valuation Result foundation
```

Category options:

- Residential Buy
- Residential Rent
- Commercial Buy
- Commercial Rent

Conditional behavior:

- Residential flows show bedrooms and bathrooms, except Land hides room fields.
- Commercial flows hide bedrooms completely and keep bathrooms optional.
- Area is always required and must be positive.
- Property types are restricted to the requested Egypt dataset taxonomy for the selected category.
- Amenities submit stable backend provider codes such as `SE`, `BA`, `CP`, and `SY`.

Location behavior:

- Hierarchical selection collects Governorate, City, District, and optional Compound, then submits `address_resolution`.
- GPS requests device permission and submits `manual_coordinates`.
- Google Maps pinning populates latitude and longitude automatically and submits `manual_coordinates`.
- `LocationAutocompleteRepository` is defined as the future integration boundary for backend suggestions. The current backend does not expose a public autocomplete route.

Backend preparation:

- `ValuationRequest` maps the product category and property type to an actual governed backend property contract.
- `ValuationRepository` defines the domain submission interface.
- `ValuationRemoteDataSource` posts with Dio to `/v1/valuation/fair-price`.
- `ValuationRepositoryImpl` connects the domain interface to the remote data source.
- `VALORAI_API_BASE_URL` is configurable with `--dart-define`; it defaults to `http://localhost:8000`.
- No client-side price estimation or hardcoded valuation result is used.

Current backend contract boundary:

- The Egypt dataset taxonomy is broader than the active governed backend contracts.
- Unsupported dataset combinations remain visible for accurate property capture and show an explicit unavailable notice instead of producing a fabricated value.
- Commercial Buy currently lacks a governed sale contract, except Land can use `land_sale`.

### Comparable Explorer

| Field | Value |
| --- | --- |
| Purpose | Explain why the valuation selected each comparable property and show how much it influenced the result. |
| Status | Completed. The existing route accepts the live `ValuationResponse` and renders similarity-first list view, distance and price sorting, context-only map view, comparable detail bottom sheet, and collapsible backend evidence section. Missing optional fields remain hidden. |
| Backend Dependencies | Valuation response `top_comps`, `comps_count`, `confidence`, `spatial_diagnostics`, and `evidence_summary`. |
| Priority | P1 |

Comparable Explorer includes:

- Header metrics for total comparable count, retrieval radius, and confidence
- Animated segmented sort controls: Similarity, Distance, and Price
- Animated List View / Map View toggle with List View as the default
- List cards with property type, price, distance, similarity, area, bedrooms, bathrooms, location, premium match badge, and valuation influence when returned
- Context-only Google Maps view with distinct subject-property and comparable markers
- Tap-to-open details sheet for backend-returned property facts, amenities, retrieval context, match reason, influence, and similarity evidence
- Collapsible "Why these comparables?" panel for available location, area, area-size, property-type, amenity, and confidence values

### Comparable Explorer Backend Mapping

| UI Section | Backend Response Fields |
| --- | --- |
| Header | `comps_count`, `spatial_diagnostics.retrieval_radius_m`, `confidence.score`, `confidence.label` |
| Cards | `top_comps[]`: `property_type`, `price_egp`, `dist_m`, `similarity_score`, `size_sqm`, `bedrooms`, `bathrooms`, `area_name`, `location_text`, `weighted_contribution`, `evidence_rank` |
| Details Sheet | Optional `price_per_sqm`, `confidence_contribution`, `age_days`, `retrieval_tier`, `tier_label`, `reason_code`, `radius_m`, `normalized_amenities`, `amenity_explanation`, `compound_name`, `furnishing_status`, `floor_number`, `view_type`, `building_quality` |
| Evidence Panel | Optional `geographic_similarity`, `weight_components`, `amenity_similarity`, `feature_similarity_components`, `confidence.factors` |
| Map View | `resolved_location.lat`, `resolved_location.lng`, optional comparable `lat` / `lng`, optional retrieval radius |

No fake comparables, client-generated property facts, or client-side valuation
logic are used. Average evidence rails are calculated only from available
backend-returned comparable scores.

### Portfolio

| Field | Value |
| --- | --- |
| Purpose | List and open tracked property states saved within the active workspace. |
| Status | Feature and route not created. |
| Backend Dependencies | `/v1/copilot/properties*` and workspace context. |
| Priority | P1 |

### Copilot

| Field | Value |
| --- | --- |
| Purpose | Provide governed AI-assisted real estate analysis in workspace and optional scenario context. |
| Status | Completed authenticated orchestrator transport. Sends the active `workspace_id`, ValorAI JWT, and optional valuation context. Local mock transport fallback and seeded mock sessions are removed. |
| Backend Dependencies | `POST /v1/copilot/orchestrator/respond` |
| Priority | P1 |

### Profile

| Field | Value |
| --- | --- |
| Purpose | Show identity, sign-out, and available account settings. |
| Status | Placeholder scaffold registered. |
| Backend Dependencies | Firebase Auth and `GET /v1/copilot/users/me`. Profile mutation and avatar APIs do not exist yet. |
| Priority | P2 |

### Workspace

| Field | Value |
| --- | --- |
| Purpose | Select, create, update, delete, and restore the active Copilot workspace. |
| Status | Completed backend-only Workspace List, Create, Update, Delete, and client-side Set Active. Generated workspace fallback and local description cache are removed because the backend schema owns `name` but does not expose `description`. |
| Backend Dependencies | `/v1/copilot/workspaces*`. |
| Priority | P0 |

## Backend Mapping

| Screen | Backend Endpoint | Status |
| --- | --- | --- |
| Splash | Secure restore and `POST /v1/auth/token-exchange` when renewal is needed | Implemented |
| Onboarding | None | No backend needed |
| Login | Firebase Auth providers then `POST /v1/auth/token-exchange` | Implemented |
| Signup | Firebase Auth `createUserWithEmailAndPassword()`, display-name update, and Google provider | Implemented |
| Forgot Password | Firebase Auth `sendPasswordResetEmail()` | Implemented |
| Home | `GET /v1/copilot/users/me`, `GET /v1/copilot/workspaces`, `GET /v1/copilot/workspaces/{workspace_id}/properties`, `GET /v1/copilot/workspaces/{workspace_id}/chats` | Completed backend-owned slice; unavailable sections hidden |
| Valuation Input | `POST /v1/valuation/fair-price` | Completed Dio submission flow; autocomplete API still pending |
| Valuation Result | Response from `POST /v1/valuation/fair-price` | Completed flagship response-backed experience |
| Comparable Explorer | Valuation response `top_comps`, `comps_count`, `confidence`, `spatial_diagnostics`, and `evidence_summary` | Completed response-backed explainability explorer |
| Portfolio | `/v1/copilot/properties*` | Backend available; feature pending |
| Copilot | `POST /v1/copilot/orchestrator/respond` | Completed authenticated response integration without mock fallback |
| Copilot staged terminal | `POST /v1/broker/stream`, `POST /v1/broker/reason`, `GET /v1/broker/session/{session_id}` | Backend available; optional later slice |
| Profile | `GET /v1/copilot/users/me` | Read available; mutation API missing |
| Workspace | `/v1/copilot/workspaces*` | Completed backend-only CRUD; active selection remains client state because no backend active-workspace route exists |

## Screen Implementation Status

- [x] Splash
- [x] Onboarding
- [x] Login
- [x] Signup
- [x] Forgot Password
- [x] Home
- [x] Valuation Input
- [x] Valuation Result
- [x] Comparable Explorer
- [x] Copilot
- [ ] Portfolio
- [ ] Profile
- [x] Workspace

Valuation Result is complete for Sprint 4B. Comparable Explorer is complete for
Sprint 5. Copilot is complete for Sprint 6. Workspace is complete for Sprint 7.

## Recommended Implementation Order

1. Supply Firebase platform files and backend `FIREBASE_PROJECT_ID`
2. Run real-device or emulator E2E walkthrough
3. Workspace-backed valuation saving
4. Portfolio
5. Profile

## Integration Verification

- `flutter analyze`: clean.
- `flutter test`: 11 tests passed.
- Targeted backend auth, route, Copilot ownership, and orchestrator tests: 9 passed.
- Docker Compose config: validates when `JWT_SECRET` and `FIREBASE_PROJECT_ID` are supplied.
- Backend `pytest -q`: blocked during collection by pre-existing unrelated stale tests and root PostGIS debug scripts.
- Real Login -> Home -> Workspace -> Valuation -> Result -> Comparables -> Copilot walkthrough: blocked until Android `google-services.json`, iOS `GoogleService-Info.plist`, and deployed backend `FIREBASE_PROJECT_ID` are supplied.

## Implementation Guardrails

- Treat the backend as the source of truth.
- Use React only for visual reference.
- Format prices in EGP.
- Do not put Firebase or backend secrets in the app.
- Do not call Gemini or any AI provider directly from Flutter.
- Do not claim live market data where the backend contract does not support it.
- Keep unsupported and off-plan states explicit.
- Add Arabic and RTL support deliberately after confirming launch scope.
- Inject a Google Maps API key through platform configuration before map tiles are used in a deployed build. Do not commit the key.
- Use `--dart-define=VALORAI_API_BASE_URL=...` when the backend is not available at `http://localhost:8000`. Android emulators typically require a reachable host such as `10.0.2.2`.
