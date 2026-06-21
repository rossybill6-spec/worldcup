"""
Beneficiary management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.core.database import get_db
from app.schemas.user_beneficiary import CreateBeneficiaryRequest, UpdateBeneficiaryRequest, BeneficiaryResponse
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_beneficiary import UserBeneficiary

router = APIRouter()


@router.get("/beneficiaries", response_model=APIResponse, summary="List beneficiaries")
async def list_beneficiaries(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all saved beneficiaries."""
    result = await db.execute(
        select(UserBeneficiary).where(
            UserBeneficiary.user_id == user.id,
            UserBeneficiary.is_deleted == False,
        )
    )
    beneficiaries = result.scalars().all()
    return APIResponse(
        success=True,
        message="Beneficiaries retrieved",
        data=[
            {
                "id": b.id, "name": b.name, "account_number": b.account_number,
                "routing_number": b.routing_number, "bank_name": b.bank_name,
                "email": b.email, "phone": b.phone, "relationship": b.relationship,
                "nickname": b.nickname, "created_at": b.created_at.isoformat() if b.created_at else None,
            }
            for b in beneficiaries
        ],
    )


@router.post("/beneficiaries", response_model=APIResponse, status_code=status.HTTP_201_CREATED, summary="Add beneficiary")
async def add_beneficiary(
    data: CreateBeneficiaryRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a new beneficiary."""
    beneficiary = UserBeneficiary(user_id=user.id, **data.model_dump())
    db.add(beneficiary)
    await db.commit()
    await db.refresh(beneficiary)
    return APIResponse(success=True, message="Beneficiary added", data={"id": beneficiary.id})


@router.put("/beneficiaries/{beneficiary_id}", response_model=APIResponse, summary="Update beneficiary")
async def update_beneficiary(
    beneficiary_id: str,
    data: UpdateBeneficiaryRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a beneficiary."""
    result = await db.execute(
        select(UserBeneficiary).where(
            UserBeneficiary.id == beneficiary_id,
            UserBeneficiary.user_id == user.id,
        )
    )
    beneficiary = result.scalar_one_or_none()
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(beneficiary, key, value)
    
    await db.commit()
    return APIResponse(success=True, message="Beneficiary updated")


@router.delete("/beneficiaries/{beneficiary_id}", response_model=APIResponse, summary="Delete beneficiary")
async def delete_beneficiary(
    beneficiary_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a beneficiary."""
    result = await db.execute(
        select(UserBeneficiary).where(
            UserBeneficiary.id == beneficiary_id,
            UserBeneficiary.user_id == user.id,
        )
    )
    beneficiary = result.scalar_one_or_none()
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    
    beneficiary.is_deleted = True
    await db.commit()
    return APIResponse(success=True, message="Beneficiary deleted")
