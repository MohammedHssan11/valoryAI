# Copilot Orchestrator Architecture (Phase 5.5C)

## 1. Executive Summary
Phase 5.5C introduces the Copilot Orchestrator, a fully governed conversational layer that sits above the existing Tool Layer (Tools 1-8). The Orchestrator acts as the central control plane for understanding user intent, mapping intents to deterministic Tools, compressing output, and safely streaming natural language responses. It strictly preserves TruthLayer authority, eliminating LLM hallucination risks in real estate valuation.

## 2. Architectural Goals
- **Deterministic Execution:** Ensure every real estate fact, price, and comparable is mathematically derived by the TruthLayer, not an LLM.
- **Hallucination Prevention:** Enforce a strict separation between raw data extraction and LLM narration.
- **Context Optimization:** Eliminate context window overflow via deterministic output compression.
- **Conversational Continuity:** Maintain tenant-isolated state across multi-turn broker interactions.

## 3. Non-Goals
- The Orchestrator will **not** reason about real estate logic independently.
- The Orchestrator will **not** calculate ROI, fair values, or offer bands.
- The Orchestrator will **not** create new backend Tools (e.g., No Tool 9).

## 4. Governance Rules
- **Rule 1: Strict Summarization.** The LLM may *only* summarize the locked deterministic context provided by the Tool Layer.
- **Rule 2: Arithmetic Offload.** The LLM must never execute arithmetic operations (differences, averages, percentages).
- **Rule 3: Explicit Evidence.** Every generated statement must carry persisted evidence references (`tool_event_id`, `snapshot_id`).
- **Rule 4: TruthLayer Authority.** The Orchestrator must never bypass Tools 1-8 to query the database or CMT engines directly.

## 5. Orchestrator Responsibilities
- **Understand user intent:** Classify incoming chat into governed categories.
- **Select tools:** Map the intent to the correct Tool or combination of Tools.
- **Chain tools:** Manage the execution order, including parallel invocation.
- **Compose responses:** Normalize, compress, and deterministically diff Tool outputs.
- **Maintain conversation state:** Hydrate context using the Copilot Memory Layer.

## 6. Orchestrator Non-Responsibilities
- Valuing properties.
- Pricing or negotiating.
- Forecasting trends or appreciation.
- Fabricating missing comparables or scenario evidence.

## 7. High-Level Architecture

`User -> Intent Engine -> Tool Planner -> Tool Executor -> Response Composer -> LLM Narrator -> User`

- **Intent Engine:** Analyzes user input to classify the primary goal.
- **Tool Planner:** Maps the intent to the required Tool sequence.
- **Tool Executor:** Invokes Tools 1-8 securely.
- **Response Composer:** Normalizes, summarizes, and compresses Tool outputs into a strict prompt schema.
- **LLM Narrator:** Streams natural language based exclusively on the Composer's payload.

---

## 8. Intent Engine

- **Purpose:** Deterministically classify the user's natural language input into a predefined taxonomy.
- **Scope:** 1:1 mapping to Tools 1-8, plus Property Comparison and General chat.
- **Rule-Based V1 decision:** To minimize latency, V1 will utilize a fast, lightweight ML text classifier or deterministic rule-based router rather than a heavy LLM.
- **Intent taxonomy:**
  - `VALUATION`
  - `EXPLAINABILITY`
  - `COMPARABLES`
  - `FAIRNESS`
  - `WHAT_IF`
  - `NEGOTIATION`
  - `INVESTMENT`
  - `MARKET_INSIGHT`
  - `PROPERTY_COMPARISON`
  - `GENERAL_QUESTION`
- **Confidence handling:** If the classifier returns a low confidence score, the Engine must not guess.
- **Fallback behavior:** Degrade gracefully to `GENERAL_QUESTION` or re-prompt the user for clarification.

---

## 9. Tool Planner

- **Intent → Tool mapping:** Maps intents directly to their corresponding Copilot Tools. (e.g., `WHAT_IF` -> Tool 5). Note that `NEGOTIATION` -> Tool 6 naturally encompasses Tools 1-5.
- **Multi-intent handling:** Decomposes complex queries (e.g., "What's the market trend and is my property overpriced?") into independent Tool chains.
- **Parallel execution opportunities:** Executes non-dependent chains simultaneously (e.g., Tool 8 for Market Insight and Tool 1 for Valuation).

---

## 10. Tool Executor

- **Tools 1-8:** Dispatches authenticated, tenant-scoped requests to the operational Copilot Tools.
- **Execution boundaries:** Operates strictly via internal API contracts. Does not interact with PostgreSQL or PostGIS directly.
- **Failure handling:** Catches TruthLayer errors (e.g., "Insufficient Evidence"). Does not attempt to guess or bypass the failure.
- **Timeout strategy:** Enforces strict HTTP timeouts. If a parallel tool hangs, the Executor returns a partial payload to the Composer rather than crashing the entire response.

---

## 11. Response Composer

- **Output normalization:** Standardizes diverse JSON payloads from Tools 1-8 into a unified `OrchestratorContext` Pydantic schema.
- **Arithmetic offload:** Performs all required math (averages, counts, differences) in code before LLM ingestion.
- **Property comparison:** Computes mathematical deltas (size, price, features) between two distinct Tool 1 payloads natively in code.
- **Evidence summarization:** Distills metrics (e.g., computing `max_price`, `min_price` from a list of comparables).
- **Comparable compression:** Implements the Top-N rules to prevent prompt bloat.
- **Citation preservation:** Extracts `snapshot_id`, `tool_event_id`, and `comparable_ids` to attach as strict metadata in the frontend SSE stream.

---

## 12. Context Compression

- **Top-N rule:** Restrict arrays to top N elements (e.g., Top 3 comparables, Top 3 SHAP drivers).
- **Truncation rules:** Flatten deeply nested objects. Strip PII, raw geospatial geometries, and database identifiers (except for required citations).
- **Compression pipeline:** `Raw Retrieval -> Context Stripping -> Array Truncation -> Deterministic Aggregation -> LLM Prompt Assembly`.
- **Evidence preservation:** Excluded/truncated evidence MUST be passed alongside the SSE stream in a hidden `citations_payload` so the frontend UI can still render the complete evidence map.

---

## 13. Property Comparison Design

**Final Approved Decision:** NO TOOL 9.
Comparison is handled exclusively by the Orchestrator's Response Composer.

- **Workflow:** 
  1. Intent Engine detects `PROPERTY_COMPARISON`.
  2. Tool Executor runs Tool 1 for Property A and Tool 1 for Property B in parallel.
  3. Response Composer intercepts both payloads and deterministically computes the deltas (Diff: +50k EGP, +20 sqm).
  4. The Composer injects the exact deltas into the LLM context.
  5. LLM Narrator summarizes the pre-calculated diff.
- **Risks:** The LLM hallucinating math errors if raw prices are passed without explicit deltas.
- **Mitigations:** The Composer *must* calculate the diffs natively. The LLM system prompt must forbid independent arithmetic.

---

## 14. Conversation State Machine

1. **User Input:** Receive text and session context.
2. **Intent Engine:** Classify intent and confidence.
3. **Tool Planner:** Build execution graph.
4. **Tool Executor:** Fetch TruthLayer data.
5. **Response Composer:** Normalize, diff, and compress payload.
6. **LLM Narrator:** Stream text to user.
7. **Memory Update:** Persist Assistant response to `messages`.

---

## 15. Memory Architecture

- **Conversation Memory (`chats`, `messages`):** Manages narrative continuity.
- **Workspace Memory (`workspaces`):** Enforces JWT tenant isolation.
- **Property Memory (`property_states`):** Secures baseline property facts.
- **Scenario Memory (`scenario_states`, `scenario_lineage`, `assumptions`):** Preserves immutable What-if overlays.
- **Broker Session Memory (`broker_sessions`):** Handles application restart recovery.

---

## 16. Hallucination Prevention

- **Strict Composer Diffs:** All deltas and statistics are computed by Python code, not the LLM.
- **Top-N Context Limits:** Prevents lost-in-the-middle hallucination caused by massive payloads.
- **Negative Prompt Constraints:** The LLM prompt explicitly bans "predict", "will", "forecast", and "calculate".
- **Sparse Evidence Pass-through:** If Tool 8 returns "Sparse", the Orchestrator explicitly states "Sparse evidence" and is forbidden from inventing trends.
- **Citation Anchoring:** Every LLM claim is backed by a deterministic `tool_event_id` or `snapshot_id` sent to the UI.

---

## 17. Failure Handling

- **Tool failures:** Log to `shadow_logs`. LLM narrates graceful degradation (e.g., "I cannot access the valuation engine right now").
- **Sparse evidence:** Bubble up "Insufficient Evidence" or "Moderate Opportunity" directly from the TruthLayer.
- **Conflicting evidence:** Trust the TruthLayer. Display both data points and confidence metrics without fabricating a resolution.
- **Timeouts:** Use partial responses for parallel tools, or fail gracefully.
- **Missing context:** If frontend omits JWT, `workspace_id`, or `scenario_id`, immediately block execution and prompt the user.

---

## 18. Latency Strategy

- **Parallel execution:** Execute independent tool chains concurrently.
- **Streaming:** Stream intermediate progress markers (`{"status": "running_valuation"}`) to the UI via SSE to improve perceived latency before LLM generation begins.
- **Expected bottlenecks:** Intent classification and Tool Execution are the primary bottlenecks; mitigation relies on fast ML classifiers and parallelization.

---

## 19. Security Model

- **JWT:** Required for all Orchestrator routes.
- **Tenant Isolation:** Enforced via `workspace_id` matching on all memory and Tool Layer retrievals.
- **Audit Trail:** Every Orchestrator action results in a persisted `decision_history` or `tool_events` record, ensuring 100% traceability.

---

## 20. Open Questions

*(These questions remain open and must be resolved by the Product/Engineering teams during implementation)*
1. Is there a defined timeout budget for parallel tool executions before returning a partial payload?
2. What is the exact payload structure expected by the frontend for citation tracking in the SSE stream?
3. Will the Intent Classifier be deployed as an LLM or a traditional ML text classifier?
4. Will the frontend `BrokerScreen` send `workspace_id` and `scenario_id` context reliably before launch?

---

## 21. Implementation Roadmap

- **Phase 5.5C.1:** Intent Engine
- **Phase 5.5C.2:** Tool Planner
- **Phase 5.5C.3:** Tool Executor
- **Phase 5.5C.4:** Response Composer
- **Phase 5.5C.5:** Memory Integration
- **Phase 5.5C.6:** LLM Integration

---

## 22. Final Architecture Decision

**This architecture is APPROVED for Codex implementation.**

- **Reasons:** It rigorously enforces TruthLayer authority, eliminates the risk of the LLM acting as a valuation engine, mathematically secures property comparisons, and maps directly to the validated Tool 1-8 backend.
- **Tradeoffs:** Increased latency due to multi-step execution and increased codebase complexity in the Response Composer.
- **Known Risks:** Potential for context window overflow if compression rules are implemented incorrectly; dependency on frontend context injection.
- **Mitigations:** The strict Top-N truncation pipeline, Arithmetic Offload rules, and P0 blocker for frontend context integration.
