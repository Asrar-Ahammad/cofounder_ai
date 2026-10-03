"""Venture ORM model representing startup ventures."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.core.models.base import Base

if TYPE_CHECKING:
    from packages.core.models.constraint import Constraint
    from packages.core.models.tenant import Tenant


class Venture(Base):
    """Venture aggregate root protected by Row-Level Security."""

    __tablename__ = "ventures"

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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    idea: Mapped[str] = mapped_column(String, nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(50), nullable=False)
    stage: Mapped[str] = mapped_column(String(50), default="ideation", nullable=False)
    goal_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="ventures")  # noqa: F821
    constraints: Mapped[list["Constraint"]] = relationship(  # noqa: F821
        "Constraint",
        back_populates="venture",
        cascade="all, delete-orphan",
    )
