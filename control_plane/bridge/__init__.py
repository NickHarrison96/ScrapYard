"""Event bridge between Cytoscape selection events and REA / agent calls."""

from .events import SelectionEvent, GraphPatch, NodeKind
from .bridge import Bridge
from .context import build_agent_context

__all__ = ["SelectionEvent", "GraphPatch", "NodeKind", "Bridge", "build_agent_context"]
