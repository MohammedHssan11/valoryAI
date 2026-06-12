from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.broker.schemas.contracts import BrokerToolName, BrokerToolResult


class BrokerTool(ABC):
    name: BrokerToolName
    description: str

    @abstractmethod
    def execute(self, *, db: Session, **kwargs) -> BrokerToolResult:
        """Execute a typed deterministic-aware broker tool."""

