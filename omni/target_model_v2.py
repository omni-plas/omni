"""Formal target description used to avoid hard-coded target assumptions."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping

@dataclass(frozen=True)
class TargetModel:
    platform: str
    architecture: str
    abi: str | None = None
    executable_format: str | None = None
    features: frozenset[str] = field(default_factory=frozenset)
    metadata: Mapping[str, str] = field(default_factory=dict)

    def identity(self) -> str:
        parts = [self.platform, self.architecture]
        if self.abi: parts.append(self.abi)
        if self.executable_format: parts.append(self.executable_format)
        return "/".join(parts)

    def supports(self, feature: str) -> bool:
        return feature in self.features
