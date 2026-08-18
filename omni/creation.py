"""Universal digital-entity construction planning."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .digital import DigitalSpec


@dataclass(frozen=True)
class CreationStep:
    action: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class CreationPlan:
    entity: DigitalSpec
    steps: tuple[CreationStep, ...]

    @property
    def executable(self) -> bool:
        return bool(self.steps)


def plan_creation(spec: DigitalSpec) -> CreationPlan:
    """Derive deterministic construction work from an open-world entity spec."""
    spec.validate()
    steps: list[CreationStep] = [
        CreationStep("define-entity", {"kind": spec.kind, "name": spec.name}),
    ]
    if spec.data:
        steps.append(CreationStep("define-data", dict(spec.data)))
    if spec.media:
        steps.append(CreationStep("define-media", {"format": spec.format, "media": dict(spec.media)}))
    if spec.interfaces:
        steps.append(CreationStep("define-interfaces", {"interfaces": list(spec.interfaces)}))
    if spec.behavior:
        steps.append(CreationStep("define-behavior", dict(spec.behavior)))
    if spec.requirements:
        steps.append(CreationStep("satisfy-requirements", dict(spec.requirements)))
    if spec.extensions:
        steps.append(CreationStep("apply-extensions", dict(spec.extensions)))
    if spec.metadata:
        steps.append(CreationStep("attach-metadata", dict(spec.metadata)))
    steps.append(CreationStep("materialize", {"kind": spec.kind, "name": spec.name}))
    return CreationPlan(spec, tuple(steps))
