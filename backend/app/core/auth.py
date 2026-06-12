from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.copilot import User

bearer_scheme = HTTPBearer(auto_error=False)


def _unauthorized(detail: str = "Invalid or missing bearer token") -> HTTPException:
    return HTTPException(
        status_code=401,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
            options={"require": ["sub", "iat", "exp"]},
        )
    except InvalidTokenError as exc:
        raise _unauthorized() from exc


def _display_name(claims: dict[str, Any]) -> str:
    value = str(claims.get("name") or claims["sub"]).strip()
    return value[:255] or str(claims["sub"])[:255]


def _provision_user(db: Session, claims: dict[str, Any]) -> User:
    subject = str(claims["sub"]).strip()
    if not subject or len(subject) > 255:
        raise _unauthorized("JWT subject is invalid")

    user = db.query(User).filter(User.external_subject == subject, User.is_deleted.is_(False)).first()
    if user is not None:
        return user

    user = User(external_subject=subject, display_name=_display_name(claims))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        user = db.query(User).filter(User.external_subject == subject, User.is_deleted.is_(False)).first()
        if user is None:
            raise
    else:
        db.refresh(user)
    return user


def provision_user(db: Session, claims: dict[str, Any]) -> User:
    return _provision_user(db, claims)


def get_authenticated_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized()
    return _provision_user(db, decode_access_token(credentials.credentials))


def create_access_token(
    subject: str,
    *,
    display_name: str | None = None,
    expires_in: timedelta | None = None,
) -> str:
    """Generate a ValorAI access token for the trusted local authorization boundary."""
    now = datetime.now(timezone.utc)
    lifetime = expires_in or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    claims: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + lifetime,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
    }
    if display_name:
        claims["name"] = display_name
    return jwt.encode(claims, settings.JWT_SECRET, algorithm="HS256")
