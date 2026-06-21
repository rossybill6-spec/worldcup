"""
Reset password endpoint - Set new password using token.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import ResetPasswordRequest
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/reset-password",
    response_model=APIResponse,
    summary="Reset password using token from email",
)
async def reset_password(
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Reset password using the token sent to the user's email.
    """
    auth_service = AuthService(db)
    success, message = await auth_service.reset_password(
        data.token,
        data.new_password,
    )
    return APIResponse(success=success, message=message)
