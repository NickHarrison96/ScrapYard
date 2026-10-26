"""Typed events that flow through the control plane."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class NodeKind(str, Enum):
    FILE = "file"
    MODULE = "module"
    FUNCTION = "function"
    CLASS = "class"
    CLUSTER = "cluster"
    BASIC_BLOCK = "basic_block"
    SYMBOL = "symbol"


class SelectionEvent(BaseModel):
    """Emitted when the user selects one or more nodes in the Cytoscape canvas."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    node_ids: list[str]
    primary_node_id: str | None = None
    kinds: list[NodeKind] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))


class GraphPatch(BaseModel):
    """Incremental update to the graph after an agent rewrite or indexer run."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: str
    added_nodes: list[dict[str, Any]] = Field(default_factory=list)
    removed_node_ids: list[str] = Field(default_factory=list)
    added_edges: list[dict[str, Any]] = Field(default_factory=list)
    removed_edge_ids: list[str] = Field(default_factory=list)
    updated_node_attrs: dict[str, dict[str, Any]] = Field(default_factory=dict)
    source: str = "agent"  # agent | indexer | user | rea
