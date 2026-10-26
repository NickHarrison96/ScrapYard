"""Context packaging – turns a SelectionEvent + GraphEngine into an agent-ready payload."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from control_plane.bridge.events import SelectionEvent

if TYPE_CHECKING:
    from control_plane.graph_engine.engine import GraphEngine


def build_agent_context(
    event: SelectionEvent,
    engine: "GraphEngine",
    *,
    depth: int = 1,
    rea_enrichment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Produce the bounded context package that gets handed to the coding agent.

    This is the critical token-control boundary: the agent only ever sees
    the selected nodes + their immediate neighbourhood, never the whole graph.
    """
    subgraph = engine.get_bounded_subgraph(event.node_ids, depth=depth)

    return {
        "correlation_id": event.correlation_id,
        "selection": {
            "node_ids": event.node_ids,
            "primary_node_id": event.primary_node_id or (event.node_ids[0] if event.node_ids else None),
            "kinds": [k.value if hasattr(k, "value") else k for k in event.kinds],
            "metadata": event.metadata,
        },
        "bounded_subgraph": subgraph,
        "node_count": len(subgraph.get("nodes", [])),
        "edge_count": len(subgraph.get("edges", [])),
        "rea_enrichment": rea_enrichment or {},
        "instructions": (
            "You are constrained to the supplied bounded_subgraph. "
            "Do not request files or symbols outside this context. "
            "Use REA tools for any cross-reference questions. "
            "When finished, emit a GraphPatch description of structural changes."
        ),
    }
