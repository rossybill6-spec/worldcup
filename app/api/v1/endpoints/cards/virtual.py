from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.card_service import CardService
from app.services.account_service import AccountService
from app.repositories.user_repository import UserRepository
router = APIRouter()

@router.get("", summary="List cards")
async def list_cards(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); cards = await svc.get_cards(user.id)
    return APIResponse(success=True, message="Cards retrieved", data=cards)

@router.post("/create", summary="Create virtual card")
async def create_card(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    acct_svc = AccountService(db); accounts = await acct_svc.get_user_accounts(user.id)
    checking = next((a for a in accounts["accounts"] if a["account_type"]=="checking"), None)
    if not checking: return APIResponse(success=False, message="No checking account")
    repo = UserRepository(db); profile = await repo.get_profile(user.id)
    name = f"{profile.first_name} {profile.last_name}" if profile else user.username
    svc = CardService(db); card = await svc.create_virtual_card(user.id, checking["id"], name)
    await db.commit()
    return APIResponse(success=True, message="Card created", data=card)

@router.get("/{card_id}", summary="Get card details")
async def get_card(card_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); card = await svc.get_card_detail(card_id, user.id)
    if not card: return APIResponse(success=False, message="Card not found")
    return APIResponse(success=True, message="Card retrieved", data=card)

@router.post("/{card_id}/freeze", summary="Freeze card")
async def freeze(card_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); ok = await svc.freeze_card(card_id, user.id)
    await db.commit(); return APIResponse(success=ok, message="Card frozen" if ok else "Not found")

@router.post("/{card_id}/unfreeze", summary="Unfreeze card")
async def unfreeze(card_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); ok = await svc.unfreeze_card(card_id, user.id)
    await db.commit(); return APIResponse(success=ok, message="Card unfrozen" if ok else "Not found")

@router.post("/{card_id}/verify-pin", summary="Verify card PIN")
async def verify_pin(card_id: str, pin: dict, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); result = await svc.verify_pin(card_id, user.id, pin.get("pin",""))
    return APIResponse(success=result is not None, message=result or "Invalid PIN")
