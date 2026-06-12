from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

from app.broker.schemas.contracts import (
    BrokerIntent,
    BrokerIntentClassification,
    BrokerIntentSignal,
)
from app.core.config import settings
from app.core.observability import metrics


@dataclass(frozen=True)
class IntentRule:
    intent: BrokerIntent
    name: str
    terms: tuple[str, ...]
    weight: float


def _normalize(message: str) -> str:
    return re.sub(r"\s+", " ", message.lower()).strip()


def _matched_terms(normalized: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term in normalized]


class BrokerIntentClassifier:
    def __init__(self) -> None:
        self._rules: tuple[IntentRule, ...] = (
            IntentRule(
                BrokerIntent.VALUATION_EXPLANATION,
                "valuation_explanation",
                (
                    "why",
                    "explain",
                    "valued lower",
                    "valued higher",
                    "valued lower than nearby",
                    "price lower",
                    "price higher",
                    "valuation",
                ),
                0.78,
            ),
            IntentRule(
                BrokerIntent.COMPARABLE_ANALYSIS,
                "comparable_analysis",
                ("comparable analysis", "compare comps", "nearby properties", "similar listings", "top comps"),
                0.84,
            ),
            IntentRule(
                BrokerIntent.COMPARABLE_REVIEW,
                "comparable_review",
                ("comparable", "comparables", "comp ", "comps", "nearby"),
                0.72,
            ),
            IntentRule(
                BrokerIntent.DISTRICT_COMPARISON,
                "district_comparison",
                ("district comparison", "compare district", "compare areas", "area comparison", "neighborhood comparison"),
                0.82,
            ),
            IntentRule(
                BrokerIntent.DISTRICT_INTELLIGENCE,
                "district_intelligence",
                ("district", "area", "neighborhood", "location", "zone"),
                0.68,
            ),
            IntentRule(
                BrokerIntent.INVESTMENT_OPPORTUNITY,
                "investment_opportunity",
                ("opportunity", "undervalued", "upside", "yield", "roi", "investment opportunity"),
                0.82,
            ),
            IntentRule(
                BrokerIntent.INVESTOR_BRIEF,
                "investor_brief",
                ("investor", "risk analysis", "risk", "brief", "portfolio"),
                0.76,
            ),
            IntentRule(
                BrokerIntent.CONFIDENCE_DISCUSSION,
                "confidence_discussion",
                ("confidence", "reliable", "certainty", "trust", "how sure", "score"),
                0.86,
            ),
            IntentRule(
                BrokerIntent.ANOMALY_INVESTIGATION,
                "anomaly_investigation",
                ("anomaly", "outlier", "strange", "unusual", "too low", "too high", "mismatch"),
                0.84,
            ),
            IntentRule(
                BrokerIntent.MARKET_CONDITION,
                "market_condition",
                ("market", "trend", "conditions", "demand", "supply", "liquidity"),
                0.74,
            ),
            IntentRule(
                BrokerIntent.INVESTOR_WORKFLOW_GUIDANCE,
                "investor_workflow_guidance",
                ("workflow", "next step", "what should i do", "guide me", "decision process", "screening"),
                0.78,
            ),
        )

    def classify(self, *, message: str, has_valuation_request: bool) -> BrokerIntentClassification:
        normalized = _normalize(message)
        scores: dict[BrokerIntent, float] = defaultdict(float)
        signals_by_intent: dict[BrokerIntent, list[BrokerIntentSignal]] = defaultdict(list)

        for rule in self._rules:
            matches = _matched_terms(normalized, rule.terms)
            if not matches:
                continue
            match_strength = min(1.0, 0.55 + (len(matches) / max(2, len(rule.terms))))
            weighted_score = min(1.0, rule.weight * match_strength)
            scores[rule.intent] += weighted_score
            signals_by_intent[rule.intent].append(
                BrokerIntentSignal(name=rule.name, weight=round(weighted_score, 3), matched_terms=matches)
            )

        if has_valuation_request:
            scores[BrokerIntent.VALUATION_ANALYSIS] += 0.35
            signals_by_intent[BrokerIntent.VALUATION_ANALYSIS].append(
                BrokerIntentSignal(
                    name="valuation_request_present",
                    weight=0.35,
                    matched_terms=["valuation_request"],
                )
            )

        if not scores:
            intent = BrokerIntent.VALUATION_ANALYSIS if has_valuation_request else BrokerIntent.GENERAL_GUIDANCE
            confidence = 0.45 if has_valuation_request else 0.32
            fallback = not has_valuation_request
            signals: list[BrokerIntentSignal] = []
            reason = "No high-signal analytical terms matched; routed to deterministic-safe fallback."
        else:
            intent, raw_score = max(scores.items(), key=lambda item: item[1])
            confidence = min(0.98, max(0.35, raw_score))
            fallback = confidence < settings.BROKER_INTENT_FALLBACK_CONFIDENCE_THRESHOLD
            if fallback:
                intent = BrokerIntent.GENERAL_GUIDANCE
            signals = signals_by_intent.get(intent, [])
            reason = "Rule-assisted classifier selected the highest-confidence broker intent."

        classification = BrokerIntentClassification(
            intent=intent,
            confidence=round(confidence, 3),
            matched_signals=signals,
            fallback=fallback,
            routing_reason=reason,
            has_valuation_request=has_valuation_request,
        )
        metrics.increment("broker.intent_classification", {"intent": intent.value, "fallback": fallback})
        metrics.observe("broker.intent_confidence", classification.confidence, {"intent": intent.value})
        metrics.record_event(
            "broker_intent_classified",
            {
                "intent": intent.value,
                "confidence": classification.confidence,
                "fallback": fallback,
                "has_valuation_request": has_valuation_request,
            },
        )
        return classification


intent_classifier = BrokerIntentClassifier()
