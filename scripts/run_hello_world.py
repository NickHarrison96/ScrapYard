#!/usr/bin/env python3
"""Quick runner for the Phase 2 hello_world testbed (from project root)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from testbeds.hello_world.main import run


if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "alice"
    run(user)
