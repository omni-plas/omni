"""Open-world target model for operating systems, runtimes and future platforms."""

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
        for field in (self.platform, self.architecture, self.runtime, self.abi, self.execution_model):
            if not isinstance(field, str) or not field.strip():
                raise ValueError("target identity fields must be non-empty strings")

    @property
    def identity(self) -> str:
        return ":".join((self.platform, self.architecture, self.runtime, self.abi, self.execution_model))

    def supports(self, capability: str) -> bool:
        return bool(self.capabilities.get(capability, False))
