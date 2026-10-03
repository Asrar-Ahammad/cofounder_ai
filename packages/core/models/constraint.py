"""Constraint ORM model defining budget and volume limits for ventures."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.core.models.base import Base

if TYPE_CHECKING:
    from packages.core.models.venture import Venture


class Constraint(Base):
    """Versioned business and spending limits for a venture."""

    __tablename__ = "constraints"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    venture_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ventures.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    budget_cap: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    max_cac: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    outreach_cap: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    venture: Mapped["Venture"] = relationship("Venture", back_populates="constraints")  # noqa: F821
