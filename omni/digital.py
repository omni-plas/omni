"""Open-world digital artifact model for Omni."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True)
class DigitalSpec:
    kind: str
    name: str
    behavior: Mapping[str, Any] = field(default_factory=dict)
    interfaces: tuple[str, ...] = ()
    data: Mapping[str, Any] = field(default_factory=dict)
    requirements: Mapping[str, Any] = field(default_factory=dict)
    extensions: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.kind.strip() or not self.name.strip():
            raise ValueError("digital kind and name must be non-empty")
        if not isinstance(self.behavior, Mapping):
            raise TypeError("behavior must be an object")
        if not isinstance(self.data, Mapping) or not isinstance(self.requirements, Mapping):
            raise TypeError("data and requirements must be objects")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {"kind": self.kind, "name": self.name, "behavior": dict(self.behavior),
                "interfaces": list(self.interfaces), "data": dict(self.data),
                "requirements": dict(self.requirements), "extensions": dict(self.extensions)}
