"""
Savings account endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.account import CreateSavingsRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.account_service import AccountService

router = APIRouter()


@router.post("/savings", response_model=APIResponse, status_code=status.HTTP_201_CREATED, summary="Create savings account")
async def create_savings(
    data: CreateSavingsRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new savings account."""
    service = AccountService(db)
    account = await service.create_savings_account(
        user_id=user.id,
        account_name=data.account_name,
        initial_deposit=data.initial_deposit,
    )
    await db.commit()
    
    return APIResponse(
        success=True,
        message="Savings account created",
        data={
            "id": account.id,
            "account_number": account.account_number,
            "account_type": account.account_type,
            "balance": account.balance,
        },
    )


@router.get("/savings", response_model=APIResponse, summary="Get savings accounts")
async def get_savings(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all savings accounts."""
    service = AccountService(db)
    accounts = await service.get_user_accounts(user.id)
    savings = [a for a in accounts["accounts"] if a["account_type"] == "savings"]
    return APIResponse(success=True, message="Savings accounts retrieved", data=savings)
