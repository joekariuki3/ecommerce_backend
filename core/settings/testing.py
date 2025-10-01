import os

from .base import BASE_DIR
from .logging import LOGGING

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            BASE_DIR, f"{os.getenv('TEST_DB_NAME', 'test_db')}.sqlite3"
        ),
    }
}

if os.getenv("ENABLE_TEST_LOGGING", "false").lower() == "false":
    LOGGING["handlers"]["console"]["class"] = "logging.NullHandler"
else:
    LOGGING["handlers"]["console"]["formatter"] = "simple"
