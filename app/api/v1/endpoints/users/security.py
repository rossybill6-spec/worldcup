"""
Security settings endpoints - Password, PIN, security questions.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.core.database import get_db
from app.schemas.auth import ChangePasswordRequest
from app.schemas.user_security_question import SecurityQuestionResponse, UpdateSecurityQuestionsRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

router = APIRouter()


class ChangePINRequest(BaseModel):
    current_pin: Optional[str] = Field(None, min_length=4, max_length=6)
    new_pin: str = Field(..., min_length=4, max_length=6)


@router.put("/password", response_model=APIResponse, summary="Change password")
async def change_password(
    data: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change account password."""
    service = UserService(db)
    success, message = await service.change_password(user.id, data.current_password, data.new_password)
    return APIResponse(success=success, message=message)


@router.put("/pin", response_model=APIResponse, summary="Change PIN")
async def change_pin(
    data: ChangePINRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change account PIN."""
    service = UserService(db)
    success, message = await service.change_pin(user.id, data.current_pin or "", data.new_pin)
    return APIResponse(success=success, message=message)


@router.get("/security-questions", response_model=APIResponse, summary="Get security questions")
async def get_security_questions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's security questions (answers masked)."""
    service = UserService(db)
    questions = await service.get_security_questions(user.id)
    return APIResponse(success=True, message="Security questions retrieved", data=questions)


@router.put("/security-questions", response_model=APIResponse, summary="Update security questions")
async def update_security_questions(
    data: UpdateSecurityQuestionsRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update security questions. Requires password."""
    from app.utils.hashers import check_user_password, hash_user_password
    from sqlalchemy import delete
    
    if not check_user_password(data.password, user.password_hash):
        return APIResponse(success=False, message="Invalid password")
    
    repo = UserRepository(db)
    # Delete old questions
    await db.execute(
        delete(UserSecurityQuestion).where(UserSecurityQuestion.user_id == user.id)
    )
    
    from app.models.user_security_question import UserSecurityQuestion
    for i, (q, a) in enumerate([(data.question_1, data.answer_1), (data.question_2, data.answer_2)], 1):
        sq = UserSecurityQuestion(
            user_id=user.id,
            question_number=i,
            question=q,
            answer_hash=hash_user_password(a.lower().strip()),
        )
        await repo.create_security_question(sq)
    
    await db.commit()
    return APIResponse(success=True, message="Security questions updated")
