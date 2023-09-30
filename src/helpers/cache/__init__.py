import aioredis
from src.core import settings


async def get_redis_pool():
    """
    Get an AIORedis connection pool.

    This function creates and returns an AIORedis connection pool based on the configuration settings provided
    in the application settings. The pool allows you to efficiently manage connections to a Redis server.

    Returns:
        aioredis.Redis: A connection pool to the Redis server.

    Example usage:

    ```python
    redis_pool = await get_redis_pool()
    async with redis_pool.get() as redis:
        # Use the Redis connection for operations
        value = await redis.get("my_key")
    ```

    """
    redis_pool = aioredis.from_url(
        f"redis://{settings.CACHE['HOST_IP']}:{settings.CACHE['HOST_PORT']}/{settings.CACHE['DB_NUM']}",
        encoding="utf-8",
        decode_responses=True,
    )
    return redis_pool
