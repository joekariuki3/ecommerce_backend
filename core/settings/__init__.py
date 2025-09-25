import os

from dotenv import load_dotenv

from .base import *  # noqa F401, F403

load_dotenv()

ENV = os.getenv("ENVIRONMENT")

if ENV == "production":
    from .production import (
        CSRF_COOKIE_SECURE,
        DEBUG,
        SECURE_BROWSER_XSS_FILTER,
        SECURE_CONTENT_TYPE_NOSNIFF,
        SECURE_SSL_REDIRECT,
        SESSION_COOKIE_SECURE,
    )
elif ENV == "testing":
    from .testing import DATABASES as DATABASES
elif ENV == "staging":
    # No overrides needed, uses the defaults from base.py
    pass
else:
    # Default to development environment
    # No overrides needed, uses the defaults from base.py
    pass

__all__ = [
    "DEBUG",
    "CSRF_COOKIE_SECURE",
    "SESSION_COOKIE_SECURE",
    "SECURE_BROWSER_XSS_FILTER",
    "SECURE_CONTENT_TYPE_NOSNIFF",
    "SECURE_SSL_REDIRECT",
]
