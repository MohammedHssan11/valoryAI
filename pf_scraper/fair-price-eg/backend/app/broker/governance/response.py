from __future__ import annotations

import re

from app.broker.schemas.contracts import (
    BrokerAnalyticalResponse,
    BrokerContext,
    GroundingReport,
    ResponseGovernanceCheck,
    ResponseGovernanceReport,
)
from app.core.observability import metrics


_EGP_AMOUNT_RE = re.compile(r"(?<!\d)(\d{1,3}(?:,\d{3})+|\d{4,})(?:\s*)(?:EGP|egp)")


def _response_text(response: BrokerAnalyticalResponse) -> str:
    fields = [
        response.executive_summary,
        response.valuation_interpretation,
        response.comparable_reasoning,
        response.district_insights,
        response.confidence_explanation,
        response.analytical_conclusion,
        *response.opportunity_risk_notes,
    ]
    return "\n".join(item for item in fields if item)


def _egp_numbers(text: str) -> set[int]:
    values: set[int] = set()
    for match in _EGP_AMOUNT_RE.finditer(text):
        values.add(int(match.group(1).replace(",", "")))
    return values


class ResponseGovernanceLayer:
    forbidden_phrases = (
        "guaranteed return",
        "risk-free",
        "certain appreciation",
        "i estimate",
        "my valuation",
        "i value this",
    )

    def evaluate(
        self,
        *,
        context: BrokerContext,
        response: BrokerAnalyticalResponse,
        grounding: GroundingReport,
    ) -> ResponseGovernanceReport:
        checks: list[ResponseGovernanceCheck] = []
        violations: list[str] = []
        text = _response_text(response)

        self._check_grounding(grounding, checks, violations)
        self._check_forbidden_output(text, checks, violations)
        self._check_numeric_consistency(context, text, checks, violations)
        self._check_confidence_consistency(context, response, checks, violations)

        status = "failed" if violations else "passed"
        metrics.increment("broker.response_governance", {"status": status})
        metrics.record_event(
            "broker_response_governance",
            {"status": status, "violation_count": len(violations), "session_id": context.session_id},
        )
        return ResponseGovernanceReport(status=status, checks=checks, violations=violations)

    def _check_grounding(
        self,
        grounding: GroundingReport,
        checks: list[ResponseGovernanceCheck],
        violations: list[str],
    ) -> None:
        if grounding.status == "passed":
            checks.append(ResponseGovernanceCheck(name="authoritative_value_consistency", status="passed"))
            checks.append(ResponseGovernanceCheck(name="evidence_reference_consistency", status="passed"))
            return
        violations.extend(grounding.violations)
        checks.append(
            ResponseGovernanceCheck(
                name="authoritative_value_consistency",
                status="failed",
                details={"grounding_violations": grounding.violations},
            )
        )

    def _check_forbidden_output(
        self,
        text: str,
        checks: list[ResponseGovernanceCheck],
        violations: list[str],
    ) -> None:
        lowered = text.lower()
        found = [phrase for phrase in self.forbidden_phrases if phrase in lowered]
        if found:
            violations.append(f"Forbidden broker narration detected: {', '.join(found)}.")
            checks.append(ResponseGovernanceCheck(name="forbidden_output_detection", status="failed", details={"phrases": found}))
            return
        checks.append(ResponseGovernanceCheck(name="forbidden_output_detection", status="passed"))

    def _check_numeric_consistency(
        self,
        context: BrokerContext,
        text: str,
        checks: list[ResponseGovernanceCheck],
        violations: list[str],
    ) -> None:
        observed = _egp_numbers(text)
        if not observed:
            checks.append(ResponseGovernanceCheck(name="numeric_consistency", status="passed", details={"observed": []}))
            return

        allowed: set[int] = {item.price_egp for item in context.comparable_evidence}
        if context.valuation_summary is not None:
            allowed.update(
                {
                    context.valuation_summary.fair_price_egp,
                    context.valuation_summary.range_low_egp,
                    context.valuation_summary.range_high_egp,
                }
            )
        unsupported = sorted(observed - allowed)
        if unsupported:
            violations.append(f"Unsupported EGP amount(s) in broker narration: {unsupported}.")
            checks.append(
                ResponseGovernanceCheck(
                    name="numeric_consistency",
                    status="failed",
                    details={"observed": sorted(observed), "allowed": sorted(allowed), "unsupported": unsupported},
                )
            )
            return
        checks.append(
            ResponseGovernanceCheck(
                name="numeric_consistency",
                status="passed",
                details={"observed": sorted(observed), "allowed": sorted(allowed)},
            )
        )

    def _check_confidence_consistency(
        self,
        context: BrokerContext,
        response: BrokerAnalyticalResponse,
        checks: list[ResponseGovernanceCheck],
        violations: list[str],
    ) -> None:
        if context.valuation_summary is None:
            checks.append(ResponseGovernanceCheck(name="confidence_consistency", status="skipped"))
            return
        if response.authoritative_values is None:
            violations.append("Response omitted authoritative confidence values.")
            checks.append(ResponseGovernanceCheck(name="confidence_consistency", status="failed"))
            return
        expected = context.valuation_summary.confidence_label
        observed = response.authoritative_values.confidence_label
        if observed != expected:
            violations.append(f"Confidence label mismatch: expected {expected}, got {observed}.")
            checks.append(
                ResponseGovernanceCheck(
                    name="confidence_consistency",
                    status="failed",
                    details={"expected": expected, "observed": observed},
                )
            )
            return
        checks.append(ResponseGovernanceCheck(name="confidence_consistency", status="passed", details={"label": expected}))


response_governance = ResponseGovernanceLayer()
