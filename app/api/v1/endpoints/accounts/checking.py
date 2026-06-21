"""
Checking account endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.account_service import AccountService

router = APIRouter()


@router.get("/checking", response_model=APIResponse, summary="Get checking account")
async def get_checking(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the user's primary checking account."""
    service = AccountService(db)
    accounts = await service.get_user_accounts(user.id)
    checking = next((a for a in accounts["accounts"] if a["account_type"] == "checking"), None)
    
    if not checking:
        return APIResponse(success=False, message="No checking account found")
    
    return APIResponse(success=True, message="Checking account retrieved", data=checking)
