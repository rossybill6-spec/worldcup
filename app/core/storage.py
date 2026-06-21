"""
File storage utilities. Supports local filesystem and AWS S3.
"""

import os
from typing import Optional, BinaryIO
from pathlib import Path

from app.core.config import settings


async def upload_file(
    file_data: bytes,
    filename: str,
    folder: str = "documents",
    content_type: Optional[str] = None,
) -> str:
    """
    Upload a file and return its path/URL.
    
    Args:
        file_data: File bytes
        filename: Desired filename
        folder: Storage folder
        content_type: MIME type
    
    Returns:
        File path or URL
    """
    if settings.STORAGE_TYPE == "s3":
        return await _upload_to_s3(file_data, filename, folder, content_type)
    return await _upload_to_local(file_data, filename, folder)


async def _upload_to_local(file_data: bytes, filename: str, folder: str) -> str:
    """Upload file to local storage."""
    upload_dir = Path(settings.STORAGE_PATH) / folder
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / filename
    with open(file_path, "wb") as f:
        f.write(file_data)
    
    return str(file_path)


async def _upload_to_s3(
    file_data: bytes,
    filename: str,
    folder: str,
    content_type: Optional[str] = None,
) -> str:
    """Upload file to AWS S3."""
    import boto3
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
    
    key = f"{folder}/{filename}"
    s3_client.put_object(
        Bucket=settings.AWS_BUCKET_NAME,
        Key=key,
        Body=file_data,
        ContentType=content_type or "application/octet-stream",
    )
    
    return f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"


async def delete_file(file_path: str) -> bool:
    """Delete a file from storage."""
    if settings.STORAGE_TYPE == "s3":
        return await _delete_from_s3(file_path)
    return await _delete_from_local(file_path)


async def _delete_from_local(file_path: str) -> bool:
    """Delete a file from local storage."""
    try:
        os.remove(file_path)
        return True
    except FileNotFoundError:
        return False


async def _delete_from_s3(file_path: str) -> bool:
    """Delete a file from AWS S3."""
    import boto3
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
    
    # Extract key from URL
    key = file_path.split(f"{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/")[-1]
    s3_client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=key)
    return True
