"""Plan a reproducible bootstrap from an existing compiler to self-hosting Omni."""
from __future__ import annotations
from dataclasses import dataclass
from .self_host_manifest import SELF_HOST_UNITS, validate_manifest

@dataclass(frozen=True)
class BootstrapPlan:
    stages: tuple[str,...]
    units: tuple[str,...]

def plan_bootstrap(units=SELF_HOST_UNITS)->BootstrapPlan:
    units=tuple(units)
    validate_manifest(units)
    return BootstrapPlan(("bootstrap", "compile-omni", "rebuild-with-omni", "validate-self-host"), tuple(u.name for u in units))
