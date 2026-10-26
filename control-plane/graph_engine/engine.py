"""Graph engine – NetworkX core + hierarchical clustering stubs."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import networkx as nx

from control_plane.bridge.events import GraphPatch, NodeKind

logger = logging.getLogger(__name__)


class GraphEngine:
    """
    In-memory graph + persistence helpers.

    Phase 1: pure NetworkX + simple JSON dump/load.
    Later: SQLite backing store, Louvain/Leiden clustering, hierarchical views.
    """

    def __init__(self) -> None:
        self.g: nx.DiGraph = nx.DiGraph()
        self._cluster_cache: dict[str, list[str]] = {}

    def clear(self) -> None:
        self.g.clear()
        self._cluster_cache.clear()

    def load_from_json(self, path: Path | str) -> None:
        """Load a Cytoscape-compatible or simple node/edge JSON."""
        import json

        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        self.clear()

        # Accept either {"nodes": [...], "edges": [...]} or Cytoscape elements format
        if "elements" in data:
            elements = data["elements"]
            nodes = elements.get("nodes", [])
            edges = elements.get("edges", [])
        else:
            nodes = data.get("nodes", [])
            edges = data.get("edges", [])

        for n in nodes:
            nid = n.get("data", n).get("id")
            if nid is None:
                continue
            attrs = n.get("data", n)
            self.g.add_node(nid, **{k: v for k, v in attrs.items() if k != "id"})

        for e in edges:
            ed = e.get("data", e)
            src, tgt = ed.get("source"), ed.get("target")
            if src and tgt:
                eid = ed.get("id", f"{src}->{tgt}")
                self.g.add_edge(src, tgt, id=eid, **{k: v for k, v in ed.items() if k not in ("source", "target", "id")})

        logger.info("Loaded graph: %d nodes, %d edges", self.g.number_of_nodes(), self.g.number_of_edges())

    def apply_patch(self, patch: GraphPatch) -> None:
        for nid in patch.removed_node_ids:
            if self.g.has_node(nid):
                self.g.remove_node(nid)
        for n in patch.added_nodes:
            nid = n.get("id")
            if nid:
                self.g.add_node(nid, **{k: v for k, v in n.items() if k != "id"})
        for eid in patch.removed_edge_ids:
            # naive – improve later
            for u, v, data in list(self.g.edges(data=True)):
                if data.get("id") == eid:
                    self.g.remove_edge(u, v)
                    break
        for e in patch.added_edges:
            src, tgt = e.get("source"), e.get("target")
            if src and tgt:
                self.g.add_edge(src, tgt, **{k: v for k, v in e.items() if k not in ("source", "target")})
        for nid, attrs in patch.updated_node_attrs.items():
            if self.g.has_node(nid):
                self.g.nodes[nid].update(attrs)

    def get_bounded_subgraph(self, node_ids: list[str], depth: int = 1) -> dict[str, Any]:
        """Return a small subgraph around the selected nodes for agent context."""
        if not node_ids:
            return {"nodes": [], "edges": []}

        keep: set[str] = set(node_ids)
        for nid in node_ids:
            if not self.g.has_node(nid):
                continue
            keep.update(nx.ego_graph(self.g, nid, radius=depth).nodes)

        sub = self.g.subgraph(keep).copy()
        nodes = [{"id": n, **dict(d)} for n, d in sub.nodes(data=True)]
        edges = [
            {"id": d.get("id", f"{u}->{v}"), "source": u, "target": v, **{k: v_ for k, v_ in d.items() if k != "id"}}
            for u, v, d in sub.edges(data=True)
        ]
        return {"nodes": nodes, "edges": edges}

    def to_cytoscape_elements(self) -> list[dict[str, Any]]:
        """Export current graph in Cytoscape.js elements format."""
        elements: list[dict[str, Any]] = []
        for n, d in self.g.nodes(data=True):
            elements.append({"data": {"id": n, **d}})
        for u, v, d in self.g.edges(data=True):
            eid = d.get("id", f"{u}->{v}")
            elements.append({"data": {"id": eid, "source": u, "target": v, **{k: val for k, val in d.items() if k != "id"}}})
        return elements
