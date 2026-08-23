"""Machine-checkable contract for Omni's eventual self-hosting path."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SelfBuildRequirement:
    component: str
    source_language: str
    bootstrap_allowed: bool = True
    native_required: bool = True

CORE_COMPONENTS = tuple(
    SelfBuildRequirement(name, "omni")
    for name in ("compiler", "frontend", "semantic", "optimizer", "backend", "runtime", "stdlib", "package-manager")
)

def validate_self_build_requirements(requirements=CORE_COMPONENTS) -> None:
    names = {r.component for r in requirements}
    missing = {r.component for r in CORE_COMPONENTS} - names
    if missing:
        raise ValueError(f"missing self-build components: {sorted(missing)}")
    if any(r.native_required and not r.component for r in requirements):
        raise ValueError("invalid self-build requirement")
