from __future__ import annotations

from typing import Any

from app.broker.schemas.contracts import BrokerAnalyticalResponse, BrokerContext, GroundingReport
from app.core.observability import metrics


class GroundingValidator:
    def validate(self, *, context: BrokerContext, response: BrokerAnalyticalResponse) -> GroundingReport:
        violations: list[str] = []
        checked: dict[str, Any] = {}
        summary = context.valuation_summary
        authoritative = response.authoritative_values

        if summary is None and authoritative is not None:
            violations.append("Response included authoritative valuation values without deterministic context.")

        if summary is not None:
            if authoritative is None:
                violations.append("Response omitted authoritative valuation values despite deterministic context.")
            else:
                expected = {
                    "valuation_id": summary.valuation_id,
                    "fair_price_egp": summary.fair_price_egp,
                    "range_low_egp": summary.range_low_egp,
                    "range_high_egp": summary.range_high_egp,
                    "confidence_label": summary.confidence_label,
                    "engine_used": summary.engine_used,
                    "routing_reason": summary.routing_reason,
                    "source": summary.source,
                }
                observed = authoritative.model_dump(mode="json")
                checked["authoritative_values"] = observed
                for key, expected_value in expected.items():
                    if observed.get(key) != expected_value:
                        violations.append(
                            f"Authoritative value mismatch for {key}: expected {expected_value}, got {observed.get(key)}."
                        )

        evidence_ids = {item.evidence_id for item in context.evidence}
        for evidence_id in response.evidence_ids:
            if evidence_id not in evidence_ids:
                violations.append(f"Response referenced unknown evidence id {evidence_id}.")

        comp_ids = {item.listing_id for item in context.comparable_evidence}
        for listing_id in response.referenced_comp_listing_ids:
            if listing_id not in comp_ids:
                violations.append(f"Response referenced unknown comparable listing {listing_id}.")

        status = "failed" if violations else "passed"
        metrics.increment("broker.grounding_validation", {"status": status})
        return GroundingReport(status=status, violations=violations, checked_values=checked)


grounding_validator = GroundingValidator()
