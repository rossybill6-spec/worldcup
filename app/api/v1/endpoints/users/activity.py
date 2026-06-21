"""
Activity log endpoint.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter()


@router.get("/activity", response_model=APIResponse, summary="Get activity log")
async def get_activity(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated activity log."""
    service = UserService(db)
    items, total = await service.get_activity_logs(user.id, page, per_page)
    return APIResponse(success=True, message="Activity retrieved", data={
        "items": items, "page": page, "per_page": per_page, "total": total,
    })
