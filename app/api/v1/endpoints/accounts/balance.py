"""
Balance endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.account_service import AccountService

router = APIRouter()


@router.get("/balances", response_model=APIResponse, summary="Get all account balances")
async def get_balances(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get balances for all accounts."""
    service = AccountService(db)
    accounts = await service.get_user_accounts(user.id)
    return APIResponse(success=True, message="Balances retrieved", data=accounts)


@router.get("/{account_id}/balance", response_model=APIResponse, summary="Get single account balance")
async def get_account_balance(
    account_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get balance for a specific account."""
    service = AccountService(db)
    account = await service.get_account_detail(account_id, user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return APIResponse(success=True, message="Balance retrieved", data=account)
