# Phase 5.5C: Copilot Orchestrator Decision Log

## Decision 1: Architecture Pattern
- **Decision:** Adopt Alternative B (Deterministic Multi-Step Pipeline: Intent -> Plan -> Execute -> Narrate).
- **Reason:** Separates intent detection, tool planning, tool execution, and narration into distinct governed steps. This maps directly to the existing backend endpoints (`/intent`, `/reason`, `/analyze`, `/stream`) and minimizes LLM hallucination by restricting generation to the final step.
- **Alternative rejected:** Alternative A (Single-Prompt ReAct Agent) rejected due to non-deterministic tool selection and high risk of bypassing TruthLayer authority.
- **Risk:** Increased request latency due to multiple phases.
- **Mitigation:** Utilize existing SSE (`/stream`) for the final narration to improve perceived performance and time-to-first-token.

## Decision 2: Tool Registry Scope
- **Decision:** Limit the Orchestrator's Tool Registry strictly to Copilot Tools 1 through 8.
- **Reason:** These tools are implemented, Docker-validated, tenant-isolated, and preserve TruthLayer authority (Master State Section 10). The Orchestrator must not interact directly with the Router, ML, or CMT.
- **Alternative rejected:** Permitting the LLM to write database queries or call TruthLayer internal components directly.
- **Risk:** The Orchestrator cannot fulfill requests outside Tools 1-8 (e.g., arbitrary dual-property comparison).
- **Mitigation:** Unhandled intents fallback to `GENERAL_QUESTION` and gracefully decline.

## Decision 3: Hallucination Prevention Boundary
- **Decision:** The LLM prompt for `/stream` (narration) will only be provided with the strict JSON output of the executed Tools. The system prompt will forbid adding numbers or real estate logic not present in the payload.
- **Reason:** Master State Section 18 states: "LLM narration may summarize locked deterministic context. It must not become a valuation authority."
- **Alternative rejected:** Allowing the LLM to access external APIs or search the web to augment real estate data.
- **Risk:** Responses may seem dry, highly structured, or repetitive.
- **Mitigation:** Prompt engineering to ensure natural tone while remaining strictly grounded in the provided Tool payload.
