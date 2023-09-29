import uvicorn
from fastapi import Request
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi_babel.core import make_gettext as _
from fastapi_babel.middleware import InternationalizationMiddleware

from src.core import settings
from src.core.database import Basemodel
from src.core.database import engine
from src.helpers.logger import logger
from src.helpers.logger.models import LogLevel
from src.core.ratelimiter import limiter
from src.core.babel import babel

# API routers
from src.apis.users import router as user_router
from src.apis.recipes import router as recipe_router
from src.apis.relations import router as relation_router

# Application exceptions
from src.core.exceptions import CredentialException
from src.core.exceptions import BadRequestException
from src.core.exceptions import handle_credential_exception
from src.core.exceptions import handle_bad_request_exception
from src.core.exceptions import handle_value_error_exception
from src.core.exceptions import handle_rate_limit_exception

# Application events
from src.core.startup import startup_event


Basemodel.metadata.create_all(engine)

app = FastAPI(
    docs_url=settings.DOCS["swagger"],
    redoc_url=settings.DOCS["redoc"],
)

logger.log(level=LogLevel.INFO, message=dict(data="Application initialized"))  # noqa C408

# Application routers
app.include_router(user_router)
app.include_router(recipe_router)
app.include_router(relation_router)

# Application states
app.state.limiter = limiter

# Application events
app.add_event_handler("startup", startup_event)

# Add exceptions
app.add_exception_handler(ValueError, handle_value_error_exception)
app.add_exception_handler(CredentialException, handle_credential_exception)
app.add_exception_handler(BadRequestException, handle_bad_request_exception)
app.add_exception_handler(RateLimitExceeded, handle_rate_limit_exception)

# Application middlewares
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(InternationalizationMiddleware, babel=babel)


# Add static mount point
if settings.DEBUG:
    app.mount(settings.MEDIA_URL, StaticFiles(directory=settings.MEDIA_ROOT), name="media")


@app.get("/")
def index(request: Request):
    return {"data": _("welcome to FoodRecipeHub!!!")}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.UVICORN["HOST"], port=settings.UVICORN["PORT"])
