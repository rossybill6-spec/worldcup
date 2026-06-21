"""
KYC document endpoints - Upload and view verification documents.
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.kyc_service import KYCService

router = APIRouter()


@router.post("/documents/upload", response_model=APIResponse, summary="Upload KYC document")
async def upload_document(
    document_type: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload a KYC document (driver's license, passport, selfie)."""
    file_data = await file.read()
    service = KYCService(db)
    doc = await service.upload_document(
        user_id=user.id,
        document_type=document_type,
        file_data=file_data,
        file_name=file.filename or "document",
        content_type=file.content_type,
    )
    await db.commit()
    return APIResponse(
        success=True,
        message="Document uploaded",
        data={
            "id": doc.id,
            "document_type": doc.document_type,
            "verification_status": doc.verification_status,
        },
    )


@router.get("/documents", response_model=APIResponse, summary="Get KYC documents")
async def get_documents(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all uploaded KYC documents."""
    service = KYCService(db)
    docs = await service.get_documents(user.id)
    return APIResponse(
        success=True,
        message="Documents retrieved",
        data=[
            {
                "id": d.id,
                "document_type": d.document_type,
                "file_url": d.file_url,
                "file_name": d.file_name,
                "verification_status": d.verification_status,
                "rejection_reason": d.rejection_reason,
                "created_at": d.created_at.isoformat() if d.created_at else None,
            }
            for d in docs
        ],
    )
