"""Declarative manifest for the eventual self-hosted Omni compiler."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SelfHostUnit:
    name: str
    source: str
    role: str
    required: bool = True

SELF_HOST_UNITS = (
    SelfHostUnit("frontend", "compiler/frontend.omni", "frontend"),
    SelfHostUnit("semantic", "compiler/semantic.omni", "semantic"),
    SelfHostUnit("ir", "compiler/ir.omni", "ir"),
    SelfHostUnit("optimizer", "compiler/optimizer.omni", "optimizer"),
    SelfHostUnit("backend", "compiler/backend.omni", "backend"),
    SelfHostUnit("runtime", "runtime/core.omni", "runtime"),
    SelfHostUnit("stdlib", "stdlib/core.omni", "stdlib"),
    SelfHostUnit("driver", "compiler/driver.omni", "driver"),
)

def validate_manifest(units=SELF_HOST_UNITS) -> None:
    names = {u.name for u in units}
    required = {u.name for u in SELF_HOST_UNITS if u.required}
    missing = required - names
    if missing:
        raise ValueError(f"missing self-host units: {sorted(missing)}")
    if len(names) != len(tuple(units)):
        raise ValueError("duplicate self-host unit")
