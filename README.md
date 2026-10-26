# Agent-Driven Refactoring Engine (ADRE)

**Control plane + REA-powered visual refactoring platform**

Local command center that lets coding agents systematically reverse-engineer, understand, and refactor large codebases (source and binaries) under strict visual + evidence-based guidance.

## Vision
Turn the "inspect → understand → rewrite → verify" loop into a reliable, auditable, saleable engineering system.  
Start with a clean local skeleton, prove the closed loop on toy projects, graduate to binaries, then scale to multi-GB codebases via hierarchical clustering and bounded-context agent work.

## Core Principles
- Bottom-up, never lose footing
- Semi-regular top-to-bottom codebase audits (architecture, deps, performance, security, prompts, expansion backlog)
- Continuous improvement & expansion mindset
- Every change leaves measurable evidence and graph consistency

## Repository Layout

```
.
├── control-plane/          # PySide6 desktop shell + graph UI + local services
│   ├── ui/                 # PySide6 + QWebEngineView + Cytoscape.js canvas
│   ├── bridge/             # Selection events → REA queries / agent hand-off
│   ├── graph_engine/       # NetworkX / community detection / hierarchical views
│   └── db/                 # SQLite schema + migrations + graph persistence
├── rea-bridge/             # Thin Python wrappers & typed clients around REA MCP
├── testbeds/
│   ├── hello_world/        # Controlled multi-file spaghetti (Phase 2)
│   └── binaries/           # Small compiled targets (Phase 3)
├── prompts/                # Versioned agent prompts & evaluation harness
├── docs/
│   ├── architecture/       # Living system design
│   ├── adrs/               # Architecture Decision Records
│   └── audits/             # Phase / monthly audit reports
├── scripts/                # Dev, indexing, audit helpers
├── tests/                  # Unit + integration + agent-in-loop tests
└── ScrapYard/              # Experimental / throwaway work
```

## Quick Start (Phase 0/1)

```bash
# From project root
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Launch control plane (once implemented)
python -m control_plane.ui.main
```

REA itself is installed separately via the official channel:

```bash
npx rea-agents@latest setup
```

## Phase Roadmap (Summary)
1. **Skeleton** – PySide6 + Cytoscape + SQLite/NetworkX + REA bridge
2. **Hello World** – Multi-file circular-dependency testbed + live agent loop
3. **Binaries** – CFG / pseudocode ingestion + reconstruction
4. **1.6 GB scale** – Louvain/Leiden clustering, hierarchical drill-down, vertical slices

## Audit Cadence
- End of every phase
- After every major cluster/subsystem refactor
- Standing monthly (or per-release) full top-to-bottom audit

Reports live in `docs/audits/`.

## Status
Phase 0 scaffolding complete. Phase 1 skeleton under active construction.
