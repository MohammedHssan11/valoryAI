from __future__ import annotations

import ast
import json
from pathlib import Path
import time

from app.copilot.orchestrator.intents import ConfidenceLevel, Intent, intent_engine


_CASES = (
    ("VALUATION", "What is the fair price for this property?", Intent.VALUATION),
    ("EXPLAINABILITY", "Explain the valuation.", Intent.EXPLAINABILITY),
    ("COMPARABLES", "Show me nearby comparable properties.", Intent.COMPARABLES),
    ("FAIRNESS", "Is the asking price fair?", Intent.FAIRNESS),
    ("WHAT_IF", "What if I add a gym?", Intent.WHAT_IF),
    ("NEGOTIATION", "Should I negotiate?", Intent.NEGOTIATION),
    ("INVESTMENT", "Is this a good investment?", Intent.INVESTMENT),
    ("MARKET_INSIGHT", "What is happening in Mivida?", Intent.MARKET_INSIGHT),
    ("PROPERTY_COMPARISON", "Compare these two properties.", Intent.PROPERTY_COMPARISON),
    ("GENERAL_QUESTION", "Hello", Intent.GENERAL_QUESTION),
)
_FORBIDDEN_SOURCE_TERMS = (
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
_ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "collections",
    "dataclasses",
    "enum",
    "re",
    "typing",
    "unicodedata",
}


def _validate_source_boundary() -> tuple[list[str], list[str]]:
    package_root = Path(__file__).resolve().parents[1] / "copilot" / "orchestrator" / "intents"
    forbidden_references: list[str] = []
    forbidden_imports: list[str] = []

    for source_path in sorted(package_root.glob("*.py")):
        source = source_path.read_text(encoding="utf-8")
        lowered = source.casefold()
        forbidden_references.extend(
            f"{source_path.name}:{term}"
            for term in _FORBIDDEN_SOURCE_TERMS
            if term in lowered
        )
        for node in ast.walk(ast.parse(source, filename=str(source_path))):
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                imported = [node.module or ""]
            else:
                continue
            forbidden_imports.extend(
                f"{source_path.name}:{module}"
                for module in imported
                if module.split(".", maxsplit=1)[0] not in _ALLOWED_IMPORT_ROOTS
                and not module.startswith("app.copilot.orchestrator.intents")
            )
    return forbidden_references, forbidden_imports


def main() -> None:
    classifications = {
        name: intent_engine.classify(message)
        for name, message, _ in _CASES
    }
    failed_cases = [
        name
        for name, _, expected in _CASES
        if classifications[name].intent != expected
    ]
    multi_intent = intent_engine.classify("What is happening in Mivida and should I negotiate?")
    clarification = intent_engine.classify("Tell me more")
    noisy_misspelling = intent_engine.classify("  SHOULD   I   NeGoCiAtE   this overpriced listing?  ")
    deterministic_outputs = {
        json.dumps(intent_engine.classify("What if I add a gym?").to_dict(), sort_keys=True)
        for _ in range(100)
    }
    forbidden_references, forbidden_imports = _validate_source_boundary()

    iterations = 20_000
    started = time.perf_counter()
    for _ in range(iterations):
        intent_engine.classify("What is happening in Mivida and should I negotiate?")
    average_latency_ms = ((time.perf_counter() - started) * 1000) / iterations

    result = {
        "rule_based_only": not forbidden_references and not forbidden_imports,
        "classified_intent_count": len(classifications),
        "failed_cases": failed_cases,
        "multi_intent_primary": multi_intent.intent.value,
        "multi_intent_secondary": [intent.value for intent in multi_intent.secondary_intents],
        "clarification_intent": clarification.intent.value,
        "clarification_confidence": clarification.confidence.value,
        "clarification_required": clarification.requires_clarification,
        "misspelling_and_noise_intent": noisy_misspelling.intent.value,
        "deterministic_output_count": len(deterministic_outputs),
        "forbidden_source_references": forbidden_references,
        "forbidden_imports": forbidden_imports,
        "average_latency_ms": round(average_latency_ms, 6),
        "latency_target_ms": 5,
        "latency_target_passed": average_latency_ms < 5,
    }
    failures = [
        bool(failed_cases),
        multi_intent.intent != Intent.MARKET_INSIGHT,
        multi_intent.secondary_intents != (Intent.NEGOTIATION,),
        clarification.intent != Intent.GENERAL_QUESTION,
        clarification.confidence != ConfidenceLevel.LOW,
        not clarification.requires_clarification,
        noisy_misspelling.intent != Intent.NEGOTIATION,
        len(deterministic_outputs) != 1,
        bool(forbidden_references),
        bool(forbidden_imports),
        average_latency_ms >= 5,
    ]
    print(json.dumps(result, indent=2, sort_keys=True))
    if any(failures):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
