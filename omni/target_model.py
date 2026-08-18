"""Open-world target semantics used by Omni backends."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class TargetModel:
    platform: str
    architecture: str = "generic"
    runtime: str = "native"
    abi: str = "generic"
    execution_model: str = "native"
    capabilities: Mapping[str, object] = ()
    constraints: Mapping[str, object] = ()

    def __post_init__(self) -> None:
        for value in (self.platform, self.architecture, self.runtime, self.abi, self.execution_model):
            if not isinstance(value, str) or not value.strip():
                raise ValueError("target identity fields must be non-empty strings")

    @property
    def identity(self) -> str:
        return ":".join((self.platform, self.architecture, self.runtime, self.abi, self.execution_model))

    def supports(self, capability: str) -> bool:
        return bool(self.capabilities.get(capability, False))

    def to_dict(self) -> dict[str, object]:
        return {
            "platform": self.platform,
            "architecture": self.architecture,
            "runtime": self.runtime,
            "abi": self.abi,
            "execution_model": self.execution_model,
            "capabilities": dict(self.capabilities),
            "constraints": dict(self.constraints),
        }
