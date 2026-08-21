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
        if not isinstance(self.platform, str) or not self.platform.strip():
            raise ValueError("target platform cannot be empty")
        for label, value in (("architecture", self.architecture), ("abi", self.abi)):
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"target {label} cannot be empty")
        if any(not isinstance(k, str) or not k.strip() for k in self.capabilities):
            raise ValueError("target capability names must be non-empty strings")
        if any(not isinstance(v, str) or not v.strip() for v in self.capabilities.values()):
            raise ValueError("target capability values must be non-empty strings")

    def identity(self) -> str:
        return "-".join(p for p in (self.platform, self.architecture, self.abi) if p)

    def supports(self, capability: str, value: str | None = None) -> bool:
        actual = self.capabilities.get(capability)
        return actual is not None and (value is None or actual == value)

    def require(self, capability: str, value: str | None = None) -> None:
        """Raise a deterministic error when a required target capability is absent."""
        if not self.supports(capability, value):
            suffix = f"={value}" if value is not None else ""
            raise ValueError(f"target {self.identity()} lacks capability {capability}{suffix}")

    def with_capability(self, name: str, value: str) -> "TargetDescriptor":
        """Return a new target descriptor with one capability added or replaced."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("capability name cannot be empty")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("capability value cannot be empty")
        capabilities = dict(self.capabilities)
        capabilities[name] = value
        return TargetDescriptor(self.platform, self.architecture, self.abi, capabilities)
