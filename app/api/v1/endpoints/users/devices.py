"""
Trusted device management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter()


@router.get("/devices", response_model=APIResponse, summary="List trusted devices")
async def list_devices(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all trusted devices."""
    service = UserService(db)
    devices = await service.get_devices(user.id)
    return APIResponse(success=True, message="Devices retrieved", data=devices)


@router.delete("/devices/{device_id}", response_model=APIResponse, summary="Untrust device")
async def untrust_device(
    device_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove trust from a device."""
    service = UserService(db)
    success = await service.untrust_device(user.id, device_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    return APIResponse(success=True, message="Device untrusted")
