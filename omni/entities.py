"""Open-world digital entity model for Omni's creation pillar."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class EntitySpec:
    """Formal description of a digital entity, including unknown future kinds."""

    kind: str
    name: str
    structure: Mapping[str, Any] = field(default_factory=dict)
    behavior: Mapping[str, Any] = field(default_factory=dict)
    constraints: Mapping[str, Any] = field(default_factory=dict)
    inputs: tuple[Mapping[str, Any], ...] = ()
    outputs: tuple[Mapping[str, Any], ...] = ()
    execution: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.kind.strip():
            raise ValueError("entity kind must not be empty")
        if not self.name.strip():
            raise ValueError("entity name must not be empty")
        for label, value in (("structure", self.structure), ("behavior", self.behavior), ("constraints", self.constraints), ("execution", self.execution)):
            if not isinstance(value, Mapping):
                raise ValueError(f"entity {label} must be an object")
        for port in (*self.inputs, *self.outputs):
            if not isinstance(port, Mapping) or not isinstance(port.get("name"), str) or not port["name"].strip():
                raise ValueError("entity ports require a non-empty name")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {"kind": self.kind, "name": self.name, "structure": dict(self.structure), "behavior": dict(self.behavior), "constraints": dict(self.constraints), "inputs": [dict(x) for x in self.inputs], "outputs": [dict(x) for x in self.outputs], "execution": dict(self.execution)}
