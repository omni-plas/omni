"""Construction boundary: validate a digital specification and make a plan."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

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
            behavior=spec.get("behavior", {}), interfaces=tuple(spec.get("interfaces", ())),
            data=spec.get("data", {}), requirements=spec.get("requirements", {}),
            extensions=spec.get("extensions", {}),
        )
    spec.validate()
    steps = ("validate", "model", "lower", "materialize", "verify")
    return ConstructionPlan(spec, steps)
