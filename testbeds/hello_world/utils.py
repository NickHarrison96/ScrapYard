"""Shared helpers – no clear owner, called from everywhere."""

from __future__ import annotations

from testbeds.hello_world import state, config


def helper(msg: str) -> str:
    """Overloaded utility that both core and services lean on."""
    prefix = "[DBG] " if config.DEBUG else ""
    state.GLOBAL["request_count"] = int(state.GLOBAL.get("request_count", 0)) + 1
    return f"{prefix}{msg} (#{state.GLOBAL['request_count']})"


def format_user(name: str | None) -> str:
    return name or "anonymous"
