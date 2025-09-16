from .base import *
import os

print(f"ENV: Testing Environment being used")

DEBUG = os.getenv('DEBUG')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, f"{os.getenv('TEST_DB_NAME')}.sqlite3"),
    }
}