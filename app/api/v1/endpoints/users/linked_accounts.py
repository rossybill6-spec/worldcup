"""
Linked external bank account endpoints.
"""

import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.schemas.user_linked_account import AddLinkedAccountRequest, VerifyMicroDepositsRequest, LinkedAccountResponse
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_linked_account import UserLinkedAccount

router = APIRouter()


@router.get("/linked-accounts", response_model=APIResponse, summary="List linked accounts")
async def list_linked_accounts(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all linked external bank accounts."""
    result = await db.execute(
        select(UserLinkedAccount).where(
            UserLinkedAccount.user_id == user.id,
            UserLinkedAccount.is_deleted == False,
        )
    )
    accounts = result.scalars().all()
    return APIResponse(
        success=True,
        message="Linked accounts retrieved",
        data=[
            {
                "id": a.id, "bank_name": a.bank_name, "account_number": "****" + a.account_number[-4:],
                "routing_number": a.routing_number, "account_type": a.account_type,
                "is_verified": a.is_verified, "is_default": a.is_default,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in accounts
        ],
    )


@router.post("/linked-accounts", response_model=APIResponse, status_code=status.HTTP_201_CREATED, summary="Add linked account")
async def add_linked_account(
    data: AddLinkedAccountRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Link an external bank account. Micro-deposits will be simulated."""
    # Generate mock micro-deposit amounts
    amount_1 = round(random.uniform(0.01, 0.99), 2)
    amount_2 = round(random.uniform(0.01, 0.99), 2)
    
    account = UserLinkedAccount(
        user_id=user.id,
        bank_name=data.bank_name,
        account_number=data.account_number,
        routing_number=data.routing_number,
        account_type=data.account_type,
        micro_deposit_1=amount_1,
        micro_deposit_2=amount_2,
    )
    db.add(account)
    await db.commit()
    await db.refresh(account)
    
    return APIResponse(
        success=True,
        message="Account linked. Check micro-deposits to verify.",
        data={"id": account.id, "micro_deposits_note": "Two small deposits have been sent. Enter the amounts to verify."},
    )


@router.post("/linked-accounts/{account_id}/verify", response_model=APIResponse, summary="Verify linked account")
async def verify_linked_account(
    account_id: str,
    data: VerifyMicroDepositsRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Verify linked account with micro-deposit amounts."""
    result = await db.execute(
        select(UserLinkedAccount).where(
            UserLinkedAccount.id == account_id,
            UserLinkedAccount.user_id == user.id,
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if account.is_verified:
        return APIResponse(success=False, message="Account already verified")
    
    # For development: show the expected amounts
    if abs(data.amount_1 - account.micro_deposit_1) < 0.01 and abs(data.amount_2 - account.micro_deposit_2) < 0.01:
        account.is_verified = True
        await db.commit()
        return APIResponse(success=True, message="Account verified")
    
    return APIResponse(
        success=False,
        message="Verification failed. Check the amounts and try again.",
        data={"hint": f"Expected: {account.micro_deposit_1} and {account.micro_deposit_2}"},
    )


@router.delete("/linked-accounts/{account_id}", response_model=APIResponse, summary="Remove linked account")
async def remove_linked_account(
    account_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove a linked external account."""
    result = await db.execute(
        select(UserLinkedAccount).where(
            UserLinkedAccount.id == account_id,
            UserLinkedAccount.user_id == user.id,
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account.is_deleted = True
    await db.commit()
    return APIResponse(success=True, message="Linked account removed")
