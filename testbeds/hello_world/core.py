"""
Core module – intentionally imports from services, creating a cycle.

This is the left half of the circular dependency the agent must break.
"""

from __future__ import annotations

from testbeds.hello_world import state, config, utils

# Circular: services also imports core
from testbeds.hello_world import services  # noqa: E402


def init_core() -> None:
    state.GLOBAL["initialized"] = True
    print(utils.helper("core initialized"))
    # Reach into services – tight coupling
    services.register_handler("core_ready", _on_ready)


def _on_ready(payload: dict) -> None:
    state.GLOBAL["last_user"] = payload.get("user")
    print(utils.helper(f"core saw ready for {utils.format_user(payload.get('user'))}"))


def process_request(user: str) -> str:
    if not state.GLOBAL.get("initialized"):
        init_core()
    # Direct call into services instead of an interface
    return services.handle(user, config.RUNTIME_FLAGS)
