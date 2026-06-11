from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.api.schemas.copilot import (
    AssumptionCreate,
    AssumptionUpdate,
    ChatCreate,
    ChatUpdate,
    MessageCreate,
    PropertyStateCreate,
    PropertyStateUpdate,
    ScenarioStateCreate,
    ScenarioStateUpdate,
    ToolEventCreate,
    UserCreate,
    WorkspaceCreate,
    WorkspaceUpdate,
)
from app.models.copilot import (
    Assumption,
    Chat,
    DecisionHistory,
    Message,
    PropertyState,
    ScenarioLineage,
    ScenarioState,
    ToolEvent,
    User,
    ValuationSnapshot,
    Workspace,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class CopilotService:
    def __init__(self, db: Session):
        self.db = db

    def _touch(self, obj) -> None:
        obj.updated_at = _utcnow()
        obj.version += 1

    def _soft_delete(self, obj, *, deleted_by_workspace_id: int | None = None) -> None:
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.deleted_at = _utcnow()
            if hasattr(obj, "deleted_by_workspace_id"):
                obj.deleted_by_workspace_id = deleted_by_workspace_id
            self._touch(obj)

    def _restore(self, obj) -> None:
        if obj.is_deleted:
            obj.is_deleted = False
            obj.deleted_at = None
            if hasattr(obj, "deleted_by_workspace_id"):
                obj.deleted_by_workspace_id = None
            self._touch(obj)

    def _user(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id, User.is_deleted.is_(False)).first()
        if user is None:
            raise ValueError("User not found")
        return user

    def _decision(
        self,
        *,
        user_id: int,
        workspace_id: int,
        action: str,
        details: dict[str, Any] | None = None,
        chat_id: int | None = None,
        property_state_id: int | None = None,
        scenario_state_id: int | None = None,
    ) -> None:
        self.db.add(
            DecisionHistory(
                user_id=user_id,
                workspace_id=workspace_id,
                chat_id=chat_id,
                property_state_id=property_state_id,
                scenario_state_id=scenario_state_id,
                action=action,
                details=details or {},
            )
        )

    def create_user(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id, User.is_deleted.is_(False)).first()

    def create_workspace(self, user_id: int, data: WorkspaceCreate) -> Workspace:
        self._user(user_id)
        workspace = Workspace(user_id=user_id, **data.model_dump())
        self.db.add(workspace)
        self.db.flush()
        self._decision(user_id=user_id, workspace_id=workspace.id, action="workspace.created")
        self.db.commit()
        self.db.refresh(workspace)
        return workspace

    def get_workspaces(self, user_id: int, include_deleted: bool = False) -> list[Workspace]:
        query = self.db.query(Workspace).filter(Workspace.user_id == user_id)
        if not include_deleted:
            query = query.filter(Workspace.is_deleted.is_(False))
        return query.order_by(Workspace.id).all()

    def get_workspace(self, user_id: int, workspace_id: int, include_deleted: bool = False) -> Workspace | None:
        query = self.db.query(Workspace).filter(Workspace.id == workspace_id, Workspace.user_id == user_id)
        if not include_deleted:
            query = query.filter(Workspace.is_deleted.is_(False))
        return query.first()

    def update_workspace(self, user_id: int, workspace_id: int, data: WorkspaceUpdate) -> Workspace | None:
        workspace = self.get_workspace(user_id, workspace_id)
        if workspace is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(workspace, key, value)
        self._touch(workspace)
        self._decision(user_id=user_id, workspace_id=workspace.id, action="workspace.updated")
        self.db.commit()
        self.db.refresh(workspace)
        return workspace

    def delete_workspace(self, user_id: int, workspace_id: int) -> bool:
        workspace = self.get_workspace(user_id, workspace_id)
        if workspace is None:
            return False
        self._soft_delete(workspace)
        for chat in self.get_chats_for_workspace(user_id, workspace_id):
            self._soft_delete_chat(chat, deleted_by_workspace_id=workspace_id)
        for prop in self.get_property_states_for_workspace(user_id, workspace_id):
            self._soft_delete_property(prop, deleted_by_workspace_id=workspace_id)
        self._decision(user_id=user_id, workspace_id=workspace.id, action="workspace.deleted")
        self.db.commit()
        return True

    def restore_workspace(self, user_id: int, workspace_id: int) -> Workspace | None:
        workspace = self.get_workspace(user_id, workspace_id, include_deleted=True)
        if workspace is None:
            return None
        self._restore(workspace)
        restored_children = self._restore_workspace_children(user_id, workspace.id)
        self._decision(
            user_id=user_id,
            workspace_id=workspace.id,
            action="workspace.restored",
            details={"restored_children": restored_children},
        )
        self.db.commit()
        self.db.refresh(workspace)
        return workspace

    def _restore_workspace_children(self, user_id: int, workspace_id: int) -> dict[str, int]:
        restored: dict[str, int] = {}
        for label, model in [
            ("chats", Chat),
            ("messages", Message),
            ("properties", PropertyState),
            ("scenarios", ScenarioState),
            ("assumptions", Assumption),
        ]:
            rows = (
                self.db.query(model)
                .filter(
                    model.user_id == user_id,
                    model.workspace_id == workspace_id,
                    model.is_deleted.is_(True),
                    model.deleted_by_workspace_id == workspace_id,
                )
                .all()
            )
            for row in rows:
                self._restore(row)
            restored[label] = len(rows)
        return restored

    def create_chat(self, user_id: int, data: ChatCreate) -> Chat:
        workspace = self.get_workspace(user_id, data.workspace_id)
        if workspace is None:
            raise ValueError("Workspace not found")
        chat = Chat(user_id=user_id, **data.model_dump())
        self.db.add(chat)
        self.db.flush()
        self._decision(user_id=user_id, workspace_id=workspace.id, chat_id=chat.id, action="chat.created")
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_chats_for_workspace(self, user_id: int, workspace_id: int, include_deleted: bool = False) -> list[Chat]:
        if self.get_workspace(user_id, workspace_id, include_deleted=include_deleted) is None:
            return []
        query = self.db.query(Chat).filter(Chat.user_id == user_id, Chat.workspace_id == workspace_id)
        if not include_deleted:
            query = query.filter(Chat.is_deleted.is_(False))
        return query.order_by(Chat.id).all()

    def get_chat(self, user_id: int, chat_id: int, include_deleted: bool = False) -> Chat | None:
        query = self.db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id)
        if not include_deleted:
            query = query.filter(Chat.is_deleted.is_(False))
        return query.first()

    def update_chat(self, user_id: int, chat_id: int, data: ChatUpdate) -> Chat | None:
        chat = self.get_chat(user_id, chat_id)
        if chat is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(chat, key, value)
        self._touch(chat)
        self._decision(user_id=user_id, workspace_id=chat.workspace_id, chat_id=chat.id, action="chat.updated")
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def _soft_delete_chat(self, chat: Chat, *, deleted_by_workspace_id: int | None = None) -> None:
        self._soft_delete(chat, deleted_by_workspace_id=deleted_by_workspace_id)
        for message in self.db.query(Message).filter(Message.chat_id == chat.id, Message.is_deleted.is_(False)).all():
            self._soft_delete(message, deleted_by_workspace_id=deleted_by_workspace_id)

    def delete_chat(self, user_id: int, chat_id: int) -> bool:
        chat = self.get_chat(user_id, chat_id)
        if chat is None:
            return False
        self._soft_delete_chat(chat)
        self._decision(user_id=user_id, workspace_id=chat.workspace_id, chat_id=chat.id, action="chat.deleted")
        self.db.commit()
        return True

    def restore_chat(self, user_id: int, chat_id: int) -> Chat | None:
        chat = self.get_chat(user_id, chat_id, include_deleted=True)
        if chat is None or self.get_workspace(user_id, chat.workspace_id) is None:
            return None
        self._restore(chat)
        self._decision(user_id=user_id, workspace_id=chat.workspace_id, chat_id=chat.id, action="chat.restored")
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def create_message(self, user_id: int, data: MessageCreate) -> Message:
        chat = self.get_chat(user_id, data.chat_id)
        if chat is None:
            raise ValueError("Chat not found")
        message = Message(user_id=user_id, workspace_id=chat.workspace_id, **data.model_dump())
        self.db.add(message)
        self.db.flush()
        self._decision(
            user_id=user_id,
            workspace_id=chat.workspace_id,
            chat_id=chat.id,
            action="message.created",
            details={"role": message.role},
        )
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_for_chat(self, user_id: int, chat_id: int, include_deleted: bool = False) -> list[Message]:
        if self.get_chat(user_id, chat_id, include_deleted=include_deleted) is None:
            return []
        query = self.db.query(Message).filter(Message.user_id == user_id, Message.chat_id == chat_id)
        if not include_deleted:
            query = query.filter(Message.is_deleted.is_(False))
        return query.order_by(Message.created_at, Message.id).all()

    def delete_message(self, user_id: int, message_id: int) -> bool:
        message = self.db.query(Message).filter(Message.id == message_id, Message.user_id == user_id).first()
        if message is None or message.is_deleted:
            return False
        self._soft_delete(message)
        self._decision(
            user_id=user_id,
            workspace_id=message.workspace_id,
            chat_id=message.chat_id,
            action="message.deleted",
        )
        self.db.commit()
        return True

    def create_property_state(self, user_id: int, data: PropertyStateCreate) -> PropertyState:
        workspace = self.get_workspace(user_id, data.workspace_id)
        if workspace is None:
            raise ValueError("Workspace not found")
        prop = PropertyState(user_id=user_id, **data.model_dump())
        self.db.add(prop)
        self.db.flush()
        self._decision(
            user_id=user_id,
            workspace_id=prop.workspace_id,
            property_state_id=prop.id,
            action="property.created",
        )
        self.db.commit()
        self.db.refresh(prop)
        return prop

    def get_property_states_for_workspace(
        self, user_id: int, workspace_id: int, include_deleted: bool = False
    ) -> list[PropertyState]:
        if self.get_workspace(user_id, workspace_id, include_deleted=include_deleted) is None:
            return []
        query = self.db.query(PropertyState).filter(
            PropertyState.user_id == user_id, PropertyState.workspace_id == workspace_id
        )
        if not include_deleted:
            query = query.filter(PropertyState.is_deleted.is_(False))
        return query.order_by(PropertyState.id).all()

    def get_property_state(self, user_id: int, property_id: int, include_deleted: bool = False) -> PropertyState | None:
        query = self.db.query(PropertyState).filter(PropertyState.id == property_id, PropertyState.user_id == user_id)
        if not include_deleted:
            query = query.filter(PropertyState.is_deleted.is_(False))
        return query.first()

    def update_property_state(
        self, user_id: int, property_id: int, data: PropertyStateUpdate
    ) -> PropertyState | None:
        prop = self.get_property_state(user_id, property_id)
        if prop is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(prop, key, value)
        self._touch(prop)
        self._decision(
            user_id=user_id,
            workspace_id=prop.workspace_id,
            property_state_id=prop.id,
            action="property.updated",
        )
        self.db.commit()
        self.db.refresh(prop)
        return prop

    def _soft_delete_property(self, prop: PropertyState, *, deleted_by_workspace_id: int | None = None) -> None:
        self._soft_delete(prop, deleted_by_workspace_id=deleted_by_workspace_id)
        for scenario in self.db.query(ScenarioState).filter(
            ScenarioState.property_state_id == prop.id, ScenarioState.is_deleted.is_(False)
        ).all():
            self._soft_delete_scenario(scenario, deleted_by_workspace_id=deleted_by_workspace_id)
        for assumption in self.db.query(Assumption).filter(
            Assumption.property_state_id == prop.id, Assumption.is_deleted.is_(False)
        ).all():
            self._soft_delete(assumption, deleted_by_workspace_id=deleted_by_workspace_id)

    def delete_property_state(self, user_id: int, property_id: int) -> bool:
        prop = self.get_property_state(user_id, property_id)
        if prop is None:
            return False
        self._soft_delete_property(prop)
        self._decision(
            user_id=user_id,
            workspace_id=prop.workspace_id,
            property_state_id=prop.id,
            action="property.deleted",
        )
        self.db.commit()
        return True

    def restore_property_state(self, user_id: int, property_id: int) -> PropertyState | None:
        prop = self.get_property_state(user_id, property_id, include_deleted=True)
        if prop is None or self.get_workspace(user_id, prop.workspace_id) is None:
            return None
        self._restore(prop)
        self._decision(
            user_id=user_id,
            workspace_id=prop.workspace_id,
            property_state_id=prop.id,
            action="property.restored",
        )
        self.db.commit()
        self.db.refresh(prop)
        return prop

    def create_scenario_state(self, user_id: int, data: ScenarioStateCreate) -> ScenarioState:
        prop = self.get_property_state(user_id, data.property_state_id)
        if prop is None:
            raise ValueError("Property not found")
        if data.parent_scenario_id is not None:
            parent = self.get_scenario_state(user_id, data.parent_scenario_id)
            if parent is None or parent.property_state_id != prop.id:
                raise ValueError("Parent scenario must belong to the same property")
        scenario = ScenarioState(user_id=user_id, workspace_id=prop.workspace_id, **data.model_dump())
        self.db.add(scenario)
        self.db.flush()
        self.db.add(
            ScenarioLineage(
                user_id=user_id,
                workspace_id=prop.workspace_id,
                property_state_id=prop.id,
                parent_scenario_id=scenario.parent_scenario_id,
                child_scenario_id=scenario.id,
            )
        )
        self._decision(
            user_id=user_id,
            workspace_id=prop.workspace_id,
            property_state_id=prop.id,
            scenario_state_id=scenario.id,
            action="scenario.forked",
            details={"parent_scenario_id": scenario.parent_scenario_id},
        )
        self.db.commit()
        self.db.refresh(scenario)
        return scenario

    def get_scenario_states_for_property(
        self, user_id: int, property_id: int, include_deleted: bool = False
    ) -> list[ScenarioState]:
        if self.get_property_state(user_id, property_id, include_deleted=include_deleted) is None:
            return []
        query = self.db.query(ScenarioState).filter(
            ScenarioState.user_id == user_id, ScenarioState.property_state_id == property_id
        )
        if not include_deleted:
            query = query.filter(ScenarioState.is_deleted.is_(False))
        return query.order_by(ScenarioState.id).all()

    def get_scenario_state(self, user_id: int, scenario_id: int, include_deleted: bool = False) -> ScenarioState | None:
        query = self.db.query(ScenarioState).filter(ScenarioState.id == scenario_id, ScenarioState.user_id == user_id)
        if not include_deleted:
            query = query.filter(ScenarioState.is_deleted.is_(False))
        return query.first()

    def update_scenario_state(
        self, user_id: int, scenario_id: int, data: ScenarioStateUpdate
    ) -> ScenarioState | None:
        scenario = self.get_scenario_state(user_id, scenario_id)
        if scenario is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(scenario, key, value)
        self._touch(scenario)
        self._decision(
            user_id=user_id,
            workspace_id=scenario.workspace_id,
            property_state_id=scenario.property_state_id,
            scenario_state_id=scenario.id,
            action="scenario.updated",
        )
        self.db.commit()
        self.db.refresh(scenario)
        return scenario

    def _soft_delete_scenario(self, scenario: ScenarioState, *, deleted_by_workspace_id: int | None = None) -> None:
        self._soft_delete(scenario, deleted_by_workspace_id=deleted_by_workspace_id)
        for assumption in self.db.query(Assumption).filter(
            Assumption.scenario_state_id == scenario.id, Assumption.is_deleted.is_(False)
        ).all():
            self._soft_delete(assumption, deleted_by_workspace_id=deleted_by_workspace_id)

    def delete_scenario_state(self, user_id: int, scenario_id: int) -> bool:
        scenario = self.get_scenario_state(user_id, scenario_id)
        if scenario is None:
            return False
        self._soft_delete_scenario(scenario)
        self._decision(
            user_id=user_id,
            workspace_id=scenario.workspace_id,
            property_state_id=scenario.property_state_id,
            scenario_state_id=scenario.id,
            action="scenario.deleted",
        )
        self.db.commit()
        return True

    def restore_scenario_state(self, user_id: int, scenario_id: int) -> ScenarioState | None:
        scenario = self.get_scenario_state(user_id, scenario_id, include_deleted=True)
        if scenario is None or self.get_property_state(user_id, scenario.property_state_id) is None:
            return None
        self._restore(scenario)
        self._decision(
            user_id=user_id,
            workspace_id=scenario.workspace_id,
            property_state_id=scenario.property_state_id,
            scenario_state_id=scenario.id,
            action="scenario.restored",
        )
        self.db.commit()
        self.db.refresh(scenario)
        return scenario

    def get_scenario_lineage(self, user_id: int, scenario_id: int) -> list[ScenarioState]:
        scenario = self.get_scenario_state(user_id, scenario_id, include_deleted=True)
        if scenario is None:
            return []
        lineage: list[ScenarioState] = []
        seen: set[int] = set()
        while scenario is not None:
            if scenario.id in seen:
                raise ValueError("Scenario lineage cycle detected")
            seen.add(scenario.id)
            lineage.append(scenario)
            scenario = (
                self.get_scenario_state(user_id, scenario.parent_scenario_id, include_deleted=True)
                if scenario.parent_scenario_id is not None
                else None
            )
        return list(reversed(lineage))

    def get_scenario_tree(self, user_id: int, property_id: int) -> list[dict[str, Any]]:
        scenarios = self.get_scenario_states_for_property(user_id, property_id)
        children: dict[int | None, list[ScenarioState]] = {}
        for scenario in scenarios:
            children.setdefault(scenario.parent_scenario_id, []).append(scenario)

        def build(node: ScenarioState) -> dict[str, Any]:
            return {
                **{
                    column.name: getattr(node, column.name)
                    for column in ScenarioState.__table__.columns
                },
                "children": [build(child) for child in children.get(node.id, [])],
            }

        return [build(root) for root in children.get(None, [])]

    def create_assumption(self, user_id: int, data: AssumptionCreate) -> Assumption:
        prop = self.get_property_state(user_id, data.property_state_id)
        if prop is None:
            raise ValueError("Property not found")
        if data.scenario_state_id is not None:
            scenario = self.get_scenario_state(user_id, data.scenario_state_id)
            if scenario is None or scenario.property_state_id != prop.id:
                raise ValueError("Scenario must belong to the same property")
        assumption = Assumption(user_id=user_id, workspace_id=prop.workspace_id, **data.model_dump())
        self._set_assumption_timestamps(assumption)
        self.db.add(assumption)
        self.db.flush()
        self._decision(
            user_id=user_id,
            workspace_id=prop.workspace_id,
            property_state_id=prop.id,
            scenario_state_id=assumption.scenario_state_id,
            action="assumption.created",
            details={"key": assumption.key, "status": assumption.status},
        )
        self.db.commit()
        self.db.refresh(assumption)
        return assumption

    def _set_assumption_timestamps(self, assumption: Assumption) -> None:
        if assumption.status == "confirmed" and assumption.confirmed_at is None:
            assumption.confirmed_at = _utcnow()
        if assumption.status == "overridden" and assumption.overridden_at is None:
            assumption.overridden_at = _utcnow()

    def get_assumptions_for_property(self, user_id: int, property_id: int) -> list[Assumption]:
        if self.get_property_state(user_id, property_id) is None:
            return []
        return (
            self.db.query(Assumption)
            .filter(
                Assumption.user_id == user_id,
                Assumption.property_state_id == property_id,
                Assumption.is_deleted.is_(False),
            )
            .order_by(Assumption.id)
            .all()
        )

    def get_assumption(self, user_id: int, assumption_id: int) -> Assumption | None:
        return (
            self.db.query(Assumption)
            .filter(Assumption.id == assumption_id, Assumption.user_id == user_id, Assumption.is_deleted.is_(False))
            .first()
        )

    def update_assumption(self, user_id: int, assumption_id: int, data: AssumptionUpdate) -> Assumption | None:
        assumption = self.get_assumption(user_id, assumption_id)
        if assumption is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(assumption, key, value)
        self._set_assumption_timestamps(assumption)
        self._touch(assumption)
        self._decision(
            user_id=user_id,
            workspace_id=assumption.workspace_id,
            property_state_id=assumption.property_state_id,
            scenario_state_id=assumption.scenario_state_id,
            action="assumption.updated",
            details={"key": assumption.key, "status": assumption.status},
        )
        self.db.commit()
        self.db.refresh(assumption)
        return assumption

    def record_tool_event(self, user_id: int, data: ToolEventCreate) -> ToolEvent:
        if self.get_workspace(user_id, data.workspace_id) is None:
            raise ValueError("Workspace not found")
        if data.chat_id is not None:
            chat = self.get_chat(user_id, data.chat_id)
            if chat is None or chat.workspace_id != data.workspace_id:
                raise ValueError("Chat must belong to the same workspace")
        prop: PropertyState | None = None
        if data.property_state_id is not None:
            prop = self.get_property_state(user_id, data.property_state_id)
            if prop is None or prop.workspace_id != data.workspace_id:
                raise ValueError("Property must belong to the same workspace")
        if data.scenario_state_id is not None:
            scenario = self.get_scenario_state(user_id, data.scenario_state_id)
            if scenario is None or scenario.workspace_id != data.workspace_id:
                raise ValueError("Scenario must belong to the same workspace")
        payload = data.payload
        if self._is_direct_valuation_event(data):
            self._persist_direct_valuation_snapshot(user_id, data, prop, payload)
        event = ToolEvent(user_id=user_id, **data.model_dump(exclude={"payload"}), payload=payload)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    @staticmethod
    def _is_direct_valuation_event(data: ToolEventCreate) -> bool:
        return (
            data.tool_name == "direct_valuation"
            and data.event_type == "valuation.completed"
            and data.payload.get("source") == "direct_valuation"
        )

    @staticmethod
    def _payload_record(payload: dict[str, Any], key: str) -> dict[str, Any]:
        value = payload.get(key)
        if not isinstance(value, dict):
            raise ValueError(f"{key} is required for direct valuation snapshot persistence")
        return value

    @staticmethod
    def _required_int(payload: dict[str, Any], key: str) -> int:
        value = payload.get(key)
        if isinstance(value, bool):
            raise ValueError(f"{key} must be numeric")
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{key} is required for direct valuation snapshot persistence") from exc

    @staticmethod
    def _confidence_label(result: dict[str, Any]) -> str:
        confidence = result.get("confidence")
        if isinstance(confidence, dict):
            label = confidence.get("label")
            if isinstance(label, str) and label.strip():
                return label.strip()
        return "Unknown"

    @staticmethod
    def _direct_fairness_status(request_payload: dict[str, Any], result: dict[str, Any]) -> str:
        target = request_payload.get("target_price_egp")
        try:
            target_price = int(target) if target is not None else None
            low = int(result["range_low_egp"])
            high = int(result["range_high_egp"])
        except (KeyError, TypeError, ValueError):
            return "Within Fair Value Range"
        if target_price is None:
            return "Within Fair Value Range"
        if target_price < low:
            return "Below Fair Value"
        if target_price > high:
            return "Above Fair Value"
        return "Within Fair Value Range"

    def _direct_explainability_payload(
        self,
        request_payload: dict[str, Any],
        result: dict[str, Any],
    ) -> dict[str, Any]:
        explainability = result.get("explainability")
        if isinstance(explainability, dict):
            return explainability

        fair_price = self._required_int(result, "fair_price_egp")
        confidence_label = self._confidence_label(result)
        confidence_reason = f"{confidence_label} confidence from the persisted TruthLayer direct valuation."
        explanation = result.get("explanation")
        strongest = (
            str(explanation[0])
            if isinstance(explanation, list) and explanation and isinstance(explanation[0], str)
            else "Persisted TruthLayer valuation evidence anchors this snapshot."
        )
        return {
            "router_explanation": result.get("routing_reason") or "Direct valuation response persisted as TruthLayer evidence.",
            "confidence_explanation": {
                "confidence_level": confidence_label,
                "confidence_reason": confidence_reason,
            },
            "fairness_explanation": {
                "estimated_value": fair_price,
                "asking_price": request_payload.get("target_price_egp"),
                "difference_amount": None,
                "difference_percentage": None,
                "status": self._direct_fairness_status(request_payload, result),
            },
            "narrative_explanation": {
                "summary": f"The property's fair value is {fair_price:,.0f} EGP.",
                "why_this_price": "This explanation is grounded in the persisted direct TruthLayer valuation response.",
                "strongest_factors": strongest,
                "confidence_reason": confidence_reason,
            },
            "comparable_evidence": [],
            "feature_drivers": [],
        }

    def _direct_normalized_response(
        self,
        valuation_id: str,
        result: dict[str, Any],
        timestamp: datetime,
    ) -> dict[str, Any]:
        return {
            "tool_name": "valuation",
            "valuation_id": valuation_id,
            "fair_price": self._required_int(result, "fair_price_egp"),
            "price_range": {
                "low": self._required_int(result, "range_low_egp"),
                "high": self._required_int(result, "range_high_egp"),
            },
            "confidence_level": self._confidence_label(result),
            "engine_used": str(result.get("engine_used") or "UNKNOWN"),
            "routing_reason": str(result.get("routing_reason") or "UNKNOWN"),
            "timestamp": timestamp.isoformat(),
            "source": "TruthLayer",
            "source_attribution": "direct_valuation",
        }

    def _persist_direct_valuation_snapshot(
        self,
        user_id: int,
        data: ToolEventCreate,
        prop: PropertyState | None,
        payload: dict[str, Any],
    ) -> None:
        if prop is None:
            raise ValueError("Property is required for direct valuation snapshot persistence")

        request_payload = self._payload_record(payload, "valuation_request")
        result = self._payload_record(payload, "valuation_result")
        request_id = payload.get("request_id")
        valuation_id = request_id if isinstance(request_id, str) and request_id.strip() else f"val_{uuid.uuid4().hex}"
        valuation_id = valuation_id.strip()
        if len(valuation_id) > 80:
            raise ValueError("request_id is too long for valuation snapshot persistence")

        snapshot = (
            self.db.query(ValuationSnapshot)
            .filter(
                ValuationSnapshot.valuation_id == valuation_id,
                ValuationSnapshot.user_id == user_id,
                ValuationSnapshot.workspace_id == data.workspace_id,
            )
            .first()
        )
        if snapshot is None:
            snapshot = ValuationSnapshot(
                valuation_id=valuation_id,
                user_id=user_id,
                workspace_id=data.workspace_id,
                property_state_id=prop.id,
                scenario_state_id=data.scenario_state_id,
                router_request=request_payload,
                normalized_response={},
                explainability_payload=self._direct_explainability_payload(request_payload, result),
            )
            self.db.add(snapshot)
            self.db.flush()
        else:
            snapshot.property_state_id = prop.id
            snapshot.scenario_state_id = data.scenario_state_id
            snapshot.router_request = request_payload
            snapshot.explainability_payload = self._direct_explainability_payload(request_payload, result)
            self._touch(snapshot)

        timestamp = snapshot.created_at or _utcnow()
        normalized = self._direct_normalized_response(valuation_id, result, timestamp)
        snapshot.normalized_response = normalized
        payload["valuation_id"] = valuation_id
        payload["response"] = normalized

    def get_tool_events(self, user_id: int, workspace_id: int) -> list[ToolEvent]:
        if self.get_workspace(user_id, workspace_id, include_deleted=True) is None:
            return []
        return (
            self.db.query(ToolEvent)
            .filter(ToolEvent.user_id == user_id, ToolEvent.workspace_id == workspace_id)
            .order_by(ToolEvent.id)
            .all()
        )

    def get_decision_history(self, user_id: int, workspace_id: int) -> list[DecisionHistory]:
        if self.get_workspace(user_id, workspace_id, include_deleted=True) is None:
            return []
        return (
            self.db.query(DecisionHistory)
            .filter(DecisionHistory.user_id == user_id, DecisionHistory.workspace_id == workspace_id)
            .order_by(DecisionHistory.id)
            .all()
        )
