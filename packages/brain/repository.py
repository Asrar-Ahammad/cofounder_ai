"""Database repository for venture profiles, constraints, and decision logs."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from packages.brain.service import VentureConstraints, VentureProfile
from packages.core.models.constraint import Constraint
from packages.core.models.venture import Venture


class BrainRepository:
    """Async database repository for Shared Brain state aggregates."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with active transactional session.

        Args:
            session: Async SQLAlchemy database session.
        """
        self.session = session

    async def get_venture_profile(self, venture_id: UUID) -> VentureProfile | None:
        """Retrieve venture profile by ID within the current tenant scope.

        Args:
            venture_id: Venture UUID.

        Returns:
            VentureProfile | None: Profile if found, None otherwise.
        """
        stmt = select(Venture).where(Venture.id == venture_id)
        result = await self.session.execute(stmt)
        record = result.scalar_one_or_none()
        if not record:
            return None

        return VentureProfile(
            id=record.id,
            tenant_id=record.tenant_id,
            name=record.name,
            idea=record.idea,
            jurisdiction=record.jurisdiction,
            stage=record.stage,
            goal=record.goal_json,
        )

    async def get_active_constraints(self, venture_id: UUID) -> VentureConstraints | None:
        """Retrieve the latest active constraints for a venture.

        Args:
            venture_id: Venture UUID.

        Returns:
            VentureConstraints | None: Active constraints or None.
        """
        stmt = (
            select(Constraint)
            .where(Constraint.venture_id == venture_id)
            .order_by(Constraint.version.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        record = result.scalar_one_or_none()
        if not record:
            return None

        return VentureConstraints(
            venture_id=record.venture_id,
            version=record.version,
            budget_cap=float(record.budget_cap),
            max_cac=float(record.max_cac),
            outreach_cap=record.outreach_cap,
        )
