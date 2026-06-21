"""
Storage service - File upload/download management.
"""

from typing import Optional, BinaryIO
import os
from pathlib import Path

from app.core.config import settings


class StorageService:
    """Handles file storage operations."""
    
    @staticmethod
    async def upload(
        file_data: bytes,
        filename: str,
        folder: str = "documents",
        content_type: Optional[str] = None,
    ) -> str:
        """Upload a file and return its path."""
        if settings.STORAGE_TYPE == "s3":
            return await StorageService._upload_s3(file_data, filename, folder, content_type)
        return await StorageService._upload_local(file_data, filename, folder)
    
    @staticmethod
    async def _upload_local(file_data: bytes, filename: str, folder: str) -> str:
        """Upload to local storage."""
        upload_dir = Path(settings.STORAGE_PATH) / folder
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure unique filename
        base, ext = os.path.splitext(filename)
        counter = 1
        final_name = filename
        while (upload_dir / final_name).exists():
            final_name = f"{base}_{counter}{ext}"
            counter += 1
        
        file_path = upload_dir / final_name
        with open(file_path, "wb") as f:
            f.write(file_data)
        
        return f"/uploads/{folder}/{final_name}"
    
    @staticmethod
    async def _upload_s3(file_data: bytes, filename: str, folder: str, content_type: Optional[str] = None) -> str:
        """Upload to S3."""
        import boto3
        
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        
        key = f"{folder}/{filename}"
        s3.put_object(
            Bucket=settings.AWS_BUCKET_NAME,
            Key=key,
            Body=file_data,
            ContentType=content_type or "application/octet-stream",
        )
        
        return f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
