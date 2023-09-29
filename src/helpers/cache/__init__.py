import aioredis

from src.core import settings


async def get_redis_pool():

    redis_pool = aioredis.from_url(
        f"redis://{settings.CACHE['HOST_IP']}:{settings.CACHE['HOST_PORT']}/{settings.CACHE['DB_NUM']}",
        encoding="utf-8",
        decode_responses=True,
    )
    return redis_pool
