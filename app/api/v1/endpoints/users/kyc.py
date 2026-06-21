"""
KYC status endpoint.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.kyc_service import KYCService

router = APIRouter()


@router.get("/kyc/status", response_model=APIResponse, summary="Get KYC status")
async def get_kyc_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get KYC verification status."""
    service = KYCService(db)
    status = await service.get_kyc_status(user.id)
    return APIResponse(success=True, message="KYC status retrieved", data=status)
