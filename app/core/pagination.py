"""
Standard pagination utilities for list endpoints.
"""

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel


class PaginationParams:
    """Pagination parameters extracted from query string."""
    
    def __init__(self, page: int = 1, per_page: int = 20):
        self.page = page
        self.per_page = per_page
    
    @property
    def offset(self) -> int:
        """Calculate offset for SQL queries."""
        return (self.page - 1) * self.per_page
    
    @property
    def limit(self) -> int:
        """Get limit for SQL queries."""
        return self.per_page


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response wrapper."""
    
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_previous: bool
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        params: PaginationParams,
    ) -> "PaginatedResponse":
        """Create a paginated response from items and total count."""
        total_pages = (total + params.per_page - 1) // params.per_page
        return cls(
            items=items,
            total=total,
            page=params.page,
            per_page=params.per_page,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_previous=params.page > 1,
        )
