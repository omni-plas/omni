"""Explicit semantic contract captured by Omni's universal IR."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class SemanticModel:
    """Language/target-neutral meaning that a compiler must preserve."""

    types: Mapping[str, Any] = field(default_factory=dict)
    control_flow: Mapping[str, Any] = field(default_factory=dict)
    data_flow: Mapping[str, Any] = field(default_factory=dict)
    memory_model: Mapping[str, Any] = field(default_factory=dict)
    ownership: Mapping[str, Any] = field(default_factory=dict)
    lifetime: Mapping[str, Any] = field(default_factory=dict)
    concurrency: Mapping[str, Any] = field(default_factory=dict)
    error_handling: Mapping[str, Any] = field(default_factory=dict)
    io: Mapping[str, Any] = field(default_factory=dict)
    dependencies: Any = field(default_factory=list)
    security: Mapping[str, Any] = field(default_factory=dict)
    performance: Mapping[str, Any] = field(default_factory=dict)
    execution_model: Mapping[str, Any] = field(default_factory=dict)
    platform_constraints: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "types": dict(self.types),
            "control_flow": dict(self.control_flow),
            "data_flow": dict(self.data_flow),
            "memory_model": dict(self.memory_model),
            "ownership": dict(self.ownership),
            "lifetime": dict(self.lifetime),
            "concurrency": dict(self.concurrency),
            "error_handling": dict(self.error_handling),
            "io": dict(self.io),
            "dependencies": self.dependencies,
            "security": dict(self.security),
            "performance": dict(self.performance),
            "execution_model": dict(self.execution_model),
            "platform_constraints": dict(self.platform_constraints),
        }
