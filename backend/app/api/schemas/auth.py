from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.api.schemas.copilot import UserResponse


class FirebaseTokenExchangeRequest(BaseModel):
    firebase_id_token: str = Field(min_length=1)


class TokenExchangeResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int
    user: UserResponse
