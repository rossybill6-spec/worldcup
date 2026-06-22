from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.account import Account
from app.utils.generators import generate_account_number
router = APIRouter()

@router.post("/{user_id}/accounts", summary="Create account for user")
async def create_account(user_id: str, db: AsyncSession = Depends(get_db)):
    a = Account(user_id=user_id, account_number=generate_account_number(), account_type="savings", account_name="Admin Created Savings")
    db.add(a); await db.commit()
    return APIResponse(success=True, message="Account created", data={"id": a.id, "number": a.account_number})

@router.post("/accounts/{account_id}/freeze", summary="Freeze account")
async def freeze_account(account_id: str, db: AsyncSession = Depends(get_db)):
    a = (await db.execute(select(Account).where(Account.id == account_id))).scalar_one_or_none()
    if not a: return APIResponse(success=False, message="Not found")
    a.is_frozen = True; await db.commit()
    return APIResponse(success=True, message="Account frozen")

@router.post("/accounts/{account_id}/unfreeze", summary="Unfreeze account")
async def unfreeze_account(account_id: str, db: AsyncSession = Depends(get_db)):
    a = (await db.execute(select(Account).where(Account.id == account_id))).scalar_one_or_none()
    if not a: return APIResponse(success=False, message="Not found")
    a.is_frozen = False; await db.commit()
    return APIResponse(success=True, message="Account unfrozen")
