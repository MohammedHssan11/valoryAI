# Phase 5.5C: Response Composer Architecture

## Component Overview
The **Response Composer** is a strict deterministic software component sitting between Tool Execution and the final LLM generation step. It protects the LLM from raw, massive TruthLayer payloads and enforces mathematical safety.

## Responsibilities

### 1. Tool Output Normalization
- **Why it exists:** Tools return different structures (e.g., Tool 1 returns a snapshot, Tool 6 returns positions and bands). The LLM needs a predictable schema.
- **Why inside Composer:** Isolates the LLM prompt from backend API contract changes.
- **Tradeoffs:** Requires maintaining strict Pydantic mapping models.
- **Risks:** Normalization might strip critical edge-case context.
- **Mitigation:** Use extensible structured schemas that preserve TruthLayer confidence markers.

### 2. Evidence Summarization
- **Why it exists:** To prevent the LLM from doing arithmetic on raw arrays (e.g., calculating average comparable price).
- **Why inside Composer:** Code is 100% deterministic at math; LLMs are not.
- **Tradeoffs:** Summarization might hide outliers.
- **Risks:** Loss of nuance in complex distributions.
- **Mitigation:** Pass explicit max, min, and standard deviation values alongside averages.

### 3. Comparable Compression
- **Why it exists:** Truncates lists of 49 comparables into the "Top 3 Most Relevant" for the LLM prompt, preventing context overflow.
- **Why inside Composer:** Sorting by relevance/distance must be deterministic and executed outside the LLM.
- **Tradeoffs:** The LLM cannot directly reference comparable #4.
- **Risks:** User asks about a specific comparable the LLM cannot see.
- **Mitigation:** Instruct the LLM to mention "There are N other comparables available in the evidence panel" and rely on frontend UI to display them.

### 4. LLM Context Assembly
- **Why it exists:** The LLM needs strict boundaries between "system instructions" and "data payload".
- **Why inside Composer:** It prepares the final executable prompt natively.
- **Tradeoffs/Risks:** None, standard architecture practice.

### 5. Citation Assembly
- **Why it exists:** Extracts `snapshot_id`, `tool_event_id`, and `comparable_ids` and packages them alongside the SSE stream for the UI.
- **Why inside Composer:** The LLM cannot reliably generate UUIDs or ensure citation integrity.
- **Tradeoffs:** Complex SSE streaming combining text chunks and JSON metadata.
- **Risks:** Frontend desync if citations don't match the streamed text.
- **Mitigation:** Use a standardized SSE chunk wrapper (e.g., `{"text": "...", "citations": [...]}`).

### 6. Final Broker Response Assembly
- **Why it exists:** Orchestrates the LLM generation and streams it to the user to deliver the final UX.

## Open Questions
- What is the exact payload structure expected by the frontend for citation tracking in the SSE stream?
