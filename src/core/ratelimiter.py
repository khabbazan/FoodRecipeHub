from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.core import settings

limiter = Limiter(key_func=get_remote_address, default_limits=settings.RATE_LIMIT["default_limits"], enabled=not settings.DEBUG)


@limiter.limit(settings.RATE_LIMIT["router_limits"]["recipes"])
def recipes_rate_limit_depends(request: Request):
    """
    Rate limiting dependency for the 'recipes' endpoint.

    This dependency is used to apply rate limiting to the 'recipes' endpoint based on the configured limits
    specified in the application settings.

    Args:
        request (Request): The incoming request object.

    Returns:
        None: This dependency returns None, and the rate limiting is applied to the endpoint.

    Example usage:

    ```python
    from fastapi import APIRouter, Depends
    from src.core.ratelimiter import recipes_rate_limit_depends

    router = APIRouter(
        prefix="/recipe",
        tags=["Recipe"],
        responses={404: {"detail": "Not found"}},
        dependencies=[Depends(recipes_rate_limit_depends)],
    )
    ```
    """
    return None
