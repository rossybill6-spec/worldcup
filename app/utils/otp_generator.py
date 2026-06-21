"""
OTP generator utility.
"""

import random
import hashlib
import time
from typing import Tuple


def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP code."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def generate_totp(secret: str, interval: int = 30) -> Tuple[str, int]:
    """
    Generate a time-based OTP (TOTP).
    
    Args:
        secret: Base32 encoded secret
        interval: Time step in seconds (default 30)
    
    Returns:
        Tuple of (otp_code, remaining_seconds)
    """
    import base64
    import hmac
    import struct
    
    # Decode the secret
    key = base64.b32decode(secret.upper() + '=' * ((8 - len(secret)) % 8))
    
    # Calculate counter
    counter = int(time.time() / interval)
    remaining = interval - (int(time.time()) % interval)
    
    # Generate HMAC
    msg = struct.pack('>Q', counter)
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
    
    # Dynamic truncation
    offset = hmac_hash[-1] & 0x0F
    code = ((hmac_hash[offset] & 0x7F) << 24 |
            (hmac_hash[offset + 1] & 0xFF) << 16 |
            (hmac_hash[offset + 2] & 0xFF) << 8 |
            (hmac_hash[offset + 3] & 0xFF))
    
    otp = str(code % (10 ** 6)).zfill(6)
    return otp, remaining


def verify_otp(user_input: str, generated_otp: str) -> bool:
    """Verify an OTP code (constant-time comparison)."""
    if len(user_input) != len(generated_otp):
        return False
    
    result = 0
    for x, y in zip(user_input, generated_otp):
        result |= ord(x) ^ ord(y)
    return result == 0
