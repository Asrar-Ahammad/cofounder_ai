"""Unit tests for DomainEvent model and immutability."""

import pytest
from pydantic import ValidationError as PydanticValidationError

from packages.core.events import DomainEvent


def test_domain_event_creation() -> None:
    """Verify standard creation of a domain event with default values."""
    event = DomainEvent(
        tenant_id="tenant-123",
        venture_id="venture-456",
        type="idea_validated",
        emitted_by="validation_agent",
        payload={"score": 8.5},
    )
    assert event.tenant_id == "tenant-123"
    assert event.venture_id == "venture-456"
    assert event.type == "idea_validated"
    assert event.emitted_by == "validation_agent"
    assert event.payload == {"score": 8.5}
    assert event.version == 1
    assert event.id is not None
    assert event.occurred_at is not None


def test_domain_event_immutability() -> None:
    """Verify that domain event instances cannot be mutated."""
    event = DomainEvent(
        tenant_id="tenant-123",
        venture_id="venture-456",
        type="test_event",
        emitted_by="test",
    )
    with pytest.raises(PydanticValidationError):
        # Frozen models prohibit attribute assignment
        event.tenant_id = "tenant-999"
