# Phase 5.5C: Context Compression Strategy

## Problem
Tool outputs from TruthLayer (especially Tools 1, 3, 5, 6) can contain massive JSON payloads. Injecting 49 comparable rows, complete SHAP paths, and complex scenario lineages directly into the LLM context causes:
1. Context window overflow.
2. Latency degradation.
3. Lost-in-the-middle hallucination.
4. Unnecessary token costs.

## Design: Compression Rules

### 1. The "Top N" Rule
Never send unbounded arrays to the LLM. 
- **Comparables:** Compress to the Top 3 most relevant comparables (sorted deterministically by spatial/feature distance in the Composer).
- **SHAP Explanations:** Compress to the Top 3 positive drivers and Top 3 negative drivers.
- **Market Insights:** Compress time-series data to standard deltas (Start, End, % Change) rather than passing the raw daily array.

### 2. The Arithmetic Offload Rule
The LLM must never receive raw numbers and be expected to sum or average them.
- **Instead of:** `[{price: 1M}, {price: 1.1M}, {price: 1.2M}]`
- **Provide:** `{"comparable_count": 3, "avg_price": 1.1M, "min_price": 1M, "max_price": 1.2M}`

### 3. Structural Flattening
Flatten deeply nested objects before LLM ingestion. Remove database identifiers (except for final citation attachment), internal routing flags, and debugging metadata (`shadow_logs` tracing data) from the LLM prompt.

## Design: Compression Pipeline
1. **Raw Retrieval:** Tool Layer returns raw payload to Orchestrator.
2. **Context Stripping:** Response Composer removes irrelevant keys (e.g., `created_at`, raw geospatial geometries).
3. **Array Truncation:** Apply "Top N" rules.
4. **Deterministic Aggregation:** Compute counts, averages, and deltas.
5. **Context Assembly:** Wrap in the final `<payload>` tags for the LLM system prompt.
6. **Citation Preservation:** Store the raw array IDs in a parallel `metadata` object for frontend rendering.

## Design: Evidence Preservation Rules
**Rule 1: Truncation Disclosure**
Truncation must be explicitly disclosed to the LLM. 
*Example injected context:* `"comparables_truncated": true, "total_comparables": 49, "shown_in_context": 3.`

**Rule 2: Anti-Hallucination Guardrail**
The LLM must be explicitly prompted not to invent the truncated data.
*Prompt instruction:* `If the user asks for more comparables, state that there are 46 others available in the evidence panel. Do not attempt to guess them.`

**Rule 3: Dual-Channel Delivery**
The frontend UI must receive the full evidence payload independently of the LLM stream. The Orchestrator streams the LLM text, but simultaneously emits a `citations_payload` event containing the exact `snapshot_id` and all 49 `comparable_ids`. This allows the frontend to render the full visual UI map without relying on the LLM's memory.

## Open Questions
- What is the maximum acceptable token count for the compressed LLM payload before performance degrades unacceptably?
