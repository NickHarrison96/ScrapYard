"""Tests for typed events and context packaging."""

from __future__ import annotations

import pytest

from control_plane.bridge.events import SelectionEvent, GraphPatch, NodeKind
from control_plane.bridge.context import build_agent_context
from control_plane.graph_engine.engine import GraphEngine


def test_selection_event_defaults() -> None:
    ev = SelectionEvent(node_ids=["mod_a", "mod_b"])
    assert ev.primary_node_id is None
    assert len(ev.correlation_id) > 8
    assert ev.id != ev.correlation_id


def test_graph_patch_roundtrip() -> None:
    p = GraphPatch(
        correlation_id="c1",
        added_nodes=[{"id": "x", "kind": "function"}],
        removed_edge_ids=["e9"],
        source="agent",
    )
    data = p.model_dump()
    assert data["source"] == "agent"
    assert data["added_nodes"][0]["id"] == "x"


def test_build_agent_context() -> None:
    eng = GraphEngine()
    eng.g.add_node("a", label="A", kind="module")
    eng.g.add_node("b", label="B", kind="module")
    eng.g.add_edge("a", "b", id="e1")

    ev = SelectionEvent(node_ids=["a"], kinds=[NodeKind.MODULE])
    ctx = build_agent_context(ev, eng, depth=1)

    assert ctx["correlation_id"] == ev.correlation_id
    assert ctx["node_count"] == 2
    assert "bounded_subgraph" in ctx
    assert "instructions" in ctx
