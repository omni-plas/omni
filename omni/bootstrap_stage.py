"""Explicit bootstrap stages used to reason about self-hosting."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BootstrapStage:
    name: str
    complete: bool

BOOTSTRAP_STAGES=(
    BootstrapStage('bootstrap',True),
    BootstrapStage('source-to-ir',True),
    BootstrapStage('ir-to-native',False),
    BootstrapStage('rebuild-with-omni',False),
    BootstrapStage('self-host-validation',False),
)

def next_stage(stages=BOOTSTRAP_STAGES):
    for stage in stages:
        if not stage.complete: return stage.name
    return None
