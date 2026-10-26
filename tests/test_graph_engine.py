"""Basic tests for GraphEngine + bounded subgraph extraction."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from control_plane.graph_engine.engine import GraphEngine
from control_plane.bridge.events import GraphPatch


@pytest.fixture
def engine() -> GraphEngine:
    return GraphEngine()


@pytest.fixture
def sample_graph(tmp_path: Path) -> Path:
    data = {
        "nodes": [
            {"id": "a", "label": "A", "kind": "module"},
            {"id": "b", "label": "B", "kind": "module"},
            {"id": "c", "label": "C", "kind": "module"},
            {"id": "f1", "label": "fn1", "kind": "function"},
        ],
        "edges": [
            {"id": "e1", "source": "a", "target": "b"},
            {"id": "e2", "source": "b", "target": "a"},  # cycle
            {"id": "e3", "source": "a", "target": "c"},
            {"id": "e4", "source": "b", "target": "f1"},
        ],
    }
    p = tmp_path / "g.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def test_load_and_counts(engine: GraphEngine, sample_graph: Path) -> None:
    engine.load_from_json(sample_graph)
    assert engine.g.number_of_nodes() == 4
    assert engine.g.number_of_edges() == 4


def test_bounded_subgraph_depth_1(engine: GraphEngine, sample_graph: Path) -> None:
    engine.load_from_json(sample_graph)
    sub = engine.get_bounded_subgraph(["a"], depth=1)
    ids = {n["id"] for n in sub["nodes"]}
    assert "a" in ids
    assert "b" in ids
    assert "c" in ids
    assert "f1" not in ids


def test_apply_patch_removes_cycle(engine: GraphEngine, sample_graph: Path) -> None:
    engine.load_from_json(sample_graph)
    assert engine.g.has_edge("b", "a")

    patch = GraphPatch(
        correlation_id="test-1",
        removed_edge_ids=["e2"],
        source="test",
    )
    engine.apply_patch(patch)
    assert not engine.g.has_edge("b", "a")


def test_cytoscape_export(engine: GraphEngine, sample_graph: Path) -> None:
    engine.load_from_json(sample_graph)
    elements = engine.to_cytoscape_elements()
    assert any(e["data"]["id"] == "a" for e in elements)
    assert any(e["data"].get("source") == "a" for e in elements)
