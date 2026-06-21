"""
Security utilities: password hashing, JWT token creation and verification.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# bcrypt max password length is 72 bytes
BCRYPT_MAX_LENGTH = 72


def hash_password(password: str) -> str:
    """Hash a password using bcrypt. Truncates to 72 chars if needed."""
    if len(password) > BCRYPT_MAX_LENGTH:
        password = password[:BCRYPT_MAX_LENGTH]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    if len(plain_password) > BCRYPT_MAX_LENGTH:
        plain_password = plain_password[:BCRYPT_MAX_LENGTH]
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify a JWT token. Returns payload or None if invalid."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None


def hash_pin(pin: str) -> str:
    """Hash a numeric PIN using bcrypt."""
    return pwd_context.hash(pin)


def verify_pin(plain_pin: str, hashed_pin: str) -> bool:
    """Verify a plain PIN against its hash."""
    return pwd_context.verify(plain_pin, hashed_pin)
