from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from statistics import median
from typing import Any, Callable

import h3
from sqlalchemy.orm import Session

from app.api.schemas.copilot_tools import (
    ComparableToolItem,
    ComparableToolRequest,
    ComparableToolResponse,
    ExplainabilityToolRequest,
    ExplainabilityToolResponse,
    FairnessToolRequest,
    FairnessToolResponse,
    FeatureChange,
    FeatureChanges,
    BrokerTalkingPoint,
    InvestmentFinding,
    InvestmentNegotiationSummary,
    InvestmentToolRequest,
    InvestmentToolResponse,
    InvestmentWhatIfSummary,
    MarketInsightComparableDensity,
    MarketInsightConfidenceDistribution,
    MarketInsightEvidenceSummary,
    MarketInsightFairValueDistribution,
    MarketInsightSegment,
    MarketInsightStatement,
    MarketInsightToolRequest,
    MarketInsightToolResponse,
    NegotiationComparableSummary,
    NegotiationEvidenceReference,
    NegotiationEvidenceSummary,
    NegotiationToolRequest,
    NegotiationToolResponse,
    NegotiationWhatIfSummary,
    RecommendedOfferBand,
    ValuationToolRequest,
    ValuationToolResponse,
    WhatIfToolRequest,
    WhatIfToolResponse,
)
from app.api.schemas.pricing import RentFairPriceRequest, RentFairPriceResponse
from app.models.copilot import (
    PredictionLog,
    PropertyState,
    ScenarioState,
    ShadowLog,
    ToolEvent,
    ValuationSnapshot,
    Workspace,
)
from app.services.copilot_service import CopilotService
from app.services.monitoring_service import execute_shadow_pipeline, log_prediction
from app.services.router_service import price_listing_router

Router = Callable[..., RentFairPriceResponse]
_LOCATION_FIELDS = {"address", "canonical_entity_id", "lat", "lng", "location_mode"}
_ALIASES = {
    "area": "size_sqm",
    "size": "size_sqm",
    "location": "address",
    "furnished": "furnishing_status",
    "furnishing": "furnishing_status",
    "finishing": "building_quality",
}
_AMENITY_TOGGLE_FIELDS = {"parking": "CP", "gym": "SY", "clubhouse": "CH"}
_AMENITY_DISPLAY_NAMES = {"CP": "Parking", "SY": "Gym", "CH": "Clubhouse"}
_FEATURE_DISPLAY_NAMES = {
    "address": "Location",
    "bathrooms": "Bathrooms",
    "bedrooms": "Bedrooms",
    "building_quality": "Finishing",
    "canonical_entity_id": "Location",
    "compound_name": "Compound",
    "floor_number": "Floor",
    "furnishing_status": "Furnished",
    "lat": "Latitude",
    "lng": "Longitude",
    "property_category": "Property Category",
    "property_type": "Property Type",
    "size_sqm": "Size",
    "view_type": "View",
}
_ASSUMPTION_FEATURES = [
    ("furnished", "Furnished"),
    ("parking", "Parking"),
    ("gym", "Gym"),
    ("clubhouse", "Clubhouse"),
    ("finishing", "Finishing"),
]
_FAIRNESS_STATUSES = {
    "Below Fair Value": "Below Fair Value",
    "Within Fair Value": "Within Fair Value",
    "Within Fair Value Range": "Within Fair Value",
    "Above Fair Value": "Above Fair Value",
}
class ToolResourceNotFound(ValueError):
    pass


class ToolPayloadUnavailable(ValueError):
    pass


def _amenity_items(amenities: dict[str, Any]) -> list[str]:
    for key in ("items", "codes"):
        values = amenities.get(key)
        if isinstance(values, list):
            return [str(value) for value in values]
    return [str(key) for key, enabled in amenities.items() if enabled is True]


def _amenity_token(value: Any) -> str:
    text = str(value).strip()
    lowered = text.lower().replace("-", " ").replace("_", " ")
    aliases = {
        "covered parking": "CP",
        "parking": "CP",
        "garage": "CP",
        "shared gym": "SY",
        "gym": "SY",
        "fitness": "SY",
        "club house": "CH",
        "clubhouse": "CH",
    }
    return aliases.get(lowered, text.upper())


def _amenity_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        return _amenity_items(value)
    if isinstance(value, list | tuple | set):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value]
    raise ValueError("Amenities must be supplied as a list, set, tuple, string, or object")


class CopilotToolsService:
    def __init__(self, db: Session, router: Router = price_listing_router):
        self.db = db
        self.router = router
        self.copilot = CopilotService(db)

    def _workspace(self, user_id: int, workspace_id: int) -> Workspace:
        workspace = self.copilot.get_workspace(user_id, workspace_id)
        if workspace is None:
            raise ToolResourceNotFound("Workspace not found")
        return workspace

    def _property(self, user_id: int, workspace_id: int, property_id: int) -> PropertyState:
        prop = self.copilot.get_property_state(user_id, property_id)
        if prop is None or prop.workspace_id != workspace_id:
            raise ToolResourceNotFound("Property not found")
        return prop

    def _scenario(
        self, user_id: int, workspace_id: int, property_id: int, scenario_id: int | None
    ) -> ScenarioState | None:
        if scenario_id is None:
            return None
        scenario = self.copilot.get_scenario_state(user_id, scenario_id)
        if scenario is None or scenario.workspace_id != workspace_id or scenario.property_state_id != property_id:
            raise ToolResourceNotFound("Scenario not found")
        return scenario

    def _normalize_modifications(self, modifications: dict[str, Any], *, strict: bool) -> dict[str, Any]:
        normalized: dict[str, Any] = {}
        nested = modifications.get("valuation_inputs")
        if nested is not None and not isinstance(nested, dict):
            raise ValueError("valuation_inputs modifications must be an object")

        for raw_key, value in modifications.items():
            if raw_key == "valuation_inputs":
                continue
            key = _ALIASES.get(raw_key, raw_key)
            if key in _AMENITY_TOGGLE_FIELDS:
                if isinstance(value, bool):
                    normalized[key] = value
                elif strict:
                    raise ValueError(f"{raw_key} must be true or false")
                continue
            if key in {"amenities", "amenities_added", "amenities_removed"}:
                normalized[key] = _amenity_values(value)
                continue
            if key == "furnishing_status" and isinstance(value, bool):
                normalized[key] = "furnished" if value else "unfurnished"
                continue
            if key == "target_price_egp" and strict:
                raise ValueError("target_price_egp is evaluated by the Fairness Tool and cannot be a what-if modification")
            if key not in RentFairPriceRequest.model_fields:
                if strict:
                    raise ValueError(f"Unsupported what-if modification: {raw_key}")
                continue
            normalized[key] = value

        if nested:
            normalized.update(self._normalize_modifications(nested, strict=strict))
        return normalized

    def _apply_modifications(
        self,
        payload: dict[str, Any],
        modifications: dict[str, Any],
        *,
        strict: bool = False,
    ) -> dict[str, Any]:
        normalized = self._normalize_modifications(modifications, strict=strict)

        amenity_changes = any(
            key in normalized for key in {"amenities", "amenities_added", "amenities_removed", *_AMENITY_TOGGLE_FIELDS}
        )
        if amenity_changes:
            current = {
                _amenity_token(value): str(value)
                for value in _amenity_values(normalized.get("amenities", payload.get("amenities", [])))
            }
            for value in normalized.get("amenities_removed", []):
                current.pop(_amenity_token(value), None)
            for value in normalized.get("amenities_added", []):
                current[_amenity_token(value)] = _amenity_token(value)
            for key, symbol in _AMENITY_TOGGLE_FIELDS.items():
                if normalized.get(key) is True:
                    current[symbol] = symbol
                elif normalized.get(key) is False:
                    current.pop(symbol, None)
            payload["amenities"] = [current[key] for key in sorted(current)]

        for key, value in normalized.items():
            if key in {"amenities", "amenities_added", "amenities_removed", *_AMENITY_TOGGLE_FIELDS}:
                continue
            if key == "address":
                for location_key in _LOCATION_FIELDS:
                    payload.pop(location_key, None)
            elif key in {"lat", "lng", "canonical_entity_id"}:
                payload.pop("address", None)
                if key != "canonical_entity_id":
                    payload.pop("canonical_entity_id", None)
            payload[key] = value
        return normalized

    def _router_request(
        self,
        user_id: int,
        prop: PropertyState,
        scenario: ScenarioState | None,
        *,
        target_price_egp: int | None = None,
        sandbox_modifications: dict[str, Any] | None = None,
    ) -> tuple[RentFairPriceRequest, list[int]]:
        payload = dict(prop.valuation_inputs or {})
        payload.setdefault("property_type", prop.property_type)
        payload.setdefault("property_category", prop.property_category)
        payload.setdefault("size_sqm", float(prop.area))
        payload.setdefault("bedrooms", prop.bedrooms)
        payload.setdefault("bathrooms", prop.bathrooms)
        payload.setdefault("amenities", _amenity_items(prop.amenities))
        if not any(payload.get(key) is not None for key in _LOCATION_FIELDS):
            payload["address"] = prop.location

        scenario_lineage: list[int] = []
        if scenario is not None:
            for item in self.copilot.get_scenario_lineage(user_id, scenario.id):
                scenario_lineage.append(item.id)
                self._apply_modifications(payload, item.modifications)
        if sandbox_modifications is not None:
            self._apply_modifications(payload, sandbox_modifications)
        if target_price_egp is not None:
            payload["target_price_egp"] = target_price_egp
        return RentFairPriceRequest.model_validate(payload), scenario_lineage

    def _modification_sources(
        self,
        user_id: int,
        scenario: ScenarioState | None,
        sandbox_modifications: dict[str, Any],
    ) -> list[dict[str, Any]]:
        sources = []
        if scenario is not None:
            sources.extend(item.modifications for item in self.copilot.get_scenario_lineage(user_id, scenario.id))
        sources.append(sandbox_modifications)
        return sources

    def _assumptions_used(
        self,
        user_id: int,
        scenario: ScenarioState | None,
        sandbox_request: RentFairPriceRequest,
        sandbox_modifications: dict[str, Any],
    ) -> list[str]:
        amenities = {_amenity_token(value) for value in sandbox_request.amenities}
        known = set()
        if sandbox_request.furnishing_status is not None or "FU" in amenities:
            known.add("furnished")
        if sandbox_request.building_quality is not None or "FN" in amenities:
            known.add("finishing")
        for feature, symbol in _AMENITY_TOGGLE_FIELDS.items():
            if symbol in amenities:
                known.add(feature)

        for source in self._modification_sources(user_id, scenario, sandbox_modifications):
            normalized = self._normalize_modifications(source, strict=False)
            if "furnishing_status" in normalized:
                known.add("furnished")
            if "building_quality" in normalized:
                known.add("finishing")
            for feature in _AMENITY_TOGGLE_FIELDS:
                if feature in normalized:
                    known.add(feature)
            for key in ("amenities_added", "amenities_removed"):
                for value in normalized.get(key, []):
                    token = _amenity_token(value)
                    for feature, symbol in _AMENITY_TOGGLE_FIELDS.items():
                        if token == symbol:
                            known.add(feature)

        return [f"{label} = Unknown" for feature, label in _ASSUMPTION_FEATURES if feature not in known]

    def _feature_changes(
        self,
        base_request: RentFairPriceRequest,
        sandbox_request: RentFairPriceRequest,
    ) -> FeatureChanges:
        base = base_request.model_dump(mode="json")
        sandbox = sandbox_request.model_dump(mode="json")
        added: list[FeatureChange] = []
        removed: list[FeatureChange] = []
        modified: list[FeatureChange] = []

        base_amenities = {_amenity_token(value) for value in base.get("amenities", [])}
        sandbox_amenities = {_amenity_token(value) for value in sandbox.get("amenities", [])}
        for symbol in sorted(sandbox_amenities - base_amenities):
            added.append(
                FeatureChange(
                    feature=_AMENITY_DISPLAY_NAMES.get(symbol, symbol.replace("_", " ").title()),
                    before=False,
                    after=True,
                )
            )
        for symbol in sorted(base_amenities - sandbox_amenities):
            removed.append(
                FeatureChange(
                    feature=_AMENITY_DISPLAY_NAMES.get(symbol, symbol.replace("_", " ").title()),
                    before=True,
                    after=False,
                )
            )

        ignored = {"amenities", "location_mode", "target_price_egp"}
        for key in sorted(set(base) | set(sandbox)):
            if key in ignored or base.get(key) == sandbox.get(key):
                continue
            change = FeatureChange(
                feature=_FEATURE_DISPLAY_NAMES.get(key, key.replace("_", " ").title()),
                before=base.get(key),
                after=sandbox.get(key),
                unit="sqm" if key == "size_sqm" else None,
            )
            if base.get(key) is None:
                added.append(change)
            elif sandbox.get(key) is None:
                removed.append(change)
            else:
                modified.append(change)
        return FeatureChanges(added=added, removed=removed, modified=modified)

    def _snapshot(self, user_id: int, workspace_id: int, valuation_id: str) -> ValuationSnapshot:
        snapshot = (
            self.db.query(ValuationSnapshot)
            .filter(
                ValuationSnapshot.valuation_id == valuation_id,
                ValuationSnapshot.user_id == user_id,
                ValuationSnapshot.workspace_id == workspace_id,
            )
            .first()
        )
        if snapshot is None:
            raise ToolResourceNotFound("Valuation not found")
        return snapshot

    def _explainability_payload(self, snapshot: ValuationSnapshot) -> dict[str, Any]:
        if snapshot.explainability_payload is None:
            raise ToolPayloadUnavailable("Explainability payload is unavailable for this valuation")
        return snapshot.explainability_payload

    def _event(
        self,
        *,
        user_id: int,
        workspace_id: int,
        property_id: int | None,
        scenario_id: int | None,
        tool_name: str,
        request: dict[str, Any],
        response: dict[str, Any],
    ) -> ToolEvent:
        event = ToolEvent(
            user_id=user_id,
            workspace_id=workspace_id,
            property_state_id=property_id,
            scenario_state_id=scenario_id,
            tool_name=tool_name,
            event_type="executed",
            payload={"request": request, "response": response},
        )
        self.db.add(event)
        return event

    def _persist_truth_layer_monitoring(
        self,
        request: RentFairPriceRequest,
        response: RentFairPriceResponse,
        valuation_id: str,
    ) -> None:
        if self.router is not price_listing_router:
            return
        log_prediction(self.db, request, response, valuation_id)
        execute_shadow_pipeline(request, response, valuation_id)

    def execute_valuation(
        self,
        user_id: int,
        data: ValuationToolRequest,
        *,
        target_price_egp: int | None = None,
        sandbox_modifications: dict[str, Any] | None = None,
    ) -> ValuationToolResponse:
        self._workspace(user_id, data.workspace_id)
        prop = self._property(user_id, data.workspace_id, data.property_id)
        scenario = self._scenario(user_id, data.workspace_id, prop.id, data.scenario_id)
        request, scenario_lineage = self._router_request(
            user_id,
            prop,
            scenario,
            target_price_egp=target_price_egp,
            sandbox_modifications=sandbox_modifications,
        )
        valuation_id = f"val_{uuid.uuid4().hex}"
        truth = self.router(request, self.db, request_id=valuation_id)

        snapshot = ValuationSnapshot(
            valuation_id=valuation_id,
            user_id=user_id,
            workspace_id=data.workspace_id,
            property_state_id=prop.id,
            scenario_state_id=scenario.id if scenario else None,
            router_request=request.model_dump(mode="json"),
            normalized_response={},
            explainability_payload=truth.explainability.model_dump(mode="json") if truth.explainability else None,
        )
        self.db.add(snapshot)
        self.db.flush()
        response = ValuationToolResponse(
            valuation_id=valuation_id,
            fair_price=truth.fair_price_egp,
            price_range={"low": truth.range_low_egp, "high": truth.range_high_egp},
            confidence_level=str(truth.confidence.label),
            engine_used=truth.engine_used,
            routing_reason=truth.routing_reason,
            timestamp=snapshot.created_at,
        )
        normalized = response.model_dump(mode="json")
        snapshot.normalized_response = normalized
        self._event(
            user_id=user_id,
            workspace_id=data.workspace_id,
            property_id=prop.id,
            scenario_id=scenario.id if scenario else None,
            tool_name="valuation",
            request={
                **data.model_dump(mode="json"),
                "scenario_lineage": scenario_lineage,
                "router_request": request.model_dump(mode="json"),
                **({"sandbox_modifications": sandbox_modifications} if sandbox_modifications is not None else {}),
            },
            response=normalized,
        )
        self.db.commit()
        self._persist_truth_layer_monitoring(request, truth, valuation_id)
        return response

    def execute_explainability(self, user_id: int, data: ExplainabilityToolRequest) -> ExplainabilityToolResponse:
        self._workspace(user_id, data.workspace_id)
        snapshot = self._snapshot(user_id, data.workspace_id, data.valuation_id)
        payload = self._explainability_payload(snapshot)

        narrative = payload["narrative_explanation"]
        response = ExplainabilityToolResponse(
            valuation_id=snapshot.valuation_id,
            summary=narrative["summary"],
            why_this_price=narrative["why_this_price"],
            strongest_factors=narrative["strongest_factors"],
            confidence_reason=narrative["confidence_reason"],
            fairness_status=payload["fairness_explanation"]["status"],
            feature_drivers=payload["feature_drivers"],
            comparable_evidence=payload["comparable_evidence"],
            timestamp=snapshot.created_at,
        )
        normalized = response.model_dump(mode="json")
        self._event(
            user_id=user_id,
            workspace_id=snapshot.workspace_id,
            property_id=snapshot.property_state_id,
            scenario_id=snapshot.scenario_state_id,
            tool_name="explainability",
            request=data.model_dump(mode="json"),
            response=normalized,
        )
        self.db.commit()
        return response

    def execute_comparable(self, user_id: int, data: ComparableToolRequest) -> ComparableToolResponse:
        self._workspace(user_id, data.workspace_id)
        prop = self._property(user_id, data.workspace_id, data.property_id)
        scenario = self._scenario(user_id, data.workspace_id, prop.id, data.scenario_id)

        if data.valuation_id is None:
            valuation = self.execute_valuation(
                user_id,
                ValuationToolRequest(
                    workspace_id=data.workspace_id,
                    property_id=prop.id,
                    scenario_id=scenario.id if scenario else None,
                ),
            )
            snapshot = self._snapshot(user_id, data.workspace_id, valuation.valuation_id)
        else:
            snapshot = self._snapshot(user_id, data.workspace_id, data.valuation_id)
            expected_scenario_id = scenario.id if scenario else None
            if snapshot.property_state_id != prop.id or snapshot.scenario_state_id != expected_scenario_id:
                raise ToolResourceNotFound("Valuation not found")

        payload = self._explainability_payload(snapshot)
        comparables = [
            ComparableToolItem(
                comparable_id=item["property_id"],
                price=item["price"],
                size_sqm=item["size_sqm"],
                bedrooms=item["bedrooms"],
                bathrooms=item["bathrooms"],
                compound_name=item.get("compound_name"),
                distance_km=item["distance_km"],
                similarity_reason=item.get("similarity_reason"),
            )
            for item in payload.get("comparable_evidence", [])
        ]
        response = ComparableToolResponse(
            valuation_id=snapshot.valuation_id,
            comparable_count=len(comparables),
            comparables=comparables,
            timestamp=snapshot.created_at,
        )
        normalized = response.model_dump(mode="json")
        self._event(
            user_id=user_id,
            workspace_id=data.workspace_id,
            property_id=prop.id,
            scenario_id=scenario.id if scenario else None,
            tool_name="comparable",
            request=data.model_dump(mode="json"),
            response=normalized,
        )
        self.db.commit()
        return response

    def execute_fairness(
        self,
        user_id: int,
        data: FairnessToolRequest,
        *,
        sandbox_modifications: dict[str, Any] | None = None,
        valuation_id: str | None = None,
    ) -> FairnessToolResponse:
        self._workspace(user_id, data.workspace_id)
        prop = self._property(user_id, data.workspace_id, data.property_id)
        scenario = self._scenario(user_id, data.workspace_id, prop.id, data.scenario_id)
        if valuation_id is None:
            valuation = self.execute_valuation(
                user_id,
                ValuationToolRequest(
                    workspace_id=data.workspace_id,
                    property_id=prop.id,
                    scenario_id=scenario.id if scenario else None,
                ),
                target_price_egp=data.target_price_egp,
                sandbox_modifications=sandbox_modifications,
            )
            snapshot = self._snapshot(user_id, data.workspace_id, valuation.valuation_id)
        else:
            snapshot = self._snapshot(user_id, data.workspace_id, valuation_id)
            expected_scenario_id = scenario.id if scenario else None
            if snapshot.property_state_id != prop.id or snapshot.scenario_state_id != expected_scenario_id:
                raise ToolResourceNotFound("Valuation not found")
        payload = self._explainability_payload(snapshot)
        fairness = payload["fairness_explanation"]
        confidence = payload["confidence_explanation"]
        status = _FAIRNESS_STATUSES.get(fairness["status"])
        if status is None or fairness.get("asking_price") != data.target_price_egp:
            raise ToolPayloadUnavailable("Fairness payload is unavailable for this valuation")

        response = FairnessToolResponse(
            valuation_id=snapshot.valuation_id,
            fair_price=fairness["estimated_value"],
            target_price=fairness["asking_price"],
            fairness_status=status,
            confidence_level=confidence["confidence_level"],
            confidence_reason=confidence["confidence_reason"],
            timestamp=snapshot.created_at,
        )
        normalized = response.model_dump(mode="json")
        self._event(
            user_id=user_id,
            workspace_id=data.workspace_id,
            property_id=prop.id,
            scenario_id=scenario.id if scenario else None,
            tool_name="fairness",
            request=data.model_dump(mode="json"),
            response=normalized,
        )
        self.db.commit()
        return response

    def _negotiation_reference(
        self,
        source_tool: str,
        field: str,
        *,
        valuation_id: str | None = None,
        comparable_id: str | None = None,
    ) -> NegotiationEvidenceReference:
        return NegotiationEvidenceReference(
            source_tool=source_tool,
            valuation_id=valuation_id,
            field=field,
            comparable_id=comparable_id,
        )

    def _recommended_offer_band(
        self,
        *,
        valuation_id: str,
        fair_price: int,
        fairness_status: str,
        comparables: ComparableToolResponse,
    ) -> RecommendedOfferBand:
        fair_price_reference = self._negotiation_reference(
            "valuation",
            "fair_price",
            valuation_id=valuation_id,
        )
        fairness_reference = self._negotiation_reference(
            "fairness",
            "fairness_status",
            valuation_id=valuation_id,
        )
        if fairness_status == "Below Fair Value":
            return RecommendedOfferBand(
                derivation=(
                    "No numeric counter-offer band is emitted because the TruthLayer fairness status is "
                    "Below Fair Value. Creating a discount below the asking price would invent a number."
                ),
                evidence=[fair_price_reference, fairness_reference],
            )
        if fairness_status == "Within Fair Value":
            return RecommendedOfferBand(
                low=fair_price,
                high=fair_price,
                derivation=(
                    "The asking price is Within Fair Value, so both endpoints reuse the authoritative "
                    "TruthLayer fair_price without creating a discount."
                ),
                evidence=[fair_price_reference, fairness_reference],
            )

        supported = [item for item in comparables.comparables if item.price <= fair_price]
        if not supported:
            return RecommendedOfferBand(
                low=fair_price,
                high=fair_price,
                derivation=(
                    "The asking price is Above Fair Value and no returned comparable price is at or below "
                    "fair_price. Both endpoints reuse the authoritative TruthLayer fair_price."
                ),
                evidence=[fair_price_reference, fairness_reference],
            )

        closest_lower_comparable = max(supported, key=lambda item: (item.price, item.comparable_id))
        return RecommendedOfferBand(
            low=closest_lower_comparable.price,
            high=fair_price,
            derivation=(
                "The asking price is Above Fair Value. The low endpoint is the highest returned comparable "
                "price at or below fair_price; the high endpoint is the authoritative TruthLayer fair_price."
            ),
            comparable_ids_used=[closest_lower_comparable.comparable_id],
            evidence=[
                fair_price_reference,
                fairness_reference,
                self._negotiation_reference(
                    "comparable",
                    "comparables[].price",
                    valuation_id=valuation_id,
                    comparable_id=closest_lower_comparable.comparable_id,
                ),
            ],
        )

    def _negotiation_position(
        self,
        *,
        valuation_id: str,
        asking_price: int,
        fair_price: int,
        fairness_status: str,
        comparables: ComparableToolResponse,
    ) -> tuple[str, str, list[NegotiationEvidenceReference]]:
        fair_price_reference = self._negotiation_reference(
            "valuation",
            "fair_price",
            valuation_id=valuation_id,
        )
        fairness_reference = self._negotiation_reference(
            "fairness",
            "fairness_status",
            valuation_id=valuation_id,
        )
        references = [fair_price_reference, fairness_reference]
        if fairness_status == "Below Fair Value":
            return (
                "Strong Buy Opportunity",
                "TruthLayer classifies the asking price as Below Fair Value.",
                references,
            )
        if fairness_status == "Above Fair Value":
            return (
                "Overpriced",
                "TruthLayer classifies the asking price as Above Fair Value.",
                references,
            )
        if asking_price <= fair_price:
            return (
                "Fair Market Position",
                "TruthLayer classifies the asking price as Within Fair Value and it does not exceed fair_price.",
                references,
            )

        supporting_comparables = [item for item in comparables.comparables if item.price >= asking_price]
        if supporting_comparables:
            supported = min(supporting_comparables, key=lambda item: (item.price, item.comparable_id))
            return (
                "Premium Justified",
                (
                    "TruthLayer classifies the asking price as Within Fair Value and returned a comparable "
                    "price at or above the asking price."
                ),
                [
                    *references,
                    self._negotiation_reference(
                        "comparable",
                        "comparables[].price",
                        valuation_id=valuation_id,
                        comparable_id=supported.comparable_id,
                    ),
                ],
            )
        return (
            "Negotiation Recommended",
            (
                "TruthLayer classifies the asking price as Within Fair Value, but the asking price exceeds "
                "fair_price and no returned comparable price reaches the asking price."
            ),
            [
                *references,
                self._negotiation_reference(
                    "comparable",
                    "comparables[].price",
                    valuation_id=valuation_id,
                ),
            ],
        )

    def _what_if_summary(self, what_if: WhatIfToolResponse) -> NegotiationWhatIfSummary:
        return NegotiationWhatIfSummary(
            base_valuation=what_if.base_valuation,
            scenario_valuation=what_if.scenario_valuation,
            base_valuation_id=what_if.base_valuation_id,
            scenario_valuation_id=what_if.scenario_valuation_id,
            delta_value=what_if.delta_value,
            delta_percentage=what_if.delta_percentage,
            fairness_status=what_if.fairness_status,
            assumptions_used=what_if.assumptions_used,
            feature_changes=what_if.feature_changes,
        )

    def _broker_talking_points(
        self,
        *,
        valuation_id: str,
        asking_price: int,
        fair_price: int,
        price_gap: int,
        price_gap_percentage: float,
        explanation: ExplainabilityToolResponse,
        comparables: ComparableToolResponse,
        what_if: NegotiationWhatIfSummary | None,
    ) -> list[BrokerTalkingPoint]:
        gap_references = [
            self._negotiation_reference("input", "asking_price_egp"),
            self._negotiation_reference("valuation", "fair_price", valuation_id=valuation_id),
            self._negotiation_reference("fairness", "fairness_status", valuation_id=valuation_id),
        ]
        if price_gap > 0:
            gap_text = (
                f"Asking price exceeds the TruthLayer fair price by {price_gap:,} EGP "
                f"({price_gap_percentage:.2f}%)."
            )
        elif price_gap < 0:
            gap_text = (
                f"Asking price is below the TruthLayer fair price by {abs(price_gap):,} EGP "
                f"({abs(price_gap_percentage):.2f}%)."
            )
        else:
            gap_text = "Asking price matches the TruthLayer fair price."

        points = [
            BrokerTalkingPoint(text=gap_text, evidence=gap_references),
            BrokerTalkingPoint(
                text=f"TruthLayer valuation rationale: {explanation.why_this_price}",
                evidence=[
                    self._negotiation_reference(
                        "explainability",
                        "why_this_price",
                        valuation_id=valuation_id,
                    )
                ],
            ),
            BrokerTalkingPoint(
                text=f"TruthLayer strongest factors: {explanation.strongest_factors}",
                evidence=[
                    self._negotiation_reference(
                        "explainability",
                        "strongest_factors",
                        valuation_id=valuation_id,
                    )
                ],
            ),
        ]
        if comparables.comparables:
            lowest_price = min(item.price for item in comparables.comparables)
            highest_price = max(item.price for item in comparables.comparables)
            points.append(
                BrokerTalkingPoint(
                    text=(
                        f"TruthLayer returned {comparables.comparable_count} comparable properties with "
                        f"observed prices from {lowest_price:,} to {highest_price:,} EGP."
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "comparable",
                            "comparables[].price",
                            valuation_id=valuation_id,
                            comparable_id=item.comparable_id,
                        )
                        for item in comparables.comparables
                    ],
                )
            )
        else:
            points.append(
                BrokerTalkingPoint(
                    text="TruthLayer returned no comparable properties, so no comparable-backed discount is asserted.",
                    evidence=[
                        self._negotiation_reference(
                            "comparable",
                            "comparable_count",
                            valuation_id=valuation_id,
                        )
                    ],
                )
            )
        if what_if is not None:
            points.append(
                BrokerTalkingPoint(
                    text=(
                        "Optional What-if sensitivity changes the TruthLayer fair price by "
                        f"{what_if.delta_value:,} EGP ({what_if.delta_percentage:.2f}%)."
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "what_if",
                            "delta_value",
                            valuation_id=what_if.scenario_valuation_id,
                        ),
                        self._negotiation_reference(
                            "what_if",
                            "delta_percentage",
                            valuation_id=what_if.scenario_valuation_id,
                        ),
                    ],
                )
            )
        return points

    def _risk_notes(
        self,
        *,
        valuation_id: str,
        confidence_level: str,
        confidence_reason: str,
        comparables: ComparableToolResponse,
        what_if: NegotiationWhatIfSummary | None,
    ) -> list[BrokerTalkingPoint]:
        notes = [
            BrokerTalkingPoint(
                text=f"TruthLayer confidence is {confidence_level}: {confidence_reason}",
                evidence=[
                    self._negotiation_reference(
                        "fairness",
                        "confidence_level",
                        valuation_id=valuation_id,
                    ),
                    self._negotiation_reference(
                        "fairness",
                        "confidence_reason",
                        valuation_id=valuation_id,
                    ),
                ],
            )
        ]
        if comparables.comparable_count:
            notes.append(
                BrokerTalkingPoint(
                    text=(
                        "Comparable support is limited to the "
                        f"{comparables.comparable_count} properties returned by TruthLayer for this valuation snapshot."
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "comparable",
                            "comparable_count",
                            valuation_id=valuation_id,
                        )
                    ],
                )
            )
        else:
            notes.append(
                BrokerTalkingPoint(
                    text=(
                        "TruthLayer returned no comparable properties, so the offer band can only reuse fair_price "
                        "and must not be presented as comparable-backed."
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "valuation",
                            "fair_price",
                            valuation_id=valuation_id,
                        ),
                        self._negotiation_reference(
                            "comparable",
                            "comparable_count",
                            valuation_id=valuation_id,
                        ),
                    ],
                )
            )
        if what_if is not None:
            notes.append(
                BrokerTalkingPoint(
                    text=(
                        "Optional What-if output is sensitivity evidence only. It does not replace the current "
                        "TruthLayer fair-price snapshot or introduce offer-band endpoints."
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "what_if",
                            "scenario_valuation",
                            valuation_id=what_if.scenario_valuation_id,
                        ),
                        self._negotiation_reference(
                            "valuation",
                            "fair_price",
                            valuation_id=valuation_id,
                        ),
                    ],
                )
            )
        return notes

    def execute_negotiation(self, user_id: int, data: NegotiationToolRequest) -> NegotiationToolResponse:
        self._workspace(user_id, data.workspace_id)
        prop = self._property(user_id, data.workspace_id, data.property_id)
        scenario = self._scenario(user_id, data.workspace_id, prop.id, data.scenario_id)
        tool_request = ValuationToolRequest(
            workspace_id=data.workspace_id,
            property_id=prop.id,
            scenario_id=scenario.id if scenario else None,
        )
        valuation = self.execute_valuation(
            user_id,
            tool_request,
            target_price_egp=data.asking_price_egp,
        )
        explanation = self.execute_explainability(
            user_id,
            ExplainabilityToolRequest(
                workspace_id=data.workspace_id,
                valuation_id=valuation.valuation_id,
            ),
        )
        comparables = self.execute_comparable(
            user_id,
            ComparableToolRequest(
                workspace_id=data.workspace_id,
                property_id=prop.id,
                scenario_id=scenario.id if scenario else None,
                valuation_id=valuation.valuation_id,
            ),
        )
        fairness = self.execute_fairness(
            user_id,
            FairnessToolRequest(
                workspace_id=data.workspace_id,
                property_id=prop.id,
                scenario_id=scenario.id if scenario else None,
                target_price_egp=data.asking_price_egp,
            ),
            valuation_id=valuation.valuation_id,
        )
        if fairness.fair_price != valuation.fair_price:
            raise ToolPayloadUnavailable("Fairness payload does not match the authoritative valuation")

        what_if = None
        if data.what_if_modifications is not None:
            what_if = self._what_if_summary(
                self.execute_what_if(
                    user_id,
                    WhatIfToolRequest(
                        workspace_id=data.workspace_id,
                        property_id=prop.id,
                        scenario_id=scenario.id if scenario else None,
                        modifications=data.what_if_modifications,
                    ),
                )
            )

        observed_prices = [item.price for item in comparables.comparables]
        price_gap = data.asking_price_egp - fairness.fair_price
        price_gap_percentage = round((price_gap / fairness.fair_price) * 100, 4) if fairness.fair_price else 0.0
        negotiation_position, negotiation_position_reason, negotiation_position_evidence = self._negotiation_position(
            valuation_id=valuation.valuation_id,
            asking_price=data.asking_price_egp,
            fair_price=fairness.fair_price,
            fairness_status=fairness.fairness_status,
            comparables=comparables,
        )
        response = NegotiationToolResponse(
            valuation_id=valuation.valuation_id,
            asking_price=data.asking_price_egp,
            fair_price=fairness.fair_price,
            fairness_status=fairness.fairness_status,
            price_gap=price_gap,
            price_gap_percentage=price_gap_percentage,
            confidence_level=fairness.confidence_level,
            confidence_reason=fairness.confidence_reason,
            negotiation_position=negotiation_position,
            negotiation_position_reason=negotiation_position_reason,
            negotiation_position_evidence=negotiation_position_evidence,
            broker_talking_points=self._broker_talking_points(
                valuation_id=valuation.valuation_id,
                asking_price=data.asking_price_egp,
                fair_price=fairness.fair_price,
                price_gap=price_gap,
                price_gap_percentage=price_gap_percentage,
                explanation=explanation,
                comparables=comparables,
                what_if=what_if,
            ),
            evidence_summary=NegotiationEvidenceSummary(
                valuation_id=valuation.valuation_id,
                price_range=valuation.price_range,
                explainability_summary=explanation.summary,
                why_this_price=explanation.why_this_price,
                strongest_factors=explanation.strongest_factors,
            ),
            comparable_summary=NegotiationComparableSummary(
                valuation_id=valuation.valuation_id,
                comparable_count=comparables.comparable_count,
                comparable_ids=[item.comparable_id for item in comparables.comparables],
                observed_prices=observed_prices,
                lowest_observed_price=min(observed_prices) if observed_prices else None,
                highest_observed_price=max(observed_prices) if observed_prices else None,
            ),
            recommended_offer_band=self._recommended_offer_band(
                valuation_id=valuation.valuation_id,
                fair_price=fairness.fair_price,
                fairness_status=fairness.fairness_status,
                comparables=comparables,
            ),
            risk_notes=self._risk_notes(
                valuation_id=valuation.valuation_id,
                confidence_level=fairness.confidence_level,
                confidence_reason=fairness.confidence_reason,
                comparables=comparables,
                what_if=what_if,
            ),
            what_if_analysis=what_if,
            timestamp=valuation.timestamp,
        )
        normalized = response.model_dump(mode="json")
        self._event(
            user_id=user_id,
            workspace_id=data.workspace_id,
            property_id=prop.id,
            scenario_id=scenario.id if scenario else None,
            tool_name="negotiation",
            request=data.model_dump(mode="json"),
            response=normalized,
        )
        self.db.commit()
        return response

    def _investment_position(
        self,
        negotiation: NegotiationToolResponse,
    ) -> tuple[str, str, list[NegotiationEvidenceReference]]:
        valuation_id = negotiation.valuation_id
        fairness_reference = self._negotiation_reference(
            "fairness",
            "fairness_status",
            valuation_id=valuation_id,
        )
        fair_price_reference = self._negotiation_reference(
            "valuation",
            "fair_price",
            valuation_id=valuation_id,
        )
        confidence_reference = self._negotiation_reference(
            "fairness",
            "confidence_level",
            valuation_id=valuation_id,
        )
        comparable_reference = self._negotiation_reference(
            "comparable",
            "comparable_count",
            valuation_id=valuation_id,
        )

        if negotiation.fairness_status == "Below Fair Value":
            if negotiation.confidence_level == "High" and negotiation.comparable_summary.comparable_count > 0:
                return (
                    "Strong Opportunity",
                    (
                        "TruthLayer classifies the asking price as Below Fair Value with High confidence "
                        "and returned comparable support."
                    ),
                    [fairness_reference, fair_price_reference, confidence_reference, comparable_reference],
                )
            return (
                "Moderate Opportunity",
                (
                    "TruthLayer classifies the asking price as Below Fair Value, but confidence or comparable "
                    "support is limited."
                ),
                [fairness_reference, fair_price_reference, confidence_reference, comparable_reference],
            )
        if negotiation.fairness_status == "Above Fair Value":
            return (
                "High Risk",
                "TruthLayer classifies the asking price as Above Fair Value.",
                [fairness_reference, fair_price_reference],
            )
        if negotiation.asking_price <= negotiation.fair_price:
            return (
                "Fairly Priced",
                "TruthLayer classifies the asking price as Within Fair Value and it does not exceed fair_price.",
                [fairness_reference, fair_price_reference],
            )
        return (
            "Caution",
            (
                "TruthLayer classifies the asking price as Within Fair Value, but the asking price exceeds "
                "fair_price."
            ),
            [fairness_reference, fair_price_reference],
        )

    def _investment_strengths(self, negotiation: NegotiationToolResponse) -> list[InvestmentFinding]:
        valuation_id = negotiation.valuation_id
        strengths: list[InvestmentFinding] = []
        if negotiation.fairness_status == "Below Fair Value":
            strengths.append(
                InvestmentFinding(
                    text=(
                        f"Asking price is below the TruthLayer fair price by {abs(negotiation.price_gap):,} EGP "
                        f"({abs(negotiation.price_gap_percentage):.2f}%)."
                    ),
                    evidence=[
                        self._negotiation_reference("input", "asking_price_egp"),
                        self._negotiation_reference("valuation", "fair_price", valuation_id=valuation_id),
                        self._negotiation_reference("fairness", "fairness_status", valuation_id=valuation_id),
                    ],
                )
            )
        if negotiation.comparable_summary.comparable_count >= 5:
            strengths.append(
                InvestmentFinding(
                    text=(
                        "TruthLayer returned strong comparable support with "
                        f"{negotiation.comparable_summary.comparable_count} properties."
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "comparable",
                            "comparable_count",
                            valuation_id=valuation_id,
                        )
                    ],
                )
            )
        if negotiation.confidence_level == "High":
            strengths.append(
                InvestmentFinding(
                    text=f"TruthLayer valuation confidence is High: {negotiation.confidence_reason}",
                    evidence=[
                        self._negotiation_reference(
                            "fairness",
                            "confidence_level",
                            valuation_id=valuation_id,
                        ),
                        self._negotiation_reference(
                            "fairness",
                            "confidence_reason",
                            valuation_id=valuation_id,
                        ),
                    ],
                )
            )
        if negotiation.negotiation_position in {"Strong Buy Opportunity", "Negotiation Recommended"}:
            strengths.append(
                InvestmentFinding(
                    text=f"Negotiation Tool reports: {negotiation.negotiation_position}.",
                    evidence=[
                        self._negotiation_reference(
                            "negotiation",
                            "negotiation_position",
                            valuation_id=valuation_id,
                        )
                    ],
                )
            )
        if negotiation.what_if_analysis is not None and negotiation.what_if_analysis.delta_value > 0:
            strengths.append(
                InvestmentFinding(
                    text=(
                        "Optional What-if sensitivity increases the TruthLayer fair price by "
                        f"{negotiation.what_if_analysis.delta_value:,} EGP "
                        f"({negotiation.what_if_analysis.delta_percentage:.2f}%)."
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "what_if",
                            "delta_value",
                            valuation_id=negotiation.what_if_analysis.scenario_valuation_id,
                        ),
                        self._negotiation_reference(
                            "what_if",
                            "delta_percentage",
                            valuation_id=negotiation.what_if_analysis.scenario_valuation_id,
                        ),
                    ],
                )
            )
        return strengths

    def _investment_risks(self, negotiation: NegotiationToolResponse) -> list[InvestmentFinding]:
        valuation_id = negotiation.valuation_id
        risks: list[InvestmentFinding] = []
        if negotiation.comparable_summary.comparable_count < 5:
            risks.append(
                InvestmentFinding(
                    text=(
                        "Sparse comparable evidence: TruthLayer returned "
                        f"{negotiation.comparable_summary.comparable_count} comparable properties."
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "comparable",
                            "comparable_count",
                            valuation_id=valuation_id,
                        )
                    ],
                )
            )
        if negotiation.confidence_level != "High":
            risks.append(
                InvestmentFinding(
                    text=(
                        f"Valuation confidence is {negotiation.confidence_level}: "
                        f"{negotiation.confidence_reason}"
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "fairness",
                            "confidence_level",
                            valuation_id=valuation_id,
                        ),
                        self._negotiation_reference(
                            "fairness",
                            "confidence_reason",
                            valuation_id=valuation_id,
                        ),
                    ],
                )
            )
        if negotiation.fairness_status == "Above Fair Value":
            risks.append(
                InvestmentFinding(
                    text=(
                        f"Premium asking price: asking price exceeds the TruthLayer fair price by "
                        f"{negotiation.price_gap:,} EGP ({negotiation.price_gap_percentage:.2f}%)."
                    ),
                    evidence=[
                        self._negotiation_reference("input", "asking_price_egp"),
                        self._negotiation_reference("valuation", "fair_price", valuation_id=valuation_id),
                        self._negotiation_reference("fairness", "fairness_status", valuation_id=valuation_id),
                    ],
                )
            )
        elif negotiation.fairness_status == "Within Fair Value" and negotiation.asking_price > negotiation.fair_price:
            risks.append(
                InvestmentFinding(
                    text=(
                        "Asking price remains Within Fair Value but exceeds the current TruthLayer fair_price "
                        f"by {negotiation.price_gap:,} EGP ({negotiation.price_gap_percentage:.2f}%)."
                    ),
                    evidence=[
                        self._negotiation_reference("input", "asking_price_egp"),
                        self._negotiation_reference("valuation", "fair_price", valuation_id=valuation_id),
                        self._negotiation_reference("fairness", "fairness_status", valuation_id=valuation_id),
                    ],
                )
            )
        if negotiation.what_if_analysis is not None and negotiation.what_if_analysis.delta_value <= 0:
            risks.append(
                InvestmentFinding(
                    text=(
                        "Limited scenario upside: optional What-if sensitivity does not increase the "
                        "TruthLayer fair price."
                    ),
                    evidence=[
                        self._negotiation_reference(
                            "what_if",
                            "delta_value",
                            valuation_id=negotiation.what_if_analysis.scenario_valuation_id,
                        )
                    ],
                )
            )
        risks.append(
            InvestmentFinding(
                text=(
                    "Investment assessment is limited to current TruthLayer evidence. ROI, yield, returns, "
                    "and future-price forecasts are not asserted."
                ),
                evidence=[
                    self._negotiation_reference("valuation", "fair_price", valuation_id=valuation_id),
                    self._negotiation_reference("fairness", "fairness_status", valuation_id=valuation_id),
                ],
            )
        )
        return risks

    def _investment_what_if_summary(self, negotiation: NegotiationToolResponse) -> InvestmentWhatIfSummary:
        if negotiation.what_if_analysis is None:
            return InvestmentWhatIfSummary(
                status="Insufficient Evidence",
                reason="No optional What-if Tool sensitivity request was supplied.",
                source="Insufficient Evidence",
            )
        return InvestmentWhatIfSummary(
            status="Available",
            reason="Optional What-if Tool sensitivity evidence is available.",
            analysis=negotiation.what_if_analysis,
            source="TruthLayer",
        )

    def execute_investment(self, user_id: int, data: InvestmentToolRequest) -> InvestmentToolResponse:
        self._workspace(user_id, data.workspace_id)
        prop = self._property(user_id, data.workspace_id, data.property_id)
        scenario = self._scenario(user_id, data.workspace_id, prop.id, data.scenario_id)
        negotiation = self.execute_negotiation(
            user_id,
            NegotiationToolRequest(
                workspace_id=data.workspace_id,
                property_id=prop.id,
                scenario_id=scenario.id if scenario else None,
                asking_price_egp=data.asking_price_egp,
                what_if_modifications=data.what_if_modifications,
            ),
        )
        investment_position, investment_position_reason, investment_position_evidence = self._investment_position(
            negotiation
        )
        response = InvestmentToolResponse(
            valuation_id=negotiation.valuation_id,
            asking_price=negotiation.asking_price,
            fair_price=negotiation.fair_price,
            fairness_status=negotiation.fairness_status,
            price_gap=negotiation.price_gap,
            price_gap_percentage=negotiation.price_gap_percentage,
            investment_position=investment_position,
            investment_position_reason=investment_position_reason,
            investment_position_evidence=investment_position_evidence,
            confidence_level=negotiation.confidence_level,
            confidence_reason=negotiation.confidence_reason,
            investment_summary=(
                f"{investment_position}: {investment_position_reason} "
                "This is evidence-backed opportunity analysis only; no investment return or forecast is asserted."
            ),
            strengths=self._investment_strengths(negotiation),
            risks=self._investment_risks(negotiation),
            evidence_summary=negotiation.evidence_summary,
            comparable_summary=negotiation.comparable_summary,
            negotiation_summary=InvestmentNegotiationSummary(
                negotiation_position=negotiation.negotiation_position,
                negotiation_position_reason=negotiation.negotiation_position_reason,
                recommended_offer_band=negotiation.recommended_offer_band,
                broker_talking_points=negotiation.broker_talking_points,
            ),
            what_if_summary=self._investment_what_if_summary(negotiation),
            timestamp=negotiation.timestamp,
        )
        normalized = response.model_dump(mode="json")
        self._event(
            user_id=user_id,
            workspace_id=data.workspace_id,
            property_id=prop.id,
            scenario_id=scenario.id if scenario else None,
            tool_name="investment",
            request=data.model_dump(mode="json"),
            response=normalized,
        )
        self.db.commit()
        return response

    @staticmethod
    def _market_density_level(comparable_counts: list[int]) -> str:
        if not comparable_counts:
            return "Insufficient Evidence"
        middle = float(median(comparable_counts))
        if middle >= 5:
            return "High"
        if middle >= 1:
            return "Moderate"
        return "Sparse"

    @staticmethod
    def _market_confidence_distribution(records: list[dict[str, Any]]) -> MarketInsightConfidenceDistribution:
        counts: dict[str, int] = {}
        for record in records:
            level = record["confidence_level"] or "Unknown"
            counts[level] = counts.get(level, 0) + 1
        predominant = sorted(counts, key=lambda level: (-counts[level], level))[0] if counts else None
        return MarketInsightConfidenceDistribution(
            valuation_count=len(records),
            counts=dict(sorted(counts.items())),
            predominant_level=predominant,
        )

    @staticmethod
    def _market_fair_value_distribution(records: list[dict[str, Any]]) -> MarketInsightFairValueDistribution:
        values = [record["fair_price"] for record in records if record["fair_price"] is not None]
        return MarketInsightFairValueDistribution(
            valuation_count=len(values),
            minimum_fair_value=float(min(values)) if values else None,
            median_fair_value=float(median(values)) if values else None,
            maximum_fair_value=float(max(values)) if values else None,
        )

    @classmethod
    def _market_comparable_density(cls, records: list[dict[str, Any]]) -> MarketInsightComparableDensity:
        counts = [
            record["comparable_count"]
            for record in records
            if record["comparable_count"] is not None
        ]
        measurement_sources: dict[str, int] = {}
        for record in records:
            source = record["comparable_count_source"]
            if source is not None:
                measurement_sources[source] = measurement_sources.get(source, 0) + 1
        return MarketInsightComparableDensity(
            valuation_count=len(counts),
            minimum_comparable_count=min(counts) if counts else None,
            median_comparable_count=float(median(counts)) if counts else None,
            maximum_comparable_count=max(counts) if counts else None,
            density_level=cls._market_density_level(counts),
            measurement_sources=dict(sorted(measurement_sources.items())),
        )

    @classmethod
    def _market_segments(cls, records: list[dict[str, Any]], key: str) -> list[MarketInsightSegment]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for record in records:
            name = record[key]
            if name:
                grouped.setdefault(name, []).append(record)

        segments = []
        for name, items in grouped.items():
            fair_prices = [item["fair_price"] for item in items if item["fair_price"] is not None]
            comparable_counts = [
                item["comparable_count"]
                for item in items
                if item["comparable_count"] is not None
            ]
            confidence = cls._market_confidence_distribution(items)
            if fair_prices:
                segments.append(
                    MarketInsightSegment(
                        name=name,
                        valuation_count=len(items),
                        median_fair_value=float(median(fair_prices)),
                        confidence_distribution=confidence.counts,
                        comparable_density=cls._market_density_level(comparable_counts),
                        median_comparable_count=(
                            float(median(comparable_counts)) if comparable_counts else None
                        ),
                    )
                )
        return sorted(segments, key=lambda item: (-item.valuation_count, item.name.casefold()))

    @staticmethod
    def _market_h3_res9(router_request: dict[str, Any]) -> str | None:
        lat = router_request.get("lat")
        lng = router_request.get("lng")
        if lat is None or lng is None:
            return None
        try:
            return h3.latlng_to_cell(float(lat), float(lng), 9)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _market_refs(records: list[dict[str, Any]], source: str) -> list[str]:
        refs = []
        for record in records[:20]:
            if source == "valuation_snapshots":
                refs.append(f"valuation_snapshots:{record['valuation_id']}")
            elif source == "prediction_logs" and record["prediction"] is not None:
                refs.append(f"prediction_logs:{record['prediction'].id}")
            elif source == "shadow_logs" and record["shadow"] is not None:
                refs.append(f"shadow_logs:{record['shadow'].id}")
            elif source == "workspace_history":
                refs.append(f"property_states:{record['property'].id}")
        if len(records) > 20:
            refs.append(f"{source}:filtered_count={len(records)}")
        return sorted(set(refs))

    def execute_market_insight(self, user_id: int, data: MarketInsightToolRequest) -> MarketInsightToolResponse:
        self._workspace(user_id, data.workspace_id)
        filters_used: dict[str, Any] = {
            "workspace_id": data.workspace_id,
            "time_window": data.time_window or "all",
        }
        if data.compound_name is not None:
            filters_used["compound_name"] = data.compound_name
        if data.h3_res9 is not None:
            filters_used["h3_res9"] = data.h3_res9
        if data.property_type is not None:
            filters_used["property_type"] = data.property_type

        query = self.db.query(ValuationSnapshot).filter(
            ValuationSnapshot.user_id == user_id,
            ValuationSnapshot.workspace_id == data.workspace_id,
        )
        if data.time_window and data.time_window != "all":
            days = int(data.time_window[:-1])
            query = query.filter(ValuationSnapshot.created_at >= datetime.now(timezone.utc) - timedelta(days=days))
        snapshots = query.order_by(ValuationSnapshot.created_at, ValuationSnapshot.valuation_id).all()
        valuation_ids = [snapshot.valuation_id for snapshot in snapshots]
        property_ids = {snapshot.property_state_id for snapshot in snapshots}
        properties = {
            prop.id: prop
            for prop in self.db.query(PropertyState)
            .filter(
                PropertyState.user_id == user_id,
                PropertyState.workspace_id == data.workspace_id,
                PropertyState.id.in_(property_ids),
            )
            .all()
        } if property_ids else {}

        predictions: dict[str, PredictionLog] = {}
        shadows: dict[str, ShadowLog] = {}
        if valuation_ids:
            for row in (
                self.db.query(PredictionLog)
                .filter(PredictionLog.request_id.in_(valuation_ids))
                .order_by(PredictionLog.created_at, PredictionLog.id)
                .all()
            ):
                predictions[row.request_id] = row
            for row in (
                self.db.query(ShadowLog)
                .filter(ShadowLog.request_id.in_(valuation_ids))
                .order_by(ShadowLog.created_at, ShadowLog.id)
                .all()
            ):
                shadows[row.request_id] = row

        records: list[dict[str, Any]] = []
        for snapshot in snapshots:
            prop = properties[snapshot.property_state_id]
            prediction = predictions.get(snapshot.valuation_id)
            shadow = shadows.get(snapshot.valuation_id)
            router_request = snapshot.router_request or {}
            explainability = snapshot.explainability_payload or {}
            comparable_evidence = explainability.get("comparable_evidence") or []
            if shadow is not None and shadow.comparable_count is not None:
                comparable_count = shadow.comparable_count
                comparable_count_source = "shadow_logs"
            else:
                comparable_count = len(comparable_evidence)
                comparable_count_source = "comparable_evidence"
            record = {
                "valuation_id": snapshot.valuation_id,
                "snapshot": snapshot,
                "property": prop,
                "prediction": prediction,
                "shadow": shadow,
                "fair_price": (snapshot.normalized_response or {}).get("fair_price"),
                "confidence_level": (snapshot.normalized_response or {}).get("confidence_level"),
                "compound_name": (
                    (prediction.compound if prediction is not None else None)
                    or (shadow.compound_name if shadow is not None else None)
                    or router_request.get("compound_name")
                ),
                "h3_res9": (
                    (prediction.h3_res9 if prediction is not None else None)
                    or (shadow.h3_res9 if shadow is not None else None)
                    or self._market_h3_res9(router_request)
                ),
                "property_type": (
                    (prediction.property_type if prediction is not None else None)
                    or router_request.get("property_type")
                    or prop.property_type
                ),
                "area_name": prop.location,
                "comparable_count": comparable_count,
                "comparable_count_source": comparable_count_source,
                "comparable_evidence_count": len(comparable_evidence),
            }
            if data.compound_name is not None and (
                not record["compound_name"]
                or record["compound_name"].casefold() != data.compound_name.casefold()
            ):
                continue
            if data.h3_res9 is not None and record["h3_res9"] != data.h3_res9:
                continue
            if data.property_type is not None and (
                not record["property_type"]
                or record["property_type"].casefold() != data.property_type.casefold()
            ):
                continue
            records.append(record)

        filtered_ids = {record["valuation_id"] for record in records}
        tool_events = (
            self.db.query(ToolEvent)
            .filter(ToolEvent.user_id == user_id, ToolEvent.workspace_id == data.workspace_id)
            .order_by(ToolEvent.id)
            .all()
        )
        relevant_events = [
            event
            for event in tool_events
            if (event.payload or {}).get("response", {}).get("valuation_id") in filtered_ids
        ]
        source_record_counts = {
            "valuation_snapshots": len(records),
            "prediction_logs": sum(record["prediction"] is not None for record in records),
            "shadow_logs": sum(record["shadow"] is not None for record in records),
            "comparable_evidence": sum(record["comparable_evidence_count"] for record in records),
            "tool_events": len(relevant_events),
            "workspace_history": len({record["property"].id for record in records}),
            "scenario_history": len({
                record["snapshot"].scenario_state_id
                for record in records
                if record["snapshot"].scenario_state_id is not None
            }),
        }
        data_sources_used = [
            "valuation_snapshots",
            "prediction_logs",
            "shadow_logs",
            "tool_events",
            "workspace_history",
        ]
        if source_record_counts["comparable_evidence"]:
            data_sources_used.append("comparable_evidence")
        if source_record_counts["scenario_history"]:
            data_sources_used.append("scenario_history")

        confidence = self._market_confidence_distribution(records)
        fair_values = self._market_fair_value_distribution(records)
        comparable_density = self._market_comparable_density(records)
        compounds = self._market_segments(records, "compound_name")
        areas = self._market_segments(records, "area_name")
        snapshot_refs = self._market_refs(records, "valuation_snapshots")
        statements: list[MarketInsightStatement] = []
        if records:
            statements.append(
                MarketInsightStatement(
                    text=f"{len(records)} persisted TruthLayer valuations match the selected filters.",
                    evidence=snapshot_refs,
                )
            )
            if fair_values.median_fair_value is not None:
                statements.append(
                    MarketInsightStatement(
                        text=(
                            "Observed fair values range from "
                            f"{fair_values.minimum_fair_value:,.0f} to {fair_values.maximum_fair_value:,.0f} EGP "
                            f"with a median of {fair_values.median_fair_value:,.0f} EGP."
                        ),
                        evidence=snapshot_refs,
                    )
                )
            if confidence.predominant_level is not None:
                statements.append(
                    MarketInsightStatement(
                        text=(
                            f"Confidence levels are predominantly {confidence.predominant_level} "
                            f"({confidence.counts[confidence.predominant_level]} of {confidence.valuation_count})."
                        ),
                        evidence=snapshot_refs,
                    )
                )
            if comparable_density.median_comparable_count is not None:
                statements.append(
                    MarketInsightStatement(
                        text=(
                            f"Comparable density is {comparable_density.density_level} with a median of "
                            f"{comparable_density.median_comparable_count:g} persisted comparables per valuation."
                        ),
                        evidence=(
                            self._market_refs(records, "shadow_logs")
                            or [f"comparable_evidence:valuation_id={record['valuation_id']}" for record in records]
                        ),
                    )
                )
            if compounds:
                statements.append(
                    MarketInsightStatement(
                        text=(
                            f"Most evaluated compound is {compounds[0].name} "
                            f"with {compounds[0].valuation_count} persisted valuations."
                        ),
                        evidence=self._market_refs(records, "prediction_logs") or snapshot_refs,
                    )
                )
            if areas:
                statements.append(
                    MarketInsightStatement(
                        text=(
                            f"Most evaluated area is {areas[0].name} "
                            f"with {areas[0].valuation_count} persisted valuations."
                        ),
                        evidence=self._market_refs(records, "workspace_history"),
                    )
                )
        else:
            statements.append(
                MarketInsightStatement(
                    text="No persisted TruthLayer valuations match the selected filters.",
                    evidence=[f"valuation_snapshots:workspace_id={data.workspace_id}"],
                )
            )

        timestamp = datetime.now(timezone.utc)
        response = MarketInsightToolResponse(
            market_summary=" ".join(statement.text for statement in statements),
            valuation_volume=len(records),
            confidence_distribution=confidence,
            fair_value_distribution=fair_values,
            comparable_density=comparable_density,
            active_compounds=compounds,
            active_areas=areas,
            evidence_summary=MarketInsightEvidenceSummary(
                valuation_ids=[record["valuation_id"] for record in records],
                source_record_counts=source_record_counts,
                filters_used=filters_used,
                statements=statements,
                traceability_note=(
                    "Descriptive analytics only. Every statement is derived from persisted tenant-scoped "
                    "TruthLayer records; no forecast or future-price assertion is generated."
                ),
            ),
            data_sources_used=data_sources_used,
            timestamp=timestamp,
        )
        normalized = response.model_dump(mode="json")
        self._event(
            user_id=user_id,
            workspace_id=data.workspace_id,
            property_id=None,
            scenario_id=None,
            tool_name="market_insight",
            request={"filters_used": filters_used, "data_sources_used": data_sources_used},
            response=normalized,
        )
        self.db.commit()
        return response

    def execute_what_if(self, user_id: int, data: WhatIfToolRequest) -> WhatIfToolResponse:
        self._workspace(user_id, data.workspace_id)
        prop = self._property(user_id, data.workspace_id, data.property_id)
        scenario = self._scenario(user_id, data.workspace_id, prop.id, data.scenario_id)
        sandbox_modifications = self._normalize_modifications(data.modifications, strict=True)
        if not sandbox_modifications:
            raise ValueError("modifications must include at least one supported property change")

        valuation_request = ValuationToolRequest(
            workspace_id=data.workspace_id,
            property_id=prop.id,
            scenario_id=scenario.id if scenario else None,
        )
        base = self.execute_valuation(user_id, valuation_request)
        sandbox = self.execute_valuation(
            user_id,
            valuation_request,
            sandbox_modifications=sandbox_modifications,
        )
        explanation = self.execute_explainability(
            user_id,
            ExplainabilityToolRequest(workspace_id=data.workspace_id, valuation_id=sandbox.valuation_id),
        )
        comparables = self.execute_comparable(
            user_id,
            ComparableToolRequest(
                workspace_id=data.workspace_id,
                property_id=prop.id,
                scenario_id=scenario.id if scenario else None,
                valuation_id=sandbox.valuation_id,
            ),
        )
        fairness = self.execute_fairness(
            user_id,
            FairnessToolRequest(
                workspace_id=data.workspace_id,
                property_id=prop.id,
                scenario_id=scenario.id if scenario else None,
                target_price_egp=base.fair_price,
            ),
            sandbox_modifications=sandbox_modifications,
        )

        base_snapshot = self._snapshot(user_id, data.workspace_id, base.valuation_id)
        sandbox_snapshot = self._snapshot(user_id, data.workspace_id, sandbox.valuation_id)
        base_request = RentFairPriceRequest.model_validate(base_snapshot.router_request)
        sandbox_request = RentFairPriceRequest.model_validate(sandbox_snapshot.router_request)
        # Delta arithmetic is explicitly permitted because both operands are authoritative TruthLayer outputs.
        delta_value = sandbox.fair_price - base.fair_price
        delta_percentage = round((delta_value / base.fair_price) * 100, 4) if base.fair_price else 0.0
        response = WhatIfToolResponse(
            base_valuation=base.fair_price,
            scenario_valuation=sandbox.fair_price,
            base_valuation_id=base.valuation_id,
            scenario_valuation_id=sandbox.valuation_id,
            fairness_valuation_id=fairness.valuation_id,
            delta_value=delta_value,
            delta_percentage=delta_percentage,
            fairness_status=fairness.fairness_status,
            confidence_level=sandbox.confidence_level,
            assumptions_used=self._assumptions_used(
                user_id,
                scenario,
                sandbox_request,
                sandbox_modifications,
            ),
            feature_changes=self._feature_changes(base_request, sandbox_request),
            explainability=explanation,
            comparables=comparables,
            timestamp=sandbox.timestamp,
        )
        normalized = response.model_dump(mode="json")
        self._event(
            user_id=user_id,
            workspace_id=data.workspace_id,
            property_id=prop.id,
            scenario_id=scenario.id if scenario else None,
            tool_name="what_if",
            request={
                **data.model_dump(mode="json"),
                "sandbox_modifications": sandbox_modifications,
            },
            response=normalized,
        )
        self.db.commit()
        return response
