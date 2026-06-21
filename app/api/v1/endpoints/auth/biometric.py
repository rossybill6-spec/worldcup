"""
Biometric login endpoints - Setup and login with fingerprint/face.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import BiometricSetupRequest, BiometricLoginRequest
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post(
    "/biometric/enable",
    response_model=APIResponse,
    summary="Enable biometric login",
)
async def enable_biometric(
    data: BiometricSetupRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Enable fingerprint/face login for this device."""
    auth_service = AuthService(db)
    success, message = await auth_service.setup_biometric(
        user.id,
        data.biometric_token,
        data.device_name,
        data.device_type,
    )
    return APIResponse(success=success, message=message)


@router.post(
    "/biometric/login",
    response_model=APIResponse,
    summary="Login with biometric",
)
async def biometric_login(
    request: Request,
    data: BiometricLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Login using biometric token (fingerprint/face).
    No password required if biometric is set up.
    """
    auth_service = AuthService(db)
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    success, message, response_data = await auth_service.biometric_login(
        biometric_token=data.biometric_token,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    if not success:
        return APIResponse(success=False, message=message)
    
    return APIResponse(success=True, message=message, data=response_data)


@router.delete(
    "/biometric/disable",
    response_model=APIResponse,
    summary="Disable biometric login",
)
async def disable_biometric(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Disable biometric login for all devices."""
    auth_service = AuthService(db)
    success, message = await auth_service.disable_biometric(user.id)
    return APIResponse(success=success, message=message)
