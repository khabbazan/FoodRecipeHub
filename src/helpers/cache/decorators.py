import json
from functools import wraps
from src.core import settings
from src.helpers.logger import logger
from src.helpers.logger.models import LogLevel
from src.helpers.cache import get_redis_pool


def cache(cache_key, timeout=settings.CACHE["DEFAULT_EXPIRE_TIME"]):
    """
    Decorator for caching function results.

    This decorator caches the results of a function in Redis based on a specified cache key.
    If the result is found in the cache, it is returned; otherwise, the function is executed,
    and the result is cached for future use.

    Args:
        cache_key (str): The cache key used to store and retrieve the result.
        timeout (int): The expiration time for the cache entry in seconds (default is from settings).

    Returns:
        decorator: The cache decorator.

    Example usage:

    ```python
    @cache("my_function_cache_key", timeout=3600)
    async def my_function(...):
        # Function logic here
    ```

    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            if not settings.DEBUG:

                redis = await get_redis_pool()

                cache_key_kwargs = {k: v for k, v in kwargs.items() if k != "session"}
                cache_key_full = f"{settings.CACHE['PREFIX']}{cache_key}:{args}{cache_key_kwargs}"

                result = await redis.get(cache_key_full)

                if result is None:
                    result = await func(*args, **kwargs)
                    result = json.dumps(result)
                    await redis.setex(cache_key_full, timeout, result)

                    logger.log(
                        level=LogLevel.INFO,
                        message=f"CACHE-> {cache_key_full}:{result} ({timeout})",
                    )

                else:
                    logger.log(
                        level=LogLevel.INFO,
                        message=f"USE CACHE-> {cache_key_full}:{result}",
                    )

                result = json.loads(result)

            else:
                result = await func(*args, **kwargs)

            return result

        return wrapper

    return decorator


def expire_cache(cache_keys):
    """
    Decorator for expiring cache entries.

    This decorator wraps a function and allows you to specify cache keys that should be
    invalidated (removed) after the wrapped function is executed.

    Args:
        cache_keys (list): A list of cache keys to be invalidated.

    Returns:
        decorator: The expire cache decorator.

    Example usage:

    ```python
    @expire_cache(["my_function_cache_key"])
    async def my_function(...):
        # Function logic here
    ```

    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            result = await func(*args, **kwargs)

            if cache_keys:
                redis = await get_redis_pool()
                for cache_key in cache_keys:
                    candidate_keys = [key async for key in redis.scan_iter(f"{settings.CACHE['PREFIX']}{cache_key}:*")]
                    if candidate_keys:
                        await redis.delete(*candidate_keys)
                        logger.log(
                            level=LogLevel.INFO,
                            message=f"REMOVE CACHE-> {[*candidate_keys]}",
                        )

            return result

        return wrapper

    return decorator
