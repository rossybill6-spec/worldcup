"""
Phone verification endpoint.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import VerifyPhoneRequest
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post(
    "/verify-phone",
    response_model=APIResponse,
    summary="Verify phone number with code",
)
async def verify_phone(
    data: VerifyPhoneRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Verify the user's phone number using the code sent via SMS."""
    auth_service = AuthService(db)
    success, message = await auth_service.verify_phone(user.id, data.code)
    return APIResponse(success=success, message=message)
