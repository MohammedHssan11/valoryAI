from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.auth import FirebaseTokenExchangeRequest, TokenExchangeResponse
from app.core.auth import create_access_token, provision_user
from app.core.config import settings
from app.core.firebase_auth import (
    FirebaseTokenError,
    FirebaseTokenVerificationUnavailable,
    FirebaseTokenVerifier,
    get_firebase_token_verifier,
)
from app.db.session import get_db

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/token-exchange", response_model=TokenExchangeResponse)
def exchange_firebase_token(
    data: FirebaseTokenExchangeRequest,
    db: Session = Depends(get_db),
    verifier: FirebaseTokenVerifier = Depends(get_firebase_token_verifier),
):
    try:
        firebase_claims = verifier.verify(data.firebase_id_token)
    except FirebaseTokenError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except FirebaseTokenVerificationUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    user = provision_user(db, firebase_claims)
    access_token = create_access_token(
        str(firebase_claims["sub"]),
        display_name=user.display_name,
    )
    return TokenExchangeResponse(
        access_token=access_token,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user,
    )
