# 14. Final Architecture Specifications

This document defines the final system architecture of the platform. We detail the component interactions, user flows, security models, and background processes.

---

## 1. System Components & Interaction Diagram

```mermaid
flowchart TD
    subgraph Mobile Client (Flutter UI)
        UI[App Screens] <-->|Bloc / Riverpod States| Controllers[Feature Controllers]
        Controllers <-->|Dio HTTP Requests| PublicClient[Public API Client]
        Controllers <-->|Bearer JWT SSE| AuthClient[Authenticated SSE Client]
    end

    subgraph Backend Gateways (FastAPI Router)
        PublicClient -->|/v1/valuation/| ValRouter[Valuation Route]
        AuthClient -->|/v1/copilot/| CopilotRouter[Copilot Router]
        AuthClient -->|/v1/broker/stream| SSE[SSE Controller]
    end

    subgraph Orchestrator Plane (services/copilot_service.py)
        CopilotRouter -->|run| Exec[Runtime V1 Activation]
        Exec -->|1. Classify| Intent[Intent Engine]
        Exec -->|2. Schedule| Planner[Tool Planner]
        Exec -->|3. Invoke| ToolExec[Tool Executor]
        Exec -->|4. Normalize| Composer[Response Composer]
        Exec -->|5. Context| Memory[Memory Integration]
        Exec -->|6. Stream| LLM[LLM Narrator]
    end

    subgraph Truth Layer (Tools 1-8)
        ToolExec -->|Tool 1: valuation| ValService[valuation_service.py]
        ToolExec -->|Tool 5: what-if| WhatIfService[what_if]
        ToolExec -->|Tool 6: negotiation| NegService[negotiation]
        ToolExec -->|Tool 7: investment| InvService[investment]
        ToolExec -->|Tool 8: market-insight| MarketService[market_insight]
    end

    subgraph Mathematical Pricing Layer
        ValService -->|CMT Search Tiers| Selector[selector.py]
        Selector -->|recursive SQL| DB[(PostgreSQL + PostGIS)]
        ValService -->|Prune Outliers| MAD[filters.py: MAD outlier removal]
        ValService -->|Scoring weights| Weights[weights.py: weighted median]
        
        ValService -->|Fallback Inference| MLService[ml_service.py]
        MLService -->|Predict| CatBoost[(CatBoost Models: Rent & Sale)]
        MLService -->|Explainability| SHAP[SHAP Feature Importance]
    end

    subgraph Persistence Layer
        DB <-->|workspaces, chats, messages, properties| Memory
        DB -->|insert logs| Monitoring[monitoring_service.py]
        Monitoring -->|write prediction_logs| PredictionLogs[(prediction_logs)]
        Monitoring -->|write shadow_logs| ShadowLogs[(shadow_logs)]
    end

    style Exec fill:#ede7f6,stroke:#5e35b1,stroke-width:2px
    style ValService fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    style MLService fill:#e8eaf6,stroke:#1a237e,stroke-width:2px
    style DB fill:#efebe9,stroke:#4e342e,stroke-width:2px
```

---

## 2. Core User Flows

### Valuation Request Flow
1. **Input:** The user submits a property configuration (size, room counts, location) via the mobile client.
2. **Resolution:** The backend resolves the coordinates point and runs a spatial polygon containment check to identify the leaf area.
3. **Retrieval Tiers:** The comparable selector queries listings recursively through Tiers 1-5, expanding the search radius up to 15km if listing density is low.
4. **Filtering:** The retrieved comparables are filtered using hard guardrails and a modified Z-score using MAD.
5. **Weighted Median:** Remaining listings are weighted based on distance, size, age, and features similarities. The P20, P50 (fair price), and P80 price estimates are resolved.
6. **Confidence & Response:** The system computes the evidence confidence score, applies location caps, and compiles the structured JSON response.

### Conversational Co-pilot Flow
1. **Entry:** The user sends a natural language message in a chat thread.
2. **Intent Classification:** The RuleBasedIntentEngine classifies the request into the intent taxonomy (e.g. `WHAT_IF` or `NEGOTIATION`).
3. **Planning & Execution:** The Tool Planner maps the intent to the required tools (Tools 1-8). The Tool Executor dispatches request calls to the tools.
4. **Composition:** The Response Composer normalizes the tool outputs, executes comparison math or deltas natively in Python, and truncates the context to fit within the prompt window.
5. **Narration & Grounding:** The LLM Narrator drafts a natural language response. The Narration Admission Gate validates that every claim matches composed facts and includes citations.
6. **Fallback Recovery:** If the generated text violates grounding checks, the system suppresses the text and returns the raw JSON payload (`DETERMINISTIC_FALLBACK`).

---

## 3. Telemetry & Shadow Run Cycle
Valuation requests trigger a background monitoring loop to audit pricing engine variance:
* **Background Trigger:** When a valuation request completes, the router triggers `execute_shadow_pipeline` via FastAPI's `BackgroundTasks`.
* **Execution:** The router executes predictions on the alternate model (e.g., executing CatBoost ML if CMT was selected, or vice versa).
* **Logging:** The active price, shadow price, comparable counts, and confidence levels are logged to `shadow_logs` to audit model drift.

---

## 4. Network Boundaries & JWT Security
* **Public Boundary:** Health check routes (`/health`, `/health/ready`) and direct valuation routes are public to minimize latency for raw queries.
* **Authenticated Boundary:** Co-pilot memory, tools, and orchestrator routes require a bearer JWT token:
  - JWT tokens are validated against configured issuer and audience claims.
  - Database queries are filtered by user ID to guarantee strict tenant isolation.
  - Attempting to query another tenant's workspaces, property states, or chats returns `ACCESS_DENIED`.
