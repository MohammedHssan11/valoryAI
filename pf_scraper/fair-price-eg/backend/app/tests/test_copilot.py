from __future__ import annotations

import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.core.auth import create_access_token
from app.main import create_app
import app.models.copilot  # noqa: F401


def test_copilot_tenant_scoped_workflow():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    subject = f"api-{uuid.uuid4()}"
    headers = {"Authorization": f"Bearer {create_access_token(subject, display_name='API User')}"}
    user = client.get("/v1/copilot/users/me", headers=headers).json()

    workspace = client.post("/v1/copilot/workspaces", headers=headers, json={"name": "Portfolio"}).json()
    chat = client.post(
        "/v1/copilot/chats",
        headers=headers,
        json={"workspace_id": workspace["id"], "title": "Acquisition review"},
    ).json()
    message = client.post(
        "/v1/copilot/messages",
        headers=headers,
        json={"chat_id": chat["id"], "role": "user", "content": "Track this asset."},
    ).json()
    prop = client.post(
        "/v1/copilot/properties",
        headers=headers,
        json={
            "workspace_id": workspace["id"],
            "label": "Property A",
            "location": "Mivida",
            "area": 150,
            "bedrooms": 3,
            "bathrooms": 2,
            "amenities": {"furnished": "unknown"},
        },
    ).json()
    scenario = client.post(
        "/v1/copilot/scenarios",
        headers=headers,
        json={"property_state_id": prop["id"], "name": "Furnished", "modifications": {"furnished": True}},
    ).json()

    assert message["user_id"] == user["id"]
    assert scenario["workspace_id"] == workspace["id"]
    assert client.get(f"/v1/copilot/workspaces/{workspace['id']}/properties", headers=headers).json()[0]["label"] == "Property A"
    assert client.delete(f"/v1/copilot/workspaces/{workspace['id']}", headers=headers).status_code == 200
    assert client.get("/v1/copilot/workspaces", headers=headers).json() == []
    assert client.post(f"/v1/copilot/workspaces/{workspace['id']}/restore", headers=headers).status_code == 200


def test_copilot_rejects_caller_supplied_user_id_without_bearer_token():
    client = TestClient(create_app())

    response = client.get("/v1/copilot/workspaces", headers={"X-User-ID": "1"})

    assert response.status_code == 401
