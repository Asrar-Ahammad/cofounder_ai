"""Database connection and session factory for PostgreSQL with asyncpg/psycopg3."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from packages.core.config import get_settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_db_engine() -> AsyncEngine:
    """Retrieve or initialize the singleton SQLAlchemy async engine.

    Returns:
        AsyncEngine: The active SQLAlchemy async engine instance.
    """
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.database_url,
            echo=settings.environment == "development",
            future=True,
            pool_size=10,
            max_overflow=20,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Retrieve or initialize the singleton SQLAlchemy async session maker.

    Returns:
        async_sessionmaker[AsyncSession]: Session factory for database sessions.
    """
    global _session_factory
    if _session_factory is None:
        engine = get_db_engine()
        _session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
    return _session_factory


@asynccontextmanager
async def get_db_session(tenant_id: str | None = None) -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional async session with tenant isolation set if provided.

    Args:
        tenant_id: Optional UUID string to set for row-level security.

    Yields:
        AsyncSession: Active database session.
    """
    factory = get_session_factory()
    async with factory() as session:
        if tenant_id:
            from sqlalchemy import text
            await session.execute(
                text("SELECT set_config('app.tenant_id', :tenant_id, true)"),
                {"tenant_id": str(tenant_id)},
            )
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
