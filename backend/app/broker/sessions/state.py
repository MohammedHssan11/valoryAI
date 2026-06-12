from __future__ import annotations

import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator

from sqlalchemy.orm import Session

from app.broker.schemas.contracts import (
    BrokerIntent,
    BrokerSessionSnapshot,
    BrokerSessionTurn,
    BrokerSessionValuation,
    BrokerValuationSummary,
    InvestorPreferences,
)
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.copilot import BrokerSession, ScenarioState, Workspace


class BrokerSessionStore:
    def new_session_id(self) -> str:
        return f"brs_{uuid.uuid4().hex[:18]}"

    @contextmanager
    def _db(self, db: Session | None) -> Iterator[Session]:
        if db is not None:
            yield db
            return
        local = SessionLocal()
        try:
            yield local
        finally:
            local.close()

    def get_or_create(
        self,
        session_id: str | None = None,
        *,
        db: Session | None = None,
        user_id: int | None = None,
        workspace_id: int | None = None,
        scenario_id: int | None = None,
    ) -> BrokerSessionSnapshot:
        with self._db(db) as session:
            resolved_id = session_id or self.new_session_id()
            row = session.get(BrokerSession, resolved_id)
            if row is not None:
                self._assert_owner(row, user_id=user_id, workspace_id=workspace_id, scenario_id=scenario_id)
                return self._snapshot(row)

            if user_id is None or workspace_id is None or scenario_id is None:
                raise ValueError("Broker session ownership requires user, workspace, and scenario")
            self._validate_context(session, user_id=user_id, workspace_id=workspace_id, scenario_id=scenario_id)

            now = datetime.now(timezone.utc)
            snapshot = BrokerSessionSnapshot(
                session_id=resolved_id,
                user_id=user_id,
                workspace_id=workspace_id,
                scenario_id=scenario_id,
                created_at=now,
                updated_at=now,
            )
            session.add(
                BrokerSession(
                    session_id=resolved_id,
                    user_id=user_id,
                    workspace_id=workspace_id,
                    scenario_id=scenario_id,
                    state=snapshot.model_dump(mode="json"),
                )
            )
            session.commit()
            return snapshot

    def get(
        self,
        session_id: str,
        *,
        db: Session | None = None,
        user_id: int | None = None,
    ) -> BrokerSessionSnapshot | None:
        with self._db(db) as session:
            row = session.get(BrokerSession, session_id)
            if row is None or (user_id is not None and row.user_id != user_id):
                return None
            return self._snapshot(row)

    def _snapshot(self, row: BrokerSession) -> BrokerSessionSnapshot:
        return BrokerSessionSnapshot.model_validate(
            {
                **row.state,
                "session_id": row.session_id,
                "user_id": row.user_id,
                "workspace_id": row.workspace_id,
                "scenario_id": row.scenario_id,
            }
        )

    def _validate_context(self, session: Session, *, user_id: int, workspace_id: int, scenario_id: int) -> None:
        workspace = (
            session.query(Workspace)
            .filter(Workspace.id == workspace_id, Workspace.user_id == user_id, Workspace.is_deleted.is_(False))
            .first()
        )
        if workspace is None:
            raise ValueError("Workspace not found")
        scenario = (
            session.query(ScenarioState)
            .filter(
                ScenarioState.id == scenario_id,
                ScenarioState.workspace_id == workspace_id,
                ScenarioState.user_id == user_id,
                ScenarioState.is_deleted.is_(False),
            )
            .first()
        )
        if scenario is None:
            raise ValueError("Scenario not found")

    def _assert_owner(
        self,
        row: BrokerSession,
        *,
        user_id: int | None,
        workspace_id: int | None,
        scenario_id: int | None,
    ) -> None:
        provided = (user_id, workspace_id, scenario_id)
        if all(value is None for value in provided):
            return
        if any(value is None for value in provided):
            raise ValueError("Broker session ownership requires user, workspace, and scenario")
        if (row.user_id, row.workspace_id, row.scenario_id) != provided:
            raise PermissionError("Broker session ownership mismatch")

    def record_turn(
        self,
        *,
        session_id: str,
        message: str,
        intent: BrokerIntent,
        investor_preferences: InvestorPreferences | None,
        valuation_summary: BrokerValuationSummary | None,
        analytical_context: dict[str, Any] | None = None,
        db: Session | None = None,
    ) -> BrokerSessionSnapshot:
        with self._db(db) as session:
            row = session.get(BrokerSession, session_id)
            if row is None:
                raise ValueError("Broker session was not initialized")
            snapshot = self._snapshot(row)
            turns = [
                *snapshot.previous_requests,
                BrokerSessionTurn(message=message, intent=intent),
            ][-settings.BROKER_SESSION_HISTORY_LIMIT :]

            valuations = list(snapshot.previous_valuations)
            if valuation_summary is not None:
                valuations.append(
                    BrokerSessionValuation(
                        fair_price_egp=valuation_summary.fair_price_egp,
                        range_low_egp=valuation_summary.range_low_egp,
                        range_high_egp=valuation_summary.range_high_egp,
                        confidence_label=valuation_summary.confidence_label,
                        area_name=valuation_summary.area.get("name"),
                    )
                )
                valuations = valuations[-settings.BROKER_SESSION_HISTORY_LIMIT :]

            updated = snapshot.model_copy(
                update={
                    "updated_at": datetime.now(timezone.utc),
                    "previous_requests": turns,
                    "previous_valuations": valuations,
                    "active_district": (
                        valuation_summary.area.get("name")
                        if valuation_summary is not None
                        else snapshot.active_district
                    ),
                    "investor_preferences": investor_preferences or snapshot.investor_preferences,
                    "analytical_context": analytical_context or snapshot.analytical_context,
                },
                deep=True,
            )
            row.state = updated.model_dump(mode="json")
            row.updated_at = datetime.now(timezone.utc)
            row.version += 1
            session.commit()
            return updated


session_store = BrokerSessionStore()
