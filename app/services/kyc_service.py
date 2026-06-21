"""
KYC service - Document upload and verification management.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.user import User
from app.models.user_document import UserDocument
from app.core.storage import upload_file


class KYCService:
    """Handles KYC document uploads and verification."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def upload_document(
        self,
        user_id: str,
        document_type: str,
        file_data: bytes,
        file_name: str,
        content_type: Optional[str] = None,
    ) -> UserDocument:
        """Upload a KYC document."""
        # Upload file to storage
        file_url = await upload_file(file_data, file_name, folder=f"kyc/{user_id}", content_type=content_type)
        
        # Create document record
        doc = UserDocument(
            user_id=user_id,
            document_type=document_type,
            file_url=file_url,
            file_name=file_name,
            file_size=str(len(file_data)),
            verification_status="pending",
        )
        self.db.add(doc)
        
        # Update user KYC status
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                kyc_status="submitted",
                kyc_submitted_at=datetime.utcnow(),
            )
        )
        
        await self.db.flush()
        return doc
    
    async def get_documents(self, user_id: str) -> List[UserDocument]:
        """Get all KYC documents for a user."""
        result = await self.db.execute(
            select(UserDocument).where(
                UserDocument.user_id == user_id,
                UserDocument.is_deleted == False,
            ).order_by(UserDocument.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_kyc_status(self, user_id: str) -> dict:
        """Get KYC status for a user."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            return {"kyc_status": "not_submitted"}
        
        docs = await self.get_documents(user_id)
        
        return {
            "kyc_status": user.kyc_status,
            "kyc_submitted_at": user.kyc_submitted_at.isoformat() if user.kyc_submitted_at else None,
            "kyc_verified_at": user.kyc_verified_at.isoformat() if user.kyc_verified_at else None,
            "kyc_rejection_reason": user.kyc_rejection_reason,
            "documents": [
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
        }
