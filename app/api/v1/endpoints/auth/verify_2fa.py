"""
2FA verification endpoint - Verify 2FA code during login.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import Verify2FARequest
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService
from app.utils.tokenizers import get_user_id_from_token

router = APIRouter()


@router.post(
    "/verify-2fa",
    response_model=APIResponse,
    summary="Verify 2FA code during login",
)
async def verify_2fa(
    request: Request,
    data: Verify2FARequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Complete 2FA login by providing the code from your authenticator app.
    Requires the temp_token from the login response.
    """
    # Get temp token from header
    authorization = request.headers.get("authorization")
    if not authorization or not authorization.startswith("Bearer "):
        return APIResponse(success=False, message="Missing temp token")
    
    temp_token = authorization.split()[1]
    user_id = get_user_id_from_token(temp_token)
    
    if not user_id:
        return APIResponse(success=False, message="Invalid or expired temp token")
    
    auth_service = AuthService(db)
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    success, message, response_data = await auth_service.verify_2fa_login(
        user_id=user_id,
        code=data.code,
        trust_device=data.trust_device,
        device_name=data.device_name,
        device_type=data.device_type,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    if not success:
        return APIResponse(success=False, message=message)
    
    return APIResponse(success=True, message=message, data=response_data)
