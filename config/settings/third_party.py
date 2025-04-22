from .base import DEBUG, INSTALLED_APPS, MIDDLEWARE

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: bool(
            request.headers.get("x-requested-with") != "XMLHttpRequest"
        ),
    }
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
