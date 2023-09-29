from fastapi_babel import Babel
from fastapi_babel import BabelConfigs

from src.core import settings

configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE=settings.LANGUAGE["default"],
    BABEL_TRANSLATION_DIRECTORY=settings.LANGUAGE["dir"],
)
babel = Babel(configs=configs)
