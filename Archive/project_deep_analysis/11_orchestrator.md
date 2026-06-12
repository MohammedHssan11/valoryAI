# 11. Orchestrator Control Plane

This document details the architecture and runtime flow of the Copilot Orchestrator, the control plane that manages natural language understanding, tool chaining, context compression, and narration constraints.

---

## 1. Runtime Integration Layer
The orchestrator is initialized at runtime using the builder function:
* **Source File:** [runtime.py](file:///c:/Users/mh978/Downloads/mobile%20computing%20project/pf_scraper/fair-price-eg/backend/app/copilot/orchestrator/runtime.py)
* **Active Class:** `CopilotOrchestratorRuntimeV1`
* **Entry Method:** `run()`

```
User Message Text
  │
  ├── 1. Intent Engine (engine.py)
  │      RuleBasedIntentEngine.classify() ──► IntentResult
  │
  ├── 2. Tool Planner (planner.py)
  │      DeterministicToolPlanner.plan()  ──► ExecutionPlan
  │
  ├── 3. Tool Executor (executor.py)
  │      DeterministicToolExecutor.execute() ──► ExecutionResult
  │
  ├── 4. Response Composer (composer.py)
  │      DeterministicResponseComposer.compose() ──► ComposedResponse
  │
  ├── 5. Memory Integration (integration.py)
  │      DeterministicMemoryIntegration.remember() ──► MemoryContext
  │
  └── 6. LLM Narrator (llm/)
         CopilotOrchestratorLLMV1.narrate() ──► NarrationResult
```

---

## 2. Orchestrator Components

### 1. Intent Engine (`intents/engine.py`)
* **Purpose:** Classifies user messages into a predefined intent taxonomy.
* **Intents Supported:**
  - `VALUATION`: Direct property pricing.
  - `EXPLAINABILITY`: Rationale and drivers.
  - `COMPARABLES`: Comparable listings requests.
  - `FAIRNESS`: Asking price audit.
  - `WHAT_IF`: Renovation or feature changes.
  - `NEGOTIATION`: Offer strategies and counter-offers.
  - `INVESTMENT`: Risk and strengths summaries.
  - `MARKET_INSIGHT`: Workspace aggregations.
  - `PROPERTY_COMPARISON`: Side-by-side properties comparison.
  - `GENERAL_QUESTION`: Conversational check-ins and general questions.
* **Classification Strategy:** Uses rule-based keyword matching and syntactic checks to guarantee deterministic classification with zero latency.

### 2. Tool Planner (`planner/planner.py`)
* **Purpose:** Maps the classified intent to the required Tool or sequence of Tools.
* **Planning Output:** Generates an `ExecutionPlan` containing a list of `PlannedToolCall` records.
* **Multi-Intent Handling:** If the user asks a complex question (e.g. "What is the valuation of my apartment and is it overpriced?"), the planner schedules both the Valuation and Fairness tools.

### 3. Tool Executor (`executor/executor.py`)
* **Purpose:** Securely executes the tool calls scheduled in the execution plan.
* **Execution Boundary:** Communicates strictly via internal API calls. It has no direct access to PostgreSQL, PostGIS, or model files, preventing security leakage.
* **Error Containment:** If a tool call fails, the executor catches the error and returns a partial result to the Response Composer rather than crashing the request.

### 4. Response Composer (`composer/composer.py`)
* **Purpose:** Normalizes diverse tool payloads, executes arithmetic calculations in Python, and compresses prompt context.
* **Key Features:**
  - **Arithmetic Offloading:** Computes all required metrics (averages, counts, differences, percentages) natively in Python before assembling the prompt context.
  - **Property Comparison Deltas:** If the intent is `PROPERTY_COMPARISON`, the executor runs the Valuation Tool (Tool 1) for both properties. The Response Composer computes the size and price deltas in code and passes the pre-calculated diffs to the LLM.
  - **Context Compression (Top-N Rules):** Truncates arrays (e.g., keeping only the Top 3 comparables and Top 3 SHAP drivers) to fit the prompt within context window limits.
  - **Citations Packaging:** Packs `valuation_id`, `tool_event_id`, and `comparable_ids` into a structured metadata package sent alongside the SSE stream.

### 5. Memory Integration (`memory/integration.py`)
* **Purpose:** Manages multi-turn conversation states and scenario overlays.
* **Tenant Isolation:** Resolves and filters all database lookups (`chats`, `property_states`, `assumptions`) using the JWT-validated `workspace_id`.
* **State Updates:** Appends the user message and assistant narration to the `messages` table, maintaining thread continuity.

### 6. LLM Integration (`llm/`)
* **Purpose:** Interacts with language models to stream natural language responses.
* **System Prompts:** Instructs the model to act as a grounded narrator. The prompt strictly forbids the model from performing calculations or referencing external knowledge.
* **Narration Admission Gate:** If the generated text references unverified claims or missing citations, the gate rejects the text and defaults to the deterministic JSON payload (`DETERMINISTIC_FALLBACK`).
