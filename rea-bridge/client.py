"""
REA client skeleton.

In production this will talk to the local REA MCP server
(installed via `npx rea-agents setup`). For Phase 1 we keep
a clean async interface that the Bridge can call.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ReaClient:
    """
    Async façade over REA tools.

    Concrete methods will be added as we wire real MCP calls:
    - get_xrefs(symbol)
    - get_cfg(function_address)
    - get_pseudocode(function)
    - analyze_module(path)
    - etc.
    """

    def __init__(self, mcp_endpoint: str | None = None) -> None:
        self.mcp_endpoint = mcp_endpoint or "local"
        self._ready = False

    async def connect(self) -> None:
        """Establish connection / health-check against the REA MCP server."""
        # TODO: real MCP handshake
        logger.info("ReaClient connecting to %s (stub)", self.mcp_endpoint)
        self._ready = True

    @property
    def ready(self) -> bool:
        return self._ready

    async def health(self) -> dict[str, Any]:
        return {
            "status": "ok" if self._ready else "not_connected",
            "endpoint": self.mcp_endpoint,
            "note": "Phase 1 stub – real MCP integration coming next",
        }

    # ---- Placeholder tool methods (will be replaced by real REA calls) ----

    async def get_symbol_xrefs(self, symbol: str) -> dict[str, Any]:
        logger.debug("get_symbol_xrefs(%s) – stub", symbol)
        return {"symbol": symbol, "xrefs": [], "stub": True}

    async def get_module_boundaries(self, path: str) -> dict[str, Any]:
        logger.debug("get_module_boundaries(%s) – stub", path)
        return {"path": path, "boundaries": [], "stub": True}
