from .logging import LOGGING

DEBUG = False

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True

LOGGING["handlers"]["console"]["formatter"] = "json_formatter"
