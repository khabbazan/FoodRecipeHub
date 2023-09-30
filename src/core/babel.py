"""
This module configures and initializes Babel for internationalization and localization support in the FastAPI application.

fastapi_babel is a library that helps with translations and formatting of messages for different languages and locales.

Attributes:
    configs (BabelConfigs): An instance of BabelConfigs containing configuration settings for Babel.
    babel (Babel): An initialized Babel instance for the FastAPI application.

Example usage:

    from fastapi_babel import _

    # Get a translated message
    translated_message = _("Hello, World!")
"""

from fastapi_babel import Babel
from fastapi_babel import BabelConfigs
from src.core import settings

# Create BabelConfigs instance with the provided settings.
configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE=settings.LANGUAGE["default"],
    BABEL_TRANSLATION_DIRECTORY=settings.LANGUAGE["dir"],
)

# Initialize Babel with the configured BabelConfigs.
babel = Babel(configs=configs)
