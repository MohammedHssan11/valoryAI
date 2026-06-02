from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class Intent(str, Enum):
    VALUATION = "VALUATION"
    EXPLAINABILITY = "EXPLAINABILITY"
    COMPARABLES = "COMPARABLES"
    FAIRNESS = "FAIRNESS"
    WHAT_IF = "WHAT_IF"
    NEGOTIATION = "NEGOTIATION"
    INVESTMENT = "INVESTMENT"
    MARKET_INSIGHT = "MARKET_INSIGHT"
    PROPERTY_COMPARISON = "PROPERTY_COMPARISON"
    GENERAL_QUESTION = "GENERAL_QUESTION"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass(frozen=True)
class IntentResult:
    intent: Intent
    confidence: ConfidenceLevel
    matched_rules: tuple[str, ...]
    matched_keywords: tuple[str, ...]
    requires_clarification: bool
    reason: str
    secondary_intents: tuple[Intent, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent.value,
            "confidence": self.confidence.value,
            "matched_rules": list(self.matched_rules),
            "matched_keywords": list(self.matched_keywords),
            "requires_clarification": self.requires_clarification,
            "reason": self.reason,
            "secondary_intents": [intent.value for intent in self.secondary_intents],
        }
