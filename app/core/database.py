"""
Database connection setup for Neon PostgreSQL.
Uses SQLAlchemy async engine for FastAPI compatibility.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from app.core.config import settings

# Sync engine (for Alembic migrations and scripts)
sync_engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

# Async engine (for FastAPI endpoints)
async_engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

# Session factories
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency that provides an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> Session:
    """Dependency that provides a sync database session (for scripts)."""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
