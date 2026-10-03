"""Base agent protocols and typed contracts for Cofunder agent subgraphs."""

from typing import Any, Protocol

from pydantic import BaseModel, Field

from packages.core.events import DomainEvent


class AgentInput(BaseModel):
    """Input payload passed to an agent subgraph execution."""

    tenant_id: str = Field(..., description="Tenant identifier")
    venture_id: str = Field(..., description="Venture identifier")
    task: str = Field(..., description="Task objective or query")
    context_refs: list[str] = Field(
        default_factory=list,
        description="IDs into Shared Brain artifacts/decisions, not raw blobs",
    )


class AgentOutput(BaseModel):
    """Standardized output produced by an agent subgraph execution."""

    summary: str = Field(..., description="Executive summary of the run outcome")
    artifacts: list[str] = Field(
        default_factory=list,
        description="Brain artifact IDs generated during run",
    )
    events: list[DomainEvent] = Field(
        default_factory=list,
        description="Domain events emitted during run",
    )
    needs_human: bool = Field(
        default=False,
        description="True if run halted waiting for human approval or clarification",
    )


class Agent(Protocol):
    """Protocol defining the standard interface for all specialist agents."""

    name: str
    allowed_tools: frozenset[str]
    consumes: frozenset[str]
    emits: frozenset[str]

    def build_graph(self) -> Any:
        """Construct and return the compiled LangGraph subgraph."""
        ...
