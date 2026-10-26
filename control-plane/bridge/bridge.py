"""Core Bridge – translates UI selection events into REA queries and agent context."""

from __future__ import annotations

import logging
from typing import Any, Callable, Awaitable

from .events import SelectionEvent, GraphPatch

logger = logging.getLogger(__name__)


class Bridge:
    """
    Central event router for the control plane.

    Responsibilities:
    - Receive SelectionEvent from the UI
    - Optionally enrich with REA tool results
    - Package bounded context for the coding agent
    - Accept GraphPatch results and forward them to the graph engine
    """

    def __init__(self) -> None:
        self._selection_handlers: list[Callable[[SelectionEvent], Awaitable[None]]] = []
        self._patch_handlers: list[Callable[[GraphPatch], Awaitable[None]]] = []
        self._rea_client: Any | None = None  # injected later (rea_bridge client)

    def set_rea_client(self, client: Any) -> None:
        self._rea_client = client

    def on_selection(self, handler: Callable[[SelectionEvent], Awaitable[None]]) -> None:
        self._selection_handlers.append(handler)

    def on_patch(self, handler: Callable[[GraphPatch], Awaitable[None]]) -> None:
        self._patch_handlers.append(handler)

    async def handle_selection(self, event: SelectionEvent) -> dict[str, Any]:
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

        context: dict[str, Any] = {
            "selection": event.model_dump(),
            "rea_enrichment": {},
            "bounded_subgraph": None,  # filled by graph engine later
        }

        # Future: call REA tools here based on node kinds
        if self._rea_client is not None:
            # Placeholder – concrete calls will live in rea-bridge
            context["rea_enrichment"] = {"status": "rea_client_ready"}

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
        for handler in self._patch_handlers:
            await handler(patch)
