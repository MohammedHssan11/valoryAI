# Phase 5.5C: Tool Chaining Workflows

## Context
Tools 6 (Negotiation) and 7 (Investment) natively orchestrate Tools 1-5 in the backend. The Orchestrator does not need to manually chain Valuation -> Explainability -> Comparable -> Fairness if the intent maps directly to Negotiation or Investment. 

## User Journey Workflows

### 1. "Is this overpriced?"
- **Intent:** `NEGOTIATION`
- **Tool Chain:** Tool 6 (Negotiation). Tool 6 natively provides valuation, fairness, and offer bands.
- **Execution Order:** `Execute Tool 6` (Synchronous).
- **Parallel Opportunities:** None.
- **Failure Handling:** If Tool 6 returns "Sparse Evidence", the LLM must narrate the position as "Unable to confirm due to sparse data", relying purely on the deterministic position returned.

### 2. "What if I add a gym?"
- **Intent:** `WHAT_IF`
- **Tool Chain:** Tool 5 (What-if).
- **Execution Order:** `Execute Tool 5`.
- **Parallel Opportunities:** None.
- **Failure Handling:** If the base property lacks sufficient comparables for the overlay, Tool 5 returns TruthLayer-derived empty deltas. Orchestrator must narrate "No evidence to support price change."

### 3. "Should I negotiate?"
- **Intent:** `NEGOTIATION`
- **Tool Chain:** Tool 6 (Negotiation).
- **Execution Order:** `Execute Tool 6`.
- **Parallel Opportunities:** None.
- **Failure Handling:** Bubble up internal timeouts cleanly.

### 4. "Is this a good investment?"
- **Intent:** `INVESTMENT`
- **Tool Chain:** Tool 7 (Investment).
- **Execution Order:** `Execute Tool 7`. (Tool 7 internally handles the Tool 1-6 chain).
- **Parallel Opportunities:** None.

### 5. "What's happening in Mivida?"
- **Intent:** `MARKET_INSIGHT`
- **Tool Chain:** Tool 8 (Market Insight).
- **Execution Order:** `Execute Tool 8`.
- **Parallel Opportunities:** If the user asked "What's happening in Mivida and is my property overpriced?", Tool 8 and Tool 6 can be executed concurrently.

### 6. "Compare these two properties"
- **Intent:** `PROPERTY_COMPARISON`
- **Tool Chain:** Tool 1 (Property A) AND Tool 1 (Property B).
- **Execution Order:** `Parallel Execute Tool 1 (A)` || `Parallel Execute Tool 1 (B)`.
- **Composition Layer:** The Response Composer waits for both, calculates deterministic deltas (Diff: +50k EGP, +20 sqm), and passes the combined payload to the LLM context.
- **Failure Handling:** If Property B fails to value, the Orchestrator narrates Property A and gracefully reports the evaluation failure for Property B without hallucinating a guess.

## Open Questions
- Is there a timeout budget for parallel tool executions (e.g., if Property A values in 1s but Property B hangs)?
