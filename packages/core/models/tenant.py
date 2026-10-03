"""Tenant ORM model representing customer organizations."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.core.models.base import Base

if TYPE_CHECKING:
    from packages.core.models.venture import Venture


class Tenant(Base):
    """Customer tenant aggregate root."""

    __tablename__ = "tenants"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="standard", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    ventures: Mapped[list["Venture"]] = relationship(  # noqa: F821
        "Venture",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
