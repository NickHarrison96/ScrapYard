-- ADRE graph persistence schema (SQLite)
-- Phase 1 baseline – will grow with clustering & audit tables

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS nodes (
    id          TEXT PRIMARY KEY,
    kind        TEXT NOT NULL DEFAULT 'function',  -- file|module|function|class|cluster|basic_block|symbol
    label       TEXT,
    path        TEXT,
    address     TEXT,          -- for binary/CFG nodes
    attrs_json  TEXT NOT NULL DEFAULT '{}',
    cluster_id  TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS edges (
    id          TEXT PRIMARY KEY,
    source_id   TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    target_id   TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    kind        TEXT NOT NULL DEFAULT 'calls',  -- calls|imports|contains|xref|data|control
    attrs_json  TEXT NOT NULL DEFAULT '{}',
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id);
CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id);
CREATE INDEX IF NOT EXISTS idx_nodes_cluster ON nodes(cluster_id);
CREATE INDEX IF NOT EXISTS idx_nodes_kind ON nodes(kind);

CREATE TABLE IF NOT EXISTS graph_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Simple audit / mutation log for the control plane itself
CREATE TABLE IF NOT EXISTS mutation_log (
    id              TEXT PRIMARY KEY,
    correlation_id  TEXT,
    source          TEXT,          -- agent|indexer|user|rea
    patch_json      TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
