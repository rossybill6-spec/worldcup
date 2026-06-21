from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.bill import CreatePayeeRequest, UpdatePayeeRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.bill_service import BillService
router = APIRouter()
@router.post("/payees", summary="Add payee")
async def add_payee(data: CreatePayeeRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = BillService(db); r = await svc.add_payee(user.id, data.model_dump(exclude_none=True))
    await db.commit(); return APIResponse(success=True, message="Payee added", data=r)
@router.get("/payees", summary="List payees")
async def list_payees(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = BillService(db); payees = await svc.get_payees(user.id)
    return APIResponse(success=True, message="Payees retrieved", data=payees)
@router.put("/payees/{payee_id}", summary="Update payee")
async def update_payee(payee_id: str, data: UpdatePayeeRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = BillService(db); ok = await svc.update_payee(user.id, payee_id, data.model_dump(exclude_none=True))
    await db.commit(); return APIResponse(success=ok, message="Payee updated" if ok else "Not found")
@router.delete("/payees/{payee_id}", summary="Delete payee")
async def delete_payee(payee_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = BillService(db); ok = await svc.delete_payee(user.id, payee_id)
    await db.commit(); return APIResponse(success=ok, message="Payee deleted" if ok else "Not found")
