# ValorAI Mobile Discovery Report

**Date:** June 2, 2026  
**Purpose:** Discovery documentation for a future Flutter client. No Flutter code is included.

## 0. Scope And Source Notes

The requested requirements path, `reports frontend requirments`, does not exist as a directory. The matching requirements artifact is:

- `reports/frontend_requirements_report.md`

This report analyzes:

- `docs/`
- `reports/frontend_requirements_report.md`
- `react valorai/`

To verify the backend inventory rather than rely only on documentation, the exposed FastAPI routers were also checked directly under:

- `pf_scraper/fair-price-eg/backend/app/api/routes/`

There are two distinct React frontends in the workspace:

1. `react valorai/` is the requested AI Studio-style visual prototype. It has local component state, mocked content, and no backend API calls.
2. `pf_scraper/fair-price-eg/frontend/` is the backend-paired React/Vite client described in the master-state documents. It has real valuation and broker integration but still has authentication and product-completeness gaps.

They should be treated as separate references for the Flutter client:

- Use `react valorai/` as a visual and interaction reference.
- Use `pf_scraper/fair-price-eg/frontend/` and the backend routes as behavior and contract references.
- Use `reports/frontend_requirements_report.md` for dataset-driven field rules and missing product surfaces.

## 1. Backend Endpoint Inventory

The FastAPI application exposes **58 routes**. Health and direct valuation routes are currently unauthenticated. Broker, Copilot memory, Copilot tools, and the modern Copilot orchestrator require a bearer JWT.

### 1.1 Health Routes

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `GET` | `/health` | Public | Process liveness |
| `GET` | `/health/ready` | Public | Database readiness |
| `GET` | `/health/metrics` | Public | In-process runtime metrics snapshot |
| `GET` | `/health/operational` | Public | Operational and SLO snapshot |

### 1.2 Direct Valuation Routes

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `POST` | `/v1/valuation/fair-price` | Public | Category-aware deterministic valuation |
| `POST` | `/v1/rent/fair-price` | Public | Backward-compatible residential rent valuation alias |

Both routes execute the same handler. The mobile client should prefer `/v1/valuation/fair-price` for new work because it reflects the category-aware contract.

The valuation request supports:

- `location_mode`: `manual_coordinates`, `address_resolution`, or `canonical_entity`
- One matching location payload: `lat` + `lng`, `address`, or `canonical_entity_id`
- `property_category`
- `property_type`
- `size_sqm`
- Optional `bedrooms`, `bathrooms`, `target_price_egp`, `amenities`, `furnishing_status`, `floor_number`, `compound_name`, `view_type`, and `building_quality`

The valuation response includes:

- Fair price and price range
- Fairness flag
- Confidence score, label, and dimensions
- Engine and routing explanation
- Explainability model
- Retrieval trace
- Spatial diagnostics
- Evidence summary
- Resolved location
- Top comparable listings
- Amenity intelligence

### 1.3 Broker Routes

All broker routes require `Authorization: Bearer <JWT>`.

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/v1/broker/analyze` | Grounded broker analysis |
| `POST` | `/v1/broker/chat` | Broker conversation turn |
| `POST` | `/v1/broker/intent` | Low-latency intent classification |
| `POST` | `/v1/broker/reason` | Structured broker reasoning |
| `POST` | `/v1/broker/stream` | SSE stream for staged reasoning and final governed response |
| `GET` | `/v1/broker/session/{session_id}` | Broker session recovery |

The SSE route emits lifecycle events such as stage updates, confidence updates, narration chunks, governance updates, `stream_completed`, and `final_response`.

### 1.4 Copilot Memory Routes

All Copilot memory routes require `Authorization: Bearer <JWT>`. JWT ownership scopes data to the provisioned user.

#### Users

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/v1/copilot/users/me` | Current JWT-provisioned user |
| `GET` | `/v1/copilot/users/{user_id}` | Fetch owned user record |

#### Workspaces

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/v1/copilot/workspaces` | Create workspace |
| `GET` | `/v1/copilot/workspaces` | List workspaces |
| `GET` | `/v1/copilot/workspaces/{workspace_id}` | Fetch workspace |
| `PUT` | `/v1/copilot/workspaces/{workspace_id}` | Update workspace |
| `DELETE` | `/v1/copilot/workspaces/{workspace_id}` | Soft-delete workspace |
| `POST` | `/v1/copilot/workspaces/{workspace_id}/restore` | Restore workspace |

#### Chats And Messages

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/v1/copilot/chats` | Create chat |
| `GET` | `/v1/copilot/workspaces/{workspace_id}/chats` | List workspace chats |
| `GET` | `/v1/copilot/chats/{chat_id}` | Fetch chat |
| `PUT` | `/v1/copilot/chats/{chat_id}` | Update chat |
| `DELETE` | `/v1/copilot/chats/{chat_id}` | Soft-delete chat |
| `POST` | `/v1/copilot/chats/{chat_id}/restore` | Restore chat |
| `POST` | `/v1/copilot/messages` | Create message |
| `GET` | `/v1/copilot/chats/{chat_id}/messages` | List chat messages |
| `DELETE` | `/v1/copilot/messages/{message_id}` | Delete message |

#### Properties

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/v1/copilot/properties` | Create tracked property state |
| `GET` | `/v1/copilot/workspaces/{workspace_id}/properties` | List workspace properties |
| `GET` | `/v1/copilot/properties/{property_id}` | Fetch property |
| `PUT` | `/v1/copilot/properties/{property_id}` | Update property |
| `DELETE` | `/v1/copilot/properties/{property_id}` | Soft-delete property |
| `POST` | `/v1/copilot/properties/{property_id}/restore` | Restore property |

#### Scenarios And Assumptions

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/v1/copilot/scenarios` | Create property scenario |
| `GET` | `/v1/copilot/properties/{property_id}/scenarios` | List property scenarios |
| `GET` | `/v1/copilot/scenarios/{scenario_id}` | Fetch scenario |
| `GET` | `/v1/copilot/scenarios/{scenario_id}/lineage` | Fetch scenario lineage |
| `GET` | `/v1/copilot/properties/{property_id}/scenario-tree` | Fetch scenario tree |
| `PUT` | `/v1/copilot/scenarios/{scenario_id}` | Update scenario |
| `DELETE` | `/v1/copilot/scenarios/{scenario_id}` | Soft-delete scenario |
| `POST` | `/v1/copilot/scenarios/{scenario_id}/restore` | Restore scenario |
| `POST` | `/v1/copilot/assumptions` | Create assumption |
| `GET` | `/v1/copilot/properties/{property_id}/assumptions` | List property assumptions |
| `PUT` | `/v1/copilot/assumptions/{assumption_id}` | Update assumption |

#### Audit

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/v1/copilot/tool-events` | Record tool event |
| `GET` | `/v1/copilot/workspaces/{workspace_id}/tool-events` | List workspace tool events |
| `GET` | `/v1/copilot/workspaces/{workspace_id}/decisions` | List decision history |

### 1.5 Copilot Tool Routes

All tool routes require `Authorization: Bearer <JWT>`.

| Method | Path | Tool |
| --- | --- | --- |
| `POST` | `/v1/copilot/tools/valuation` | Tool 1: valuation |
| `POST` | `/v1/copilot/tools/explainability` | Tool 2: explainability |
| `POST` | `/v1/copilot/tools/comparable` | Tool 3: comparable evidence |
| `POST` | `/v1/copilot/tools/fairness` | Tool 4: fairness |
| `POST` | `/v1/copilot/tools/what-if` | Tool 5: scenario overlay |
| `POST` | `/v1/copilot/tools/negotiation` | Tool 6: negotiation |
| `POST` | `/v1/copilot/tools/investment` | Tool 7: investment |
| `POST` | `/v1/copilot/tools/market-insight` | Tool 8: market insight |

### 1.6 Modern Copilot Orchestrator

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `POST` | `/v1/copilot/orchestrator/respond` | Bearer JWT | Governed modern Copilot response pipeline |

This should be the preferred authority for new Flutter Copilot features. The broker routes remain useful for the staged SSE terminal experience and backward compatibility.

### 1.7 Important Missing Backend Surfaces

The exposed route inventory does **not** include:

- Login, signup, refresh-token, or password-reset endpoints
- Location autocomplete endpoint
- Listing browse or map-search endpoint
- Property-details endpoint for arbitrary source listings
- Notification endpoint
- Profile update or avatar upload endpoint
- Report generation or download endpoint
- Support ticket endpoint

These gaps directly affect mobile screen scope. Flutter can render placeholders only where the product deliberately accepts a presentation-only screen.

## 2. Frontend Screen Inventory

### 2.1 Requested `react valorai/` Prototype

The requested prototype has no URL router. Screens and overlays are selected through component-local state.

| Screen Or Overlay | Source | Current Behavior |
| --- | --- | --- |
| Splash | `src/components/Auth.tsx` | Automatically advances after 2.5 seconds |
| Onboarding | `src/components/Auth.tsx` | One visual onboarding page with Skip and Next |
| Login | `src/components/Auth.tsx` | Form advances to main UI without API authentication |
| Signup | `src/components/Auth.tsx` | Form advances to main UI without account creation |
| Reset Password | `src/components/Auth.tsx` | Form advances to main UI without reset delivery |
| Home Dashboard | `src/components/Home.tsx` | Static greeting, insight, portfolio counts, and market signal |
| New Valuation Wizard | `src/components/Valuations.tsx` | Five generic local steps using `Option 1` to `Option 4` |
| Valuation Result | `src/components/Valuations.tsx` | Hardcoded value, confidence, insight, and map preview |
| Copilot Chat | `src/components/Copilot.tsx` | Hardcoded transcript and static action chips |
| Profile | `src/components/Profile.tsx` | Local-only user details, stats, image selector, and menu rows |
| Edit Profile Modal | `src/components/Profile.tsx` | Updates local component state only |
| Logout Confirmation Modal | `src/components/Profile.tsx` | Returns to local auth screen |

Prototype-only controls without implemented destinations:

- Home hamburger menu
- Home profile shortcut
- Home `View All` market signals
- Copilot attachment, suggestion, save-to-portfolio, and send controls
- Profile account settings, notifications, support, and about rows
- Profile image selection persistence
- Valuation wizard close action

### 2.2 Backend-Paired React Frontend

The docs and route source identify a second web client at `pf_scraper/fair-price-eg/frontend/`.

| Screen | Path | Status |
| --- | --- | --- |
| Nexus | `/nexus` | Implemented cinematic home/status surface |
| Broker | `/broker` | Initial integrated SSE reasoning terminal |
| Valuation | `/valuation` | Strongest integrated screen |
| Pulse | `/pulse` | Presentation surface with hardcoded data |
| Assets | `/assets` | Thin alias, not a real asset-management screen |
| Vault | `/vault` | Placeholder/presentation surface |

Integrated sub-panels:

- Comparable evidence panel
- Explainability panel
- Confidence visualization
- Evidence map

### 2.3 Dataset-Driven Required Screens

The frontend requirements report calls for these data-backed product surfaces:

| Required Surface | Dataset Support | Notes |
| --- | --- | --- |
| Valuation Tool | Strong for residential, medium for commercial | Must use category-aware conditional fields |
| Map Search | Coordinates available for almost all active listings | Must cluster or spider overlapping compound-center coordinates |
| Comparable Properties | Comparable statistics and backend evidence available | Must support fallback retrieval tiers |
| Property Details | Images, price, type, amenities, hierarchy, and source URL available | Full descriptions are not present |
| Off-Plan Unavailable State | New-project directory data only | New projects lack pricing, area, and valuation attributes |

## 3. User Flows

### 3.1 Prototype Flows That Exist Today

#### Entry And Local Auth

`Splash -> Onboarding -> Login / Signup / Reset -> Main Tabs`

This flow is visual only. It does not obtain or store the bearer JWT required by Broker and Copilot endpoints.

#### Prototype Valuation

`Home -> New Valuation -> Five generic wizard steps -> Hardcoded result -> Back to wizard`

This is not connected to `/v1/valuation/fair-price`.

#### Prototype Copilot

`Home or bottom tab -> Copilot static transcript`

Message submission, chat persistence, session recovery, tools, and orchestrator calls are absent.

#### Prototype Profile

`Bottom tab -> Profile -> Edit local name/bio or confirm local logout`

No profile API exists, so persistence requires a new backend decision.

### 3.2 Required Flutter Valuation Flow

`Authenticated or allowed-public entry -> Select category -> Select property type -> Enter size and conditional rooms -> Resolve location -> Add optional details -> Submit valuation -> Review fair-price result -> Review confidence -> Review comparables -> Review explainability -> Save property to workspace`

Category behavior:

- Residential buy and rent: rooms are generally required except for category-specific exceptions such as land.
- Commercial buy and rent: bedrooms should be hidden; bathrooms should be optional.
- Off-plan projects: show an explicit estimate-unavailable state.

### 3.3 Required Flutter Copilot Flow

`Authenticate -> Bootstrap user -> Select or create workspace -> Select optional property/scenario -> Create or resume chat -> Send message -> Call governed orchestrator -> Render structured response -> Persist or refresh history`

Optional transitional terminal:

`Send broker reasoning request -> Consume /v1/broker/stream SSE -> Render stage events -> Render final governed response -> Recover session when reopening`

### 3.4 Required Flutter Portfolio And Scenario Flow

`Workspace -> Tracked properties -> Property detail -> Base valuation snapshot -> Create what-if scenario -> Review delta, fairness, evidence, and assumptions -> View lineage tree -> Ask Copilot or request negotiation/investment analysis`

### 3.5 Required Flutter Map Flow

`Search or valuation location field -> Hierarchical suggestions -> Select canonical area or place pin -> Browse clustered listing pins -> Expand overlapping pins -> Open property detail -> Start valuation or save property`

The requirements call for:

- Governorate dropdown
- Searchable city selection
- District typeahead after two characters
- Compound or street search-as-you-type with full hierarchy paths

No backend location-suggestion endpoint currently exists.

## 4. Missing Screens For The Flutter Product

### 4.1 Launch-Critical Screens

| Missing Screen | Why It Is Needed | Backend Dependency |
| --- | --- | --- |
| Auth bootstrap and session gate | Broker and Copilot APIs require JWT | External identity provider or new auth API decision |
| Workspace selector and creator | Copilot state is workspace-scoped | Existing workspace routes |
| Real category-aware valuation form | Prototype wizard is generic | Existing direct valuation route |
| Location search and map pin picker | Required by valuation contract and UX report | Missing autocomplete API; valuation accepts address/entity/coordinates |
| Valuation loading, error, retry, and empty states | Required for production API use | Existing error envelopes |
| Valuation result detail | Must expose confidence, fair range, routing, evidence, and explainability | Existing valuation response |
| Comparable evidence list and detail | Core trust surface | Existing valuation response and Tool 3 |
| Off-plan unavailable state | New-project valuation is unsupported | Dataset rule |

### 4.2 Next Product Screens

| Missing Screen | Why It Is Needed | Backend Dependency |
| --- | --- | --- |
| Portfolio / tracked property list | Prototype home and profile claim tracked properties | Existing property routes |
| Tracked property detail | Entry point for scenarios and Copilot context | Existing property routes |
| Copilot workspace chat list | Chats are persisted but not surfaced in prototype | Existing chat routes |
| Copilot conversation | Replace static transcript | Orchestrator route and message routes |
| Broker session recovery | Resume staged reasoning terminal | Existing broker session route |
| Scenario list and detail | Expose what-if analysis | Existing scenario routes and Tool 5 |
| Scenario lineage tree | Explain scenario-on-scenario history | Existing lineage and tree routes |
| Negotiation analysis | Expose Tool 6 | Existing Tool 6 |
| Investment analysis | Expose Tool 7 | Existing Tool 7 |
| Market insight / Pulse | Replace hardcoded market signals | Existing Tool 8; general district browsing API may still be needed |

### 4.3 Screens Blocked By Missing APIs

| Missing Screen | Missing API |
| --- | --- |
| Full map listing browser | Listing browse and map-search API |
| Arbitrary source-listing property details | Listing detail API |
| Notifications center | Notification API |
| Persisted profile editor and avatar upload | Profile mutation and upload APIs |
| Reports vault and downloads | Report generation, list, and download APIs |
| Support ticket form | Support API |

## 5. React Issues

### 5.1 Requested `react valorai/` Prototype Issues

| Priority | Issue | Evidence | Flutter Implication |
| --- | --- | --- | --- |
| P0 | No backend integration exists | No `fetch`, Axios, or service layer exists under `react valorai/src/` | Do not port component logic as application logic |
| P0 | Auth is simulated | `src/components/Auth.tsx` submits every auth mode directly to `onNext()` | Build a real session bootstrap and token boundary |
| P0 | Valuation is simulated | `src/components/Valuations.tsx` uses generic options and a hardcoded result | Build from the backend valuation contract |
| P0 | Copilot is simulated | `src/components/Copilot.tsx` contains a static transcript and inactive send button | Use the governed backend orchestrator; do not call a model directly |
| P0 | Currency is wrong for the product | Result uses `$1,250,000` while the backend and requirements are EGP-based | Format values as EGP and keep currency explicit |
| P1 | Navigation is local state only | `src/App.tsx` and `src/components/MainLayout.tsx` use local view and tab state | Flutter needs declarative routes and recoverable navigation |
| P1 | User, portfolio, and market values are hardcoded | `src/components/Home.tsx` and `src/components/Profile.tsx` | Replace with repository-backed view models or clearly marked placeholders |
| P1 | Multiple visible controls are dead ends | Home, Copilot, Profile, and valuation close controls have no action | Define route or disabled-state behavior before porting |
| P1 | Direct Gemini dependency is misleading | `package.json`, `.env.example`, and README reference Gemini, but no client integration exists | Flutter must call ValorAI backend only; no provider secret belongs in the app |
| P2 | Type safety is weakened | `src/components/Home.tsx` types navigation as `(v: any) => void` | Use typed route arguments and feature models |
| P2 | Styling typo | `src/components/MainLayout.tsx` uses `bg-backgroundz-10` | Treat prototype styles as reference, not production-ready tokens |
| P2 | Remote Googleusercontent visual assets are embedded | Auth, valuation result, and profile components | Own or proxy production assets and define fallbacks |
| P2 | Vite comment contains corrupted encoding | `vite.config.ts` comment text | Normalize encoding while extracting design assets |
| P2 | HTML title is boilerplate | `index.html` says `My Google AI Studio App` | Apply ValorAI branding and metadata |
| P2 | No accessibility pass is evident | Icon-only controls lack labels; visual states rely heavily on color and glow | Add semantic labels, focus order, contrast checks, and reduced-motion behavior |

`react valorai/` has no installed `node_modules`, so its lint and build scripts could not be executed during this discovery pass.

### 5.2 Backend-Paired React Frontend Issues From The Docs

The separate web client has a stronger implementation but remains incomplete:

| Priority | Issue | Impact On Flutter |
| --- | --- | --- |
| P0 | Axios requests do not attach bearer JWT | Flutter networking must add JWT interception from the first authenticated feature |
| P0 | Broker streaming requests do not attach bearer JWT | SSE client must add authorization headers |
| P0 | Broker requests omit required workspace and scenario context | Flutter Copilot state must own workspace and optional scenario context |
| P1 | Persisted broker sessions are not surfaced | Add session recovery to mobile conversation entry |
| P1 | Pulse is hardcoded | Avoid claiming live market intelligence until Tool 8 or a browsing API backs the screen |
| P1 | Assets is not true portfolio management | Implement tracked-property list and detail against Copilot property routes |
| P1 | Vault is a placeholder | Keep it out of launch scope unless report APIs are added |
| P1 | No location picker exists | Build location selection as a first-class mobile feature |
| P2 | No completed mobile/browser accessibility QA | Include accessibility and device QA in Flutter acceptance criteria |

## 6. Recommended Flutter Architecture

### 6.1 Architecture Style

Use a feature-first Flutter architecture with a small shared core:

```text
lib/
  app/
    bootstrap/
    router/
    theme/
  core/
    auth/
    config/
    error/
    network/
    storage/
    ui/
  features/
    onboarding/
    auth/
    workspace/
    home/
    valuation/
    location/
    evidence/
    portfolio/
    copilot/
    scenarios/
    market_insight/
    profile/
    vault/
```

Within each feature, separate:

```text
feature/
  data/
    dto/
    datasource/
    repository/
  domain/
    model/
    repository/
    usecase/
  presentation/
    controller/
    screen/
    widget/
```

Keep the split pragmatic. Use domain interfaces where they protect API boundaries or simplify testing; avoid creating one-file abstractions with no behavior.

### 6.2 Recommended Libraries

| Concern | Recommendation |
| --- | --- |
| State management | Riverpod |
| Navigation | `go_router` |
| JSON HTTP | Dio with interceptors |
| SSE broker stream | Raw streamed HTTP response client with explicit SSE parser |
| JWT storage | `flutter_secure_storage` |
| DTO generation | `json_serializable` and immutable model generation such as `freezed` |
| Local cache | Lightweight local persistence only for UX continuity; backend remains source of truth |
| Maps | Provider selected after licensing review; require clustering and overlapping-marker expansion |
| Testing | Unit tests for repositories/controllers, widget tests for form states, integration tests for valuation and SSE flows |

### 6.3 Network Boundary

Create separate API clients:

| Client | Routes | Notes |
| --- | --- | --- |
| Public system client | Health and optionally direct valuation | Direct valuation auth policy must be decided |
| Authenticated JSON client | Copilot memory, tools, and orchestrator | Attach bearer token and request ID |
| Authenticated SSE client | `/v1/broker/stream` | Attach bearer token, parse events, support disconnect and retry policy |

Do not include Gemini, model-provider SDKs, or provider API keys in Flutter. The mobile app should call the governed ValorAI backend only.

### 6.4 State Ownership

| State | Owner |
| --- | --- |
| JWT and session readiness | Auth controller |
| Current workspace | Workspace controller |
| Optional selected property and scenario | Copilot context controller |
| Valuation draft | Valuation-form controller |
| Latest valuation result | Valuation-result controller |
| Broker SSE lifecycle | Copilot stream controller |
| Chat history and recovered session | Copilot conversation controller |
| Portfolio list | Portfolio controller |
| Map query, viewport, and clusters | Location/map controller |

Avoid one global application store. Persist only identifiers and drafts needed for continuity.

### 6.5 Backend Mapping For Flutter Features

| Flutter Feature | Primary Backend Surface |
| --- | --- |
| Auth session bootstrap | External JWT issuer plus `/v1/copilot/users/me` |
| Valuation | `/v1/valuation/fair-price` |
| Evidence and explainability | Valuation response, `/v1/copilot/tools/comparable`, `/v1/copilot/tools/explainability` |
| Workspace and portfolio | `/v1/copilot/workspaces*`, `/v1/copilot/properties*` |
| Copilot | `/v1/copilot/orchestrator/respond` |
| Transitional staged broker terminal | `/v1/broker/stream`, `/v1/broker/reason`, `/v1/broker/session/{session_id}` |
| Scenarios | `/v1/copilot/scenarios*`, `/v1/copilot/tools/what-if` |
| Negotiation and investment | `/v1/copilot/tools/negotiation`, `/v1/copilot/tools/investment` |
| Market insight | `/v1/copilot/tools/market-insight` |

### 6.6 Mobile Design Guidance

- Preserve the dark ValorAI visual language, but make data provenance visible.
- Label mocked or unavailable data explicitly until APIs exist.
- Use EGP formatting consistently.
- Keep confidence, comparable evidence, and explainability near the valuation result.
- Use category-driven form schemas so residential and commercial flows diverge cleanly.
- Treat map clustering and overlapping-pin expansion as required behavior, not polish.
- Provide clear unsupported/off-plan states.
- Support RTL and Arabic localization from the beginning; normalize the existing requirements artifact before importing Arabic labels.

## 7. Screen Implementation Order

The order below minimizes rework and establishes backend-critical state before presentation-only surfaces.

| Order | Screen Or Slice | Reason |
| --- | --- | --- |
| 1 | App shell, theme, router, error model, and loading states | Foundation for every screen |
| 2 | Auth bootstrap and session gate | Required before any Broker or Copilot feature |
| 3 | Onboarding and entry routing | Simple first-run UX on top of the session gate |
| 4 | Workspace selector and workspace creation | Required Copilot context |
| 5 | Home dashboard shell | Navigation hub with honest placeholders where APIs are missing |
| 6 | Category-aware valuation form | Core user value and strongest backend contract |
| 7 | Location input abstraction and pin picker | Required to submit trustworthy valuations |
| 8 | Valuation result with confidence and fairness | First complete end-to-end flow |
| 9 | Comparable evidence and explainability detail | Trust and auditability layer |
| 10 | Portfolio list and tracked-property detail | Enables saved property context |
| 11 | Copilot chat using `/v1/copilot/orchestrator/respond` | Builds on JWT, workspace, and property context |
| 12 | Broker SSE terminal and session recovery | Add staged reasoning after basic Copilot works |
| 13 | Scenario list, what-if detail, and lineage | Builds on tracked properties and Copilot context |
| 14 | Negotiation and investment analysis | Adds Tools 6 and 7 after scenarios |
| 15 | Market insight / Pulse | Use Tool 8; avoid unsupported map browsing claims |
| 16 | Full map listing browser and listing details | Blocked until listing browse/detail APIs exist |
| 17 | Profile settings, notifications, support, and Vault | Implement only as matching APIs and product scope become available |

## 8. Decisions Required Before Flutter Coding

1. Decide how the mobile app obtains JWTs. The backend validates externally issued bearer tokens but exposes no login, signup, refresh, or reset endpoints.
2. Decide whether `/v1/valuation/fair-price` remains public or becomes authenticated.
3. Define a location-autocomplete API for governorate, city, district, compound, and canonical entity selection.
4. Decide whether launch includes map listing browse. If yes, add map-search and listing-detail APIs.
5. Confirm whether the Flutter visual source of truth is the `react valorai/` prototype, the backend-paired React client, or a curated combination.
6. Decide whether the broker SSE terminal ships in the first mobile release or follows the basic governed Copilot flow.
7. Decide whether Arabic and RTL are launch requirements. The data report includes bilingual amenity labels, but encoding must be normalized before reuse.
8. Keep Vault, notifications, profile persistence, uploads, and support tickets out of committed launch scope unless their backend contracts are added.

## 9. Recommended First Flutter Release

The smallest coherent mobile release is:

1. Session bootstrap
2. Workspace selection
3. Home shell
4. Category-aware valuation form
5. Location selection using the best available contract
6. Valuation result
7. Confidence, comparables, and explainability
8. Save tracked property
9. Basic governed Copilot conversation
10. Explicit loading, error, empty, unsupported, and off-plan states

This release uses the strongest existing backend capabilities without promising screens that the current APIs cannot support.

