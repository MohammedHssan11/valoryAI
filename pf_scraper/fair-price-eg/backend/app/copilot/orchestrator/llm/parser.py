from __future__ import annotations

import hashlib
import json

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.copilot.orchestrator.llm.contracts import ParsedNarrationCandidate, ProviderTransportResponse
from app.copilot.orchestrator.llm.policy import (
    CITATION_TOKEN_PATTERN,
    MAX_CITATIONS,
    MAX_NARRATION_CHARACTERS,
)


class CandidateParserError(ValueError):
    pass


class _CandidateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    narration_text: str = Field(min_length=1, max_length=MAX_NARRATION_CHARACTERS)
    citation_references: list[str] = Field(default_factory=list, max_length=MAX_CITATIONS)


class CandidateParser:
    """Parse one original provider response without repair or normalization."""

    def parse(self, response: ProviderTransportResponse) -> ParsedNarrationCandidate:
        if not isinstance(response, ProviderTransportResponse):
            raise CandidateParserError("INVALID_PROVIDER_TRANSPORT_RESPONSE")
        try:
            transport_payload = json.loads(response.original_response_body)
        except json.JSONDecodeError as exc:
            raise CandidateParserError("MALFORMED_PROVIDER_RESPONSE") from exc
        if not isinstance(transport_payload, dict):
            raise CandidateParserError("MALFORMED_PROVIDER_RESPONSE")

        candidates = transport_payload.get("candidates")
        if not isinstance(candidates, list) or len(candidates) != 1:
            raise CandidateParserError("EXPECTED_EXACTLY_ONE_PROVIDER_CANDIDATE")
        candidate_envelope = candidates[0]
        if not isinstance(candidate_envelope, dict):
            raise CandidateParserError("MALFORMED_PROVIDER_CANDIDATE")
        content = candidate_envelope.get("content")
        if not isinstance(content, dict):
            raise CandidateParserError("MALFORMED_PROVIDER_CANDIDATE")
        parts = content.get("parts")
        if not isinstance(parts, list) or len(parts) != 1:
            raise CandidateParserError("EXPECTED_EXACTLY_ONE_PROVIDER_TEXT_PART")
        part = parts[0]
        if not isinstance(part, dict) or set(part) != {"text"} or not isinstance(part["text"], str):
            raise CandidateParserError("PROVIDER_CANDIDATE_TEXT_PART_REQUIRED")

        original_candidate_json = part["text"]
        try:
            candidate = _CandidateSchema.model_validate_json(original_candidate_json)
        except ValidationError as exc:
            raise CandidateParserError("INVALID_CANDIDATE_SCHEMA") from exc
        except json.JSONDecodeError as exc:
            raise CandidateParserError("MALFORMED_CANDIDATE_JSON") from exc

        if len(set(candidate.citation_references)) != len(candidate.citation_references):
            raise CandidateParserError("DUPLICATE_CANDIDATE_CITATION")
        if any(not CITATION_TOKEN_PATTERN.fullmatch(token) for token in candidate.citation_references):
            raise CandidateParserError("UNSAFE_CANDIDATE_CITATION")
        response_hash = hashlib.sha256(response.original_response_body.encode("utf-8")).hexdigest()
        return ParsedNarrationCandidate(
            narration_text=candidate.narration_text,
            citation_references=tuple(candidate.citation_references),
            original_candidate_json=original_candidate_json,
            original_response_sha256=response_hash,
        )
