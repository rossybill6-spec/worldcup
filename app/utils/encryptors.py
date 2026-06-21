"""
Encryption wrappers for encrypting/decrypting sensitive database fields.
Wraps the core encryption module for easy use in models and services.
"""

from app.core.encryption import encrypt_data, decrypt_data


def encrypt_field(value: str) -> str:
    """Encrypt a sensitive field before storing in database."""
    if not value:
        return value
    return encrypt_data(value)


def decrypt_field(encrypted_value: str) -> str:
    """Decrypt a sensitive field when reading from database."""
    if not encrypted_value:
        return encrypted_value
    return decrypt_data(encrypted_value)


def mask_and_encrypt_ssn(ssn: str) -> dict:
    """
    Encrypt SSN and return both encrypted and masked versions.
    Returns dict with 'encrypted' and 'masked' keys.
    """
    import re
    digits = re.sub(r'\D', '', ssn)
    
    return {
        "encrypted": encrypt_field(digits),
        "masked": f"***-**-{digits[-4:]}" if len(digits) == 9 else "*********",
    }
