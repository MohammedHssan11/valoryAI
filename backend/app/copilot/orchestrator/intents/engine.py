from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import re
import unicodedata

from app.copilot.orchestrator.intents.contracts import ConfidenceLevel, Intent, IntentResult


_NON_WORD_RE = re.compile(r"[^\w]+", flags=re.UNICODE)
_WHITESPACE_RE = re.compile(r"\s+")
_CONFIDENCE_RANK = {
    ConfidenceLevel.LOW: 0,
    ConfidenceLevel.MEDIUM: 1,
    ConfidenceLevel.HIGH: 2,
}
_INTENT_PRECEDENCE = {intent: index for index, intent in enumerate(Intent)}


@dataclass(frozen=True)
class IntentRule:
    name: str
    intent: Intent
    confidence: ConfidenceLevel
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class _RuleMatch:
    rule: IntentRule
    keywords: tuple[str, ...]
    first_position: int


@dataclass(frozen=True)
class _IntentEvidence:
    intent: Intent
    confidence: ConfidenceLevel
    matches: tuple[_RuleMatch, ...]
    matched_keywords: tuple[str, ...]
    first_position: int
    specificity: int

    @property
    def ranking_key(self) -> tuple[int, int, int, int, int]:
        return (
            _CONFIDENCE_RANK[self.confidence],
            self.specificity,
            len(self.matched_keywords),
            -self.first_position,
            -_INTENT_PRECEDENCE[self.intent],
        )

    @property
    def is_safe_secondary(self) -> bool:
        return self.confidence == ConfidenceLevel.HIGH or len(self.matched_keywords) >= 2


def _normalize(message: str) -> str:
    normalized = unicodedata.normalize("NFKC", message).casefold()
    normalized = _NON_WORD_RE.sub(" ", normalized)
    return _WHITESPACE_RE.sub(" ", normalized).strip()


def _unique_in_order(values: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


class RuleBasedIntentEngine:
    def __init__(self) -> None:
        self._rules = _build_rules()

    @property
    def rules(self) -> tuple[IntentRule, ...]:
        return self._rules

    def classify(self, message: str) -> IntentResult:
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        normalized = _normalize(message)
        if not normalized:
            return self._clarification_result("The user message is empty after whitespace normalization.")

        evidence = self._collect_evidence(normalized)
        if not evidence:
            return self._clarification_result(
                "No governed intent rule matched; clarification is required before downstream planning."
            )

        ranked = sorted(evidence, key=lambda item: item.ranking_key, reverse=True)
        primary = ranked[0]
        secondaries = tuple(item for item in ranked[1:] if item.is_safe_secondary)
        selected = (primary, *secondaries)
        secondary_intents = tuple(item.intent for item in secondaries)
        matched_rules = _unique_in_order(
            [
                match.rule.name
                for item in selected
                for match in item.matches
            ]
        )
        matched_keywords = _unique_in_order(
            [
                keyword
                for item in selected
                for keyword in item.matched_keywords
            ]
        )
        reason = (
            f"Matched deterministic rules for {primary.intent.value}; selected it as the primary intent."
            if not secondary_intents
            else (
                f"Matched deterministic rules for {primary.intent.value}; selected it as the primary intent and "
                f"preserved secondary intents: {', '.join(intent.value for intent in secondary_intents)}."
            )
        )
        return IntentResult(
            intent=primary.intent,
            confidence=primary.confidence,
            matched_rules=matched_rules,
            matched_keywords=matched_keywords,
            requires_clarification=False,
            reason=reason,
            secondary_intents=secondary_intents,
        )

    def _collect_evidence(self, normalized: str) -> tuple[_IntentEvidence, ...]:
        matches_by_intent: dict[Intent, list[_RuleMatch]] = defaultdict(list)
        padded_message = f" {normalized} "

        for rule in self._rules:
            keyword_positions = [
                (keyword, padded_message.find(f" {keyword} "))
                for keyword in rule.keywords
            ]
            matched = [(keyword, position) for keyword, position in keyword_positions if position >= 0]
            if matched:
                matches_by_intent[rule.intent].append(
                    _RuleMatch(
                        rule=rule,
                        keywords=tuple(keyword for keyword, _ in matched),
                        first_position=min(position for _, position in matched),
                    )
                )

        evidence: list[_IntentEvidence] = []
        for intent, matches in matches_by_intent.items():
            matched_keywords = _unique_in_order(
                [
                    keyword
                    for match in matches
                    for keyword in match.keywords
                ]
            )
            evidence.append(
                _IntentEvidence(
                    intent=intent,
                    confidence=max(
                        (match.rule.confidence for match in matches),
                        key=lambda confidence: _CONFIDENCE_RANK[confidence],
                    ),
                    matches=tuple(matches),
                    matched_keywords=matched_keywords,
                    first_position=min(match.first_position for match in matches),
                    specificity=max(len(keyword.split()) for keyword in matched_keywords),
                )
            )
        return tuple(evidence)

    @staticmethod
    def _clarification_result(reason: str) -> IntentResult:
        return IntentResult(
            intent=Intent.GENERAL_QUESTION,
            confidence=ConfidenceLevel.LOW,
            matched_rules=(),
            matched_keywords=(),
            requires_clarification=True,
            reason=reason,
        )


def _rule(
    name: str,
    intent: Intent,
    confidence: ConfidenceLevel,
    *keywords: str,
) -> IntentRule:
    return IntentRule(
        name=name,
        intent=intent,
        confidence=confidence,
        keywords=_unique_in_order([_normalize(keyword) for keyword in keywords]),
    )


def _build_rules() -> tuple[IntentRule, ...]:
    return (
        _rule(
            "property_evaluation.explicit_request",
            Intent.PROPERTY_EVALUATION,
            ConfidenceLevel.HIGH,
            "evaluate this property",
            "evaluate the property",
            "evaluate this listing",
            "evaluate the listing",
            "evaluate it",
            "what s it worth",
            "whats it worth",
            "what is it worth",
            "how much is it worth",
            "estimate fair value",
            "estimate the fair value",
            "estimate this listing",
            "value this listing",
            "this listing worth",
            "that apartment worth",
            "this property worth",
        ),
        _rule(
            "valuation.explicit_request",
            Intent.VALUATION,
            ConfidenceLevel.HIGH,
            "value this property",
            "valuate this property",
            "property valuation",
            "valuation estimate",
            "estimate the value",
            "estimate this property",
            "what is this property worth",
            "how much is this property worth",
            "fair price",
            "price estimate",
            "valution estimate",
            "valuaton estimate",
        ),
        _rule(
            "valuation.keyword",
            Intent.VALUATION,
            ConfidenceLevel.MEDIUM,
            "valuation",
            "valuate",
            "valution",
            "valuaton",
        ),
        _rule(
            "explainability.explicit_request",
            Intent.EXPLAINABILITY,
            ConfidenceLevel.HIGH,
            "explain the valuation",
            "explain valuation",
            "explain the price",
            "why this price",
            "why is the valuation",
            "why was it valued",
            "how was the price calculated",
            "how did you calculate the price",
            "what drove the valuation",
            "explainability",
        ),
        _rule(
            "explainability.keyword",
            Intent.EXPLAINABILITY,
            ConfidenceLevel.MEDIUM,
            "explain",
            "price drivers",
            "valuation drivers",
        ),
        _rule(
            "comparables.explicit_request",
            Intent.COMPARABLES,
            ConfidenceLevel.HIGH,
            "comparables",
            "comparable evidence",
            "comparable properties",
            "comparable listings",
            "show comps",
            "review comps",
            "nearby properties",
            "nearby listings",
            "similar properties",
            "similar listings",
            "comparibles",
        ),
        _rule(
            "comparables.keyword",
            Intent.COMPARABLES,
            ConfidenceLevel.MEDIUM,
            "comps",
            "comparable",
            "nearby",
        ),
        _rule(
            "fairness.explicit_request",
            Intent.FAIRNESS,
            ConfidenceLevel.HIGH,
            "is the asking price fair",
            "asking price fair",
            "is this price fair",
            "price fair",
            "priced fairly",
            "fairness",
            "fair market position",
            "fair value position",
            "is this fair",
        ),
        _rule(
            "fairness.keyword",
            Intent.FAIRNESS,
            ConfidenceLevel.MEDIUM,
            "fairly priced",
            "fair market",
        ),
        _rule(
            "what_if.explicit_request",
            Intent.WHAT_IF,
            ConfidenceLevel.HIGH,
            "what if",
            "add gym",
            "add a gym",
            "add parking",
            "add a parking space",
            "add clubhouse",
            "add a clubhouse",
            "renovate",
            "renovation",
            "rennovate",
            "remodel",
            "make it furnished",
            "furnish it",
            "scenario",
            "simulate",
        ),
        _rule(
            "what_if.keyword",
            Intent.WHAT_IF,
            ConfidenceLevel.MEDIUM,
            "furnished",
            "furnishing",
            "modification",
            "modify",
        ),
        _rule(
            "negotiation.explicit_request",
            Intent.NEGOTIATION,
            ConfidenceLevel.HIGH,
            "negotiate",
            "negotiation",
            "negociate",
            "counter offer",
            "counteroffer",
            "overpriced",
            "underpriced",
            "bargain",
        ),
        _rule(
            "negotiation_support.explicit_request",
            Intent.NEGOTIATION_SUPPORT,
            ConfidenceLevel.HIGH,
            "can i negotiate",
            "can we negotiate",
            "negotiation support",
            "what s a fair offer",
            "whats a fair offer",
            "what is a fair offer",
            "fair offer",
            "offer strategy",
            "find negotiation opportunities",
        ),
        _rule(
            "negotiation.keyword",
            Intent.NEGOTIATION,
            ConfidenceLevel.MEDIUM,
            "offer",
            "asking price",
        ),
        _rule(
            "investment.explicit_request",
            Intent.INVESTMENT,
            ConfidenceLevel.HIGH,
            "investment",
            "invest",
            "investement",
            "opportunity",
            "worth buying",
            "good investment",
            "buying opportunity",
        ),
        _rule(
            "investment_analysis.explicit_request",
            Intent.INVESTMENT_ANALYSIS,
            ConfidenceLevel.HIGH,
            "should i buy it",
            "should i buy this property",
            "should i buy this listing",
            "investment analysis",
            "investment outlook",
            "generate investment analysis",
            "give me investment analysis",
            "roi analysis",
            "return analysis",
            "buy or pass",
        ),
        _rule(
            "risk_analysis.explicit_request",
            Intent.RISK_ANALYSIS,
            ConfidenceLevel.HIGH,
            "what are the risks",
            "show risks",
            "show risk factors",
            "risk factors",
            "risk assessment",
            "what should i worry about",
            "biggest risks",
            "market risks",
            "investment risks",
        ),
        _rule(
            "market_insight.explicit_request",
            Intent.MARKET_INSIGHT,
            ConfidenceLevel.HIGH,
            "market insight",
            "area trend",
            "compound trend",
            "market trend",
            "market activity",
            "market condition",
            "market conditions",
            "happening in",
            "mivida",
        ),
        _rule(
            "market_comparison.explicit_request",
            Intent.MARKET_COMPARISON,
            ConfidenceLevel.HIGH,
            "compare to market",
            "compare with market",
            "compare against market",
            "compare nearby",
            "how does it compare nearby",
            "how does this compare nearby",
            "market comparison",
            "market comps",
            "compare with nearby listings",
            "compare to nearby properties",
        ),
        _rule(
            "market_insight.keyword",
            Intent.MARKET_INSIGHT,
            ConfidenceLevel.MEDIUM,
            "market",
            "trend",
            "trends",
            "activity",
            "demand",
            "supply",
            "markit",
        ),
        _rule(
            "property_comparison.explicit_request",
            Intent.PROPERTY_COMPARISON,
            ConfidenceLevel.HIGH,
            "compare these two properties",
            "compare two properties",
            "compare properties",
            "compare property",
            "property comparison",
            "property comparision",
            "side by side",
            "difference between",
            "better than",
            "versus",
            "vs",
            "comparsion",
        ),
    )


intent_engine = RuleBasedIntentEngine()
