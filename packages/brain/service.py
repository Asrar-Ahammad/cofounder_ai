"""Shared Brain service: Persistent centralized business brain for all agents."""

from typing import Any, Protocol
from uuid import UUID

from pydantic import BaseModel, Field


class VentureProfile(BaseModel):
    """Venture profile aggregate managed by the Shared Brain."""

    id: UUID
    tenant_id: UUID
    name: str
    idea: str
    jurisdiction: str
    stage: str
    goal: dict[str, Any] = Field(default_factory=dict)


class VentureConstraints(BaseModel):
    """Structured constraints governing agent budgets and outreach caps."""

    venture_id: UUID
    version: int = 1
    budget_cap: float
    max_cac: float
    outreach_cap: int


class SharedBrain(Protocol):
    """Protocol for Shared Brain read and write operations."""

    async def get_venture_profile(self, venture_id: UUID) -> VentureProfile | None:
        """Retrieve venture profile by ID."""
        ...

    async def get_active_constraints(self, venture_id: UUID) -> VentureConstraints | None:
        """Retrieve the latest active constraints for a venture."""
        ...

    async def record_decision(
        self,
        *,
        venture_id: UUID,
        summary: str,
        rationale: str,
        evidence_refs: list[str],
        decided_by: str,
    ) -> UUID:
        """Record an immutable architectural or business decision in the decision log."""
        ...


class InMemorySharedBrain:
    """In-memory implementation of the Shared Brain for tests and local execution."""

    def __init__(self) -> None:
        """Initialize empty in-memory Shared Brain."""
        self.profiles: dict[UUID, VentureProfile] = {}
        self.constraints: dict[UUID, VentureConstraints] = {}
        self.decisions: list[dict[str, Any]] = []

    async def get_venture_profile(self, venture_id: UUID) -> VentureProfile | None:
        """Retrieve venture profile from memory."""
        return self.profiles.get(venture_id)

    async def get_active_constraints(self, venture_id: UUID) -> VentureConstraints | None:
        """Retrieve active constraints from memory."""
        return self.constraints.get(venture_id)

    async def record_decision(
        self,
        *,
        venture_id: UUID,
        summary: str,
        rationale: str,
        evidence_refs: list[str],
        decided_by: str,
    ) -> UUID:
        """Record a decision in memory and return assigned UUID."""
        from uuid import uuid4

        decision_id = uuid4()
        self.decisions.append(
            {
                "id": decision_id,
                "venture_id": venture_id,
                "summary": summary,
                "rationale": rationale,
                "evidence_refs": evidence_refs,
                "decided_by": decided_by,
            }
        )
        return decision_id
