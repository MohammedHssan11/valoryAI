from __future__ import annotations

from typing import Any

from app.broker.schemas.contracts import BrokerIntentClassification, BrokerSessionSnapshot


class AnalyticalDialogueEngine:
    def continuity_context(
        self,
        *,
        session: BrokerSessionSnapshot,
        classification: BrokerIntentClassification,
    ) -> dict[str, Any]:
        return {
            "follow_up_turn": bool(session.previous_requests),
            "previous_request_count": len(session.previous_requests),
            "previous_valuation_count": len(session.previous_valuations),
            "active_district": session.active_district,
            "last_intent": session.analytical_context.get("last_intent"),
            "current_intent": classification.intent.value,
            "can_reference_previous_valuation_summary": bool(session.previous_valuations),
        }


analytical_dialogue_engine = AnalyticalDialogueEngine()
