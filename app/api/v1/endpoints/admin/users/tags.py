from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user_tag import UserTag
router = APIRouter()

class TagRequest(BaseModel): tag: str

@router.post("/{user_id}/tags", summary="Add tag")
async def add_tag(user_id: str, data: TagRequest, db: AsyncSession = Depends(get_db)):
    t = UserTag(user_id=user_id, tag=data.tag)
    db.add(t); await db.commit()
    return APIResponse(success=True, message="Tag added")
