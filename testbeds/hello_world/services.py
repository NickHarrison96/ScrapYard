"""
Services module – intentionally imports from core, completing the cycle.

This is the right half of the circular dependency.
"""

from __future__ import annotations

from testbeds.hello_world import state, config, utils

# Circular: core also imports services
from testbeds.hello_world import core  # noqa: E402


_HANDLERS: dict[str, callable] = {}


def register_handler(name: str, fn: callable) -> None:
    _HANDLERS[name] = fn
    print(utils.helper(f"registered handler {name}"))


def handle(user: str, flags: dict) -> str:
    state.GLOBAL["last_user"] = user
    if flags.get("verbose"):
        print(utils.helper(f"handling {user}"))

    # Reach back into core – the cycle in action
    if not state.GLOBAL.get("initialized"):
        core.init_core()

    result = f"handled:{user}"
    if "core_ready" in _HANDLERS:
        _HANDLERS["core_ready"]({"user": user})
    return result
