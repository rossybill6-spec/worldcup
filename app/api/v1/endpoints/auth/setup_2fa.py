"""
2FA setup and management endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.schemas.auth import Enable2FARequest, Disable2FARequest, Verify2FARequest
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post(
    "/2fa/enable",
    response_model=APIResponse,
    summary="Enable two-factor authentication",
)
async def enable_2fa(
    data: Enable2FARequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Start 2FA setup. Returns QR code for authenticator apps."""
    auth_service = AuthService(db)
    success, message, setup_data = await auth_service.setup_2fa(
        user.id,
        method=data.method,
        phone_number=data.phone_number,
    )
    
    if not success:
        return APIResponse(success=False, message=message)
    
    return APIResponse(success=True, message=message, data=setup_data)


@router.post(
    "/2fa/verify-setup",
    response_model=APIResponse,
    summary="Verify 2FA setup with code",
)
async def verify_2fa_setup(
    data: Verify2FARequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Verify the 2FA setup by entering a code from your authenticator app."""
    auth_service = AuthService(db)
    success, message = await auth_service.verify_2fa_setup(user.id, data.code)
    return APIResponse(success=success, message=message)


@router.delete(
    "/2fa/disable",
    response_model=APIResponse,
    summary="Disable two-factor authentication",
)
async def disable_2fa(
    data: Disable2FARequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Disable 2FA. Requires your 2FA code and password."""
    auth_service = AuthService(db)
    success, message = await auth_service.disable_2fa(
        user.id,
        data.code,
        data.password,
    )
    return APIResponse(success=success, message=message)
