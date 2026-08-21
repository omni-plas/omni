"""Extensible target descriptors for Omni compilation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class TargetDescriptor:
    """Describes a compilation target without a closed OS/CPU enumeration."""

    platform: str
    architecture: str | None = None
    abi: str | None = None
    capabilities: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.platform.strip():
            raise ValueError("target platform cannot be empty")
        for label, value in (("architecture", self.architecture), ("abi", self.abi)):
            if value is not None and not value.strip():
                raise ValueError(f"target {label} cannot be empty")
        if any(not isinstance(k, str) or not k.strip() for k in self.capabilities):
            raise ValueError("target capability names must be non-empty strings")
        if any(not isinstance(v, str) for v in self.capabilities.values()):
            raise ValueError("target capability values must be strings")

    def identity(self) -> str:
        return "-".join(p for p in (self.platform, self.architecture, self.abi) if p)

    def supports(self, capability: str, value: str | None = None) -> bool:
        """Check an open-world target capability without enumerating platforms."""
        actual = self.capabilities.get(capability)
        return actual is not None and (value is None or actual == value)
