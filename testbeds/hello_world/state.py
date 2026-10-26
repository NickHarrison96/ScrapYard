"""Global mutable state – classic anti-pattern used by the circular modules."""

from __future__ import annotations

GLOBAL: dict[str, object] = {
    "initialized": False,
    "request_count": 0,
    "last_user": None,
}


def reset() -> None:
    GLOBAL["initialized"] = False
    GLOBAL["request_count"] = 0
    GLOBAL["last_user"] = None
