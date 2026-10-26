"""Config touched by both core and services – creates extra coupling."""

from __future__ import annotations

DEBUG = True
APP_NAME = "hello_spaghetti"
MAX_RETRIES = 3

# Both sides will import and sometimes mutate this at runtime
RUNTIME_FLAGS: dict[str, bool] = {
    "use_cache": True,
    "verbose": False,
}
