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
    """Turn an open-world digital specification into explicit construction work.

    The planner does not assume a fixed catalog of entity kinds. It derives a
    deterministic sequence from the entity's declared structure, interfaces,
    data, behavior, and requirements.
    """
    spec.validate()
    steps: list[CreationStep] = [
        CreationStep("define-entity", {"kind": spec.kind, "name": spec.name}),
    ]
    if spec.data:
        steps.append(CreationStep("define-data", dict(spec.data)))
    if spec.interfaces:
        steps.append(CreationStep("define-interfaces", {"interfaces": list(spec.interfaces)}))
    if spec.behavior:
        steps.append(CreationStep("define-behavior", dict(spec.behavior)))
    if spec.requirements:
        steps.append(CreationStep("satisfy-requirements", dict(spec.requirements)))
    if spec.extensions:
        steps.append(CreationStep("apply-extensions", dict(spec.extensions)))
    steps.append(CreationStep("materialize", {"kind": spec.kind, "name": spec.name}))
    return CreationPlan(spec, tuple(steps))
