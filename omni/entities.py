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
    properties: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("entity kind must be a non-empty string")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("entity name must be a non-empty string")
        for label, value in (("structure", self.structure), ("behavior", self.behavior), ("constraints", self.constraints), ("execution", self.execution), ("properties", self.properties)):
            if not isinstance(value, Mapping):
                raise ValueError(f"entity {label} must be an object")
        for label, ports in (("inputs", self.inputs), ("outputs", self.outputs)):
            if not isinstance(ports, (tuple, list)):
                raise ValueError(f"entity {label} must be an array")
            for port in ports:
                if not isinstance(port, Mapping):
                    raise ValueError(f"entity {label} must contain objects")
                if not isinstance(port.get("name"), str) or not port["name"].strip():
                    raise ValueError(f"entity {label} ports require a non-empty name")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "kind": self.kind,
            "name": self.name,
            "structure": dict(self.structure),
            "behavior": dict(self.behavior),
            "constraints": dict(self.constraints),
            "inputs": [dict(x) for x in self.inputs],
            "outputs": [dict(x) for x in self.outputs],
            "execution": dict(self.execution),
            "properties": dict(self.properties),
        }
