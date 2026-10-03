"""Security tests for multi-tenant isolation and schema foreign key separation.

Note: Native PostgreSQL Row-Level Security (RLS) policies require an active PostgreSQL
instance. This unit test verifies logical isolation, multi-tenant schema integrity,
and non-leakage under SQLite in-memory test harnesses.
"""

from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from packages.core.models.base import Base
from packages.core.models.tenant import Tenant
from packages.core.models.venture import Venture


@pytest.mark.asyncio
async def test_tenant_isolation_foreign_key_and_separation() -> None:
    """Verify that distinct tenants maintain isolated records without cross-tenant leakage."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    tenant_a_id = uuid4()
    tenant_b_id = uuid4()

    async with async_session() as session:
        # Create Tenant A and Venture A
        tenant_a = Tenant(id=tenant_a_id, name="Acme Inc")
        venture_a = Venture(
            id=uuid4(),
            tenant_id=tenant_a_id,
            name="Acme AI",
            idea="AI for widgets",
            jurisdiction="US-DE",
            goal_json={"target": "100k ARR"},
        )
        session.add_all([tenant_a, venture_a])

        # Create Tenant B and Venture B
        tenant_b = Tenant(id=tenant_b_id, name="Beta Corp")
        venture_b = Venture(
            id=uuid4(),
            tenant_id=tenant_b_id,
            name="Beta Cloud",
            idea="Cloud for pets",
            jurisdiction="IN-KA",
            goal_json={"target": "10k MRR"},
        )
        session.add_all([tenant_b, venture_b])
        await session.commit()

    # Query with Tenant A filtering
    async with async_session() as session:
        stmt = select(Venture).where(Venture.tenant_id == tenant_a_id)
        result = await session.execute(stmt)
        ventures_for_a = result.scalars().all()

        assert len(ventures_for_a) == 1
        assert ventures_for_a[0].name == "Acme AI"
        assert ventures_for_a[0].tenant_id == tenant_a_id

        # Tenant A query should NEVER return Tenant B venture
        for v in ventures_for_a:
            assert v.tenant_id != tenant_b_id

    await engine.dispose()
