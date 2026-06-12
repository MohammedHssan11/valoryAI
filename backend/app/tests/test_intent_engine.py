from __future__ import annotations

import ast
import json
from pathlib import Path
import time

import pytest

from app.copilot.orchestrator.intents import ConfidenceLevel, Intent, intent_engine


@pytest.mark.parametrize(
    ("message", "expected_intent"),
    [
        ("What is the fair price for this property?", Intent.VALUATION),
        ("Explain the valuation.", Intent.EXPLAINABILITY),
        ("Show me nearby comparable properties.", Intent.COMPARABLES),
        ("Is the asking price fair?", Intent.FAIRNESS),
        ("What if I add a gym?", Intent.WHAT_IF),
        ("Should I negotiate?", Intent.NEGOTIATION),
        ("Is this a good investment?", Intent.INVESTMENT),
        ("What is happening in Mivida?", Intent.MARKET_INSIGHT),
        ("Compare these two properties.", Intent.PROPERTY_COMPARISON),
        ("Evaluate this property.", Intent.PROPERTY_EVALUATION),
        ("Should I buy it?", Intent.INVESTMENT_ANALYSIS),
        ("What are the risks?", Intent.RISK_ANALYSIS),
        ("Compare with market.", Intent.MARKET_COMPARISON),
        ("What's a fair offer?", Intent.NEGOTIATION_SUPPORT),
        ("Hello", Intent.GENERAL_QUESTION),
    ],
)
def test_classifies_approved_intent_taxonomy(message, expected_intent):
    result = intent_engine.classify(message)

    assert result.intent == expected_intent
    if expected_intent == Intent.GENERAL_QUESTION:
        assert result.confidence == ConfidenceLevel.LOW
        assert result.requires_clarification is True
    else:
        assert result.confidence == ConfidenceLevel.HIGH
        assert result.requires_clarification is False
        assert result.matched_rules
        assert result.matched_keywords


def test_preserves_primary_and_secondary_intents():
    result = intent_engine.classify("What is happening in Mivida and should I negotiate?")

    assert result.intent == Intent.MARKET_INSIGHT
    assert result.secondary_intents == (Intent.NEGOTIATION,)
    assert "market_insight.explicit_request" in result.matched_rules
    assert "negotiation.explicit_request" in result.matched_rules
    assert "mivida" in result.matched_keywords
    assert "negotiate" in result.matched_keywords


@pytest.mark.parametrize("message", ["Tell me more", "Hello", "   \t\n  ", "price"])
def test_low_confidence_messages_require_clarification(message):
    result = intent_engine.classify(message)

    assert result.intent == Intent.GENERAL_QUESTION
    assert result.confidence == ConfidenceLevel.LOW
    assert result.requires_clarification is True
    assert result.matched_rules == ()
    assert result.matched_keywords == ()


def test_mixed_casing_and_whitespace_noise_are_normalized():
    result = intent_engine.classify("  WhAt   IF  I   ADD   A   GYM ? ")

    assert result.intent == Intent.WHAT_IF
    assert result.confidence == ConfidenceLevel.HIGH
    assert "what if" in result.matched_keywords
    assert "add a gym" in result.matched_keywords


@pytest.mark.parametrize(
    ("message", "expected_intent"),
    [
        ("Can you give me a valution estimate?", Intent.VALUATION),
        ("Show me the comparibles.", Intent.COMPARABLES),
        ("Should I negociate this overpriced listing?", Intent.NEGOTIATION),
        ("Is this a good investement?", Intent.INVESTMENT),
        ("Show the property comparision.", Intent.PROPERTY_COMPARISON),
    ],
)
def test_explicit_misspelling_aliases_are_auditable(message, expected_intent):
    result = intent_engine.classify(message)

    assert result.intent == expected_intent
    assert result.confidence == ConfidenceLevel.HIGH
    assert result.matched_keywords


def test_keyword_matching_respects_word_boundaries():
    result = intent_engine.classify("The offering document is ready.")

    assert result.intent == Intent.GENERAL_QUESTION
    assert result.requires_clarification is True


def test_weak_secondary_signal_is_not_promoted():
    result = intent_engine.classify("Is the asking price fair?")

    assert result.intent == Intent.FAIRNESS
    assert result.secondary_intents == ()


def test_medium_confidence_signal_is_classified_without_guessing_beyond_the_rule():
    result = intent_engine.classify("Can you explain?")

    assert result.intent == Intent.EXPLAINABILITY
    assert result.confidence == ConfidenceLevel.MEDIUM
    assert result.requires_clarification is False
    assert result.matched_rules == ("explainability.keyword",)


def test_result_contract_serializes_primary_and_secondary_intents():
    result = intent_engine.classify("What is happening in Mivida and should I negotiate?").to_dict()

    assert result == {
        "intent": "MARKET_INSIGHT",
        "confidence": "HIGH",
        "matched_rules": [
            "market_insight.explicit_request",
            "negotiation.explicit_request",
        ],
        "matched_keywords": ["happening in", "mivida", "negotiate"],
        "requires_clarification": False,
        "reason": (
            "Matched deterministic rules for MARKET_INSIGHT; selected it as the primary intent and preserved "
            "secondary intents: NEGOTIATION."
        ),
        "secondary_intents": ["NEGOTIATION"],
    }


def test_repeated_classification_is_deterministic():
    outputs = {
        json.dumps(intent_engine.classify("What if I add a gym?").to_dict(), sort_keys=True)
        for _ in range(100)
    }

    assert len(outputs) == 1


def test_intent_engine_imports_are_in_process_standard_library_only():
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "intents"
    allowed_import_roots = {
        "__future__",
        "collections",
        "dataclasses",
        "enum",
        "re",
        "typing",
        "unicodedata",
    }
    forbidden_imports = []

    for source_path in package_root.glob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                imported = [node.module or ""]
            else:
                continue
            forbidden_imports.extend(
                module
                for module in imported
                if module.split(".", maxsplit=1)[0] not in allowed_import_roots
                and not module.startswith("app.copilot.orchestrator.intents")
            )

    assert forbidden_imports == []


def test_intent_engine_has_no_forbidden_classifier_or_service_references():
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "intents"
    source = "\n".join(
        source_path.read_text(encoding="utf-8").casefold()
        for source_path in package_root.glob("*.py")
    )
    forbidden_terms = (
        "anthropic",
        "catboost",
        "embedding",
        "gemini",
        "httpx",
        "openai",
        "requests",
        "sklearn",
        "socket",
        "sqlalchemy",
        "transformers",
        "vector",
    )

    assert [term for term in forbidden_terms if term in source] == []


@pytest.mark.performance
def test_intent_engine_average_latency_is_below_five_milliseconds():
    iterations = 20_000
    started = time.perf_counter()

    for _ in range(iterations):
        intent_engine.classify("What is happening in Mivida and should I negotiate?")

    average_latency_ms = ((time.perf_counter() - started) * 1000) / iterations
    assert average_latency_ms < 5
