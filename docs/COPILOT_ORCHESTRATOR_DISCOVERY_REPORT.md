# Phase 5.5C: Copilot Orchestrator Discovery Report

## MISSING INFORMATION REQUIRED
- **Property Comparison Tool:** The User Journey Analysis requested handling for "Compare these two properties." However, Section 10 of `PROJECT_MASTER_STATE_V2.md` lists only Tools 1-8. None of these tools explicitly support arbitrary dual-property comparison. Tool 3 only retrieves TruthLayer comparable evidence for a single property/snapshot. An architectural decision for this specific journey cannot be made until this capability is defined.
- **Intent and Reason Endpoint Schemas:** Section 7 lists `/v1/broker/intent` and `/v1/broker/reason` as implemented. The exact request and response schemas for these endpoints are undocumented, blocking concrete schema design for the state machine.

---

## 1. Current State Assessment
- **What exists today?**
  - **Tool Layer:** Tools 1 through 8 (Valuation, Explainability, Comparable, Fairness, What-if, Negotiation, Investment, Market Insight) are fully implemented, authenticated, tenant-isolated, and Docker-validated. (Source: Section 10)
  - **Broker Adapter:** Implemented and Docker-validated, but currently only utilizes Tool 1 and Tool 2. Direct pricing route usage was eliminated. (Source: Section 6, Phase 5.5B.2A)
  - **Copilot Memory Layer:** Workspaces, chats, messages, property_states, scenario_states, assumptions, decision_history, tool_events, valuation_snapshots, scenario_lineage, broker_sessions are implemented and durable. (Source: Section 9)
  - **Backend Endpoints:** `/v1/broker/analyze`, `/chat`, `/intent`, `/reason`, `/stream`, `/session/{session_id}` exist. (Source: Section 7)

## 2. Capability Gap Analysis
- **Missing before broker can chat naturally:**
  - Tools 3 through 8 are not yet registered in the Broker Adapter's Tool Registry. The Orchestrator cannot route to them.
  - Multi-tool chaining logic (e.g., calling Tool 1, then Tool 5, then Tool 6 sequentially) within a single conversation turn is not orchestrated dynamically.
  - Frontend integration for JWT, `workspace_id`, and `scenario_id` is missing, which breaks tenant isolation in the chat context. (Source: Section 8)

## 3. User Journey Analysis
- **"Is this property overpriced?"**
  - **Required Tools:** Tool 1 (Valuation) + Tool 4 (Fairness). Optional: Tool 6 (Negotiation) if offer band is requested.
- **"What if I add a gym?"**
  - **Required Tools:** Tool 5 (What-if).
- **"Should I negotiate?"**
  - **Required Tools:** Tool 6 (Negotiation).
- **"Compare these two properties."**
  - **Required Tools:** **UNVERIFIED / MISSING INFORMATION REQUIRED**. No Tool 9 exists for dual-property comparison.
- **"What is happening in Mivida?"**
  - **Required Tools:** Tool 8 (Market Insight).

## 4. Intent Taxonomy
- **VALUATION:** Determine property value. (Maps to Tool 1)
- **EXPLAINABILITY:** Understand valuation rationale. (Maps to Tool 2)
- **COMPARABLES:** View similar properties used as evidence. (Maps to Tool 3)
- **FAIRNESS:** Assess asking price fairness. (Maps to Tool 4)
- **WHAT_IF:** Evaluate hypothetical scenarios. (Maps to Tool 5)
- **NEGOTIATION:** Request negotiation positions, offer bands. (Maps to Tool 6)
- **INVESTMENT:** Request investment opportunity analysis. (Maps to Tool 7)
- **MARKET_INSIGHT:** Request descriptive historical and compound trends. (Maps to Tool 8)
- **PROPERTY_COMPARISON:** **UNVERIFIED**. Needs clarification.
- **GENERAL_QUESTION:** Non-real estate or casual chat.

*Why these intents?* They map deterministically 1:1 with the governed Copilot Tools 1-8 to ensure TruthLayer authority is preserved without LLM hallucination.

## 5. Tool Routing Matrix
| Intent | Required Tool(s) | Response Type |
|--------|------------------|---------------|
| VALUATION | Tool 1 | Deterministic valuation snapshot & confidence |
| EXPLAINABILITY | Tool 2 | Structured explanation & feature drivers |
| COMPARABLES | Tool 3 | Real CMT evidence list |
| FAIRNESS | Tool 4 | Normalized fairness response |
| WHAT_IF | Tool 5 | Deltas, assumptions, fresh valuation |
| NEGOTIATION | Tool 6 | Positions, offer bands, talking points, risks |
| INVESTMENT | Tool 7 | Opportunity positions, strengths, risks |
| MARKET_INSIGHT | Tool 8 | Traceable descriptive observations |

*Why?* The Orchestrator must not reason about real estate. Mapping intent directly to Tool Layer adapters guarantees no LLM price generation.

## 6. Conversation State Machine
`User Input -> Intent Detection (/intent) -> Tool Planning (/reason or /analyze) -> Tool Execution (Tool Layer) -> Response Composition (/stream)`

*Why?* This follows the existing Broker endpoint surface (`/v1/broker/analyze`, `/chat`, `/intent`, `/reason`, `/stream`) documented in Section 7. It ensures planning is logically decoupled from response generation, allowing validation before LLM streaming.

## 7. Memory Architecture
- **Conversation Memory (`chats`, `messages`):** Stored to maintain dialogue context and conversational continuity.
- **Workspace Memory (`workspaces`):** Stored to enforce JWT tenant isolation boundaries.
- **Property Memory (`property_states`):** Stored to keep baseline property facts immutable.
- **Scenario Memory (`scenario_states`, `scenario_lineage`, `assumptions`):** Stored to allow ephemeral what-if overlays without mutating base properties.
- **Broker Session Memory (`broker_sessions`):** Stored for restart recovery and context hydration.
*Retention strategy:* Kept persistently in PostgreSQL/PostGIS. Survived backend/DB restarts in Phase 5.5B.1R.

## 8. Hallucination Prevention
*MANDATORY*
The orchestrator prevents invented prices, insights, comparables, and unsupported recommendations by:
- Operating ONLY as a deterministic orchestrator over Tools 1-8. It DOES NOT value or price. (Source: Section 1)
- Enforcing LLM narration to *only* summarize locked deterministic context. (Source: Section 18)
- Outputting "Insufficient Evidence" or "Sparse" directly when TruthLayer returns sparse data, explicitly forbidding the invention of trends or comparable replacements. (Source: Section 16)

## 9. Failure Handling
- **Tool timeout / Tool failure:** Bubble up technical failure gracefully to user, do not guess values. Log to `shadow_logs` or `tool_events`.
- **No evidence / Sparse evidence:** Echo Tool 7 / Tool 8 handling (return `Insufficient Evidence` or `Moderate Opportunity`). Do NOT invent evidence.
- **Conflicting evidence:** Trust TruthLayer. Orchestrator must not resolve conflicts; it must display the TruthLayer's output and confidence levels.

## 10. Architecture Alternatives
**Alternative A: Single-Prompt ReAct LLM Agent**
- *Pros:* Flexible, simple to implement.
- *Cons:* LLM handles planning and execution simultaneously; high hallucination risk; non-deterministic tool chaining.
- *Status:* Rejected.

**Alternative B: Deterministic Multi-Step Pipeline (Intent -> Plan -> Execute -> Narrate)**
- *Pros:* Strictly maps to existing `/intent`, `/reason`, `/analyze` endpoints. Low hallucination risk. Governed execution.
- *Cons:* Higher latency due to multiple discrete phases.
- *Status:* Accepted. Maps to existing API design and strictly enforces governance.

**Alternative C: Hardcoded Rule-Based Router**
- *Pros:* Zero hallucination in routing.
- *Cons:* Cannot handle complex conversational requests easily.
- *Status:* Rejected.

## 11. Decision Log
*(See `COPILOT_ORCHESTRATOR_DECISION_LOG.md` for full details)*
- Adopt Alternative B (Deterministic Multi-Step Pipeline).
- Limit the Orchestrator's Tool Registry strictly to Copilot Tools 1 through 8.
- Restrict LLM narration strictly to the JSON output of the executed Tools.

## 12. Open Questions
*(See `COPILOT_ORCHESTRATOR_OPEN_QUESTIONS.md` for full details)*
- Missing Property Comparison Tool.
- Undocumented schemas for `/intent` and `/reason`.

## 13. Architecture Recommendation
**Decision**
Implement the Copilot Orchestrator as a Deterministic Multi-Step Pipeline (Alternative B) orchestrating exclusively over Tools 1-8, utilizing the existing `/intent`, `/reason`, `/analyze`, and `/stream` endpoints.

**Evidence**
- Master State Section 7: Existing Broker endpoints (`/intent`, `/reason`, `/stream`) are already implemented.
- Master State Section 10: Tools 1-8 are implemented, tenant-isolated, and ready for orchestration.
- Master State Section 18: "LLM narration may summarize locked deterministic context. It must not become a valuation authority."

**Why**
The Orchestrator MUST NOT value, price, negotiate, or forecast. By decoupling intent detection and tool planning from the final generative narration, the architecture forces the LLM to act strictly as a summarizer of the Tool Layer's deterministic outputs, mathematically eliminating the risk of ungrounded real estate reasoning.

**Tradeoffs**
Increased total response latency compared to a single-pass LLM, as multiple discrete network hops/inference steps are required before the final SSE stream begins.

**Risks**
Large JSON payloads from combined tool outputs (e.g., Tool 1 + Tool 2 + Tool 3) may exceed the LLM's context window during response composition.

**Open Questions**
How should payload truncation be handled if the combined output of Tools 1-8 exceeds the LLM context limits, without losing TruthLayer authority?
