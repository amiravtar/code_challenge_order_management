import pathlib

from .base import BASE_DIR

LOGGING_LEVEL = "DEBUG"
LOGGING_DIR = "logs"
if not (log_path := BASE_DIR / LOGGING_DIR).exists():
    log_path.mkdir(parents=True, exist_ok=True)
for file in {"general.log", "app.log"}:
    if not (log_path / file).exists():
        (log_path / file).touch()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file_general": {
            "level": LOGGING_LEVEL,
            "class": "logging.FileHandler",
            "filename": BASE_DIR / LOGGING_DIR / "general.log",
            "formatter": "file",
        },
        "file_app": {
            "level": LOGGING_LEVEL,
            "class": "logging.FileHandler",
            "filename": BASE_DIR / LOGGING_DIR / "app.log",
            "formatter": "file",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "level": LOGGING_LEVEL,
        },
    },
    "formatters": {
        "console": {"format": "%(name)-12s %(levelname)-8s %(message)s"},
        "file": {
            "format": "%(asctime)s %(name)-12s %(filename)-5s %(funcName)-5s %(levelname)-8s %(message)s"
        },
    },
    "loggers": {
        "": {
            "handlers": ["file_general"],
            "level": LOGGING_LEVEL,
        },
        "app": {
            "handlers": ["file_app", "console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
    },
}
