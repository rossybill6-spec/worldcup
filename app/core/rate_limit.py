"""
Rate limiting utilities to protect API endpoints.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

# Create a rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        f"{settings.RATE_LIMIT_PER_MINUTE}/minute",
        f"{settings.RATE_LIMIT_PER_HOUR}/hour",
    ],
)


def get_rate_limit_key():
    """Get the rate limit key function."""
    return get_remote_address
