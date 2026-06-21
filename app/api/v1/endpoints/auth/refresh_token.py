"""
Token refresh endpoint - Get new access token using refresh token.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import TokenRefreshRequest
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/refresh-token",
    response_model=APIResponse,
    summary="Refresh access token",
)
async def refresh_token(
    data: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a new access token and refresh token pair.
    Provide the current refresh token.
    """
    auth_service = AuthService(db)
    success, message, response_data = await auth_service.refresh_token(
        data.refresh_token,
    )
    
    if not success:
        return APIResponse(success=False, message=message)
    
    return APIResponse(success=True, message=message, data=response_data)
