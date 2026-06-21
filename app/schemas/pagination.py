"""
Pagination schema for list endpoints.
"""

from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    page: int = 1
    per_page: int = 20


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_previous: bool
