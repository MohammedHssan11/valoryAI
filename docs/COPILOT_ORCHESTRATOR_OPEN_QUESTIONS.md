# Phase 5.5C: Copilot Orchestrator Open Questions

## MISSING INFORMATION REQUIRED

**1. Property Comparison Capability**
- **Question:** The User Journey Analysis requires handling for: *"Compare these two properties."* However, Section 10 of `PROJECT_MASTER_STATE_V2.md` lists Tools 1-8, none of which explicitly support dual-property comparison. Tool 3 only retrieves comparables for a single property/snapshot. Does a Tool 9 exist, or is the Orchestrator expected to invoke Tool 1 twice and compare the results deterministically?
- **Status:** UNVERIFIED. Cannot architect this specific user journey without further clarification. Do not assume LLM should do the comparison.

**2. Backend Intent and Reason Endpoints**
- **Question:** Section 7 lists `/v1/broker/intent` and `/v1/broker/reason` as implemented. What are the exact request and response schemas for these endpoints? Do they currently rely on deterministic models, ML classifiers, or LLMs?
- **Status:** UNVERIFIED. Cannot accurately design the Orchestrator state machine data contracts without this definition.

---

## Technical Open Questions

**3. Tool Chaining Logic & UX**
- **Question:** Are Tools 3-8 expected to be called synchronously and silently within a single conversational turn, or should the Orchestrator stream intermediate progress markers to the frontend via SSE (e.g., "Running Valuation...", "Running What-if...")?
- **Status:** UNVERIFIED. Affects SSE and WebSocket architectural decisions for the frontend broker terminal.

**4. Frontend Context Integration**
- **Question:** Section 8 states `BrokerScreen` sends a local `session_id` but not `workspace_id` and `scenario_id`. Will the frontend provide these before Phase 5.5C is deployed, or must the Orchestrator handle missing context errors as a primary conversational flow and prompt the user to select a workspace?
- **Status:** UNVERIFIED. Affects whether the Orchestrator needs a "Context Elicitation" state in its state machine.

**5. Payload Truncation**
- **Question:** If the combined output of multiple Tools (e.g., Tool 1 + Tool 2 + Tool 3) exceeds the LLM context limits during the final Response Composition phase, how should payload truncation be handled without losing TruthLayer authority?
- **Status:** UNVERIFIED. Needs a defined strategy for truncating comparable lists vs. dropping SHAP values.
