"""
Signup endpoint - Register a new user.
"""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import SignupRequest, SignupResponse
from app.schemas.common import APIResponse, ErrorResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/signup",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def signup(
    request: Request,
    data: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user account.
    
    - **email**: Valid email address
    - **username**: 4-30 characters, alphanumeric and underscore
    - **password**: 8+ characters, uppercase, lowercase, number, special char
    - **ssn**: US Social Security Number (9 digits)
    - **agree_to_terms**: Must be true
    """
    auth_service = AuthService(db)
    ip_address = request.client.host if request.client else None
    
    success, message, user_data = await auth_service.signup(
        data.model_dump(),
        ip_address,
    )
    
    if not success:
        return APIResponse(success=False, message=message)
    
    return APIResponse(success=True, message=message, data=user_data)
