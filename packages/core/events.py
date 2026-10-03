"""Domain events schema and models for the Cofunder event-driven architecture."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    """Immutable domain event model published to Redis Streams."""

    id: UUID = Field(default_factory=uuid4, description="Unique event identifier")
    tenant_id: str = Field(..., description="Target tenant identifier")
    venture_id: str = Field(..., description="Target venture identifier")
    type: str = Field(..., description="Domain event type identifier")
    version: int = Field(default=1, description="Event schema version")
    payload: dict[str, Any] = Field(default_factory=dict, description="Event body payload")
    emitted_by: str = Field(..., description="Originating agent or service name")
    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when event occurred",
    )
    causation_id: UUID | None = Field(default=None, description="ID of preceding causing event")
    correlation_id: UUID | None = Field(default=None, description="Overall transaction correlation ID")

    model_config = {
        "frozen": True,
    }
