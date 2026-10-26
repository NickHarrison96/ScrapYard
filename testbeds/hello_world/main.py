"""Entry point that forces the circular modules to load."""

from __future__ import annotations

from testbeds.hello_world import core, services, state, config


def run(user: str = "alice") -> str:
    config.RUNTIME_FLAGS["verbose"] = True
    result = core.process_request(user)
    print(f"result={result}  state={state.GLOBAL}")
    return result


if __name__ == "__main__":
    run()
