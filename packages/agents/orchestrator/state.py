"""State definition for Orchestrator Supervisor."""

from typing import Any

from pydantic import BaseModel, Field

from packages.core.events import DomainEvent


class Milestone(BaseModel):
    """Venture milestone tracking progress toward the north-star goal."""

    id: str
    title: str
    stage: str
    status: str = "pending"  # pending, in_progress, completed, blocked
    completed_at: str | None = None


class OrchestratorState(BaseModel):
    """Master state passing through the Orchestrator Supervisor."""

    tenant_id: str
    venture_id: str
    venture_name: str
    idea: str
    jurisdiction: str
    north_star_goal: str
    stage: str = "ideation"  # ideation, validation, build, gtm, scale
    active_agent: str | None = None
    next_action: str = "market_intel"
    milestones: list[Milestone] = Field(default_factory=list)
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    decisions: list[dict[str, Any]] = Field(default_factory=list)
    emitted_events: list[DomainEvent] = Field(default_factory=list)
    needs_human: bool = False
    summary: str = ""
