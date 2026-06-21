"""
General helper functions used across the application.
"""

import hashlib
import random
import string
from typing import Optional
from datetime import datetime, timezone


def generate_random_string(length: int = 32, include_special: bool = False) -> str:
    """Generate a cryptographically secure random string."""
    chars = string.ascii_letters + string.digits
    if include_special:
        chars += "!@#$%^&*"
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))


def generate_numeric_code(length: int = 6) -> str:
    """Generate a random numeric code (for OTP, verification, etc.)."""
    return ''.join(str(random.SystemRandom().randint(0, 9)) for _ in range(length))


def hash_sha256(data: str) -> str:
    """Generate SHA256 hash of a string."""
    return hashlib.sha256(data.encode()).hexdigest()


def hash_md5(data: str) -> str:
    """Generate MD5 hash of a string."""
    return hashlib.md5(data.encode()).hexdigest()


def mask_string(value: str, visible_start: int = 4, visible_end: int = 4, mask_char: str = "*") -> str:
    """Mask a string showing only first and last few characters."""
    if not value:
        return ""
    if len(value) <= visible_start + visible_end:
        return mask_char * len(value)
    return value[:visible_start] + mask_char * (len(value) - visible_start - visible_end) + value[-visible_end:]


def parse_boolean(value) -> bool:
    """Parse various boolean representations."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', 'yes', '1', 'on')
    return bool(value)


def safe_get_dict(data: dict, key: str, default=None):
    """Safely get a value from a dict with a default."""
    if not isinstance(data, dict):
        return default
    return data.get(key, default)


def now_utc() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values."""
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    return ((new_value - old_value) / abs(old_value)) * 100


def paginate_list(items: list, page: int = 1, per_page: int = 20) -> dict:
    """Paginate a list in memory (for small datasets)."""
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
    }
