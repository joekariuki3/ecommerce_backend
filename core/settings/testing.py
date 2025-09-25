import os

from .base import BASE_DIR

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            BASE_DIR, f"{os.getenv('TEST_DB_NAME', 'test_db')}.sqlite3"
        ),
    }
}
