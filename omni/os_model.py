"""Open-world operating-system build model for Omni."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Tuple

from .targets import TargetDescriptor


class OSModelError(ValueError):
    """Raised when an operating-system definition is incomplete."""


@dataclass(frozen=True)
class OperatingSystemSpec:
    name: str
    target: TargetDescriptor
    kernel: str
    bootloader: str | None = None
    runtime: str | None = None
    drivers: Tuple[str, ...] = field(default_factory=tuple)
    filesystem: str | None = None
    packages: Tuple[str, ...] = field(default_factory=tuple)
    installation_capabilities: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise OSModelError("operating-system name cannot be empty")
        if not isinstance(self.target, TargetDescriptor):
            raise TypeError("operating-system target must be a TargetDescriptor")
        if not isinstance(self.kernel, str) or not self.kernel.strip():
            raise OSModelError("kernel definition cannot be empty")
        for label, value in (("bootloader", self.bootloader), ("runtime", self.runtime), ("filesystem", self.filesystem)):
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise OSModelError(f"{label} cannot be empty")
        for label, values in (("drivers", self.drivers), ("packages", self.packages)):
            if not isinstance(values, tuple) or any(not isinstance(v, str) or not v.strip() for v in values):
                raise OSModelError(f"{label} must contain non-empty strings")
        if not isinstance(self.installation_capabilities, Mapping):
            raise TypeError("installation capabilities must be a mapping")

    def requires_bootloader(self) -> bool:
        return self.bootloader is not None

    def requires_filesystem(self) -> bool:
        return self.filesystem is not None

    def capability(self, name: str, default: object = None) -> object:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("capability name cannot be empty")
        return self.installation_capabilities.get(name, default)
