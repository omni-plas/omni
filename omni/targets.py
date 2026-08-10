"""Extensible target descriptors for Omni compilation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class TargetDescriptor:
    """Describes a compilation target without hard-coding an OS or CPU list."""

    platform: str
    architecture: str | None = None
    abi: str | None = None
    capabilities: Mapping[str, str] = field(default_factory=dict)

    def identity(self) -> str:
        parts = [self.platform]
        if self.architecture:
            parts.append(self.architecture)
        if self.abi:
            parts.append(self.abi)
        return "-".join(parts)
