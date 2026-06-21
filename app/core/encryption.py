"""
Encryption utilities for sensitive data (SSN, card numbers, etc.).
Uses Fernet symmetric encryption.
"""

from cryptography.fernet import Fernet
import base64
import hashlib

from app.core.config import settings


def _get_cipher() -> Fernet:
    """Get a Fernet cipher instance using the encryption key."""
    # Ensure key is 32 bytes for Fernet
    key = hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key)
    return Fernet(fernet_key)


def encrypt_data(plain_text: str) -> str:
    """
    Encrypt a string value.
    
    Args:
        plain_text: The text to encrypt
    
    Returns:
        Encrypted string (base64 encoded)
    """
    if not plain_text:
        return plain_text
    cipher = _get_cipher()
    encrypted = cipher.encrypt(plain_text.encode())
    return encrypted.decode()


def decrypt_data(encrypted_text: str) -> str:
    """
    Decrypt an encrypted string value.
    
    Args:
        encrypted_text: The encrypted text to decrypt
    
    Returns:
        Original plain text
    """
    if not encrypted_text:
        return encrypted_text
    cipher = _get_cipher()
    decrypted = cipher.decrypt(encrypted_text.encode())
    return decrypted.decode()
