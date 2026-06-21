"""
Login endpoint - Authenticate user and return tokens.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/login",
    response_model=APIResponse,
    summary="Login with email/username and password",
)
async def login(
    request: Request,
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate a user and return access/refresh tokens.
    
    - **login**: Email or username
    - **password**: Account password
    - **device_name**: Optional name of the device
    - **device_type**: Optional type (mobile, desktop, tablet)
    
    If 2FA is enabled, returns requires_2fa=true with a temp token.
    """
    auth_service = AuthService(db)
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    success, message, response_data = await auth_service.login(
        login=data.login,
        password=data.password,
        ip_address=ip_address,
        user_agent=user_agent,
        device_name=data.device_name,
        device_type=data.device_type,
    )
    
    if not success:
        return APIResponse(success=False, message=message)
    
    return APIResponse(success=True, message=message, data=response_data)
