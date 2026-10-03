"""Approval ORM model for pending and resolved human-in-the-loop actions."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from packages.core.models.base import Base


class StoredApproval(Base):
    """Pending and historic approval requests."""

    __tablename__ = "approvals"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "venture_id"],
            ["ventures.tenant_id", "ventures.id"],
            ondelete="CASCADE",
            name="fk_approvals_tenant_venture",
        ),
        {"comment": "PostgreSQL RLS: CREATE POLICY approval_isolation ON approvals USING (tenant_id = current_setting('app.tenant_id')::uuid)"},
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
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
