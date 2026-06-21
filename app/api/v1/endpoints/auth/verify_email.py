"""
Email verification endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.schemas.auth import VerifyEmailRequest, ResendVerificationRequest
from app.schemas.common import APIResponse
from app.models.user import User

router = APIRouter()


@router.post(
    "/verify-email",
    response_model=APIResponse,
    summary="Verify email address with code",
)
async def verify_email(
    data: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Verify email address using the verification code.
    Provide the email and the code sent to it.
    """
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == data.email.lower())
    )
    user = result.scalar_one_or_none()
    
    if not user:
        return APIResponse(success=False, message="User not found")
    
    if user.is_email_verified:
        return APIResponse(success=False, message="Email already verified")
    
    if user.email_verification_code != data.code:
        return APIResponse(success=False, message="Invalid verification code")
    
    from datetime import datetime
    if user.email_verification_expires and user.email_verification_expires < datetime.utcnow():
        return APIResponse(success=False, message="Verification code expired")
    
    from sqlalchemy import update
    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(
            is_email_verified=True,
            email_verification_code=None,
            email_verification_expires=None,
        )
    )
    await db.commit()
    
    return APIResponse(success=True, message="Email verified successfully")


@router.post(
    "/resend-verification",
    response_model=APIResponse,
    summary="Resend verification code",
)
async def resend_verification(
    data: ResendVerificationRequest,
    db: AsyncSession = Depends(get_db),
):
    """Resend verification code to email."""
    result = await db.execute(
        select(User).where(User.email == data.email.lower())
    )
    user = result.scalar_one_or_none()
    
    if not user:
        return APIResponse(success=False, message="User not found")
    
    if user.is_email_verified:
        return APIResponse(success=False, message="Email already verified")
    
    from app.services.auth_service import AuthService
    auth_service = AuthService(db)
    success, message = await auth_service.resend_verification(user.id, "email")
    return APIResponse(success=success, message=message)


# TESTING ONLY
@router.get(
    "/test-verification-code",
    summary="[TESTING] Get verification code",
)
async def get_test_code(email: str, db: AsyncSession = Depends(get_db)):
    """TESTING: Get verification code directly."""
    result = await db.execute(
        select(User).where(User.email == email.lower())
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "email": user.email,
        "code": user.email_verification_code,
    }
