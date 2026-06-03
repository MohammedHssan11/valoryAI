# ValorAI Project Master State v3

**Last updated:** June 2, 2026  
**Purpose:** Single source of truth for overall project status.  
**Detailed mobile discovery:** `DISCOVERY_REPORT.md`  
**Frontend implementation guide:** `frontend.md`

## Project Overview

**ValorAI**  
**AI-Powered Real Estate Intelligence Platform**

ValorAI is a mobile-first real estate intelligence platform for explainable property valuation, comparable evidence, portfolio tracking, and governed AI-assisted analysis.

## Current Architecture

### Backend

- FastAPI backend under `pf_scraper/fair-price-eg/backend/`.
- PostgreSQL/PostGIS persistence.
- Deterministic category-aware valuation API.
- JWT-scoped Copilot memory, tools, and orchestrator APIs.
- Broker reasoning APIs with SSE streaming.
- Backend contracts and persisted state are the product source of truth.

### Frontend

- Flutter mobile app under `flutter_valorai/`.
- Feature-first folder structure exists.
- Material 3 dark theme foundation exists.
- GoRouter route foundation exists.
- Splash, Onboarding, Login, and authenticated session restore are implemented.
- Valuation Input is implemented as a backend-ready six-step experience.
- Valuation Result is implemented as the flagship response-backed intelligence screen.
- Comparable Explorer, Workspace, Copilot, and the backend-owned Home data slice are integrated.
- React implementations are visual and behavior references only.

### Authentication

- Product decision: Firebase Authentication.
- Planned providers: email/password, Google Sign-In, and Apple Sign-In.
- Flutter Firebase initialization and Firebase auth exception mapping exist.
- Login supports Firebase email/password, Google Sign-In, and Apple Sign-In.
- Backend `POST /v1/auth/token-exchange` verifies Firebase ID tokens and returns ValorAI JWTs.
- Flutter stores the ValorAI JWT and user metadata with `flutter_secure_storage`.
- Splash session restore, protected-route redirection, logout cleanup, and shared Dio JWT injection are implemented.

### Infrastructure

- Backend infrastructure includes FastAPI, Docker-oriented deployment, PostgreSQL, and PostGIS.
- Existing backend health routes: `/health`, `/health/ready`, `/health/metrics`, and `/health/operational`.
- Flutter platform configuration and Firebase environment configuration still need verification.

## Major Decisions

1. Use Firebase Authentication for the mobile application.
2. Build the primary product frontend as a Flutter mobile app.
3. Use React as a visual reference only. Do not port React application logic.
4. Treat backend APIs, contracts, and persisted state as the source of truth.
5. Keep provider secrets and direct AI-provider SDK calls out of the Flutter app.

## Current Phase

**Integration Sprint**

Current status: Firebase-to-ValorAI token exchange, secure mobile session
storage, authenticated Dio requests, workspace CRUD, Copilot transport, and the
backend-owned Home data slice are integrated. Real-device login walkthrough is
blocked until Firebase platform files and the deployed `FIREBASE_PROJECT_ID`
are supplied.

## Completed

- [x] Discovery Report
- [x] Flutter Folder Structure
- [x] Theme Foundation
- [x] Router Foundation
- [x] Splash
- [x] Onboarding
- [x] Login
- [x] Signup
- [x] Forgot Password
- [x] Home Dashboard
- [x] Valuation Input
- [x] Valuation Result
- [x] Comparable Explorer
- [x] Copilot
- [x] Workspace

Valuation Input includes:

- Four Egypt dataset categories: Residential Buy, Residential Rent, Commercial Buy, and Commercial Rent
- Category-aware property type lists with no placeholder options
- Hierarchical Governorate -> City -> District -> Compound location capture
- Device GPS support with runtime permission request
- Google Maps pin selection with automatic latitude and longitude population
- Conditional residential, commercial, and land detail layouts
- Positive required area validation
- Grouped multi-select amenity chips backed by real amenity codes
- Editable final review
- Real Dio submission to `POST /v1/valuation/fair-price`
- `ValuationRequest`, `ValuationRepository`, `ValuationRepositoryImpl`, and `ValuationRemoteDataSource`
- Response handoff into the Valuation Result foundation

Valuation Result includes:

- Dominant animated EGP fair-value hero with confidence badge and comparable count
- Dedicated low / expected / high fair-value spectrum
- Response-backed explainability cards from ML feature impacts or CMT confidence factors
- Truth-layer AI summary from backend narrative and explanation payloads only
- Evidence grid for comparable count, resolved area, district, governorate, radius, market tier, confidence tier, and resolution precision when available
- Top-three comparable cards with price, distance, similarity, area, size, and property type
- Optional market-context section that renders only backend-returned market values
- Compact Google Maps location-context preview using returned coordinates
- Sticky Explain, Comparables, Copilot, and Save action bar
- Response handoff navigation into Comparable Explorer

Comparable Explorer includes:

- Header metrics for total comparables, retrieval radius, and confidence
- Similarity, distance, and price sorting with similarity as the default
- Default list view with response-backed comparable cards and valuation influence when returned
- Context-only Google Maps view with visually distinct subject and comparable markers
- Comparable details bottom sheet with backend-returned property, amenity, retrieval, influence, and match evidence
- Collapsible "Why these comparables?" section with available backend similarity and confidence values

Copilot includes:

- Interactive drawer-based sidebar showing New Chat action, searchable list of sessions, and separate sections for Pinned Chats and Recent Sessions/History.
- Support for session Pinning, Renaming, and Deletion with confirmation.
- Context handoff from Valuation Result screen: renders active context chips (Property, Value, Confidence, Comps) above the chat.
- Live chat message canvas with typing indicators, loading states, and multiline composer locking.
- Structured component mapping for five high-fidelity cards: Property Summary Cards, Model Confidence Cards, Evidence Drivers Cards, Comparable Control Cards, and Market Signals Cards.
- Structured API response integration targeting `POST /v1/copilot/orchestrator/respond` using authenticated Dio.
- No mock transport fallback. Backend failures remain visible.

Workspace includes:

- Workspace Selector screen displaying backend-owned name, property count, creation/activity times, and active status.
- Live CRUD dialogs (Create, Edit, Delete) through `/v1/copilot/workspaces*`.
- No generated workspaces, local description cache, or offline mock fallback.
- Active Workspace State (`WorkspaceStateManager`) that feeds current workspace IDs directly to the Copilot query payload and renders dynamically on the Home screen.

Home integration includes:

- `GET /v1/copilot/users/me`
- `GET /v1/copilot/workspaces`
- `GET /v1/copilot/workspaces/{workspace_id}/properties`
- `GET /v1/copilot/workspaces/{workspace_id}/chats`
- Graceful hiding for unavailable saved-valuation, market-signal, and AI-insight sections.

Auth integration includes:

- `POST /v1/auth/token-exchange`
- Firebase RS256 signature verification against Google signing certificates.
- Firebase issuer and audience validation against configured `FIREBASE_PROJECT_ID`.
- Reuse of the existing user provisioning and ValorAI HS256 JWT authorization boundary.
- Secure JWT and user metadata storage, app-launch restore, logout cleanup, and one-time `401` re-exchange.
- Protected-route redirect to Login after an expired session and explicit `403` handling.

## In Progress

- [ ] Firebase Deployment Configuration

Current Firebase foundation includes:

- `Firebase.initializeApp()` bootstrap
- Firebase authentication exception-to-message mapping
- Firebase email/password login
- Firebase Google Sign-In
- Firebase Apple Sign-In
- Firebase email/password signup with display-name update
- Firebase password-reset email flow

Still required:

- Add Android `google-services.json`.
- Add iOS `GoogleService-Info.plist`.
- Configure the deployed backend `FIREBASE_PROJECT_ID`.
- Run a real Firebase account walkthrough on an emulator or device.

## Pending

- [ ] Portfolio
- [ ] Profile

## Risks

- Firebase deployment configuration files are absent from the Flutter project, so device login cannot initialize against a real Firebase project yet.
- Direct valuation routes are currently public while Broker and Copilot routes require bearer JWTs. The intended mobile policy must be confirmed.
- The backend does not expose location autocomplete, listing browse, or listing-detail APIs.
- The backend does not expose profile mutation, avatar upload, notification, support-ticket, or report-download APIs.
- Portfolio and Profile remain placeholder or pending Flutter product screens.
- React prototypes include mocked values and inactive controls; they must not be treated as functional requirements.
- Egypt dataset property types exceed the active governed valuation contracts. Unsupported combinations are captured honestly and do not produce fabricated results.
- Google Maps requires deployment-time native API key injection. No Maps secret is committed.

## Blockers

1. Supply the Firebase project ID to the backend and add Flutter platform Firebase configuration files.
2. Run the physical-device or emulator Login -> Home -> Workspace -> Valuation -> Result -> Comparables -> Copilot walkthrough.
3. Decide whether direct valuation remains public or requires authentication.
4. Define a location autocomplete API to replace typed City, District, and Compound entry with backend suggestions.
5. Inject native Google Maps API keys for deployment builds.

## Next Actions

1. Configure Firebase platform files and backend `FIREBASE_PROJECT_ID`.
2. Execute the real-device integration walkthrough.
3. Connect workspace-backed valuation saving after the persistence flow is defined.
4. Define the backend location autocomplete route and connect `LocationAutocompleteRepository`.

## Change Log

| Date | Change |
| --- | --- |
| June 2, 2026 | Created project documentation foundation: `PROJECT_MASTER_STATE_v3.md` and `frontend.md`. |
| June 2, 2026 | Completed Sprint 2 entry slice: premium Splash, two-page Onboarding, and Firebase-backed Login with email/password, Google, and Apple providers. Verified with `flutter analyze`. |
| June 2, 2026 | Completed Sprint 3A: Firebase email/password Signup with Google continuation and Firebase Forgot Password reset-email flow. Verified with `flutter analyze`. |
| June 2, 2026 | Completed Sprint 3B Home Dashboard: mock-data hero, quick actions, AI insight, portfolio overview, market signals, recent valuations, recent Copilot sessions, and five-item bottom navigation. Verified with `flutter analyze`. |
| June 2, 2026 | Completed Sprint 4A Valuation Input rebuild: six-step premium category-aware flow, GPS, Google Maps pinning, hierarchical address resolution, conditional details, real amenity chips, editable review, Dio-backed valuation submission, backend contract boundary handling, and response-backed Valuation Result foundation. Verified with `flutter analyze`. |
| June 2, 2026 | Completed Sprint 4B flagship Valuation Result rebuild: animated fair-value hero, valuation spectrum, typed response mapping, backend-only explainability and AI summary, evidence grid, top-three comparable evidence, optional market context, compact map, sticky actions, and response-backed Comparable Explorer navigation. Verified with `flutter analyze` and `flutter test`. |
| June 2, 2026 | Completed Sprint 5 Comparable Explorer: response-backed list and map views, similarity / distance / price sorting, comparable detail bottom sheet, valuation-influence display, collapsible backend evidence panel, and graceful hiding for unavailable fields. Verified with `flutter test`; `flutter analyze` reports only existing Copilot-file findings outside this feature. |
| June 2, 2026 | Completed Sprint 6 Copilot: drawer-based sidebar (New Chat, History, Pin, Rename, Delete, Search), response-backed message canvas, five high-fidelity structural cards (Property Summary, Confidence, Evidence, Comparable References, Market Insights), context chip banners, and Dio-based response integrations with fallback. Verified with `flutter analyze`. |
| June 2, 2026 | Completed Sprint 7 Workspace: dynamic Selector screen, Create/Edit/Delete dialogs, active workspace state binding, Home header integration, Copilot context integration, backend `/v1/copilot/workspaces*` API mapping, and comprehensive unit tests. Verified clean with `flutter analyze` and `flutter test`. |
| June 2, 2026 | Completed Integration Sprint code path: Firebase ID token exchange, Firebase claim verification, ValorAI JWT minting, secure Flutter session storage, session restore, Dio auth retry/cleanup, protected-route redirect, backend-only Workspace CRUD, live Copilot transport, backend-owned Home mapping, and integration tests. Verified with clean `flutter analyze`, 11 passing Flutter tests, 9 passing targeted backend tests, and Docker Compose config validation with required environment placeholders. Real Firebase walkthrough remains blocked by missing deployment configuration. |
