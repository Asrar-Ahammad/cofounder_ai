"""Event ORM model for domain event persistence."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from packages.core.models.base import Base


class StoredEvent(Base):
    """Append-only domain event log table with RLS."""

    __tablename__ = "events"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "venture_id"],
            ["ventures.tenant_id", "ventures.id"],
            ondelete="CASCADE",
            name="fk_events_tenant_venture",
        ),
        {"comment": "PostgreSQL RLS: CREATE POLICY event_isolation ON events USING (tenant_id = current_setting('app.tenant_id')::uuid)"},
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    venture_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ventures.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    emitted_by: Mapped[str] = mapped_column(String(100), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    causation_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    correlation_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
