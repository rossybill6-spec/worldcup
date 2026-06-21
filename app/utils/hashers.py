"""
Hashing wrapper utilities for passwords, PINs, and tokens.
"""

from app.core.security import hash_password, verify_password, hash_pin, verify_pin

BCRYPT_MAX_LENGTH = 72


def hash_user_password(password: str) -> str:
    """Hash a user password for storage."""
    if len(password) > BCRYPT_MAX_LENGTH:
        password = password[:BCRYPT_MAX_LENGTH]
    return hash_password(password)


def check_user_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plain password against its hash."""
    if len(plain_password) > BCRYPT_MAX_LENGTH:
        plain_password = plain_password[:BCRYPT_MAX_LENGTH]
    return verify_password(plain_password, hashed_password)


def hash_user_pin(pin: str) -> str:
    """Hash a numeric PIN for storage."""
    return hash_pin(pin)


def check_user_pin(plain_pin: str, hashed_pin: str) -> bool:
    """Check a plain PIN against its hash."""
    return verify_pin(plain_pin, hashed_pin)
