"""
Base model class with common fields for all database tables.
Every model inherits from this to get id, created_at, updated_at automatically.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDMixin:
    """Mixin that adds a UUID primary key."""
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )


class SoftDeleteMixin:
    """Mixin that adds soft delete capability."""
    
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class BaseModel(UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Complete base model with UUID, timestamps, and soft delete.
    All application models should inherit from this.
    """
    __abstract__ = True
