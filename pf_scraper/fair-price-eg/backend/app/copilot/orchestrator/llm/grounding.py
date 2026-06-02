from __future__ import annotations

from app.copilot.orchestrator.llm.contracts import (
    GroundingDecision,
    GroundingResult,
    ParsedNarrationCandidate,
    PromptAssemblyMetadata,
    ScopedNarrationEnvelope,
)
from app.copilot.orchestrator.llm.gate import canonical_json
from app.copilot.orchestrator.llm.policy import (
    ASSEMBLY_POLICY_VERSION,
    CITATION_TOKEN_PATTERN,
    CONTRACT_VERSION,
    EVICTION_POLICY_VERSION,
    FACT_LINE_PATTERN,
    INLINE_CITATION_PATTERN,
    MAX_CITATIONS,
    MAX_NARRATION_CHARACTERS,
    MAX_NARRATION_LINES,
    PROHIBITED_CLAIMS_POLICY_VERSION,
    PROVIDER_PROFILE_ID,
    SERIALIZER_VERSION,
    TOKENIZER_VERSION,
)


class DeterministicGroundingLayer:
    """Decision-only original-candidate grounding with no I/O or repair."""

    def validate(
        self,
        *,
        candidate: ParsedNarrationCandidate,
        envelope: ScopedNarrationEnvelope,
        assembly_metadata: PromptAssemblyMetadata,
    ) -> GroundingResult:
        checked_versions = {
            "contract": CONTRACT_VERSION,
            "prohibited_claims": PROHIBITED_CLAIMS_POLICY_VERSION,
            "assembly": f"{ASSEMBLY_POLICY_VERSION}:{EVICTION_POLICY_VERSION}",
            "serializer": SERIALIZER_VERSION,
            "tokenizer": TOKENIZER_VERSION,
            "provider_profile": PROVIDER_PROFILE_ID,
        }
        binding_failure = self._binding_failure(envelope=envelope, assembly_metadata=assembly_metadata)
        if binding_failure is not None:
            return self._result(GroundingDecision.ACCESS_DENIED, binding_failure, checked_versions, 0)
        if (
            envelope.grounding_manifest.contract_version != CONTRACT_VERSION
            or envelope.grounding_manifest.prohibited_claims_policy_version != PROHIBITED_CLAIMS_POLICY_VERSION
        ):
            return self._result(GroundingDecision.REJECT_NARRATION, "POLICY_VERSION_MISMATCH", checked_versions, 0)
        if not isinstance(candidate, ParsedNarrationCandidate):
            return self._result(GroundingDecision.REJECT_NARRATION, "MALFORMED_CANDIDATE", checked_versions, 0)
        if not candidate.narration_text or len(candidate.narration_text) > MAX_NARRATION_CHARACTERS:
            return self._result(GroundingDecision.REJECT_NARRATION, "CANDIDATE_TEXT_OUT_OF_BOUNDS", checked_versions, 0)
        if len(candidate.citation_references) > MAX_CITATIONS:
            return self._result(GroundingDecision.REJECT_NARRATION, "CANDIDATE_CITATION_LIMIT_EXCEEDED", checked_versions, 0)

        allowed_citations = {
            token
            for values in envelope.grounding_manifest.citation_tokens.values()
            for token in values
        }
        if any(not CITATION_TOKEN_PATTERN.fullmatch(token) for token in candidate.citation_references):
            return self._result(GroundingDecision.REJECT_NARRATION, "UNSAFE_CANDIDATE_CITATION", checked_versions, 0)
        if not set(candidate.citation_references).issubset(allowed_citations):
            return self._result(GroundingDecision.REJECT_NARRATION, "CITATION_MISMATCH", checked_versions, 0)

        lines = candidate.narration_text.splitlines()
        if not lines or len(lines) > MAX_NARRATION_LINES or any(not line for line in lines):
            return self._result(GroundingDecision.REJECT_NARRATION, "AMBIGUOUS_VALIDATION", checked_versions, 0)

        included_segments = set(assembly_metadata.included_segment_ids)
        facts = {
            fact.fact_id: fact
            for fact in envelope.grounding_manifest.facts
            if fact.segment_id in included_segments
        }
        used_fact_ids = []
        observed_citations = []
        for line in lines:
            match = FACT_LINE_PATTERN.fullmatch(line)
            if match is None:
                return self._result(GroundingDecision.REJECT_NARRATION, "AMBIGUOUS_VALIDATION", checked_versions, 0)
            fact_id = match.group("fact_id")
            fact = facts.get(fact_id)
            if fact is None:
                return self._result(GroundingDecision.REJECT_NARRATION, "UNGROUNDED_FACT", checked_versions, 0)
            if match.group("value") != canonical_json(fact.value):
                return self._result(GroundingDecision.REJECT_NARRATION, "UNGROUNDED_VALUE", checked_versions, 0)
            line_citations = tuple(INLINE_CITATION_PATTERN.findall(match.group("citations")))
            if not line_citations or not set(fact.required_citations).issubset(set(line_citations)):
                return self._result(GroundingDecision.REJECT_NARRATION, "MISSING_REQUIRED_CITATION", checked_versions, 0)
            if not set(line_citations).issubset(allowed_citations):
                return self._result(GroundingDecision.REJECT_NARRATION, "CITATION_MISMATCH", checked_versions, 0)
            used_fact_ids.append(fact_id)
            for token in line_citations:
                if token not in observed_citations:
                    observed_citations.append(token)

        if tuple(observed_citations) != candidate.citation_references:
            return self._result(
                GroundingDecision.REJECT_NARRATION,
                "INLINE_CITATION_LIST_MISMATCH",
                checked_versions,
                len(observed_citations),
            )
        if not set(envelope.grounding_manifest.required_disclosure_fact_ids).issubset(set(used_fact_ids)):
            return self._result(
                GroundingDecision.REJECT_NARRATION,
                "REQUIRED_LIMITATION_DISCLOSURE_MISSING",
                checked_versions,
                len(observed_citations),
            )
        return self._result(
            GroundingDecision.ACCEPT_NARRATION,
            "ORIGINAL_CANDIDATE_GROUNDED",
            checked_versions,
            len(observed_citations),
        )

    @staticmethod
    def _binding_failure(
        *,
        envelope: ScopedNarrationEnvelope,
        assembly_metadata: PromptAssemblyMetadata,
    ) -> str | None:
        if envelope.binding_attestation != envelope.grounding_manifest.binding_attestation:
            return "BINDING_MISMATCH"
        if assembly_metadata.binding_attestation != envelope.binding_attestation:
            return "BINDING_MISMATCH"
        if assembly_metadata.provider_profile_id != PROVIDER_PROFILE_ID:
            return "PROVIDER_PROFILE_MISMATCH"
        if assembly_metadata.serializer_version != SERIALIZER_VERSION:
            return "SERIALIZER_VERSION_MISMATCH"
        if assembly_metadata.tokenizer_version != TOKENIZER_VERSION:
            return "TOKENIZER_VERSION_MISMATCH"
        if assembly_metadata.assembly_policy_version != f"{ASSEMBLY_POLICY_VERSION}:{EVICTION_POLICY_VERSION}":
            return "ASSEMBLY_POLICY_VERSION_MISMATCH"
        return None

    @staticmethod
    def _result(
        decision: GroundingDecision,
        reason: str,
        checked_versions: dict[str, str],
        citation_count: int,
    ) -> GroundingResult:
        return GroundingResult(
            decision=decision,
            reason_codes=(reason,),
            checked_policy_versions=checked_versions,
            checked_citation_count=citation_count,
        )


grounding_layer = DeterministicGroundingLayer()
