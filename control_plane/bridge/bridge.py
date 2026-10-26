"""Core Bridge – translates UI selection events into REA queries and agent context."""

from __future__ import annotations

import logging
from typing import Any, Callable, Awaitable

from .events import SelectionEvent, GraphPatch
from .context import build_agent_context

logger = logging.getLogger(__name__)


class Bridge:
    """
    Central event router for the control plane.

    Responsibilities:
    - Receive SelectionEvent from the UI
    - Optionally enrich with REA tool results
    - Package bounded context for the coding agent (via GraphEngine)
    - Accept GraphPatch results and forward them to the graph engine
    """

    def __init__(self) -> None:
        self._selection_handlers: list[Callable[[SelectionEvent], Awaitable[None]]] = []
        self._patch_handlers: list[Callable[[GraphPatch], Awaitable[None]]] = []
        self._rea_client: Any | None = None
        self._graph_engine: Any | None = None  # GraphEngine instance

    def set_rea_client(self, client: Any) -> None:
        self._rea_client = client

    def set_graph_engine(self, engine: Any) -> None:
        self._graph_engine = engine

    def on_selection(self, handler: Callable[[SelectionEvent], Awaitable[None]]) -> None:
        self._selection_handlers.append(handler)

    def on_patch(self, handler: Callable[[GraphPatch], Awaitable[None]]) -> None:
        self._patch_handlers.append(handler)

    async def handle_selection(self, event: SelectionEvent, *, depth: int = 1) -> dict[str, Any]:
        """
        Main entry point called by the UI when the user selects nodes.

        Returns a context package that can be handed to an agent prompt.
        """
        logger.info(
            "SelectionEvent %s – nodes=%s correlation=%s",
            event.id,
            event.node_ids,
            event.correlation_id,
        )

        rea_enrichment: dict[str, Any] = {}
        if self._rea_client is not None and getattr(self._rea_client, "ready", False):
            rea_enrichment = {
                "status": "rea_client_ready",
                "endpoint": getattr(self._rea_client, "mcp_endpoint", "local"),
            }

        if self._graph_engine is not None:
            context = build_agent_context(
                event,
                self._graph_engine,
                depth=depth,
                rea_enrichment=rea_enrichment,
            )
        else:
            context = {
                "correlation_id": event.correlation_id,
                "selection": event.model_dump(),
                "bounded_subgraph": None,
                "rea_enrichment": rea_enrichment,
                "warning": "graph_engine not attached",
            }

        for handler in self._selection_handlers:
            await handler(event)

        return context

    async def apply_patch(self, patch: GraphPatch) -> None:
        """Called after an agent (or indexer) has modified the codebase / graph."""
        logger.info(
            "GraphPatch %s – source=%s correlation=%s",
            patch.id,
            patch.source,
            patch.correlation_id,
        )
        if self._graph_engine is not None:
            self._graph_engine.apply_patch(patch)
        for handler in self._patch_handlers:
            await handler(patch)
