from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from decimal import Decimal
import hashlib
import json
from typing import Any

from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.copilot.orchestrator.composer import ComposedResponse
from app.copilot.orchestrator.executor import ExecutionResult
from app.copilot.orchestrator.memory.contracts import MemoryContext, MemoryStatus
from app.models.copilot import (
    Assumption,
    BrokerSession,
    Chat,
    DecisionHistory,
    Message,
    PropertyState,
    ScenarioState,
    ToolEvent,
    ValuationSnapshot,
    Workspace,
)


SCHEMA_VERSION = "1.0"
RECENT_TOOL_EVENTS_LIMIT = 10
RECENT_DECISIONS_LIMIT = 10
RECENT_VALUATIONS_LIMIT = 5
ACTIVE_ASSUMPTIONS_LIMIT = 20
RECENT_CONVERSATION_METADATA_LIMIT = 10
SCENARIO_LINEAGE_LIMIT = 10
MEMORY_DECISION_ACTION = "memory.composed_response.remembered"

_SUMMARY_FIELDS = (
    "asking_price",
    "base_valuation",
    "confidence_level",
    "delta_percentage",
    "delta_value",
    "engine_used",
    "fair_price",
    "fairness_status",
    "investment_position",
    "market_summary",
    "negotiation_position",
    "price_gap",
    "price_gap_percentage",
    "price_range",
    "scenario_valuation",
    "source",
    "target_price",
    "valuation_volume",
)


def _json_safe(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def _canonical_json(value: Any) -> str:
    return json.dumps(_json_safe(value), ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def derive_memory_id(payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()
    return f"memory_{digest}"


def _unique(values: list[Any]) -> list[Any]:
    seen = set()
    unique = []
    for value in values:
        marker = _canonical_json(value)
        if marker not in seen:
            seen.add(marker)
            unique.append(value)
    return unique


def _extract_citations(value: Any) -> dict[str, list[Any]]:
    valuation_ids: list[Any] = []
    tool_event_ids: list[Any] = []
    comparable_ids: list[Any] = []

    def append(values: list[Any], item: Any) -> None:
        if isinstance(item, (str, int)) and not isinstance(item, bool) and item != "":
            values.append(item)

    def walk(item: Any) -> None:
        if isinstance(item, dict):
            comparable_evidence = item.get("comparable_evidence")
            if isinstance(comparable_evidence, list):
                for comparable in comparable_evidence:
                    if isinstance(comparable, dict):
                        append(comparable_ids, comparable.get("property_id"))
            for key, child in item.items():
                if key in {"valuation_id", "base_valuation_id", "scenario_valuation_id", "fairness_valuation_id"}:
                    append(valuation_ids, child)
                elif key == "valuation_ids" and isinstance(child, list):
                    for identifier in child:
                        append(valuation_ids, identifier)
                elif key == "tool_event_id":
                    append(tool_event_ids, child)
                elif key == "tool_event_ids" and isinstance(child, list):
                    for identifier in child:
                        append(tool_event_ids, identifier)
                elif key == "comparable_id":
                    append(comparable_ids, child)
                elif key in {"comparable_ids", "comparable_ids_used"} and isinstance(child, list):
                    for identifier in child:
                        append(comparable_ids, identifier)
                walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)

    walk(value)
    return {
        "valuation_ids": _unique(valuation_ids),
        "tool_event_ids": _unique(tool_event_ids),
        "comparable_ids": _unique(comparable_ids),
    }


def _merge_citations(*packages: dict[str, Any]) -> dict[str, list[Any]]:
    merged = {
        "valuation_ids": [],
        "tool_event_ids": [],
        "comparable_ids": [],
    }
    for package in packages:
        for key in merged:
            values = package.get(key, [])
            if isinstance(values, list):
                merged[key].extend(values)
    return {key: _unique(values) for key, values in merged.items()}


def _compact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    request = payload.get("request") if isinstance(payload.get("request"), dict) else {}
    response = payload.get("response") if isinstance(payload.get("response"), dict) else {}
    summary = {key: response[key] for key in _SUMMARY_FIELDS if key in response}
    return {
        "request_context": {
            key: request[key]
            for key in ("workspace_id", "property_id", "scenario_id", "valuation_id")
            if key in request
        },
        "response_summary": _json_safe(summary),
        "citations": _extract_citations(payload),
    }


class DeterministicMemoryIntegration:
    def __init__(self, db: Session):
        self.db = db

    def remember(
        self,
        *,
        user_id: int,
        workspace_id: int,
        execution_result: ExecutionResult,
        composed_response: ComposedResponse,
        scenario_id: int | None = None,
        broker_session_id: str | None = None,
    ) -> MemoryContext:
        try:
            scope = self._scope(
                user_id=user_id,
                workspace_id=workspace_id,
                scenario_id=scenario_id,
                broker_session_id=broker_session_id,
            )
            if scope is None:
                return self._failure(MemoryStatus.ACCESS_DENIED, "MEMORY_SCOPE_NOT_ACCESSIBLE")
            workspace, scenario, _, prop = scope
            if not self._runtime_matches(execution_result, composed_response):
                return self._failure(MemoryStatus.FAILED, "RUNTIME_CONTEXT_MISMATCH")

            details = {
                "response_id": composed_response.response_id,
                "execution_id": composed_response.execution_id,
                "plan_id": composed_response.plan_id,
                "composition_status": composed_response.status.value,
                "primary_intent": composed_response.primary_intent.value,
                "secondary_intents": [intent.value for intent in composed_response.secondary_intents],
                "citation_package": _json_safe(deepcopy(composed_response.citation_package)),
                "active_comparison_context": _json_safe(
                    deepcopy(composed_response.evidence_summary.get("property_comparison"))
                ),
                "broker_session_id": broker_session_id,
            }
            existing = (
                self.db.query(DecisionHistory)
                .filter(
                    DecisionHistory.user_id == user_id,
                    DecisionHistory.workspace_id == workspace.id,
                    DecisionHistory.action == MEMORY_DECISION_ACTION,
                )
                .order_by(DecisionHistory.id.desc())
                .all()
            )
            if not any((row.details or {}).get("response_id") == composed_response.response_id for row in existing):
                self.db.add(
                    DecisionHistory(
                        user_id=user_id,
                        workspace_id=workspace.id,
                        property_state_id=prop.id if prop is not None else None,
                        scenario_state_id=scenario.id if scenario is not None else None,
                        action=MEMORY_DECISION_ACTION,
                        details=details,
                    )
                )
                self.db.commit()
            return self.build_context(
                user_id=user_id,
                workspace_id=workspace.id,
                scenario_id=scenario.id if scenario is not None else None,
                broker_session_id=broker_session_id,
            )
        except SQLAlchemyError:
            self.db.rollback()
            return self._failure(MemoryStatus.FAILED, "PERSISTENCE_FAILURE")

    def build_context(
        self,
        *,
        user_id: int,
        workspace_id: int,
        scenario_id: int | None = None,
        broker_session_id: str | None = None,
    ) -> MemoryContext:
        try:
            scope = self._scope(
                user_id=user_id,
                workspace_id=workspace_id,
                scenario_id=scenario_id,
                broker_session_id=broker_session_id,
            )
            if scope is None:
                return self._failure(MemoryStatus.ACCESS_DENIED, "MEMORY_SCOPE_NOT_ACCESSIBLE")
            workspace, scenario, broker_session, prop = scope

            tool_query = self.db.query(ToolEvent).filter(
                ToolEvent.user_id == user_id,
                ToolEvent.workspace_id == workspace.id,
            )
            decision_query = self.db.query(DecisionHistory).filter(
                DecisionHistory.user_id == user_id,
                DecisionHistory.workspace_id == workspace.id,
            )
            valuation_query = self.db.query(ValuationSnapshot).filter(
                ValuationSnapshot.user_id == user_id,
                ValuationSnapshot.workspace_id == workspace.id,
            )
            if scenario is not None:
                tool_query = tool_query.filter(
                    or_(ToolEvent.scenario_state_id == scenario.id, ToolEvent.scenario_state_id.is_(None))
                )
                decision_query = decision_query.filter(
                    or_(
                        DecisionHistory.scenario_state_id == scenario.id,
                        DecisionHistory.scenario_state_id.is_(None),
                    )
                )
                valuation_query = valuation_query.filter(
                    or_(
                        ValuationSnapshot.scenario_state_id == scenario.id,
                        ValuationSnapshot.scenario_state_id.is_(None),
                    )
                )

            source_counts = {
                "tool_events": tool_query.count(),
                "decisions": decision_query.count(),
                "valuations": valuation_query.count(),
            }
            tools = tool_query.order_by(ToolEvent.id.desc()).limit(RECENT_TOOL_EVENTS_LIMIT).all()
            decisions = (
                decision_query.order_by(DecisionHistory.id.desc()).limit(RECENT_DECISIONS_LIMIT).all()
            )
            valuations = (
                valuation_query.order_by(
                    ValuationSnapshot.created_at.desc(),
                    ValuationSnapshot.valuation_id.desc(),
                )
                .limit(RECENT_VALUATIONS_LIMIT)
                .all()
            )
            assumptions, assumption_count = self._assumptions(user_id=user_id, prop=prop, scenario=scenario)
            conversation, conversation_count = self._conversation_metadata(user_id, workspace.id)
            source_counts["assumptions"] = assumption_count
            source_counts["conversation_messages"] = conversation_count

            latest_memory = self._latest_memory_decision(decision_query)
            active_comparison = (
                _json_safe(deepcopy((latest_memory.details or {}).get("active_comparison_context")))
                if latest_memory is not None
                else None
            )
            recent_tools = tuple(self._tool_event(item) for item in tools)
            recent_decisions = tuple(self._decision(item) for item in decisions)
            recent_valuations = tuple(self._valuation(item) for item in valuations)
            active_assumptions = tuple(self._assumption(item) for item in assumptions)
            broker_context = self._broker_session_context(broker_session)
            workspace_context = self._workspace_context(workspace, prop)
            scenario_context = self._scenario_context(scenario)

            citations = _merge_citations(
                *[item["citation_package"] for item in recent_tools],
                *[item["citation_package"] for item in recent_valuations],
                (
                    (latest_memory.details or {}).get("citation_package", {})
                    if latest_memory is not None
                    else {}
                ),
            )
            citation_package = {
                "workspace_id": workspace.id,
                "scenario_id": scenario.id if scenario is not None else None,
                **citations,
            }
            status = self._status(
                scenario=scenario,
                broker_session=broker_session,
                source_counts=source_counts,
                active_comparison=active_comparison,
                latest_memory=latest_memory,
            )
            metadata = {
                "schema_version": SCHEMA_VERSION,
                "memory_mode": "DETERMINISTIC_PERSISTENCE_ONLY",
                "persistence_sources": [
                    "workspaces",
                    "chats",
                    "messages",
                    "property_states",
                    "scenario_states",
                    "assumptions",
                    "decision_history",
                    "tool_events",
                    "broker_sessions",
                    "valuation_snapshots",
                ],
                "scope": {
                    "workspace_scoped": True,
                    "scenario_scoped": scenario is not None,
                    "tenant_isolated": True,
                },
                "governed_limits": {
                    "recent_tool_history": RECENT_TOOL_EVENTS_LIMIT,
                    "recent_decisions": RECENT_DECISIONS_LIMIT,
                    "recent_valuations": RECENT_VALUATIONS_LIMIT,
                    "active_assumptions": ACTIVE_ASSUMPTIONS_LIMIT,
                    "recent_conversation_metadata": RECENT_CONVERSATION_METADATA_LIMIT,
                    "scenario_lineage": SCENARIO_LINEAGE_LIMIT,
                },
                "source_counts": source_counts,
                "compression": {
                    "recent_tool_history_truncated": source_counts["tool_events"] > len(recent_tools),
                    "recent_decisions_truncated": source_counts["decisions"] > len(recent_decisions),
                    "recent_valuations_truncated": source_counts["valuations"] > len(recent_valuations),
                    "active_assumptions_truncated": source_counts["assumptions"] > len(active_assumptions),
                    "recent_conversation_metadata_truncated": conversation_count > len(conversation),
                    "ordering": "most recent first with persisted identifier tie-breakers",
                },
                "latest_composed_response_id": (
                    (latest_memory.details or {}).get("response_id") if latest_memory is not None else None
                ),
            }
            payload = {
                "status": status.value,
                "workspace_context": workspace_context,
                "scenario_context": scenario_context,
                "broker_session_context": broker_context,
                "recent_tool_history": recent_tools,
                "recent_decisions": recent_decisions,
                "recent_valuations": recent_valuations,
                "active_assumptions": active_assumptions,
                "active_comparison_context": active_comparison,
                "recent_conversation_metadata": conversation,
                "citation_package": citation_package,
                "memory_metadata": metadata,
            }
            return MemoryContext(
                memory_id=derive_memory_id(payload),
                status=status,
                workspace_context=workspace_context,
                scenario_context=scenario_context,
                broker_session_context=broker_context,
                recent_tool_history=recent_tools,
                recent_decisions=recent_decisions,
                recent_valuations=recent_valuations,
                active_assumptions=active_assumptions,
                active_comparison_context=active_comparison,
                recent_conversation_metadata=conversation,
                citation_package=citation_package,
                memory_metadata=metadata,
            )
        except SQLAlchemyError:
            self.db.rollback()
            return self._failure(MemoryStatus.FAILED, "PERSISTENCE_FAILURE")

    load_context = build_context

    def _scope(
        self,
        *,
        user_id: int,
        workspace_id: int,
        scenario_id: int | None,
        broker_session_id: str | None,
    ) -> tuple[Workspace, ScenarioState | None, BrokerSession | None, PropertyState | None] | None:
        workspace = (
            self.db.query(Workspace)
            .filter(
                Workspace.id == workspace_id,
                Workspace.user_id == user_id,
                Workspace.is_deleted.is_(False),
            )
            .first()
        )
        if workspace is None:
            return None

        broker_session = self.db.get(BrokerSession, broker_session_id) if broker_session_id is not None else None
        if broker_session_id is not None:
            if broker_session is None or broker_session.user_id != user_id or broker_session.workspace_id != workspace.id:
                return None
            if scenario_id is not None and broker_session.scenario_id != scenario_id:
                return None
            scenario_id = scenario_id or broker_session.scenario_id

        scenario = None
        prop = None
        if scenario_id is not None:
            scenario = (
                self.db.query(ScenarioState)
                .filter(
                    ScenarioState.id == scenario_id,
                    ScenarioState.workspace_id == workspace.id,
                    ScenarioState.user_id == user_id,
                    ScenarioState.is_deleted.is_(False),
                )
                .first()
            )
            if scenario is None:
                return None
            prop = (
                self.db.query(PropertyState)
                .filter(
                    PropertyState.id == scenario.property_state_id,
                    PropertyState.workspace_id == workspace.id,
                    PropertyState.user_id == user_id,
                    PropertyState.is_deleted.is_(False),
                )
                .first()
            )
            if prop is None:
                return None
        return workspace, scenario, broker_session, prop

    @staticmethod
    def _runtime_matches(execution_result: ExecutionResult, composed_response: ComposedResponse) -> bool:
        return (
            isinstance(execution_result, ExecutionResult)
            and isinstance(composed_response, ComposedResponse)
            and composed_response.execution_id == execution_result.execution_id
            and composed_response.plan_id == execution_result.plan_id
            and composed_response.primary_intent == execution_result.primary_intent
            and composed_response.secondary_intents == execution_result.secondary_intents
        )

    @staticmethod
    def _latest_memory_decision(decision_query) -> DecisionHistory | None:
        return (
            decision_query.filter(DecisionHistory.action == MEMORY_DECISION_ACTION)
            .order_by(DecisionHistory.id.desc())
            .first()
        )

    def _assumptions(
        self,
        *,
        user_id: int,
        prop: PropertyState | None,
        scenario: ScenarioState | None,
    ) -> tuple[list[Assumption], int]:
        if prop is None:
            return [], 0
        query = self.db.query(Assumption).filter(
            Assumption.user_id == user_id,
            Assumption.workspace_id == prop.workspace_id,
            Assumption.property_state_id == prop.id,
            Assumption.is_deleted.is_(False),
        )
        if scenario is not None:
            query = query.filter(
                or_(Assumption.scenario_state_id == scenario.id, Assumption.scenario_state_id.is_(None))
            )
        count = query.count()
        return query.order_by(Assumption.id.desc()).limit(ACTIVE_ASSUMPTIONS_LIMIT).all(), count

    def _conversation_metadata(self, user_id: int, workspace_id: int) -> tuple[tuple[dict[str, Any], ...], int]:
        query = (
            self.db.query(Message, Chat)
            .join(
                Chat,
                (Message.chat_id == Chat.id)
                & (Message.workspace_id == Chat.workspace_id)
                & (Message.user_id == Chat.user_id),
            )
            .filter(
                Message.user_id == user_id,
                Message.workspace_id == workspace_id,
                Message.is_deleted.is_(False),
                Chat.is_deleted.is_(False),
            )
        )
        count = query.count()
        rows = (
            query.order_by(Message.created_at.desc(), Message.id.desc())
            .limit(RECENT_CONVERSATION_METADATA_LIMIT)
            .all()
        )
        return tuple(
            {
                "message_id": message.id,
                "chat_id": chat.id,
                "chat_title": chat.title,
                "role": message.role,
                "created_at": _json_safe(message.created_at),
            }
            for message, chat in rows
        ), count

    def _workspace_context(self, workspace: Workspace, prop: PropertyState | None) -> dict[str, Any]:
        property_count = (
            self.db.query(PropertyState)
            .filter(
                PropertyState.user_id == workspace.user_id,
                PropertyState.workspace_id == workspace.id,
                PropertyState.is_deleted.is_(False),
            )
            .count()
        )
        chat_count = (
            self.db.query(Chat)
            .filter(
                Chat.user_id == workspace.user_id,
                Chat.workspace_id == workspace.id,
                Chat.is_deleted.is_(False),
            )
            .count()
        )
        return {
            "workspace_id": workspace.id,
            "name": workspace.name,
            "version": workspace.version,
            "property_count": property_count,
            "chat_count": chat_count,
            "active_property": self._property_context(prop),
        }

    @staticmethod
    def _property_context(prop: PropertyState | None) -> dict[str, Any] | None:
        if prop is None:
            return None
        return {
            "property_state_id": prop.id,
            "label": prop.label,
            "location": prop.location,
            "area": _json_safe(prop.area),
            "bedrooms": prop.bedrooms,
            "bathrooms": prop.bathrooms,
            "amenities": _json_safe(prop.amenities),
            "property_type": prop.property_type,
            "property_category": prop.property_category,
            "valuation_inputs": _json_safe(prop.valuation_inputs),
            "version": prop.version,
        }

    def _scenario_context(self, scenario: ScenarioState | None) -> dict[str, Any] | None:
        if scenario is None:
            return None
        lineage = []
        cursor = scenario
        seen = set()
        while cursor is not None and len(lineage) < SCENARIO_LINEAGE_LIMIT:
            if cursor.id in seen:
                break
            seen.add(cursor.id)
            lineage.append(self._scenario_item(cursor))
            cursor = (
                self.db.query(ScenarioState)
                .filter(
                    ScenarioState.id == cursor.parent_scenario_id,
                    ScenarioState.user_id == scenario.user_id,
                    ScenarioState.workspace_id == scenario.workspace_id,
                )
                .first()
                if cursor.parent_scenario_id is not None
                else None
            )
        return {
            "current": self._scenario_item(scenario),
            "lineage": list(reversed(lineage)),
            "lineage_truncated": cursor is not None,
        }

    @staticmethod
    def _scenario_item(scenario: ScenarioState) -> dict[str, Any]:
        return {
            "scenario_id": scenario.id,
            "property_state_id": scenario.property_state_id,
            "parent_scenario_id": scenario.parent_scenario_id,
            "name": scenario.name,
            "modifications": _json_safe(scenario.modifications),
            "delta_value": _json_safe(scenario.delta_value),
            "version": scenario.version,
            "is_deleted": scenario.is_deleted,
        }

    @staticmethod
    def _broker_session_context(session: BrokerSession | None) -> dict[str, Any] | None:
        if session is None:
            return None
        state = session.state or {}
        return {
            "session_id": session.session_id,
            "workspace_id": session.workspace_id,
            "scenario_id": session.scenario_id,
            "version": session.version,
            "updated_at": _json_safe(session.updated_at),
            "active_district": state.get("active_district"),
            "investor_preferences": _json_safe(state.get("investor_preferences")),
            "analytical_context": _json_safe(state.get("analytical_context", {})),
            "previous_request_count": len(state.get("previous_requests", [])),
            "previous_valuation_count": len(state.get("previous_valuations", [])),
        }

    @staticmethod
    def _tool_event(event: ToolEvent) -> dict[str, Any]:
        citations = _merge_citations(
            {"tool_event_ids": [event.id]},
            _extract_citations(event.payload or {}),
        )
        return {
            "tool_event_id": event.id,
            "property_state_id": event.property_state_id,
            "scenario_state_id": event.scenario_state_id,
            "tool_name": event.tool_name,
            "event_type": event.event_type,
            "created_at": _json_safe(event.created_at),
            "payload_summary": _compact_payload(event.payload or {}),
            "citation_package": citations,
        }

    @staticmethod
    def _decision(decision: DecisionHistory) -> dict[str, Any]:
        details = decision.details or {}
        return {
            "decision_id": decision.id,
            "property_state_id": decision.property_state_id,
            "scenario_state_id": decision.scenario_state_id,
            "action": decision.action,
            "details": {
                key: _json_safe(details[key])
                for key in (
                    "response_id",
                    "execution_id",
                    "plan_id",
                    "composition_status",
                    "primary_intent",
                    "secondary_intents",
                    "citation_package",
                    "active_comparison_context",
                    "broker_session_id",
                )
                if key in details
            },
            "created_at": _json_safe(decision.created_at),
        }

    @staticmethod
    def _valuation(snapshot: ValuationSnapshot) -> dict[str, Any]:
        citations = _merge_citations(
            {"valuation_ids": [snapshot.valuation_id]},
            _extract_citations(snapshot.normalized_response or {}),
            _extract_citations(snapshot.explainability_payload or {}),
        )
        return {
            "valuation_id": snapshot.valuation_id,
            "property_state_id": snapshot.property_state_id,
            "scenario_state_id": snapshot.scenario_state_id,
            "created_at": _json_safe(snapshot.created_at),
            "response_summary": {
                key: _json_safe((snapshot.normalized_response or {})[key])
                for key in _SUMMARY_FIELDS
                if key in (snapshot.normalized_response or {})
            },
            "citation_package": citations,
        }

    @staticmethod
    def _assumption(assumption: Assumption) -> dict[str, Any]:
        return {
            "assumption_id": assumption.id,
            "property_state_id": assumption.property_state_id,
            "scenario_state_id": assumption.scenario_state_id,
            "key": assumption.key,
            "value": _json_safe(assumption.value),
            "status": assumption.status,
            "source": assumption.source,
            "confirmed_at": _json_safe(assumption.confirmed_at),
            "overridden_at": _json_safe(assumption.overridden_at),
            "override_reason": assumption.override_reason,
            "version": assumption.version,
        }

    @staticmethod
    def _status(
        *,
        scenario: ScenarioState | None,
        broker_session: BrokerSession | None,
        source_counts: dict[str, int],
        active_comparison: dict[str, Any] | None,
        latest_memory: DecisionHistory | None,
    ) -> MemoryStatus:
        if (
            scenario is None
            and broker_session is None
            and not active_comparison
            and all(
                source_counts[key] == 0
                for key in ("tool_events", "valuations", "assumptions", "conversation_messages")
            )
        ):
            return MemoryStatus.EMPTY_CONTEXT
        if latest_memory is not None and (latest_memory.details or {}).get("composition_status") in {
            "PARTIAL_SUCCESS",
            "FAILED",
        }:
            return MemoryStatus.PARTIAL_SUCCESS
        return MemoryStatus.SUCCESS

    @staticmethod
    def _failure(status: MemoryStatus, reason: str) -> MemoryContext:
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "memory_mode": "DETERMINISTIC_PERSISTENCE_ONLY",
            "fail_closed": True,
            "reason_code": reason,
        }
        payload = {
            "status": status.value,
            "workspace_context": {},
            "scenario_context": None,
            "broker_session_context": None,
            "recent_tool_history": (),
            "recent_decisions": (),
            "recent_valuations": (),
            "active_assumptions": (),
            "active_comparison_context": None,
            "recent_conversation_metadata": (),
            "citation_package": {
                "workspace_id": None,
                "scenario_id": None,
                "valuation_ids": [],
                "tool_event_ids": [],
                "comparable_ids": [],
            },
            "memory_metadata": metadata,
        }
        return MemoryContext(
            memory_id=derive_memory_id(payload),
            status=status,
            workspace_context={},
            scenario_context=None,
            broker_session_context=None,
            recent_tool_history=(),
            recent_decisions=(),
            recent_valuations=(),
            active_assumptions=(),
            active_comparison_context=None,
            recent_conversation_metadata=(),
            citation_package=payload["citation_package"],
            memory_metadata=metadata,
        )
