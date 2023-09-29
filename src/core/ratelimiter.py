from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core import settings

limiter = Limiter(key_func=get_remote_address, default_limits=settings.RATE_LIMIT["default_limits"], enabled=not settings.DEBUG)


@limiter.limit(settings.RATE_LIMIT["router_limits"]["recipes"])
def recipes_rate_limit_depends(request: Request):
    return None
