from __future__ import annotations

import re

from app.copilot.orchestrator.intents import Intent


PROVIDER_PROFILE_ID = "gemini-2.5-pro-stateless-v1"
PROVIDER_NAME = "gemini"
PROVIDER_MODEL = "gemini-2.5-pro"
PROVIDER_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"

MAX_REQUEST_TOKENS = 12_000
MAX_RESPONSE_TOKENS = 1_500
MAX_CITATIONS = 50
MAX_NARRATION_CHARACTERS = 12_000
PROVIDER_TIMEOUT_SECONDS = 20.0
RESPONSE_RESERVE_TOKENS = 1_500
MAX_CURRENT_TURN_CHARACTERS = 4_000
MAX_PROJECTION_FACTS = 512
MAX_NARRATION_LINES = 12

# These byte ceilings are conservative transport bounds derived from the
# approved token and narration-character limits. They prevent unbounded I/O.
MAX_PROVIDER_HTTP_REQUEST_BYTES = (MAX_REQUEST_TOKENS * 4) + 65_536
MAX_PROVIDER_HTTP_RESPONSE_BYTES = (MAX_NARRATION_CHARACTERS * 4) + 65_536

ASSEMBLY_POLICY_VERSION = "prompt-assembly-v1"
SERIALIZER_VERSION = "canonical-json-ascii-sorted-v1"
TOKENIZER_VERSION = "utf8-byte-ceiling-div4-v1"
CONTRACT_VERSION = "narration-contracts-v1"
PROHIBITED_CLAIMS_POLICY_VERSION = "prohibited-claims-v1"
EVICTION_POLICY_VERSION = "optional-memory-summary-oldest-first-v1"

APPROVED_INTENTS = frozenset(
    {
        Intent.PROPERTY_EVALUATION,
        Intent.INVESTMENT_ANALYSIS,
        Intent.RISK_ANALYSIS,
        Intent.MARKET_COMPARISON,
        Intent.NEGOTIATION_SUPPORT,
        Intent.VALUATION,
        Intent.EXPLAINABILITY,
        Intent.COMPARABLES,
        Intent.FAIRNESS,
        Intent.WHAT_IF,
        Intent.NEGOTIATION,
        Intent.INVESTMENT,
        Intent.MARKET_INSIGHT,
        Intent.PROPERTY_COMPARISON,
    }
)

CONTRACT_IDS = {
    Intent.VALUATION: "VALUATION_NARRATION_CONTRACT",
    Intent.PROPERTY_EVALUATION: "PROPERTY_EVALUATION_NARRATION_CONTRACT",
    Intent.INVESTMENT_ANALYSIS: "INVESTMENT_ANALYSIS_NARRATION_CONTRACT",
    Intent.RISK_ANALYSIS: "RISK_ANALYSIS_NARRATION_CONTRACT",
    Intent.MARKET_COMPARISON: "MARKET_COMPARISON_NARRATION_CONTRACT",
    Intent.NEGOTIATION_SUPPORT: "NEGOTIATION_SUPPORT_NARRATION_CONTRACT",
    Intent.EXPLAINABILITY: "EXPLAINABILITY_NARRATION_CONTRACT",
    Intent.COMPARABLES: "COMPARABLES_NARRATION_CONTRACT",
    Intent.FAIRNESS: "FAIRNESS_NARRATION_CONTRACT",
    Intent.WHAT_IF: "WHAT_IF_NARRATION_CONTRACT",
    Intent.NEGOTIATION: "NEGOTIATION_NARRATION_CONTRACT",
    Intent.INVESTMENT: "INVESTMENT_NARRATION_CONTRACT",
    Intent.MARKET_INSIGHT: "MARKET_INSIGHT_NARRATION_CONTRACT",
    Intent.PROPERTY_COMPARISON: "PROPERTY_COMPARISON_NARRATION_CONTRACT",
}

ALLOWED_PROJECTION_SEGMENT_CLASSES = frozenset(
    {
        "governance",
        "untrusted_current_turn",
        "composer_facts",
        "limitations",
        "citation_tokens",
        "memory_summary",
    }
)

OPTIONAL_SEGMENT_CLASS_ORDER = {
    "memory_summary": 0,
}

FORBIDDEN_PROVIDER_VISIBLE_KEYS = frozenset(
    {
        "user_id",
        "workspace_id",
        "scenario_id",
        "broker_session_id",
        "session_id",
        "chat_id",
        "property_state_id",
        "raw_jwt",
        "jwt",
        "token",
        "secret",
        "credential",
        "connection_string",
        "frontend_payload",
    }
)

CITATION_TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,159}$")
INLINE_CITATION_PATTERN = re.compile(r"\[citation:([A-Za-z0-9][A-Za-z0-9._:-]{0,159})\]")
FACT_LINE_PATTERN = re.compile(
    r"^The approved upstream fact "
    r"(?P<fact_id>[A-Za-z0-9_.-]+) "
    r"is (?P<value>.+?) "
    r"(?P<citations>(?:\[citation:[A-Za-z0-9][A-Za-z0-9._:-]{0,159}\])"
    r"(?: \[citation:[A-Za-z0-9][A-Za-z0-9._:-]{0,159}\])*)\.$"
)
