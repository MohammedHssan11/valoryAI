from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.schemas.copilot import PropertyStateCreate, ScenarioStateCreate, UserCreate, WorkspaceCreate
from app.api.schemas.copilot_tools import (
    ExplainabilityToolRequest,
    InvestmentToolRequest,
    NegotiationToolRequest,
    ValuationToolRequest,
    WhatIfToolRequest,
)
from app.api.schemas.pricing import RentFairPriceResponse
from app.db.base import Base
from app.models.copilot import ToolEvent, ValuationSnapshot
from app.services.copilot_service import CopilotService
from app.services.copilot_tools_service import CopilotToolsService, ToolResourceNotFound
import app.models.copilot  # noqa: F401


def truth_router(request, db, **kwargs):
    size = int(request.size_sqm)
    low = size * 90
    high = size * 110
    if request.target_price_egp is None:
        fairness_status = "Within Fair Value Range"
    elif request.target_price_egp < low:
        fairness_status = "Below Fair Value"
    elif request.target_price_egp > high:
        fairness_status = "Above Fair Value"
    else:
        fairness_status = "Within Fair Value Range"
    return RentFairPriceResponse(
        fair_price_egp=size * 100,
        range_low_egp=low,
        range_high_egp=high,
        flag="NO_TARGET",
        tier_used=1,
        comps_count=12,
        confidence={"score": 0.8, "label": "High", "factors": {}, "dimensions": {}},
        engine_used="CMT",
        routing_reason="GoldilocksZone",
        explainability={
            "router_explanation": "CMT selected by the Router.",
            "confidence_explanation": {
                "confidence_level": "High",
                "confidence_reason": "High confidence because 12 similar properties were found.",
            },
            "fairness_explanation": {
                "estimated_value": size * 100,
                "asking_price": request.target_price_egp,
                "difference_amount": None,
                "difference_percentage": None,
                "status": fairness_status,
            },
            "narrative_explanation": {
                "summary": f"The property's fair value is {size * 100:,.0f} EGP.",
                "why_this_price": "This is based on similar nearby properties.",
                "strongest_factors": "Nearby prices anchor the valuation.",
                "confidence_reason": "High confidence because 12 similar properties were found.",
            },
            "comparable_evidence": [
                {
                    "property_id": "comp-1",
                    "price": size * 100,
                    "size_sqm": float(size),
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "furnishing_status": None,
                    "distance_km": 0.4,
                    "similarity_score": 0.9,
                    "listing_date": "Recent",
                }
            ],
            "feature_drivers": [{"name": "location", "direction": "Positive", "strength": "High"}],
        },
        explanation=["Existing truth-layer explanation."],
        area={"name": "Central Cairo"},
        resolved_location={"lat": 30.0444, "lng": 31.2357},
    )


def premium_truth_router(request, db, **kwargs):
    truth = truth_router(request, db, **kwargs)
    if request.target_price_egp is not None:
        truth.explainability.comparable_evidence.append(
            truth.explainability.comparable_evidence[0].model_copy(
                update={
                    "property_id": "comp-premium",
                    "price": request.target_price_egp,
                }
            )
        )
    return truth


def sparse_truth_router(request, db, **kwargs):
    truth = truth_router(request, db, **kwargs)
    truth.comps_count = 0
    truth.confidence = truth.confidence.model_copy(update={"score": 0.2, "label": "Low"})
    truth.explainability.confidence_explanation = truth.explainability.confidence_explanation.model_copy(
        update={
            "confidence_level": "Low",
            "confidence_reason": "Low confidence due to sparse market data.",
        }
    )
    truth.explainability.narrative_explanation = truth.explainability.narrative_explanation.model_copy(
        update={"confidence_reason": "Low confidence due to sparse market data."}
    )
    truth.explainability.comparable_evidence = []
    return truth


def test_valuation_and_explainability_tools_apply_scenario_state_and_persist_audit_events():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with factory() as db:
        copilot = CopilotService(db)
        user = copilot.create_user(UserCreate(external_subject="tool-user", display_name="Tool User"))
        other = copilot.create_user(UserCreate(external_subject="other-user", display_name="Other User"))
        workspace = copilot.create_workspace(user.id, WorkspaceCreate(name="Tool Workspace"))
        prop = copilot.create_property_state(
            user.id,
            PropertyStateCreate(
                workspace_id=workspace.id,
                label="Property A",
                location="Central Cairo",
                area=150,
                bedrooms=3,
                bathrooms=2,
                amenities={"codes": ["BA", "SE"]},
                valuation_inputs={"lat": 30.0444, "lng": 31.2357},
            ),
        )
        base = copilot.create_scenario_state(
            user.id,
            ScenarioStateCreate(property_state_id=prop.id, name="Base", modifications={"size_sqm": 160}),
        )
        scenario = copilot.create_scenario_state(
            user.id,
            ScenarioStateCreate(
                property_state_id=prop.id,
                parent_scenario_id=base.id,
                name="Expanded",
                modifications={"size_sqm": 170},
            ),
        )
        tools = CopilotToolsService(db, router=truth_router)

        base_result = tools.execute_valuation(
            user.id, ValuationToolRequest(workspace_id=workspace.id, property_id=prop.id)
        )
        scenario_result = tools.execute_valuation(
            user.id,
            ValuationToolRequest(workspace_id=workspace.id, property_id=prop.id, scenario_id=scenario.id),
        )
        explanation = tools.execute_explainability(
            user.id,
            ExplainabilityToolRequest(workspace_id=workspace.id, valuation_id=scenario_result.valuation_id),
        )

        assert base_result.fair_price == 15000
        assert scenario_result.fair_price == 17000
        assert scenario_result.source == "TruthLayer"
        assert explanation.summary == "The property's fair value is 17,000 EGP."
        assert explanation.feature_drivers[0]["name"] == "location"
        assert explanation.fairness_status == "Within Fair Value Range"
        snapshots = db.query(ValuationSnapshot).order_by(ValuationSnapshot.created_at).all()
        assert snapshots[1].router_request["size_sqm"] == 170
        events = db.query(ToolEvent).filter(ToolEvent.workspace_id == workspace.id).order_by(ToolEvent.id).all()
        assert [event.tool_name for event in events] == ["valuation", "valuation", "explainability"]
        assert events[1].payload["request"]["scenario_lineage"] == [base.id, scenario.id]
        assert "debug" not in events[1].payload["response"]

        try:
            tools.execute_valuation(
                other.id,
                ValuationToolRequest(workspace_id=workspace.id, property_id=prop.id),
            )
        except ToolResourceNotFound:
            pass
        else:
            raise AssertionError("Cross-tenant tool execution must be rejected")

    engine.dispose()


def test_negotiation_tool_orchestrates_grounded_positions_risks_and_optional_what_if():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with factory() as db:
        copilot = CopilotService(db)
        user = copilot.create_user(UserCreate(external_subject="negotiation-user", display_name="Negotiation User"))
        workspace = copilot.create_workspace(user.id, WorkspaceCreate(name="Negotiation Workspace"))
        prop = copilot.create_property_state(
            user.id,
            PropertyStateCreate(
                workspace_id=workspace.id,
                label="Property A",
                location="Central Cairo",
                area=150,
                bedrooms=3,
                bathrooms=2,
                amenities={"codes": ["BA"]},
                valuation_inputs={"lat": 30.0444, "lng": 31.2357},
            ),
        )
        tools = CopilotToolsService(db, router=truth_router)
        requests = {
            "Strong Buy Opportunity": NegotiationToolRequest(
                workspace_id=workspace.id,
                property_id=prop.id,
                asking_price_egp=13000,
            ),
            "Fair Market Position": NegotiationToolRequest(
                workspace_id=workspace.id,
                property_id=prop.id,
                asking_price_egp=15000,
            ),
            "Negotiation Recommended": NegotiationToolRequest(
                workspace_id=workspace.id,
                property_id=prop.id,
                asking_price_egp=16000,
            ),
            "Overpriced": NegotiationToolRequest(
                workspace_id=workspace.id,
                property_id=prop.id,
                asking_price_egp=17000,
                what_if_modifications={"size_sqm": 180},
            ),
        }
        results = {
            expected: tools.execute_negotiation(user.id, request)
            for expected, request in requests.items()
        }
        premium = CopilotToolsService(db, router=premium_truth_router).execute_negotiation(
            user.id,
            NegotiationToolRequest(
                workspace_id=workspace.id,
                property_id=prop.id,
                asking_price_egp=16000,
            ),
        )
        events = db.query(ToolEvent).filter(ToolEvent.workspace_id == workspace.id).order_by(ToolEvent.id).all()

        assert {result.negotiation_position for result in results.values()} == set(requests)
        assert premium.negotiation_position == "Premium Justified"
        assert all(result.source == "TruthLayer" for result in [*results.values(), premium])
        assert all(result.negotiation_position_evidence for result in [*results.values(), premium])
        assert all(result.risk_notes for result in [*results.values(), premium])
        assert all(note.evidence for result in [*results.values(), premium] for note in result.risk_notes)
        assert results["Strong Buy Opportunity"].recommended_offer_band.low is None
        assert results["Strong Buy Opportunity"].recommended_offer_band.high is None
        assert results["Overpriced"].recommended_offer_band.low == 15000
        assert results["Overpriced"].recommended_offer_band.high == 15000
        assert results["Overpriced"].what_if_analysis is not None
        assert results["Overpriced"].what_if_analysis.scenario_valuation == 18000
        assert results["Overpriced"].what_if_analysis.delta_value == 3000
        assert any(
            reference.source_tool == "what_if"
            for point in results["Overpriced"].broker_talking_points
            for reference in point.evidence
        )
        audit = next(
            event
            for event in events
            if event.tool_name == "negotiation"
            and event.payload["response"]["valuation_id"] == results["Overpriced"].valuation_id
        )
        assert audit.payload["request"]["asking_price_egp"] == 17000
        assert audit.payload["request"]["what_if_modifications"] == {"size_sqm": 180}
        assert audit.payload["response"]["fairness_status"] == "Above Fair Value"
        assert audit.payload["response"]["negotiation_position"] == "Overpriced"
        assert audit.payload["response"]["what_if_analysis"]["delta_value"] == 3000

    engine.dispose()


def test_investment_tool_orchestrates_grounded_positions_strengths_risks_and_optional_what_if():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with factory() as db:
        copilot = CopilotService(db)
        user = copilot.create_user(UserCreate(external_subject="investment-user", display_name="Investment User"))
        other = copilot.create_user(UserCreate(external_subject="investment-other", display_name="Investment Other"))
        workspace = copilot.create_workspace(user.id, WorkspaceCreate(name="Investment Workspace"))
        prop = copilot.create_property_state(
            user.id,
            PropertyStateCreate(
                workspace_id=workspace.id,
                label="Property A",
                location="Central Cairo",
                area=150,
                bedrooms=3,
                bathrooms=2,
                amenities={"codes": ["BA"]},
                valuation_inputs={"lat": 30.0444, "lng": 31.2357},
            ),
        )
        scenario = copilot.create_scenario_state(
            user.id,
            ScenarioStateCreate(property_state_id=prop.id, name="Expanded", modifications={"size_sqm": 160}),
        )
        tools = CopilotToolsService(db, router=truth_router)
        results = {
            "Strong Opportunity": tools.execute_investment(
                user.id,
                InvestmentToolRequest(
                    workspace_id=workspace.id,
                    property_id=prop.id,
                    asking_price_egp=13000,
                ),
            ),
            "Fairly Priced": tools.execute_investment(
                user.id,
                InvestmentToolRequest(
                    workspace_id=workspace.id,
                    property_id=prop.id,
                    asking_price_egp=15000,
                ),
            ),
            "Caution": tools.execute_investment(
                user.id,
                InvestmentToolRequest(
                    workspace_id=workspace.id,
                    property_id=prop.id,
                    asking_price_egp=16000,
                ),
            ),
            "High Risk": tools.execute_investment(
                user.id,
                InvestmentToolRequest(
                    workspace_id=workspace.id,
                    property_id=prop.id,
                    scenario_id=scenario.id,
                    asking_price_egp=18000,
                    what_if_modifications={"size_sqm": 180},
                ),
            ),
        }
        moderate = CopilotToolsService(db, router=sparse_truth_router).execute_investment(
            user.id,
            InvestmentToolRequest(
                workspace_id=workspace.id,
                property_id=prop.id,
                asking_price_egp=13000,
            ),
        )
        events = db.query(ToolEvent).filter(ToolEvent.workspace_id == workspace.id).order_by(ToolEvent.id).all()

        assert {result.investment_position for result in results.values()} == set(results)
        assert moderate.investment_position == "Moderate Opportunity"
        assert all(result.source == "TruthLayer" for result in [*results.values(), moderate])
        assert all(result.investment_position_evidence for result in [*results.values(), moderate])
        assert all(finding.evidence for result in [*results.values(), moderate] for finding in result.strengths)
        assert all(finding.evidence for result in [*results.values(), moderate] for finding in result.risks)
        assert results["Strong Opportunity"].fairness_status == "Below Fair Value"
        assert results["Fairly Priced"].fairness_status == "Within Fair Value"
        assert results["Caution"].fairness_status == "Within Fair Value"
        assert results["High Risk"].fairness_status == "Above Fair Value"
        assert results["Strong Opportunity"].what_if_summary.status == "Insufficient Evidence"
        assert results["Strong Opportunity"].what_if_summary.source == "Insufficient Evidence"
        assert results["High Risk"].what_if_summary.status == "Available"
        assert results["High Risk"].what_if_summary.source == "TruthLayer"
        assert results["High Risk"].what_if_summary.analysis is not None
        assert results["High Risk"].what_if_summary.analysis.delta_value == 2000
        assert results["High Risk"].negotiation_summary.source == "TruthLayer"
        assert results["High Risk"].price_gap == results["High Risk"].asking_price - results["High Risk"].fair_price
        assert any("ROI" in risk.text for risk in results["Strong Opportunity"].risks)
        audit = next(
            event
            for event in events
            if event.tool_name == "investment"
            and event.payload["response"]["valuation_id"] == results["High Risk"].valuation_id
        )
        assert audit.scenario_state_id == scenario.id
        assert audit.payload["request"]["asking_price_egp"] == 18000
        assert audit.payload["request"]["what_if_modifications"] == {"size_sqm": 180}
        assert audit.payload["response"]["investment_position"] == "High Risk"
        assert audit.payload["response"]["what_if_summary"]["analysis"]["delta_value"] == 2000

        try:
            tools.execute_investment(
                other.id,
                InvestmentToolRequest(
                    workspace_id=workspace.id,
                    property_id=prop.id,
                    asking_price_egp=15000,
                ),
            )
        except ToolResourceNotFound:
            pass
        else:
            raise AssertionError("Cross-tenant investment execution must be rejected")

    engine.dispose()


def test_what_if_tool_uses_ephemeral_overlay_and_orchestrates_truth_layer_tools():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with factory() as db:
        copilot = CopilotService(db)
        user = copilot.create_user(UserCreate(external_subject="what-if-user", display_name="What If User"))
        workspace = copilot.create_workspace(user.id, WorkspaceCreate(name="What-if Workspace"))
        prop = copilot.create_property_state(
            user.id,
            PropertyStateCreate(
                workspace_id=workspace.id,
                label="Property A",
                location="Central Cairo",
                area=150,
                bedrooms=3,
                bathrooms=2,
                amenities={"codes": ["BA"]},
                valuation_inputs={"lat": 30.0444, "lng": 31.2357},
            ),
        )
        persisted_scenario = copilot.create_scenario_state(
            user.id,
            ScenarioStateCreate(property_state_id=prop.id, name="Expanded", modifications={"size_sqm": 160}),
        )
        tools = CopilotToolsService(db, router=truth_router)

        result = tools.execute_what_if(
            user.id,
            WhatIfToolRequest(
                workspace_id=workspace.id,
                property_id=prop.id,
                scenario_id=persisted_scenario.id,
                modifications={"size_sqm": 180, "bedrooms": 4, "parking": True},
            ),
        )

        db.refresh(prop)
        db.refresh(persisted_scenario)
        events = db.query(ToolEvent).filter(ToolEvent.workspace_id == workspace.id).order_by(ToolEvent.id).all()
        sandbox_snapshot = (
            db.query(ValuationSnapshot).filter(ValuationSnapshot.valuation_id == result.scenario_valuation_id).one()
        )
        fairness_snapshot = (
            db.query(ValuationSnapshot).filter(ValuationSnapshot.valuation_id == result.fairness_valuation_id).one()
        )

        assert result.base_valuation == 16000
        assert result.scenario_valuation == 18000
        assert result.delta_value == 2000
        assert result.delta_percentage == 12.5
        assert result.fairness_status == "Below Fair Value"
        assert result.source == "TruthLayer"
        assert result.comparables.source == "TruthLayer"
        assert result.explainability.source == "TruthLayer"
        assert {change.feature for change in result.feature_changes.added} == {"Parking"}
        assert {change.feature for change in result.feature_changes.modified} == {"Bedrooms", "Size"}
        assert "Furnished = Unknown" in result.assumptions_used
        assert "Finishing = Unknown" in result.assumptions_used
        assert prop.area == 150
        assert prop.bedrooms == 3
        assert prop.amenities == {"codes": ["BA"]}
        assert persisted_scenario.modifications == {"size_sqm": 160}
        assert sandbox_snapshot.router_request["size_sqm"] == 180
        assert sandbox_snapshot.router_request["bedrooms"] == 4
        assert "CP" in sandbox_snapshot.router_request["amenities"]
        assert fairness_snapshot.router_request["target_price_egp"] == 16000
        assert [event.tool_name for event in events] == [
            "valuation",
            "valuation",
            "explainability",
            "comparable",
            "valuation",
            "fairness",
            "what_if",
        ]
        assert events[-1].payload["request"]["sandbox_modifications"] == {
            "size_sqm": 180,
            "bedrooms": 4,
            "parking": True,
        }
        assert events[-1].payload["response"]["base_valuation_id"] == result.base_valuation_id
        assert events[-1].payload["response"]["scenario_valuation_id"] == result.scenario_valuation_id

    engine.dispose()


def test_router_ml_fallback_keeps_existing_explainability_payload(monkeypatch):
    from app.api.schemas.pricing import RentFairPriceRequest
    from app.services import router_service

    def fail_cmt(*args, **kwargs):
        raise ValueError("CMT unavailable")

    def ml_truth(*args, **kwargs):
        return RentFairPriceResponse(
            fair_price_egp=20000,
            range_low_egp=17000,
            range_high_egp=23000,
            flag="NO_TARGET",
            tier_used=0,
            comps_count=0,
            confidence={"score": 0.85, "label": "High", "factors": {}, "dimensions": {}},
            explanation=["Existing ML truth-layer explanation."],
            area={"name": "ML Inferred Area"},
            resolved_location={"lat": 30.0444, "lng": 31.2357},
            debug={
                "top_positive_features": [
                    {"feature_name": "size", "impact_egp": 1000, "impact_percentage": 5.0}
                ]
            },
        )

    monkeypatch.setattr(router_service, "price_listing_cmt", fail_cmt)
    monkeypatch.setattr(router_service, "price_listing_ml", ml_truth)
    monkeypatch.setattr(
        router_service.exposure_registry,
        "get_exposure_metrics",
        lambda compound_name, h3_index: (False, False, 1.0),
    )
    response = router_service.price_listing_router(
        RentFairPriceRequest(
            lat=30.0444,
            lng=31.2357,
            property_type="Apartment",
            bedrooms=3,
            bathrooms=2,
            size_sqm=150,
        ),
        db=None,
    )

    assert response.engine_used == "ML"
    assert response.routing_reason == "Fallback_CMT_Failure"
    assert response.explainability is not None
    assert response.explainability.narrative_explanation.summary == "The property's fair value is 20,000 EGP."
