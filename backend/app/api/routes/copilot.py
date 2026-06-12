from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.copilot import (
    AssumptionCreate,
    AssumptionResponse,
    AssumptionUpdate,
    ChatCreate,
    ChatResponse,
    ChatUpdate,
    DecisionHistoryResponse,
    MessageCreate,
    MessageResponse,
    PropertyStateCreate,
    PropertyStateResponse,
    PropertyStateUpdate,
    ScenarioStateCreate,
    ScenarioStateResponse,
    ScenarioStateUpdate,
    ScenarioTreeNode,
    ToolEventCreate,
    ToolEventResponse,
    UserResponse,
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspaceUpdate,
)
from app.core.auth import get_authenticated_user
from app.db.session import get_db
from app.models.copilot import User
from app.services.copilot_service import CopilotService

router = APIRouter(prefix="/v1/copilot", tags=["copilot"])


def get_copilot_service(db: Session = Depends(get_db)) -> CopilotService:
    return CopilotService(db)


def get_actor_user_id(user: User = Depends(get_authenticated_user)) -> int:
    return user.id


def _require(value, detail: str):
    if value is None:
        raise HTTPException(status_code=404, detail=detail)
    return value


def _bad_request(exc: ValueError) -> HTTPException:
    return HTTPException(status_code=400, detail=str(exc))


@router.get("/users/me", response_model=UserResponse)
def get_current_user(user: User = Depends(get_authenticated_user)):
    return user


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    actor_user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    if user_id != actor_user_id:
        return _require(None, "User not found")
    return _require(service.get_user(user_id), "User not found")


@router.post("/workspaces", response_model=WorkspaceResponse, status_code=201)
def create_workspace(
    data: WorkspaceCreate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    try:
        return service.create_workspace(user_id, data)
    except ValueError as exc:
        raise _bad_request(exc) from exc


@router.get("/workspaces", response_model=list[WorkspaceResponse])
def get_workspaces(
    include_deleted: bool = False,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return service.get_workspaces(user_id, include_deleted)


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(
    workspace_id: int,
    include_deleted: bool = False,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.get_workspace(user_id, workspace_id, include_deleted), "Workspace not found")


@router.put("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
def update_workspace(
    workspace_id: int,
    data: WorkspaceUpdate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.update_workspace(user_id, workspace_id, data), "Workspace not found")


@router.delete("/workspaces/{workspace_id}")
def delete_workspace(
    workspace_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return {"status": "deleted"} if service.delete_workspace(user_id, workspace_id) else _require(None, "Workspace not found")


@router.post("/workspaces/{workspace_id}/restore", response_model=WorkspaceResponse)
def restore_workspace(
    workspace_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.restore_workspace(user_id, workspace_id), "Workspace not found")


@router.post("/chats", response_model=ChatResponse, status_code=201)
def create_chat(
    data: ChatCreate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    try:
        return service.create_chat(user_id, data)
    except ValueError as exc:
        raise _bad_request(exc) from exc


@router.get("/workspaces/{workspace_id}/chats", response_model=list[ChatResponse])
def get_workspace_chats(
    workspace_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return service.get_chats_for_workspace(user_id, workspace_id)


@router.get("/chats/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.get_chat(user_id, chat_id), "Chat not found")


@router.put("/chats/{chat_id}", response_model=ChatResponse)
def update_chat(
    chat_id: int,
    data: ChatUpdate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.update_chat(user_id, chat_id, data), "Chat not found")


@router.delete("/chats/{chat_id}")
def delete_chat(
    chat_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return {"status": "deleted"} if service.delete_chat(user_id, chat_id) else _require(None, "Chat not found")


@router.post("/chats/{chat_id}/restore", response_model=ChatResponse)
def restore_chat(
    chat_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.restore_chat(user_id, chat_id), "Chat not found")


@router.post("/messages", response_model=MessageResponse, status_code=201)
def create_message(
    data: MessageCreate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    try:
        return service.create_message(user_id, data)
    except ValueError as exc:
        raise _bad_request(exc) from exc


@router.get("/chats/{chat_id}/messages", response_model=list[MessageResponse])
def get_chat_messages(
    chat_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return service.get_messages_for_chat(user_id, chat_id)


@router.delete("/messages/{message_id}")
def delete_message(
    message_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return {"status": "deleted"} if service.delete_message(user_id, message_id) else _require(None, "Message not found")


@router.post("/properties", response_model=PropertyStateResponse, status_code=201)
def create_property_state(
    data: PropertyStateCreate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    try:
        return service.create_property_state(user_id, data)
    except ValueError as exc:
        raise _bad_request(exc) from exc


@router.get("/workspaces/{workspace_id}/properties", response_model=list[PropertyStateResponse])
def get_workspace_properties(
    workspace_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return service.get_property_states_for_workspace(user_id, workspace_id)


@router.get("/properties/{property_id}", response_model=PropertyStateResponse)
def get_property_state(
    property_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.get_property_state(user_id, property_id), "Property not found")


@router.put("/properties/{property_id}", response_model=PropertyStateResponse)
def update_property_state(
    property_id: int,
    data: PropertyStateUpdate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.update_property_state(user_id, property_id, data), "Property not found")


@router.delete("/properties/{property_id}")
def delete_property_state(
    property_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return {"status": "deleted"} if service.delete_property_state(user_id, property_id) else _require(None, "Property not found")


@router.post("/properties/{property_id}/restore", response_model=PropertyStateResponse)
def restore_property_state(
    property_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.restore_property_state(user_id, property_id), "Property not found")


@router.post("/scenarios", response_model=ScenarioStateResponse, status_code=201)
def create_scenario_state(
    data: ScenarioStateCreate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    try:
        return service.create_scenario_state(user_id, data)
    except ValueError as exc:
        raise _bad_request(exc) from exc


@router.get("/properties/{property_id}/scenarios", response_model=list[ScenarioStateResponse])
def get_property_scenarios(
    property_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return service.get_scenario_states_for_property(user_id, property_id)


@router.get("/scenarios/{scenario_id}", response_model=ScenarioStateResponse)
def get_scenario_state(
    scenario_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.get_scenario_state(user_id, scenario_id), "Scenario not found")


@router.get("/scenarios/{scenario_id}/lineage", response_model=list[ScenarioStateResponse])
def get_scenario_lineage(
    scenario_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    lineage = service.get_scenario_lineage(user_id, scenario_id)
    return lineage if lineage else _require(None, "Scenario not found")


@router.get("/properties/{property_id}/scenario-tree", response_model=list[ScenarioTreeNode])
def get_scenario_tree(
    property_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return service.get_scenario_tree(user_id, property_id)


@router.put("/scenarios/{scenario_id}", response_model=ScenarioStateResponse)
def update_scenario_state(
    scenario_id: int,
    data: ScenarioStateUpdate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.update_scenario_state(user_id, scenario_id, data), "Scenario not found")


@router.delete("/scenarios/{scenario_id}")
def delete_scenario_state(
    scenario_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return {"status": "deleted"} if service.delete_scenario_state(user_id, scenario_id) else _require(None, "Scenario not found")


@router.post("/scenarios/{scenario_id}/restore", response_model=ScenarioStateResponse)
def restore_scenario_state(
    scenario_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.restore_scenario_state(user_id, scenario_id), "Scenario not found")


@router.post("/assumptions", response_model=AssumptionResponse, status_code=201)
def create_assumption(
    data: AssumptionCreate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    try:
        return service.create_assumption(user_id, data)
    except ValueError as exc:
        raise _bad_request(exc) from exc


@router.get("/properties/{property_id}/assumptions", response_model=list[AssumptionResponse])
def get_property_assumptions(
    property_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return service.get_assumptions_for_property(user_id, property_id)


@router.put("/assumptions/{assumption_id}", response_model=AssumptionResponse)
def update_assumption(
    assumption_id: int,
    data: AssumptionUpdate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return _require(service.update_assumption(user_id, assumption_id, data), "Assumption not found")


@router.post("/tool-events", response_model=ToolEventResponse, status_code=201)
def create_tool_event(
    data: ToolEventCreate,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    try:
        return service.record_tool_event(user_id, data)
    except ValueError as exc:
        raise _bad_request(exc) from exc


@router.get("/workspaces/{workspace_id}/tool-events", response_model=list[ToolEventResponse])
def get_tool_events(
    workspace_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return service.get_tool_events(user_id, workspace_id)


@router.get("/workspaces/{workspace_id}/decisions", response_model=list[DecisionHistoryResponse])
def get_decision_history(
    workspace_id: int,
    user_id: int = Depends(get_actor_user_id),
    service: CopilotService = Depends(get_copilot_service),
):
    return service.get_decision_history(user_id, workspace_id)
