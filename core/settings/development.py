import os

from .logging import LOGGING

DEBUG = True

LOGGING["handlers"]["console"]["formatter"] = "simple"

if os.getenv("DEBUG_LOGGING", "false").lower() == "true":
    LOGGING["handlers"]["console"]["formatter"] = "detailed"

CORS_ALLOW_ALL_ORIGINS = True
