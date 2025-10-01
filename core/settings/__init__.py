import os

from dotenv import load_dotenv

load_dotenv()

from .base import *  # noqa

ENV = os.getenv("ENVIRONMENT", "development")

if ENV == "production":
    from .production import CSRF_COOKIE_SECURE as CSRF_COOKIE_SECURE
    from .production import DEBUG as DEBUG
    from .production import LOGGING as LOGGING
    from .production import SECURE_BROWSER_XSS_FILTER as SECURE_BROWSER_XSS_FILTER
    from .production import SECURE_CONTENT_TYPE_NOSNIFF as SECURE_CONTENT_TYPE_NOSNIFF
    from .production import SECURE_SSL_REDIRECT as SECURE_SSL_REDIRECT
    from .production import SESSION_COOKIE_SECURE as SESSION_COOKIE_SECURE
elif ENV == "testing":
    from .testing import DATABASES as DATABASES
    from .testing import LOGGING as LOGGING
else:
    # Default to development
    from .development import DEBUG as DEBUG
    from .development import LOGGING as LOGGING
