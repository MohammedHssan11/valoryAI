from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import logging
import re
from typing import Any

import jwt
from jwt import InvalidTokenError
import requests

from app.core.config import settings

logger = logging.getLogger(__name__)


class FirebaseTokenError(ValueError):
    pass


class FirebaseTokenVerificationUnavailable(RuntimeError):
    pass


@dataclass
class _CachedCertificates:
    values: dict[str, str]
    expires_at: datetime


class FirebaseTokenVerifier:
    def __init__(self) -> None:
        self._cached_certificates: _CachedCertificates | None = None

    def verify(self, token: str) -> dict[str, Any]:
        project_id = (settings.FIREBASE_PROJECT_ID or "").strip()
        if not project_id:
            raise FirebaseTokenVerificationUnavailable("Firebase token exchange is not configured")

        try:
            header = jwt.get_unverified_header(token)
        except InvalidTokenError as exc:
            raise FirebaseTokenError("Firebase ID token is invalid") from exc

        if header.get("alg") != "RS256":
            raise FirebaseTokenError("Firebase ID token must use RS256")
        key_id = header.get("kid")
        if not isinstance(key_id, str) or not key_id:
            raise FirebaseTokenError("Firebase ID token is missing a key identifier")

        certificate_str = self._certificates().get(key_id)
        if certificate_str is None:
            self._cached_certificates = None
            certificate_str = self._certificates().get(key_id)
        if certificate_str is None:
            logger.warning("Firebase ID token signing key is unknown: kid=%s", key_id)
            raise FirebaseTokenError("Firebase ID token signing key is unknown")

        from cryptography.x509 import load_pem_x509_certificate
        try:
            cert_obj = load_pem_x509_certificate(certificate_str.encode())
            public_key = cert_obj.public_key()
        except Exception as exc:
            logger.error("Firebase ID token signing certificate is invalid: kid=%s, error=%r", key_id, exc)
            raise FirebaseTokenError("Firebase ID token signing certificate is invalid") from exc

        issuer = f"https://securetoken.google.com/{project_id}"
        try:
            claims = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=project_id,
                issuer=issuer,
                leeway=120,
                options={"require": ["sub", "iat", "exp", "aud", "iss"]},
            )
        except InvalidTokenError as exc:
            logger.warning("Firebase ID token verification failed: %r", exc)
            raise FirebaseTokenError("Firebase ID token is invalid") from exc

        subject = claims.get("sub")
        if not isinstance(subject, str) or not subject or len(subject) > 128:
            raise FirebaseTokenError("Firebase ID token subject is invalid")
        return claims

    def _certificates(self) -> dict[str, str]:
        now = datetime.now(timezone.utc)
        if self._cached_certificates is not None and self._cached_certificates.expires_at > now:
            return self._cached_certificates.values

        try:
            response = requests.get(settings.FIREBASE_CERT_URL, timeout=5)
            response.raise_for_status()
            certificates = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise FirebaseTokenVerificationUnavailable("Firebase signing certificates are unavailable") from exc
        if not isinstance(certificates, dict) or not all(
            isinstance(key, str) and isinstance(value, str) for key, value in certificates.items()
        ):
            raise FirebaseTokenVerificationUnavailable("Firebase signing certificates are malformed")

        max_age = settings.FIREBASE_CERT_CACHE_SECONDS
        cache_control = response.headers.get("Cache-Control", "")
        match = re.search(r"(?:^|,)\s*max-age=(\d+)", cache_control)
        if match is not None:
            max_age = int(match.group(1))
        self._cached_certificates = _CachedCertificates(
            values=certificates,
            expires_at=now + timedelta(seconds=max_age),
        )
        return certificates


firebase_token_verifier = FirebaseTokenVerifier()


def get_firebase_token_verifier() -> FirebaseTokenVerifier:
    return firebase_token_verifier
