"""Construction boundary: validate a digital specification and make a plan."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

from .creation import CreationPlan, plan_creation
from .digital import DigitalSpec

@dataclass(frozen=True)
class ConstructionPlan:
    artifact: DigitalSpec
    steps: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"artifact": self.artifact.to_dict(), "steps": list(self.steps)}


def plan_construction(spec: DigitalSpec | Mapping[str, Any]) -> ConstructionPlan:
    if not isinstance(spec, DigitalSpec):
        spec = DigitalSpec(
            kind=str(spec.get("kind", "")), name=str(spec.get("name", "")),
            behavior=spec.get("behavior", {}), structure=spec.get("structure", {}),
            interfaces=tuple(spec.get("interfaces", ())), data=spec.get("data", {}),
            requirements=spec.get("requirements", {}), constraints=spec.get("constraints", {}),
            extensions=spec.get("extensions", {}),
        )
    creation = plan_creation(spec)
    steps = ("validate", "model", "lower", "materialize", "verify")
    if creation.executable:
        steps = ("validate",) + tuple(step.action for step in creation.steps) + ("verify",)
    return ConstructionPlan(spec, steps)
