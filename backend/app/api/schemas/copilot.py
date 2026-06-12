from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ORMResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class VersionedResponse(ORMResponse):
    id: int
    created_at: datetime
    updated_at: datetime
    version: int


class SoftDeleteResponse(VersionedResponse):
    is_deleted: bool
    deleted_at: datetime | None = None


class UserCreate(BaseModel):
    external_subject: str = Field(min_length=1, max_length=255)
    display_name: str = Field(min_length=1, max_length=255)


class UserResponse(SoftDeleteResponse):
    external_subject: str
    display_name: str


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class WorkspaceResponse(SoftDeleteResponse):
    user_id: int
    name: str


class ChatCreate(BaseModel):
    workspace_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)


class ChatUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class ChatResponse(SoftDeleteResponse):
    user_id: int
    workspace_id: int
    title: str


class MessageCreate(BaseModel):
    chat_id: int = Field(gt=0)
    role: Literal["user", "assistant", "system", "tool"]
    content: str = Field(min_length=1)


class MessageResponse(SoftDeleteResponse):
    user_id: int
    workspace_id: int
    chat_id: int
    role: str
    content: str


class PropertyStateCreate(BaseModel):
    workspace_id: int = Field(gt=0)
    label: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=255)
    area: Decimal = Field(gt=0)
    bedrooms: int = Field(ge=0)
    bathrooms: int = Field(ge=0)
    amenities: dict[str, Any] = Field(default_factory=dict)
    property_type: str = Field(default="Apartment", min_length=1, max_length=120)
    property_category: str = Field(default="residential_rent", min_length=1, max_length=120)
    valuation_inputs: dict[str, Any] = Field(default_factory=dict)


class PropertyStateUpdate(BaseModel):
    label: str | None = Field(default=None, min_length=1, max_length=255)
    location: str | None = Field(default=None, min_length=1, max_length=255)
    area: Decimal | None = Field(default=None, gt=0)
    bedrooms: int | None = Field(default=None, ge=0)
    bathrooms: int | None = Field(default=None, ge=0)
    amenities: dict[str, Any] | None = None
    property_type: str | None = Field(default=None, min_length=1, max_length=120)
    property_category: str | None = Field(default=None, min_length=1, max_length=120)
    valuation_inputs: dict[str, Any] | None = None


class PropertyStateResponse(SoftDeleteResponse):
    user_id: int
    workspace_id: int
    label: str
    location: str
    area: Decimal
    bedrooms: int
    bathrooms: int
    amenities: dict[str, Any]
    property_type: str
    property_category: str
    valuation_inputs: dict[str, Any]


class ScenarioStateCreate(BaseModel):
    property_state_id: int = Field(gt=0)
    parent_scenario_id: int | None = Field(default=None, gt=0)
    name: str = Field(min_length=1, max_length=255)
    modifications: dict[str, Any] = Field(default_factory=dict)
    delta_value: Decimal | None = Field(default=None, ge=0)


class ScenarioStateUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    modifications: dict[str, Any] | None = None
    delta_value: Decimal | None = Field(default=None, ge=0)


class ScenarioStateResponse(SoftDeleteResponse):
    user_id: int
    workspace_id: int
    property_state_id: int
    parent_scenario_id: int | None = None
    name: str
    modifications: dict[str, Any]
    delta_value: Decimal | None = None


class ScenarioTreeNode(ScenarioStateResponse):
    children: list["ScenarioTreeNode"] = Field(default_factory=list)


class AssumptionCreate(BaseModel):
    property_state_id: int = Field(gt=0)
    scenario_state_id: int | None = Field(default=None, gt=0)
    key: str = Field(min_length=1, max_length=120)
    value: Any = None
    status: Literal["unknown", "proposed", "confirmed", "overridden"] = "unknown"
    source: str = Field(min_length=1, max_length=120)
    override_reason: str | None = None


class AssumptionUpdate(BaseModel):
    value: Any = None
    status: Literal["unknown", "proposed", "confirmed", "overridden"] | None = None
    source: str | None = Field(default=None, min_length=1, max_length=120)
    override_reason: str | None = None


class AssumptionResponse(SoftDeleteResponse):
    user_id: int
    workspace_id: int
    property_state_id: int
    scenario_state_id: int | None = None
    key: str
    value: Any = None
    status: str
    source: str
    confirmed_at: datetime | None = None
    overridden_at: datetime | None = None
    override_reason: str | None = None


class ToolEventCreate(BaseModel):
    workspace_id: int = Field(gt=0)
    chat_id: int | None = Field(default=None, gt=0)
    property_state_id: int | None = Field(default=None, gt=0)
    scenario_state_id: int | None = Field(default=None, gt=0)
    tool_name: str = Field(min_length=1, max_length=120)
    event_type: str = Field(min_length=1, max_length=120)
    payload: dict[str, Any] = Field(default_factory=dict)


class ToolEventResponse(VersionedResponse):
    user_id: int
    workspace_id: int
    chat_id: int | None = None
    property_state_id: int | None = None
    scenario_state_id: int | None = None
    tool_name: str
    event_type: str
    payload: dict[str, Any]


class DecisionHistoryResponse(VersionedResponse):
    user_id: int
    workspace_id: int
    chat_id: int | None = None
    property_state_id: int | None = None
    scenario_state_id: int | None = None
    action: str
    details: dict[str, Any]


class ScenarioLineageResponse(VersionedResponse):
    user_id: int
    workspace_id: int
    property_state_id: int
    parent_scenario_id: int | None = None
    child_scenario_id: int
    action: str
