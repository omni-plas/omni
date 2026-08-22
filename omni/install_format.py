"""Target-neutral installable artifact descriptors."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from .targets import TargetDescriptor


class InstallFormatError(ValueError):
    """Raised when an install format is incomplete."""


@dataclass(frozen=True)
class InstallFormat:
    name: str
    version: str
    target: TargetDescriptor
    bootable: bool = False
    filesystem: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise InstallFormatError("install format name must be non-empty")
        if not isinstance(self.version, str) or not self.version.strip():
            raise InstallFormatError("install format version must be non-empty")
        if not isinstance(self.target, TargetDescriptor):
            raise TypeError("install format target must be a TargetDescriptor")
        if not isinstance(self.bootable, bool):
            raise TypeError("bootable must be boolean")
        if self.bootable and (not self.filesystem or not self.filesystem.strip()):
            raise InstallFormatError("bootable install format requires filesystem")
        if self.filesystem is not None and not isinstance(self.filesystem, str):
            raise TypeError("filesystem must be a string")
        if not isinstance(self.metadata, Mapping):
            raise TypeError("install format metadata must be a mapping")

    def identity(self) -> str:
        return f"{self.name}:{self.version}:{self.target.identity()}"
