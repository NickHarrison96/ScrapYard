# Phase 2 Testbed – Hello World (Intentional Spaghetti)

Controlled multi-file Python project with deliberate design flaws so we can
prove the ADRE closed loop:

- Circular imports between modules
- Tight coupling / god functions
- Shared mutable state
- Missing clear interface boundaries

## Files

| File            | Role                                      |
|-----------------|-------------------------------------------|
| `core.py`       | "Core" that imports from services         |
| `services.py`   | Services that import back from core       |
| `utils.py`      | Shared helpers used by both               |
| `state.py`      | Global mutable state (anti-pattern)       |
| `main.py`       | Entry point that wires everything         |
| `config.py`     | Config that both core and services touch  |

## Intentional problems

1. `core.py` ↔ `services.py` circular import
2. Both modules mutate `state.GLOBAL`
3. `utils.helper()` is called from everywhere with no clear ownership
4. No interfaces / protocols – everything is concrete

## How ADRE will attack it

1. Index → graph shows the cycle clearly
2. Select the cycle nodes in the UI
3. Agent receives only the bounded subgraph
4. Agent proposes an interface boundary and rewrites
5. Graph updates live, cycle disappears
