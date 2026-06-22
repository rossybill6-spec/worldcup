from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user import User
from app.models.user_profile import UserProfile
router = APIRouter()

@router.get("/list", summary="List all users")
async def list_users(
    page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100),
    search: str = Query(None), status: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    q = select(User, UserProfile).join(UserProfile, User.id == UserProfile.user_id).where(User.is_deleted == False)
    if search:
        q = q.where(or_(User.email.ilike(f"%{search}%"), User.username.ilike(f"%{search}%"), UserProfile.first_name.ilike(f"%{search}%"), UserProfile.last_name.ilike(f"%{search}%")))
    if status == "active": q = q.where(User.is_active == True, User.is_suspended == False)
    elif status == "suspended": q = q.where(User.is_suspended == True)
    elif status == "inactive": q = q.where(User.is_active == False)
    count_q = select(func.count()).select_from(q.subquery())
    total = (await db.execute(count_q)).scalar()
    offset = (page-1)*per_page
    r = await db.execute(q.offset(offset).limit(per_page))
    rows = r.all()
    items = [{"id": u.id, "email": u.email, "username": u.username, "phone": u.phone, "is_active": u.is_active, "is_suspended": u.is_suspended, "kyc_status": u.kyc_status, "first_name": p.first_name, "last_name": p.last_name, "created_at": u.created_at.isoformat() if u.created_at else None} for u, p in rows]
    return APIResponse(success=True, data={"items": items, "total": total, "page": page, "per_page": per_page})
