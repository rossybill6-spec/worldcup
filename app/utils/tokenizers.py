"""
Token generation and verification utilities.
Wraps the core security module for JWT operations.
"""

from typing import Dict, Any, Optional
from datetime import timedelta

from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.config import settings


def generate_access_token(user_id: str, email: str, extra_data: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate an access token for a user.
    
    Args:
        user_id: User's unique ID
        email: User's email
        extra_data: Any additional data to include in token
    
    Returns:
        JWT access token string
    """
    payload = {
        "sub": user_id,
        "email": email,
    }
    if extra_data:
        payload.update(extra_data)
    
    return create_access_token(
        data=payload,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def generate_refresh_token_for_user(user_id: str, email: str) -> str:
    """
    Generate a refresh token for a user.
    
    Args:
        user_id: User's unique ID
        email: User's email
    
    Returns:
        JWT refresh token string
    """
    payload = {
        "sub": user_id,
        "email": email,
    }
    return create_refresh_token(
        data=payload,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Token payload dict or None if invalid/expired
    """
    return decode_token(token)


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        User ID string or None
    """
    payload = decode_token(token)
    if payload:
        return payload.get("sub")
    return None


def generate_admin_access_token(admin_id: str, email: str, role: str) -> str:
    """
    Generate an access token for an admin user.
    
    Args:
        admin_id: Admin's unique ID
        email: Admin's email
        role: Admin's role name
    
    Returns:
        JWT access token string
    """
    payload = {
        "sub": admin_id,
        "email": email,
        "role": role,
        "is_admin": True,
    }
    return create_access_token(
        data=payload,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
