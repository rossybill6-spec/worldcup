"""
Forgot password endpoint - Send reset email.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import ForgotPasswordRequest
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/forgot-password",
    response_model=APIResponse,
    summary="Request a password reset email",
)
async def forgot_password(
    data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Send a password reset link to the user's email.
    Always returns success regardless of whether the email exists (security).
    """
    auth_service = AuthService(db)
    success, message = await auth_service.forgot_password(data.email)
    return APIResponse(success=True, message=message)
