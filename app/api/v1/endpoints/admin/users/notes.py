from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user_note import UserNote
router = APIRouter()

class NoteRequest(BaseModel): note: str; is_pinned: bool = False

@router.post("/{user_id}/notes", summary="Add note")
async def add_note(user_id: str, data: NoteRequest, db: AsyncSession = Depends(get_db)):
    n = UserNote(user_id=user_id, note=data.note, is_pinned=data.is_pinned, author_name="Admin")
    db.add(n); await db.commit()
    return APIResponse(success=True, message="Note added", data={"id": n.id})
