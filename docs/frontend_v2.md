# Frontend Requirements Document

---

# Executive Summary

Based on the FastAPI backend capabilities, the frontend application must be a real estate analytics portal named **ValorAI** (combining a core deterministic geospatial pricing system and a conversational AI copilot). The frontend client must support:
1. **Authentication Flow**: Exchanging client-side Firebase ID tokens for internal HS256 JWT access tokens.
2. **Property Management**: Managing user workspaces, active chat sessions, saved property states, assumptions tracking, and decision history records.
3. **Property Valuation**: Form wizard inputs gathering geospatial coordinates, sizes, layout rooms, and amenities to query deterministic valuation estimates (P20/P50/P80 pricing bounds) or trigger ML fallback models.
4. **Conversational Copilot**: A chat interface streaming agentic responses, executing planners and analytical tools (What-If, Negotiation, Investment, and Market Insight segmentations), and rendering grounded source citations.

---

# User Roles

Only a single user role is defined and verified in the database schema:

### Authenticated User
* **Permissions**:
  * Read, create, update, delete workspaces, chats, messages, property states, scenario states, assumptions, and tool events.
  * Execute valuation queries, scenario calculations, and copilot responses.
* **Accessible Features**: All REST endpoints exposed under `/v1/auth/*`, `/v1/pricing/*`, `/v1/copilot/*`.
* **Restricted Features**: None (no RBAC groups or administrative scopes exist in the backend schema).

#### Source References
* `pf_scraper/fair-price-eg/backend/app/models/copilot.py` (User model): Lines 46-55
* `pf_scraper/fair-price-eg/backend/app/core/auth.py` (get_authenticated_user): Lines 74-80

---

# Navigation Structure

The client application must implement the following hierarchy:

* **Workspace Selector (Root view)**
  * Lists available active Workspaces.
* **Main App Shell (Dashboard view)**
  * **Home / Dashboard**: Lists active properties list, recent valuations snapshot feed, and decision history trace.
  * **Valuation Wizard**: Tab-based pricing calculator form (Rent and Sales price estimate inputs).
  * **Copilot Chat**: Conversational panel with agent messages list, suggested actions shortcuts, and sliding context window.
  * **Assets Portfolio**: Workspace-specific properties view showing saved property states list and assumptions tables.
  * **Scenario Lineage Tree**: Visual lineage tree displaying what-if modifications branches.

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/routes/copilot.py` (workspaces, chats, properties, scenarios endpoints): Lines 56-412
* `pf_scraper/fair-price-eg/backend/app/api/routes/pricing.py` (pricing endpoints): Lines 16-86

---

# Screen Inventory

## 1. Workspace Selector

* **Purpose**: Allows users to choose an isolated analytical workspace session.
* **Required Inputs**: None.
* **Displayed Data**: Workspaces names list (`WorkspaceResponse`).
* **Actions**: Select workspace, Create new workspace (`WorkspaceCreate`), Delete workspace.
* **Backend APIs Used**: 
  * `GET /v1/copilot/workspaces`
  * `POST /v1/copilot/workspaces`
  * `DELETE /v1/copilot/workspaces/{id}`
* **Required Permissions**: Authenticated User.
* **Error States**: 401 Unauthorized, 400 Bad Request.
* **Loading States**: Blocking spinner during workspace list fetching.
* **Empty States**: Render "Create your first workspace to begin property valuation."
* **Source References**: `app/api/routes/copilot.py` lines 72-120

## 2. Valuation Calculator

* **Purpose**: Input property specifications to calculate deterministic fair prices.
* **Required Inputs**: Latitude, longitude, property type (Apartment, etc.), size in square meters (usable space), bedrooms, bathrooms, compound name, floor number, furnishing status, view type, building quality, amenities list.
* **Displayed Data**: P20 (lower band), P50 (fair price), P80 (upper band), price flag (Below/Within/Above Fair Value), confidence score and label (High/Medium/Low), retrieval tier used (1 to 5), comps list count, text explanation narrative list.
* **Actions**: Submit form, Toggle location mode (manual coords vs address geocoder vs canonical entity), Open Comparable Explorer, Reset form.
* **Backend APIs Used**: 
  * `POST /v1/valuation/fair-price`
  * `POST /v1/rent/fair-price`
* **Required Permissions**: Authenticated User.
* **Error States**: 422 Validation Error (e.g. invalid size sqm, mismatched category type), 429 Rate Limit.
* **Loading States**: Skeleton loaders mimicking pricing bands output card.
* **Empty States**: None.
* **Source References**: `app/api/routes/pricing.py` lines 16-86, `app/api/schemas/pricing.py` lines 18-140

## 3. Comparable Explorer

* **Purpose**: Map and list the comparable properties used to compute the valuation.
* **Required Inputs**: Valuation ID.
* **Displayed Data**: Map pins (coords), comparable ID, price, size, bedrooms, bathrooms, distance in kilometers, recency (age in days), feature similarity score, calculated weight.
* **Actions**: Toggle map pins overlay, Sort comparables list (by weight, distance, similarity).
* **Backend APIs Used**: 
  * `POST /v1/copilot/tools/comparable`
* **Required Permissions**: Authenticated User.
* **Error States**: 404 Valuation ID not found, 409 Payload unavailable.
* **Loading States**: Skeleton list items showing comps rows.
* **Empty States**: Show "No comparables found for this valuation scope."
* **Source References**: `app/api/routes/copilot_tools.py` lines 68-82, `app/api/schemas/copilot_tools.py` lines 51-77

## 4. Copilot Chat Room

* **Purpose**: Chat with the agent, execute planning pipelines, and run tools in context.
* **Required Inputs**: Message text (1-4000 chars), active workspace ID.
* **Displayed Data**: Messages history (role, text content), citation sources package (tool output bindings), scenario inputs overlay.
* **Actions**: Send message, Trigger tool execute shortcuts, Load chat session history.
* **Backend APIs Used**: 
  * `POST /v1/copilot/orchestrator/respond`
  * `GET /v1/copilot/chats/{chat_id}/messages`
* **Required Permissions**: Authenticated User.
* **Error States**: 503 Service Unavailable, 400 Invalid Scenario / Workspace IDs.
* **Loading States**: Animated typing bubble indicators, step logs pipeline tracer.
* **Empty States**: Show "Ask Copilot: 'Is this apartment overpriced?' or 'Run what-if scenario.'"
* **Source References**: `app/api/routes/copilot_orchestrator.py` lines 22-108, `app/api/routes/copilot.py` lines 201-208

## 5. Assets Portfolio / Saved Properties

* **Purpose**: View and edit saved properties states list.
* **Required Inputs**: None.
* **Displayed Data**: Properties labels, location strings, areas, property types, saved valuation requests.
* **Actions**: Edit property metadata, delete saved property, trigger new valuation.
* **Backend APIs Used**:
  * `GET /v1/copilot/workspaces/{workspace_id}/properties`
  * `PUT /v1/copilot/properties/{property_id}`
  * `DELETE /v1/copilot/properties/{property_id}`
* **Required Permissions**: Authenticated User.
* **Error States**: 404 Property not found.
* **Loading States**: Progressive row loading.
* **Empty States**: Render "No properties saved in this workspace."
* **Source References**: `app/api/routes/copilot.py` lines 231-265

## 6. Scenario Tree Explorer

* **Purpose**: Visualizes what-if parameter modification branches lineage.
* **Required Inputs**: Property ID.
* **Displayed Data**: Hierarchical nodes of scenarios (name, parameter changes, delta values).
* **Actions**: Fork new scenario node, delete scenario state.
* **Backend APIs Used**:
  * `GET /v1/copilot/properties/{property_id}/scenario-tree`
  * `GET /v1/copilot/scenarios/{scenario_id}/lineage`
* **Required Permissions**: Authenticated User.
* **Error States**: 404 Scenario/Property not found.
* **Loading States**: Visual tree node loader indicators.
* **Empty States**: Render "No scenario branches computed. Trigger a What-If analysis."
* **Source References**: `app/api/routes/copilot.py` lines 289-324

---

# Authentication Requirements

* **Login Screen**:
  * Frontend handles credentials/identity verify via Firebase Auth.
  * Obtains Firebase `firebase_id_token`.
  * Sends token exchange POST request to internal server.
  * Server provisions user display name and registers external subject reference.
* **Session Management**:
  * Backend returns HS256 ValorAI token in bearer scheme.
  * Frontend stores token, injecting it into `Authorization: Bearer <token>` API request headers.
  * Token expiry time is configured via `expires_in` attribute.
* **Token Refresh / MFA / SSO**:
  * **NOT VERIFIED FROM CODEBASE** (handled upstream directly by Firebase Auth SDK clients).

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/routes/auth.py` (exchange_firebase_token): Lines 20-42
* `pf_scraper/fair-price-eg/backend/app/core/auth.py` (get_authenticated_user): Lines 74-80

---

# Dashboard Requirements

The dashboard must display the following widgets:

1. **Workspace List Widget**:
   * Data Source: `GET /v1/copilot/workspaces`
   * Metrics: Workspace name, created timestamp.
   * Actions: Navigate to workspace, rename workspace, delete workspace.
2. **Decision History Log**:
   * Data Source: `GET /v1/copilot/workspaces/{workspace_id}/decisions`
   * Metrics: Log of user and tool action events list, audit metadata payload JSON.
   * Refresh Behavior: Pull to refresh.
   * User Actions: View details modal.
3. **Recent Saved Properties Feed**:
   * Data Source: `GET /v1/copilot/workspaces/{workspace_id}/properties`
   * Metrics: Property labels, area in sqm, property categories.
   * Actions: Run pricing update, open scenarion tree.

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/routes/copilot.py` (workspaces, decisions, properties endpoints): Lines 84-90, 231-237, 406-412

---

# Property Management Requirements

The backend supports full CRUD and state tracking for properties inside workspaces:

1. **Property Creation**:
   * Endpoints: `POST /v1/copilot/properties`
   * Inputs collected: `label`, `location` name, `area` size, `bedrooms` count, `bathrooms` count, `amenities` dictionary, `property_type`, `property_category`, and JSON `valuation_inputs`.
2. **Property Editing**:
   * Endpoints: `PUT /v1/copilot/properties/{property_id}`
   * Updates property specs.
3. **Property Valuation Snapshot**:
   * Database saves a complete snapshot of valuation queries logs (`valuation_snapshots`).
   * Traceable to: `POST /v1/copilot/tools/valuation` which returns `valuation_id`, `fair_price`, `price_range`, and confidence levels.
4. **Property Comparison**:
   * Comparable listings are queried using `POST /v1/copilot/tools/comparable` which compiles comparable price distributions, distance in km, and reasons for similarity matching.

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/routes/copilot.py` (properties): Lines 219-274
* `pf_scraper/fair-price-eg/backend/app/api/routes/copilot_tools.py` (valuation/comparable tools): Lines 40-52, 68-82
* `pf_scraper/fair-price-eg/backend/app/models/copilot.py` (PropertyState & ValuationSnapshot models): Lines 123-166, 310-345

---

# Valuation Engine UI Requirements

The UI must support the following specifications for the Valuation Engine:

* **Required Inputs**:
  * Geospatial coordinates (latitude ge=-90 to le=90, longitude ge=-180 to le=180).
  * Size in sqm (must be gt=0).
  * Bedrooms/Bathrooms (ge=0, le=10).
  * Furnishing status, View type, Floor number (ge=-5, le=200).
  * Compound name, Building quality string.
* **Expected Outputs**:
  * Fair rent/price in EGP.
  * Pricing bounds envelope: range low to range high.
  * Price flag (Stable Enum values: OK, Too High, Too Low).
  * Confidence rating dimensions breakdown.
  * Feature driver indicators (Direction: positive/negative, strength).
  * Explanations narrative strings list.
* **Validation Rules**:
  * Category contracts check: Property types and sizes must fit Category limits (e.g. Residential rent size cannot exceed category contract maximum limits).
  * Manual coordinates location mode requires complete lat/lng values. Address mode requires query string. Canonical mode requires stable entity id.
* **Error Cases**:
  * 422 Request Parameter error (payload fails contract validation bounds).
  * 503 Backend service unavailable (pipeline routing fails).
* **Result Visualization**:
  * Gauges displaying fair price centering within P20/P80 boundaries.
  * Map rendering targeting pins and matched comps locations.
  * Charts displaying confidence dimensions (kept comps ratio, count, tier, dispersion, distance, recency, similarity).

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/schemas/pricing.py` (RentFairPriceRequest/RentFairPriceResponse): Lines 18-140, 279-356
* `pf_scraper/fair-price-eg/backend/app/pricing/contracts.py` (Category contracts): Lines 9-105

---

# Copilot Requirements

The Conversational Copilot UI requirements must be implemented as follows:

* **Chat Interface**:
  * Standard text inputs with max length 4000 characters.
  * Dynamic list displaying dialogue messages (User / Assistant / System roles).
* **Suggested Actions**:
  * Suggests tool actions based on message intents (e.g., "Trigger What-If Scenario", "View comparable explorer map").
* **Agent Responses & Streaming**:
  * Supports streaming response packages. Emits intermediate status updates (Intent classification engine matched -> planner scheduling tools -> execution traces -> output delivery).
* **Conversation History & Context Injection**:
  * Frontend must supply `workspace_id`, and optional `scenario_id`/`broker_session_id` to maintain context window continuity.
* **Tool Usage Visibility**:
  * UI must display expandable cards for executed tools results inside the message thread (e.g., showing negotiation offer bands and ROI metrics alongside agent summaries).

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/routes/copilot_orchestrator.py` (orchestrator respond): Lines 22-108
* `pf_scraper/fair-price-eg/backend/app/api/schemas/copilot_orchestrator.py` (orchestrator model): Lines 21-53
* `pf_scraper/fair-price-eg/backend/app/models/copilot.py` (Message and BrokerSession tables): Lines 98-121, 473-497

---

# Agent System Requirements

The backend exposes a single conversational Agent Orchestrator runtime combining NLP classifiers and planners:

### Copilot Agent
* **Purpose**: Resolves conversational dialogue queries, dispatches analytical real-estate calculations tools, and composes citations-grounded summaries.
* **User Entry Point**: Message input box on the Copilot screen tab.
* **Expected Inputs**: `workspace_id`, user `message` query, optional active `scenario_id` and `broker_session_id`, and explicit `tool_inputs` parameter overrides overrides.
* **Outputs**: `runtime_id`, `response_id`, classified `intent`, response string/object, `citation_package` containing references, and an execution `audit` log dict.
* **Loading States**: Displays progressive status tracers (e.g. "Classifying query", "Calculating Comparable weights", "Validating grounding gate").
* **Failure States**: 
  * 400 Bad Request if parameters are invalid.
  * 503 Service Unavailable if downstream providers fail.

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/routes/copilot_orchestrator.py` (respond): Lines 22-108
* `pf_scraper/fair-price-eg/backend/app/api/schemas/copilot_orchestrator.py` (request/response models): Lines 21-53

---

# Search Requirements

### Comparable Listings Search
* **Standard Search**: PostGIS bounding box radius matches using `ST_DWithin` spatial query calculations.
* **Semantic Search**: **NOT VERIFIED FROM CODEBASE** (LLM operations are for intent mapping and response narration only).
* **Hybrid Search**: **NOT VERIFIED FROM CODEBASE** (No semantic vector indices queried in backend services).
* **Filters**: Mapped in estimator logic filtering categories, transaction types, active status, size sqm bounds, and rooms.
* **Sorting**: Comparable listings sorted in pricing calculations by feature similarity weighting scores and recency.
* **Pagination**: **NOT VERIFIED FROM CODEBASE** (Comps returns top-comps array of weighted comparables).

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/schemas/pricing.py` (CompItem model): Lines 143-190
* `pf_scraper/fair-price-eg/backend/app/pricing/filters.py` (Comps filter logic): Lines 6-50

---

# CMT Requirements

The Comparable Market Tier (CMT) engine defines the core spatial search parameters that frontend should expose:

* **Trigger Points**: Executing Valuation query or triggering the Valuation Agent tool.
* **Inputs**: Target coordinates, category contracts parameters.
* **Outputs**: `retrieval_trace` containing attempts log list showing:
  * Tier number (1 to 5).
  * Geographic scope (e.g. compound, sector, H3 cell).
  * Radius attempted in meters.
  * Comparables found volume and shortfall.
  * Selection status (boolean flag if this tier was selected for output calculations).
* **User Interactions**: Visualizing search tiers expansions overlays.
* **Visualizations**: Multi-tier search radius circles displayed on maps.

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/schemas/pricing.py` (RetrievalStageItem schema): Lines 207-220
* `pf_scraper/fair-price-eg/backend/app/pricing/settings.py` (Tier settings): Lines 5-30

---

# Maps Requirements

* **Map Providers**: **NOT VERIFIED FROM CODEBASE** (Client choice, e.g. Google Maps or Mapbox, as backend only communicates coordinates).
* **Coordinate Handling**: Latitude/Longitude decimal coordinates mapped in WGS84 format.
* **Geocoding & Reverse Geocoding**:
  * Address resolution query parameters mapped via `address_resolver.py`.
  * Address resolution inputs cache.
* **Property Pinning**: Mapping target property pin and surrounding comps coordinates (`lat`/`lng` attributes inside `top_comps`).
* **Spatial Search**: Visual bounds bounding parameters mapping area polygons (`ST_Contains` and spatial areas coordinates).

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/schemas/pricing.py` (manual lat/lng coords): Lines 45-46
* `pf_scraper/fair-price-eg/backend/app/geo/address_resolver.py` (Resolves addresses): Lines 10-50
* `pf_scraper/fair-price-eg/backend/app/geo/area_resolver.py` (ST_Contains polygon checks): Lines 8-40

---

# Forms Inventory

## 1. Firebase Token Exchange Form
* **Required Fields**:
  * `firebase_id_token` (string, min_length=1)
* **Validation Rules**: Must be valid non-empty string.
* **Error Messages**: 401 Unauthorized (invalid signature/claims), 503 Firebase Unavailable.
* **Source**: `app/api/schemas/auth.py` lines 10-12

## 2. Valuation Request Form
* **Required Fields**:
  * `property_type` (Apartment, Villa, etc.)
  * `size_sqm` (float, gt=0)
* **Location input dependencies (Must select one mode)**:
  * Mode `address_resolution`: Requires `address` (string, min_length=1). Cannot contain coordinates or canonical_entity_id.
  * Mode `manual_coordinates`: Requires `lat` (float, ge=-90, le=90) and `lng` (float, ge=-180, le=180). Cannot contain address or canonical_entity_id.
  * Mode `canonical_entity`: Requires `canonical_entity_id` (string). Cannot contain address or coordinates.
* **Optional Fields**:
  * `property_category` (default: residential_rent)
  * `bedrooms` (integer, ge=0)
  * `bathrooms` (integer, ge=0)
  * `target_price_egp` (integer, gt=0)
  * `amenities` (array of strings)
  * `furnishing_status` (string)
  * `floor_number` (integer, ge=-5, le=200)
  * `compound_name` (string)
  * `view_type` (string)
  * `building_quality` (string)
* **Validation Rules**:
  * `property_type` must match the category contract types allowed.
  * `size_sqm` must not exceed category contract maximum limits.
  * `target_price_egp` must not exceed category contract maximum limits.
* **Error Messages**:
  * "Property type is not valid for category."
  * "size_sqm exceeds the category maximum."
  * "A location input is required."
  * "location_mode is required when location inputs are ambiguous."
* **Source**: `app/api/schemas/pricing.py` lines 18-140

## 3. What-If Tool Modifications Form
* **Required Fields**:
  * `workspace_id` (integer, gt=0)
  * `property_id` (integer, gt=0)
  * `modifications` (dict, must contain at least one property feature modification change, e.g. size_sqm adjustments, bedrooms change, amenities added or removed).
* **Optional Fields**:
  * `scenario_id` (integer, gt=0)
* **Validation Rules**: `modifications` cannot be empty.
* **Source**: `app/api/schemas/copilot_tools.py` lines 98-109

## 4. Negotiation Tool Request Form
* **Required Fields**:
  * `workspace_id` (integer, gt=0)
  * `property_id` (integer, gt=0)
  * `asking_price_egp` (integer, gt=0)
* **Optional Fields**:
  * `scenario_id` (integer, gt=0)
  * `what_if_modifications` (dict)
* **Validation Rules**: `what_if_modifications` if provided cannot be empty.
* **Source**: `app/api/schemas/copilot_tools.py` lines 143-156

---

# API Contract Catalog

### 1. exchange_firebase_token
* **Method**: `POST`
* **Route**: `/v1/auth/token-exchange`
* **Request Body**: `FirebaseTokenExchangeRequest`
* **Response Body**: `TokenExchangeResponse`
* **Authentication**: None (Anonymous exchanging token).
* **Frontend Consumer**: Login Screen / Auth Interceptors.
* **Source**: `app/api/routes/auth.py` lines 20-42

### 2. rent_fair_price
* **Method**: `POST`
* **Route**: `/v1/rent/fair-price`
* **Request Body**: `RentFairPriceRequest`
* **Response Body**: `SuccessResponse[RentFairPriceResponse]`
* **Authentication**: None (Anonymous pricing query allowed).
* **Frontend Consumer**: Valuation Wizard.
* **Source**: `app/api/routes/pricing.py` lines 25-87

### 3. valuation_fair_price
* **Method**: `POST`
* **Route**: `/v1/valuation/fair-price`
* **Request Body**: `RentFairPriceRequest`
* **Response Body**: `SuccessResponse[RentFairPriceResponse]`
* **Authentication**: None.
* **Frontend Consumer**: Valuation Wizard.
* **Source**: `app/api/routes/pricing.py` lines 16-24

### 4. orchestrator_respond
* **Method**: `POST`
* **Route**: `/v1/copilot/orchestrator/respond`
* **Request Body**: `CopilotOrchestratorRequest`
* **Response Body**: `CopilotOrchestratorResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Copilot Chat Room.
* **Source**: `app/api/routes/copilot_orchestrator.py` lines 22-108

### 5. execute_valuation_tool
* **Method**: `POST`
* **Route**: `/v1/copilot/tools/valuation`
* **Request Body**: `ValuationToolRequest`
* **Response Body**: `ValuationToolResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Copilot Actions Panel.
* **Source**: `app/api/routes/copilot_tools.py` lines 40-52

### 6. execute_explainability_tool
* **Method**: `POST`
* **Route**: `/v1/copilot/tools/explainability`
* **Request Body**: `ExplainabilityToolRequest`
* **Response Body**: `ExplainabilityToolResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Copilot Results view.
* **Source**: `app/api/routes/copilot_tools.py` lines 54-66

### 7. execute_comparable_tool
* **Method**: `POST`
* **Route**: `/v1/copilot/tools/comparable`
* **Request Body**: `ComparableToolRequest`
* **Response Body**: `ComparableToolResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Comparable Explorer.
* **Source**: `app/api/routes/copilot_tools.py` lines 68-82

### 8. execute_fairness_tool
* **Method**: `POST`
* **Route**: `/v1/copilot/tools/fairness`
* **Request Body**: `FairnessToolRequest`
* **Response Body**: `FairnessToolResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Valuation results details.
* **Source**: `app/api/routes/copilot_tools.py` lines 84-98

### 9. execute_what_if_tool
* **Method**: `POST`
* **Route**: `/v1/copilot/tools/what-if`
* **Request Body**: `WhatIfToolRequest`
* **Response Body**: `WhatIfToolResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: What-If Scenario Wizard.
* **Source**: `app/api/routes/copilot_tools.py` lines 146-160

### 10. execute_negotiation_tool
* **Method**: `POST`
* **Route**: `/v1/copilot/tools/negotiation`
* **Request Body**: `NegotiationToolRequest`
* **Response Body**: `NegotiationToolResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Copilot Chat / Analysis dashboard.
* **Source**: `app/api/routes/copilot_tools.py` lines 100-114

### 11. execute_investment_tool
* **Method**: `POST`
* **Route**: `/v1/copilot/tools/investment`
* **Request Body**: `InvestmentToolRequest`
* **Response Body**: `InvestmentToolResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Investment metrics screen.
* **Source**: `app/api/routes/copilot_tools.py` lines 116-130

### 12. execute_market_insight_tool
* **Method**: `POST`
* **Route**: `/v1/copilot/tools/market-insight`
* **Request Body**: `MarketInsightToolRequest`
* **Response Body**: `MarketInsightToolResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Market Insight Dashboard.
* **Source**: `app/api/routes/copilot_tools.py` lines 132-144

### 13. get_workspaces
* **Method**: `GET`
* **Route**: `/v1/copilot/workspaces`
* **Request Body**: None.
* **Response Body**: `list[WorkspaceResponse]`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Workspace Selector.
* **Source**: `app/api/routes/copilot.py` lines 84-91

### 14. create_workspace
* **Method**: `POST`
* **Route**: `/v1/copilot/workspaces`
* **Request Body**: `WorkspaceCreate`
* **Response Body**: `WorkspaceResponse`
* **Authentication**: Bearer Token required.
* **Frontend Consumer**: Workspace Selector.
* **Source**: `app/api/routes/copilot.py` lines 72-82

---

# State Management Requirements

Based on database configurations, active endpoints, and schemas constraints, the frontend client must manage:

* **Global State**:
  * `authenticated_user`: Current logged-in user profile details (`UserResponse`).
  * `active_workspace_id`: Selected workspace context identifier.
  * `active_chat_id`: Current open chat thread.
  * `active_property_state_id`: Selected property state active on dashboard.
  * `active_scenario_id`: Selected scenario node active in tree viewport.
* **Local State**:
  * Form fields validation data (Valuation input wizard, What-If parameter modifications forms).
  * Geocoding maps viewport states (selected map pins coords).
  * Local message input strings.
* **Caching Requirements**:
  * Address resolver requests cached locally to avoid redundant API geocoding lookups.
* **Offline Requirements**:
  * **NOT VERIFIED FROM CODEBASE** (no offline synchronization or local storage databases are defined in backend schemas).
* **Real-Time Requirements**:
  * SSE connection state for conversational dialogue stream `/v1/broker/stream`.

#### Source References
* `pf_scraper/fair-price-eg/backend/app/models/copilot.py` (schemas relationships): Lines 46-213
* `pf_scraper/fair-price-eg/backend/app/api/routes/broker.py` (stream channel): Lines 18-35

---

# Error Handling Matrix

| Endpoint | Possible Error | HTTP Code | User Message | Recovery Action |
| --- | --- | --- | --- | --- |
| `/v1/auth/token-exchange` | Firebase token expired / invalid | 401 | "Authentication session expired. Please log in again." | Redirect to Login Splash screen to sign in again. |
| `/v1/auth/token-exchange` | Firebase Auth unavailable | 503 | "Authentication servers are temporarily unavailable. Retrying..." | Auto-retry exchange request after exponential backoff. |
| `/v1/pricing/*` | Category contract limit violated | 422 | "Property parameters exceed maximum limits allowed." | Highlight offending size/price inputs and prompt adjustments. |
| `/v1/pricing/*` | Incomplete coordinates | 422 | "A location query is required." | Focus geocoding input field or center map picker. |
| `/v1/pricing/*` | Rate limit hit | 429 | "Too many requests. Please wait a moment before calculating." | Disable calculate button briefly, execute cooling countdown. |
| `/v1/copilot/orchestrator/respond` | LLM token overflow / pipeline failure | 503 | "Copilot is temporarily busy. Please try sending your message again." | Resend user query input package. |
| `/v1/copilot/tools/explainability` | Valuation ID unavailable | 409 | "Pricing details are not compiled for this property." | Run valuation request first to generate a valuation ID. |
| `/v1/copilot/workspaces/*` | Workspace deleted or missing | 404 | "The selected workspace is no longer available." | Redirect to Workspace Selector screen. |

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/routes/pricing.py` (HTTP code exceptions): Lines 47-85
* `pf_scraper/fair-price-eg/backend/app/api/routes/copilot_orchestrator.py` (Orchestrator error handling): Lines 67-94
* `pf_scraper/fair-price-eg/backend/app/services/copilot_tools_service.py` (Tool exceptions): Lines 27-30

---

# Loading Strategy

1. **Blocking Loaders**:
   * Initial page loads fetching active workspaces list (`GET /v1/copilot/workspaces`).
   * REST calls calculating what-if scenarion comparisons (`POST /v1/copilot/tools/what-if`).
2. **Skeleton Loaders**:
   * Dashboard widgets (properties cards, decision logs list) during initial background fetch.
   * Valuation calculations results panels matching pricing bounds gauge.
3. **Progressive / Streaming Response**:
   * Conversational Chat messages: Displays incremental text chunks as streamed from `/v1/broker/stream` or `/v1/copilot/orchestrator/respond`.
   * Execution step trace: Renders checkboxes updating in real-time as background planner dispatches steps to the executor.

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/routes/copilot_orchestrator.py` (elapsed response times logging): Lines 96-107
* `pf_scraper/fair-price-eg/backend/app/api/routes/broker.py` (stream SSE endpoints): Lines 18-35

---

# Data Models

Frontend TypeScript interfaces directly reverse-engineered from Pydantic schemas:

```typescript
export interface UserResponse {
  id: number;
  display_name: string;
}

export interface WorkspaceResponse {
  id: number;
  user_id: number;
  name: string;
}

export interface WorkspaceCreate {
  name: string;
}

export interface ChatResponse {
  id: number;
  workspace_id: number;
  title: string;
}

export interface MessageResponse {
  id: number;
  chat_id: number;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
}

export interface PropertyStateResponse {
  id: number;
  workspace_id: number;
  label: string;
  location: string;
  area: number;
  bedrooms: number;
  bathrooms: number;
  property_type: string;
  property_category: string;
  amenities: Record<string, any>;
}

export interface ScenarioTreeNode {
  id: number;
  property_state_id: number;
  parent_scenario_id: number | null;
  name: string;
  modifications: Record<string, any>;
  delta_value: number | null;
}

export interface RentFairPriceResponse {
  fair_price_egp: number;
  range_low_egp: number;
  range_high_egp: number;
  flag: 'OK' | 'Too High' | 'Too Low';
  tier_used: number;
  comps_count: number;
  confidence: {
    score: number;
    label: 'High' | 'Medium' | 'Low';
    factors: Record<string, number>;
  };
  explanation: string[];
}
```

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/schemas/pricing.py`: Lines 18-356
* `pf_scraper/fair-price-eg/backend/app/api/schemas/copilot.py`: Lines 10-300
* `pf_scraper/fair-price-eg/backend/app/api/schemas/auth.py`: Lines 10-19

---

# Security Requirements

1. **JWT Authorization**:
   * Access tokens generated in `/v1/auth/token-exchange` must be sent inside the `Authorization: Bearer <token>` header for all copilot and tool requests.
2. **Inputs Sanitization**:
   * String lengths on messages are capped at 4000 characters to prevent buffer issues.
   * Coordinate parameters are validated inside boundaries limits (lat -90/90, lng -180/180).
3. **Data Protection & Verification**:
   * Cross-checks workspace operations ensuring users cannot modify property states belonging to other workspaces.

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/schemas/copilot_orchestrator.py` (message length restrictions): Line 25
* `pf_scraper/fair-price-eg/backend/app/core/auth.py` (token decoding): Lines 28-39
* `pf_scraper/fair-price-eg/backend/app/services/copilot_service.py` (workspace verification checks): Lines 40-413

---

# Feature Matrix

| Feature | Backend Exists | API Exists | Frontend Needed | Source Reference |
| --- | --- | --- | --- | --- |
| Firebase Authentication | Yes | Yes | Login Screen & Interceptors | `routes/auth.py` |
| Deterministic Valuation (CMT) | Yes | Yes | Pricing Calculator Wizard | `routes/pricing.py` |
| Outlier Filtering Visibility | Yes | Yes | Comparable listings detail tables | `schemas/pricing.py` (CompItem) |
| Conversational Copilot Chat | Yes | Yes | Messaging Thread Panel | `routes/copilot_orchestrator.py` |
| What-If Scenario Analysis | Yes | Yes | Property modifications form controls | `routes/copilot_tools.py` |
| Negotiation Offers Estimations | Yes | Yes | Suggestion offerings visual bands | `routes/copilot_tools.py` |
| Investment Yield Appraisals | Yes | Yes | ROI projections summary grids | `routes/copilot_tools.py` |
| Geographical Market Analytics | Yes | Yes | Compounds/areas density visual maps | `routes/copilot_tools.py` |
| Workspaces Sessions CRUD | Yes | Yes | Workspaces Selector views | `routes/copilot.py` |
| Scenario Lineage Trees | Yes | Yes | Hierarchical tree nodes viewer | `routes/copilot.py` |

---

# UX Recommendations

* **Interactive Map Pickers**: Since the manual coordinates mode requires exact decimals, the UI must allow users to tap a location on a map to extract coordinates, resolving local addresses asynchronously.
* **Citations Panel**: When grounding gate warnings or zero citations occur, the message text should highlights assertions requiring confirmation, linking directly to the corresponding listing details in the comparables inspector.
* **Scenario comparison gauges**: When modifications are calculated via What-If scenario tools, the delta value should render red or green based on negative/positive impact compared to baseline.

#### Source References
* `pf_scraper/fair-price-eg/backend/app/api/schemas/pricing.py` (LocationMode constraints): Lines 90-140
* `pf_scraper/fair-price-eg/backend/app/api/schemas/copilot_tools.py` (WhatIfToolResponse changes): Lines 124-140
