from __future__ import annotations

import json
import time
from typing import Any, Protocol
from urllib import request

from app.copilot.orchestrator.llm.contracts import PromptBundle, ProviderTransportResponse
from app.copilot.orchestrator.llm.policy import (
    MAX_PROVIDER_HTTP_REQUEST_BYTES,
    MAX_PROVIDER_HTTP_RESPONSE_BYTES,
    MAX_REQUEST_TOKENS,
    MAX_RESPONSE_TOKENS,
    PROVIDER_ENDPOINT,
    PROVIDER_MODEL,
    PROVIDER_NAME,
    PROVIDER_TIMEOUT_SECONDS,
)


_CANDIDATE_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "narration_text": {"type": "string"},
        "citation_references": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["narration_text", "citation_references"],
    "additionalProperties": False,
}


class ProviderTransportError(RuntimeError):
    pass


class NarrationProvider(Protocol):
    name: str
    model: str

    def generate(self, prompt: PromptBundle) -> ProviderTransportResponse:
        """Send one stateless provider request and preserve the original response."""


class GeminiStatelessProviderAdapter:
    name = PROVIDER_NAME
    model = PROVIDER_MODEL

    def __init__(
        self,
        *,
        api_key: str,
        timeout_seconds: float = PROVIDER_TIMEOUT_SECONDS,
        endpoint: str = PROVIDER_ENDPOINT,
    ) -> None:
        if not api_key:
            raise ValueError("Gemini API key is required")
        if timeout_seconds != PROVIDER_TIMEOUT_SECONDS:
            raise ValueError("Gemini timeout must match the approved provider profile")
        if endpoint != PROVIDER_ENDPOINT:
            raise ValueError("Gemini endpoint must match the approved provider profile")
        self._api_key = api_key
        self._timeout_seconds = timeout_seconds
        self._endpoint = endpoint

    def generate(self, prompt: PromptBundle) -> ProviderTransportResponse:
        if prompt.token_count_estimate > MAX_REQUEST_TOKENS:
            raise ProviderTransportError("PROVIDER_REQUEST_TOKEN_LIMIT_EXCEEDED")
        if prompt.max_output_tokens != MAX_RESPONSE_TOKENS:
            raise ProviderTransportError("PROVIDER_OUTPUT_TOKEN_PROFILE_MISMATCH")

        payload = {
            "systemInstruction": {"parts": [{"text": prompt.instructions}]},
            "contents": [{"role": "user", "parts": [{"text": prompt.input_text}]}],
            "generationConfig": {
                "candidateCount": 1,
                "maxOutputTokens": MAX_RESPONSE_TOKENS,
                "responseMimeType": "application/json",
                "responseJsonSchema": _CANDIDATE_JSON_SCHEMA,
                "temperature": 0,
            },
        }
        body = json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True).encode("utf-8")
        if len(body) > MAX_PROVIDER_HTTP_REQUEST_BYTES:
            raise ProviderTransportError("PROVIDER_HTTP_REQUEST_LIMIT_EXCEEDED")

        req = request.Request(
            self._endpoint,
            data=body,
            headers={
                "x-goog-api-key": self._api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        start = time.perf_counter()
        try:
            with request.urlopen(req, timeout=self._timeout_seconds) as response:
                response_body = response.read(MAX_PROVIDER_HTTP_RESPONSE_BYTES + 1)
        except Exception as exc:
            raise ProviderTransportError(f"PROVIDER_TRANSPORT_FAILURE:{type(exc).__name__}") from exc
        latency_ms = round((time.perf_counter() - start) * 1000, 3)
        if len(response_body) > MAX_PROVIDER_HTTP_RESPONSE_BYTES:
            raise ProviderTransportError("PROVIDER_HTTP_RESPONSE_LIMIT_EXCEEDED")
        try:
            original_response_body = response_body.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ProviderTransportError("PROVIDER_RESPONSE_NOT_UTF8") from exc
        token_usage = self._token_usage(original_response_body)
        return ProviderTransportResponse(
            provider=self.name,
            model=self.model,
            original_response_body=original_response_body,
            latency_ms=latency_ms,
            response_bytes=len(response_body),
            token_usage=token_usage,
        )

    @staticmethod
    def _token_usage(original_response_body: str) -> dict[str, Any]:
        try:
            payload = json.loads(original_response_body)
        except json.JSONDecodeError:
            return {}
        usage = payload.get("usageMetadata")
        return usage if isinstance(usage, dict) else {}
