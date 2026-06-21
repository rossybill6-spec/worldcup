"""
Forgot username endpoint - Send username to email.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import ForgotUsernameRequest
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/forgot-username",
    response_model=APIResponse,
    summary="Request username via email",
)
async def forgot_username(
    data: ForgotUsernameRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Send the username to the registered email address.
    """
    auth_service = AuthService(db)
    success, message = await auth_service.forgot_username(data.email)
    return APIResponse(success=True, message=message)
