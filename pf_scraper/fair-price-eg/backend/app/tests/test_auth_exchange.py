from __future__ import annotations

from datetime import datetime, timedelta, timezone
import uuid

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
import jwt
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.auth import decode_access_token
from app.core.config import settings
from app.core.firebase_auth import FirebaseTokenError, FirebaseTokenVerifier, get_firebase_token_verifier
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
import app.models.copilot  # noqa: F401


class _Verifier:
    def __init__(self, claims: dict[str, object]) -> None:
        self.claims = claims

    def verify(self, token: str) -> dict[str, object]:
        assert token == "firebase-id-token"
        return self.claims


class _Response:
    def __init__(self, certificates: dict[str, str]) -> None:
        self._certificates = certificates
        self.headers = {"Cache-Control": "public, max-age=3600"}

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, str]:
        return self._certificates


def _testing_client(verifier: _Verifier) -> TestClient:
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
    app.dependency_overrides[get_firebase_token_verifier] = lambda: verifier
    return TestClient(app)


def _firebase_token(
    private_key,
    *,
    project_id: str,
    issuer: str | None = None,
    audience: str | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "sub": "firebase-user",
            "name": "Firebase User",
            "iat": now,
            "exp": now + timedelta(minutes=5),
            "iss": issuer or f"https://securetoken.google.com/{project_id}",
            "aud": audience or project_id,
        },
        private_key,
        algorithm="RS256",
        headers={"kid": "test-key"},
    )


def test_token_exchange_provisions_user_and_returns_usable_valorai_jwt():
    subject = f"firebase-{uuid.uuid4()}"
    client = _testing_client(_Verifier({"sub": subject, "name": "Firebase User"}))

    response = client.post("/v1/auth/token-exchange", json={"firebase_id_token": "firebase-id-token"})

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    assert body["user"]["external_subject"] == subject
    assert decode_access_token(body["access_token"])["sub"] == subject
    me = client.get("/v1/copilot/users/me", headers={"Authorization": f"Bearer {body['access_token']}"})
    assert me.status_code == 200
    assert me.json()["id"] == body["user"]["id"]
    headers = {"Authorization": f"Bearer {body['access_token']}"}
    workspace = client.post("/v1/copilot/workspaces", headers=headers, json={"name": "Mobile Workspace"})
    assert workspace.status_code == 201
    workspace_id = workspace.json()["id"]
    assert client.get("/v1/copilot/workspaces", headers=headers).json()[0]["id"] == workspace_id
    assert client.put(
        f"/v1/copilot/workspaces/{workspace_id}",
        headers=headers,
        json={"name": "Updated Mobile Workspace"},
    ).json()["name"] == "Updated Mobile Workspace"
    assert client.delete(f"/v1/copilot/workspaces/{workspace_id}", headers=headers).status_code == 200


def test_firebase_verifier_validates_project_issuer_and_audience(monkeypatch):
    project_id = "valorai-test"
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    # Generate a mock self-signed X509 certificate for testing
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "securetoken.system.gserviceaccount.com"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc) - timedelta(days=1)
    ).not_valid_after(
        datetime.now(timezone.utc) + timedelta(days=30)
    ).sign(private_key, hashes.SHA256())
    
    cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode("ascii")

    monkeypatch.setattr(settings, "FIREBASE_PROJECT_ID", project_id)
    monkeypatch.setattr("app.core.firebase_auth.requests.get", lambda *args, **kwargs: _Response({"test-key": cert_pem}))

    verifier = FirebaseTokenVerifier()
    claims = verifier.verify(_firebase_token(private_key, project_id=project_id))
    assert claims["sub"] == "firebase-user"

    with pytest.raises(FirebaseTokenError):
        verifier.verify(_firebase_token(private_key, project_id=project_id, audience="different-project"))

    with pytest.raises(FirebaseTokenError):
        verifier.verify(_firebase_token(private_key, project_id=project_id, issuer="https://securetoken.google.com/different"))
