# Phase 5.5C: Copilot Orchestrator Review Round 2

## Section 1: Property Comparison Strategy

**Decision:**
Implement Property Comparison via the **Orchestrator Composition Layer** using parallel execution of existing Tool 1 (Valuation), rather than creating a new Tool 9 in the backend.

**Evidence:**
- Master State Section 10 explicitly lists Tools 1-8 as complete and Docker-validated. 
- Master State Section 18 states the Orchestrator's role is to select, chain, and compose.

**Why:**
Creating a new Tool 9 in the backend Tool Layer violates the boundaries of the current validated phase and duplicates valuation invocation logic. By delegating this to the Orchestrator's Response Composer, the Orchestrator can call Tool 1 in parallel for Property A and Property B, deterministically compute the mathematical deltas (price, size, features), and pass the pre-calculated diff to the LLM. This keeps the backend Tool Registry locked to Tools 1-8.

**Alternative Considered:**
Create a new Tool 9 (Property Comparison Tool) directly inside the backend TruthLayer Tool execution boundary.

**Alternative Rejected:**
Rejected because it introduces backend architectural drift, forces a re-validation of the backend Copilot service, and property comparison is fundamentally a compositional task over two independent valuations.

**Tradeoffs:**
Shifts deterministic math (delta calculation) into the Orchestrator's Response Composer rather than keeping all pricing logic strictly below the Orchestrator boundary.

**Risks:**
If the Orchestrator relies on the LLM to compute the deltas between the two Tool 1 payloads, the LLM will hallucinate math errors.

**Mitigation:**
The Response Composer must contain strict deterministic code to calculate the deltas *before* passing the payload to the LLM. The LLM must only narrate the pre-calculated diffs.

**Open Questions:**
How should frontend context be passed when requesting two separate property states simultaneously for comparison?

---

## Section 5: Latency Review

**Review Areas:**
- **Intent Detection:** Adding an LLM call purely for intent routing adds 500ms - 1500ms latency.
- **Planning:** Further chain planning adds additional latency.
- **Execution:** TruthLayer tools take baseline execution time. 
- **Composition & Streaming:** TTFT (Time to First Token) will be delayed by the entire pre-processing chain.

**Potential Bottlenecks:**
Serial execution of planning -> tool execution -> context compression -> LLM generation.

**Parallel Execution Opportunities:**
- **Dual-Property Comparison:** Tool 1 (Prop A) and Tool 1 (Prop B) must execute concurrently.
- **Independent Intents:** If a user asks for Valuation AND Market Insight, Tool 1 and Tool 8 can execute concurrently.

**Risk Mitigation:**
- Use a fast, fine-tuned lightweight classifier for Intent Detection/Planning.
- Stream intermediate state events to the frontend via SSE (`{"status": "running_valuation"}`) during the Tool Execution phases so the user sees immediate system response before the final LLM stream begins.

---

## Section 6: Hallucination Review

**Remaining Hallucination Risks:**
1. **Context Math Leakage:** Asking the LLM to compare two numbers (e.g., offering a discount percentage) if the delta wasn't explicitly provided by the Composer.
2. **Comparable Fabrication:** The LLM inventing a "better comparable" to justify an argument because the context was truncated.
3. **Forecasting Leakage:** The LLM using Tool 8 (Market Insight) historical data to predict future prices.

**Remaining Authority Leaks:**
Allowing the LLM prompt to contain phrases like "What do you think the price should be?" rather than "Summarize the TruthLayer evaluation."

**Mitigations:**
- **Strict Composer Diffs:** The Orchestrator Composition Layer must compute all percentages, deltas, and counts deterministically in code.
- **Prompt Guardrails:** The final LLM system prompt must contain strict negative constraints: "DO NOT calculate math. DO NOT forecast future trends. DO NOT invent comparables."
- **Citation Anchoring:** Every claim made by the LLM must be tied to a `tool_event_id` or `snapshot_id`.

---

## Section 7: Decision Review

**Major Decision: Enforce Deterministic Composition over LLM Reasoning**
- **Decision:** The Response Composer will deterministically structure, compress, and diff all tool outputs before LLM ingestion.
- **Why:** To mathematically eliminate LLM reasoning errors in property comparison and evidence summarization.
- **Alternative Considered:** Prompting the LLM to review the raw JSON of Tool 1 and Tool 3 and reason about the numbers.
- **Alternative Rejected:** High probability of hallucination, failing the governance requirement that the LLM must not act as a valuation engine.
- **Tradeoffs:** Increases the complexity of the Orchestrator code (requires data models and math logic).
- **Risks:** The composer logic could accidentally become a parallel business logic layer, violating TruthLayer authority.
- **Mitigation:** The Composer must strictly only perform extraction, sorting, and arithmetic diffs, never valuation modeling or pricing rules.

**Open Questions:**
Will the Intent Classifier be deployed as an LLM or a traditional ML text classifier?
