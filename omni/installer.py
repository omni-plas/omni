"""Open-world installation planning for Omni-built digital entities."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .targets import TargetDescriptor


class InstallationError(ValueError):
    """Raised when an installation plan is incomplete or inconsistent."""


class InstallerKind(str, Enum):
    PACKAGE = "package"
    BOOTABLE = "bootable"
    NETWORK = "network"
    RECOVERY = "recovery"
    CUSTOM = "custom"


@dataclass(frozen=True)
class InstallationPlan:
    target: TargetDescriptor
    kind: InstallerKind
    artifact_format: str
    bootable: bool = False
    filesystem: str | None = None
    metadata: Mapping[str, str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.target, TargetDescriptor):
            raise TypeError("installation target must be a TargetDescriptor")
        if not isinstance(self.kind, InstallerKind):
            raise TypeError("installer kind must be an InstallerKind")
        if not isinstance(self.artifact_format, str) or not self.artifact_format.strip():
            raise ValueError("artifact format must be non-empty")
        if not isinstance(self.bootable, bool):
            raise TypeError("bootable must be boolean")
        if self.filesystem is not None and (not isinstance(self.filesystem, str) or not self.filesystem.strip()):
            raise ValueError("filesystem must be non-empty when supplied")
        if self.metadata is None:
            object.__setattr__(self, "metadata", {})
        elif not isinstance(self.metadata, Mapping):
            raise TypeError("installer metadata must be a mapping")
        elif any(not isinstance(k, str) or not k.strip() for k in self.metadata):
            raise ValueError("installer metadata keys must be non-empty strings")

    def identity(self) -> str:
        return f"{self.kind.value}:{self.target.identity()}:{self.artifact_format.strip()}"


def plan_installation(
    target: TargetDescriptor,
    *,
    kind: InstallerKind = InstallerKind.PACKAGE,
    artifact_format: str,
    bootable: bool = False,
    filesystem: str | None = None,
    metadata: Mapping[str, str] | None = None,
) -> InstallationPlan:
    """Create a validated installation plan without assuming a fixed OS list."""
    if kind in (InstallerKind.BOOTABLE, InstallerKind.RECOVERY) and not bootable:
        raise InstallationError(f"{kind.value} installer must be marked bootable")
    if bootable and kind == InstallerKind.PACKAGE:
        raise InstallationError("package installer cannot be bootable; use bootable kind")
    if kind == InstallerKind.BOOTABLE and not filesystem:
        raise InstallationError("bootable installer requires a filesystem")
    return InstallationPlan(target, kind, artifact_format, bootable, filesystem, metadata)
