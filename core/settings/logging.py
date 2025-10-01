import os


def get_log_level():
    """Get the appropriate log level based on environment variables."""
    # Check if INFO logs are explicitly disabled
    if os.getenv("ENABLE_INFO_LOGS", "true").lower() == "false":
        return "WARNING"  # Skip INFO and DEBUG, only show WARNING and above

    # Get the general log level, default to INFO
    return os.getenv("LOG_LEVEL", "INFO").upper()


def get_django_log_level():
    """Get log level specifically for Django framework logs."""
    return os.getenv("DJANGO_LOG_LEVEL", get_log_level()).upper()


def get_apps_log_level():
    """Get log level specifically for custom app logs."""
    return os.getenv("APPS_LOG_LEVEL", get_log_level()).upper()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "class": "pythonjsonlogger.json.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(lineno)d %(pathname)s",
        },
        "simple": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "detailed": {
            "format": "{levelname} {asctime} {name} {module} {funcName}:{lineno} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": get_log_level(),  # Handler-level filtering
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": get_django_log_level(),
            "propagate": True,
        },
        "apps": {
            "handlers": ["console"],
            "level": get_apps_log_level(),
            "propagate": True,
        },
        # logger for third-party packages
        "urllib3": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
