from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class TimestampVersionMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class WorkspaceCascadeDeleteMixin:
    deleted_by_workspace_id: Mapped[int | None] = mapped_column(Integer, nullable=True)


class User(TimestampVersionMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    external_subject: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)

    workspaces: Mapped[list["Workspace"]] = relationship("Workspace", back_populates="user")


class Workspace(TimestampVersionMixin, SoftDeleteMixin, Base):
    __tablename__ = "workspaces"
    __table_args__ = (
        Index("ix_workspaces_user_active", "user_id", "is_deleted"),
        UniqueConstraint("id", "user_id", name="uq_workspaces_id_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="workspaces")
    chats: Mapped[list["Chat"]] = relationship("Chat", back_populates="workspace", foreign_keys="Chat.workspace_id")
    properties: Mapped[list["PropertyState"]] = relationship(
        "PropertyState", back_populates="workspace", foreign_keys="PropertyState.workspace_id"
    )


class Chat(TimestampVersionMixin, SoftDeleteMixin, WorkspaceCascadeDeleteMixin, Base):
    __tablename__ = "chats"
    __table_args__ = (
        Index("ix_chats_user_workspace_active", "user_id", "workspace_id", "is_deleted"),
        Index("ix_chats_workspace_cascade_restore", "user_id", "workspace_id", "deleted_by_workspace_id"),
        CheckConstraint("deleted_by_workspace_id IS NULL OR is_deleted", name="ck_chats_workspace_cascade_delete"),
        UniqueConstraint("id", "workspace_id", "user_id", name="uq_chats_id_workspace_user"),
        ForeignKeyConstraint(
            ["workspace_id", "user_id"],
            ["workspaces.id", "workspaces.user_id"],
            name="fk_chats_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="chats", foreign_keys=[workspace_id])
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", foreign_keys="Message.chat_id")


class Message(TimestampVersionMixin, SoftDeleteMixin, WorkspaceCascadeDeleteMixin, Base):
    __tablename__ = "messages"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant', 'system', 'tool')", name="ck_messages_role"),
        Index("ix_messages_chat_created_active", "user_id", "chat_id", "is_deleted", "created_at"),
        Index("ix_messages_workspace_cascade_restore", "user_id", "workspace_id", "deleted_by_workspace_id"),
        CheckConstraint("deleted_by_workspace_id IS NULL OR is_deleted", name="ck_messages_workspace_cascade_delete"),
        ForeignKeyConstraint(
            ["chat_id", "workspace_id", "user_id"],
            ["chats.id", "chats.workspace_id", "chats.user_id"],
            name="fk_messages_chat_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="RESTRICT"), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages", foreign_keys=[chat_id])


class PropertyState(TimestampVersionMixin, SoftDeleteMixin, WorkspaceCascadeDeleteMixin, Base):
    __tablename__ = "property_states"
    __table_args__ = (
        CheckConstraint("area > 0", name="ck_property_states_area_positive"),
        CheckConstraint("bedrooms >= 0", name="ck_property_states_bedrooms_non_negative"),
        CheckConstraint("bathrooms >= 0", name="ck_property_states_bathrooms_non_negative"),
        Index("ix_property_states_user_workspace_active", "user_id", "workspace_id", "is_deleted"),
        Index("ix_property_states_workspace_cascade_restore", "user_id", "workspace_id", "deleted_by_workspace_id"),
        CheckConstraint(
            "deleted_by_workspace_id IS NULL OR is_deleted",
            name="ck_property_states_workspace_cascade_delete",
        ),
        UniqueConstraint("id", "workspace_id", "user_id", name="uq_property_states_id_workspace_user"),
        ForeignKeyConstraint(
            ["workspace_id", "user_id"],
            ["workspaces.id", "workspaces.user_id"],
            name="fk_property_states_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    area: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    bathrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    amenities: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    property_type: Mapped[str] = mapped_column(String(120), nullable=False, default="Apartment", server_default="Apartment")
    property_category: Mapped[str] = mapped_column(
        String(120), nullable=False, default="residential_rent", server_default="residential_rent"
    )
    valuation_inputs: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="properties", foreign_keys=[workspace_id])
    scenarios: Mapped[list["ScenarioState"]] = relationship(
        "ScenarioState", back_populates="property_state", foreign_keys="ScenarioState.property_state_id"
    )
    assumptions: Mapped[list["Assumption"]] = relationship(
        "Assumption", back_populates="property_state", foreign_keys="Assumption.property_state_id"
    )


class ScenarioState(TimestampVersionMixin, SoftDeleteMixin, WorkspaceCascadeDeleteMixin, Base):
    __tablename__ = "scenario_states"
    __table_args__ = (
        CheckConstraint("delta_value IS NULL OR delta_value >= 0", name="ck_scenario_states_delta_non_negative"),
        Index("ix_scenario_states_user_property_active", "user_id", "property_state_id", "is_deleted"),
        Index("ix_scenario_states_parent", "parent_scenario_id"),
        Index("ix_scenario_states_workspace_cascade_restore", "user_id", "workspace_id", "deleted_by_workspace_id"),
        CheckConstraint(
            "deleted_by_workspace_id IS NULL OR is_deleted",
            name="ck_scenario_states_workspace_cascade_delete",
        ),
        UniqueConstraint(
            "id", "property_state_id", "workspace_id", "user_id", name="uq_scenario_states_id_property_workspace_user"
        ),
        UniqueConstraint("id", "workspace_id", "user_id", name="uq_scenario_states_id_workspace_user"),
        ForeignKeyConstraint(
            ["property_state_id", "workspace_id", "user_id"],
            ["property_states.id", "property_states.workspace_id", "property_states.user_id"],
            name="fk_scenario_states_property_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    property_state_id: Mapped[int] = mapped_column(ForeignKey("property_states.id", ondelete="RESTRICT"), nullable=False)
    parent_scenario_id: Mapped[int | None] = mapped_column(
        ForeignKey("scenario_states.id", ondelete="RESTRICT"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    modifications: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    delta_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)

    property_state: Mapped["PropertyState"] = relationship(
        "PropertyState", back_populates="scenarios", foreign_keys=[property_state_id]
    )
    parent_scenario: Mapped["ScenarioState | None"] = relationship(
        "ScenarioState", remote_side=[id], back_populates="child_scenarios"
    )
    child_scenarios: Mapped[list["ScenarioState"]] = relationship("ScenarioState", back_populates="parent_scenario")
    assumptions: Mapped[list["Assumption"]] = relationship(
        "Assumption", back_populates="scenario_state", foreign_keys="Assumption.scenario_state_id"
    )


class Assumption(TimestampVersionMixin, SoftDeleteMixin, WorkspaceCascadeDeleteMixin, Base):
    __tablename__ = "assumptions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('unknown', 'proposed', 'confirmed', 'overridden')",
            name="ck_assumptions_status",
        ),
        Index("ix_assumptions_user_property_active", "user_id", "property_state_id", "is_deleted"),
        Index("ix_assumptions_scenario_active", "scenario_state_id", "is_deleted"),
        Index("ix_assumptions_workspace_cascade_restore", "user_id", "workspace_id", "deleted_by_workspace_id"),
        CheckConstraint(
            "deleted_by_workspace_id IS NULL OR is_deleted",
            name="ck_assumptions_workspace_cascade_delete",
        ),
        ForeignKeyConstraint(
            ["property_state_id", "workspace_id", "user_id"],
            ["property_states.id", "property_states.workspace_id", "property_states.user_id"],
            name="fk_assumptions_property_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["scenario_state_id", "property_state_id", "workspace_id", "user_id"],
            ["scenario_states.id", "scenario_states.property_state_id", "scenario_states.workspace_id", "scenario_states.user_id"],
            name="fk_assumptions_scenario_property_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    property_state_id: Mapped[int] = mapped_column(ForeignKey("property_states.id", ondelete="RESTRICT"), nullable=False)
    scenario_state_id: Mapped[int | None] = mapped_column(
        ForeignKey("scenario_states.id", ondelete="RESTRICT"), nullable=True
    )
    key: Mapped[str] = mapped_column(String(120), nullable=False)
    value: Mapped[Any] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="unknown", server_default="unknown")
    source: Mapped[str] = mapped_column(String(120), nullable=False)
    confirmed_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    overridden_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    override_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    property_state: Mapped["PropertyState"] = relationship(
        "PropertyState", back_populates="assumptions", foreign_keys=[property_state_id]
    )
    scenario_state: Mapped["ScenarioState | None"] = relationship(
        "ScenarioState", back_populates="assumptions", foreign_keys=[scenario_state_id]
    )


class ToolEvent(TimestampVersionMixin, Base):
    __tablename__ = "tool_events"
    __table_args__ = (
        Index("ix_tool_events_user_workspace_created", "user_id", "workspace_id", "created_at"),
        ForeignKeyConstraint(
            ["workspace_id", "user_id"],
            ["workspaces.id", "workspaces.user_id"],
            name="fk_tool_events_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["chat_id", "workspace_id", "user_id"],
            ["chats.id", "chats.workspace_id", "chats.user_id"],
            name="fk_tool_events_chat_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["property_state_id", "workspace_id", "user_id"],
            ["property_states.id", "property_states.workspace_id", "property_states.user_id"],
            name="fk_tool_events_property_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["scenario_state_id", "workspace_id", "user_id"],
            ["scenario_states.id", "scenario_states.workspace_id", "scenario_states.user_id"],
            name="fk_tool_events_scenario_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    chat_id: Mapped[int | None] = mapped_column(ForeignKey("chats.id", ondelete="RESTRICT"), nullable=True)
    property_state_id: Mapped[int | None] = mapped_column(
        ForeignKey("property_states.id", ondelete="RESTRICT"), nullable=True
    )
    scenario_state_id: Mapped[int | None] = mapped_column(
        ForeignKey("scenario_states.id", ondelete="RESTRICT"), nullable=True
    )
    tool_name: Mapped[str] = mapped_column(String(120), nullable=False)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class ValuationSnapshot(TimestampVersionMixin, Base):
    __tablename__ = "valuation_snapshots"
    __table_args__ = (
        Index("ix_valuation_snapshots_user_workspace_created", "user_id", "workspace_id", "created_at"),
        ForeignKeyConstraint(
            ["workspace_id", "user_id"],
            ["workspaces.id", "workspaces.user_id"],
            name="fk_valuation_snapshots_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["property_state_id", "workspace_id", "user_id"],
            ["property_states.id", "property_states.workspace_id", "property_states.user_id"],
            name="fk_valuation_snapshots_property_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["scenario_state_id", "workspace_id", "user_id"],
            ["scenario_states.id", "scenario_states.workspace_id", "scenario_states.user_id"],
            name="fk_valuation_snapshots_scenario_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    valuation_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    property_state_id: Mapped[int] = mapped_column(ForeignKey("property_states.id", ondelete="RESTRICT"), nullable=False)
    scenario_state_id: Mapped[int | None] = mapped_column(
        ForeignKey("scenario_states.id", ondelete="RESTRICT"), nullable=True
    )
    router_request: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    normalized_response: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    explainability_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    __table_args__ = (
        Index("ix_prediction_logs_request_created", "request_id", "created_at"),
        Index("ix_prediction_logs_market_filters", "compound", "h3_res9", "property_type", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_id: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    engine: Mapped[str | None] = mapped_column(String(120), nullable=True)
    routing_decision: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lat: Mapped[float | None] = mapped_column(nullable=True)
    lng: Mapped[float | None] = mapped_column(nullable=True)
    property_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    size_sqm: Mapped[float | None] = mapped_column(nullable=True)
    compound: Mapped[str | None] = mapped_column(String(255), nullable=True)
    h3_res9: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ShadowLog(Base):
    __tablename__ = "shadow_logs"
    __table_args__ = (
        Index("ix_shadow_logs_request_created", "request_id", "created_at"),
        Index("ix_shadow_logs_market_filters", "compound_name", "h3_res9", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_id: Mapped[str] = mapped_column(String(120), nullable=False)
    actual_response: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    router_prediction: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    ml_prediction: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    cmt_prediction: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    engine_used: Mapped[str | None] = mapped_column(String(120), nullable=True)
    routing_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    comparable_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(nullable=True)
    compound_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    h3_res9: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class DecisionHistory(TimestampVersionMixin, Base):
    __tablename__ = "decision_history"
    __table_args__ = (
        Index("ix_decision_history_user_workspace_created", "user_id", "workspace_id", "created_at"),
        ForeignKeyConstraint(
            ["workspace_id", "user_id"],
            ["workspaces.id", "workspaces.user_id"],
            name="fk_decision_history_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["chat_id", "workspace_id", "user_id"],
            ["chats.id", "chats.workspace_id", "chats.user_id"],
            name="fk_decision_history_chat_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["property_state_id", "workspace_id", "user_id"],
            ["property_states.id", "property_states.workspace_id", "property_states.user_id"],
            name="fk_decision_history_property_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["scenario_state_id", "workspace_id", "user_id"],
            ["scenario_states.id", "scenario_states.workspace_id", "scenario_states.user_id"],
            name="fk_decision_history_scenario_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    chat_id: Mapped[int | None] = mapped_column(ForeignKey("chats.id", ondelete="RESTRICT"), nullable=True)
    property_state_id: Mapped[int | None] = mapped_column(
        ForeignKey("property_states.id", ondelete="RESTRICT"), nullable=True
    )
    scenario_state_id: Mapped[int | None] = mapped_column(
        ForeignKey("scenario_states.id", ondelete="RESTRICT"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class ScenarioLineage(TimestampVersionMixin, Base):
    __tablename__ = "scenario_lineage"
    __table_args__ = (
        Index("ix_scenario_lineage_user_property", "user_id", "property_state_id"),
        Index("ix_scenario_lineage_child", "child_scenario_id"),
        ForeignKeyConstraint(
            ["property_state_id", "workspace_id", "user_id"],
            ["property_states.id", "property_states.workspace_id", "property_states.user_id"],
            name="fk_scenario_lineage_property_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["child_scenario_id", "property_state_id", "workspace_id", "user_id"],
            ["scenario_states.id", "scenario_states.property_state_id", "scenario_states.workspace_id", "scenario_states.user_id"],
            name="fk_scenario_lineage_child_property_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["parent_scenario_id", "property_state_id", "workspace_id", "user_id"],
            ["scenario_states.id", "scenario_states.property_state_id", "scenario_states.workspace_id", "scenario_states.user_id"],
            name="fk_scenario_lineage_parent_property_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    property_state_id: Mapped[int] = mapped_column(ForeignKey("property_states.id", ondelete="RESTRICT"), nullable=False)
    parent_scenario_id: Mapped[int | None] = mapped_column(
        ForeignKey("scenario_states.id", ondelete="RESTRICT"), nullable=True
    )
    child_scenario_id: Mapped[int] = mapped_column(ForeignKey("scenario_states.id", ondelete="RESTRICT"), nullable=False)
    action: Mapped[str] = mapped_column(String(60), nullable=False, default="forked", server_default="forked")


class BrokerSession(TimestampVersionMixin, Base):
    __tablename__ = "broker_sessions"
    __table_args__ = (
        Index("ix_broker_sessions_workspace_updated", "workspace_id", "updated_at"),
        Index("ix_broker_sessions_owner_scenario_updated", "user_id", "workspace_id", "scenario_id", "updated_at"),
        ForeignKeyConstraint(
            ["workspace_id", "user_id"],
            ["workspaces.id", "workspaces.user_id"],
            name="fk_broker_sessions_workspace_user",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["scenario_id", "workspace_id", "user_id"],
            ["scenario_states.id", "scenario_states.workspace_id", "scenario_states.user_id"],
            name="fk_broker_sessions_scenario_workspace_user",
            ondelete="RESTRICT",
        ),
    )

    session_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenario_states.id", ondelete="RESTRICT"), nullable=False)
    state: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
