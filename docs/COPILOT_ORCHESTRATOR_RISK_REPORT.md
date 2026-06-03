# Phase 5.5C: Copilot Orchestrator Risk Report

| Priority | Risk | Mitigation Strategy | Evidence Source |
|----------|------|---------------------|-----------------|
| **P0** | Frontend does not send JWT, `workspace_id`, or `scenario_id` during broker chat. | Must block production deployment of Phase 5.5C until frontend context bootstrap is implemented. The Orchestrator cannot enforce tenant isolation or state retrieval without these. | Master State Section 8, 16 |
| **P1** | Direct valuation routes remain unauthenticated, posing a backdoor risk if Orchestrator is bypassed. | Enforce intended public/internal authentication policy before Orchestrator launch. | Master State Section 16 |
| **P2** | Sparse TruthLayer comparable results can truthfully limit Orchestrator tool outputs (Tools 6, 7). | Orchestrator narration must accurately convey "Sparse" or "Insufficient Evidence" without hallucinating replacements. | Master State Section 16 |
| **P2** | Immediate Market Insight telemetry persistence adds latency to Tool 8, affecting Orchestrator response time. | Monitor latency in staging. Move telemetry persistence to a durable queue if it degrades conversational UX. | Master State Section 16 |
| **P2** | Feature-rich What-if overlays (Tool 5) can produce zero retained comparables. | Orchestrator must preserve evidence-depth disclosure and handle empty sandbox results gracefully in chat. | Master State Section 16 |

## Architectural Risks

**1. Latency Accumulation**
Chaining intent detection, tool execution, and response generation sequentially may violate UX latency SLAs. 
*Mitigation:* Parallelize tool execution where possible (e.g., executing Tool 3 and Tool 4 simultaneously if both intents are detected).

**2. Context Window Overflow**
Tools 1-8 returning massive JSON payloads (e.g., 49 comparables, full SHAP explanations) could overwhelm the LLM's context window during the `/stream` response composition phase.
*Mitigation:* Implement deterministic response summarization or strict payload truncation in the Tool Layer adapter before injecting the payload into the LLM context.

**3. Intent Classification Drift**
The Orchestrator's intent detector may misclassify nuanced questions (e.g., confusing "Is this a good investment?" with "Is this overpriced?"), leading to the wrong Tool being executed.
*Mitigation:* Ensure strict fallback logic and allow the LLM to transparently state which tool it used to answer the question, preserving explainability of the conversation state.
