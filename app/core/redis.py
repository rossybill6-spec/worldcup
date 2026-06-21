"""
Redis connection setup for caching, rate limiting, and session storage.
"""

import redis.asyncio as redis
from typing import Optional

from app.core.config import settings

redis_client: Optional[redis.Redis] = None


async def init_redis() -> None:
    """Initialize Redis connection."""
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        await redis_client.ping()
        print("Redis connected")
    except Exception as e:
        print(f"Redis connection failed: {e}")
        redis_client = None


async def close_redis() -> None:
    """Close Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


async def get_redis() -> Optional[redis.Redis]:
    """Get the Redis client. Returns None if Redis is unavailable."""
    global redis_client
    if redis_client is None:
        try:
            await init_redis()
        except Exception:
            pass
    return redis_client


async def cache_get(key: str) -> Optional[str]:
    """Get a value from cache."""
    client = await get_redis()
    if client:
        return await client.get(key)
    return None


async def cache_set(key: str, value: str, expire_seconds: int = 3600) -> bool:
    """Set a value in cache with expiration."""
    client = await get_redis()
    if client:
        await client.set(key, value, ex=expire_seconds)
        return True
    return False


async def cache_delete(key: str) -> bool:
    """Delete a value from cache."""
    client = await get_redis()
    if client:
        await client.delete(key)
        return True
    return False
