"""
User note schemas (admin only).
"""

from typing import Optional
from pydantic import BaseModel, Field


class NoteResponse(BaseModel):
    """Admin note about a user."""
    id: str
    note: str
    author_name: Optional[str] = None
    is_pinned: bool = False
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
