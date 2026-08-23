"""Describe the transition from bootstrap compiler to self-hosted compiler."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BootstrapStage:
    name: str
    compiler: str
    output: str
    validates: tuple[str, ...]

BOOTSTRAP_STAGES = (
    BootstrapStage("seed", "bootstrap compiler", "native Omni compiler", ("parser", "IR", "native backend")),
    BootstrapStage("self_compile", "native Omni compiler", "Omni compiler", ("frontend", "semantic", "optimizer", "backend")),
    BootstrapStage("recompile", "Omni compiler", "Omni compiler", ("byte-identical-or-equivalent",)),
)

def validate_bootstrap_stages(stages=BOOTSTRAP_STAGES) -> None:
    if not stages or stages[0].name != "seed":
        raise ValueError("bootstrap must begin with seed stage")
    if stages[-1].name != "recompile":
        raise ValueError("bootstrap must end with recompile stage")
