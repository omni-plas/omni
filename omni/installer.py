"""Open-world installation planning and materialization metadata for Omni."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
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
    """A target-neutral description of how a completed artifact is installed."""

    target: TargetDescriptor
    kind: InstallerKind
    artifact_format: str
    bootable: bool = False
    filesystem: str | None = None
    artifacts: tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)

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
        if not isinstance(self.artifacts, tuple) or any(not isinstance(a, str) or not a.strip() for a in self.artifacts):
            raise ValueError("installation artifacts must contain non-empty strings")
        if not isinstance(self.metadata, Mapping):
            raise TypeError("installer metadata must be a mapping")
        if any(not isinstance(k, str) or not k.strip() for k in self.metadata):
            raise ValueError("installer metadata keys must be non-empty strings")
        if any(not isinstance(v, str) for v in self.metadata.values()):
            raise ValueError("installer metadata values must be strings")

    def identity(self) -> str:
        return f"{self.kind.value}:{self.target.identity()}:{self.artifact_format.strip()}"

    def with_artifact(self, artifact: str) -> "InstallationPlan":
        if not isinstance(artifact, str) or not artifact.strip():
            raise ValueError("installer artifact cannot be empty")
        return InstallationPlan(
            self.target, self.kind, self.artifact_format, self.bootable,
            self.filesystem, self.artifacts + (artifact,), self.metadata
        )

    def manifest(self) -> bytes:
        """Serialize a deterministic installation manifest for downstream materializers."""
        document = {
            "schema": "omni.installation.v1",
            "identity": self.identity(),
            "target": {
                "platform": self.target.platform,
                "architecture": self.target.architecture,
                "abi": self.target.abi,
                "capabilities": dict(self.target.capabilities),
            },
            "kind": self.kind.value,
            "artifact_format": self.artifact_format.strip(),
            "bootable": self.bootable,
            "filesystem": self.filesystem,
            "artifacts": list(self.artifacts),
            "metadata": dict(self.metadata),
        }
        return (json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def plan_installation(
    target: TargetDescriptor,
    *,
    kind: InstallerKind = InstallerKind.PACKAGE,
    artifact_format: str,
    bootable: bool = False,
    filesystem: str | None = None,
    artifacts: tuple[str, ...] = (),
    metadata: Mapping[str, str] | None = None,
) -> InstallationPlan:
    """Create a validated installation plan without a fixed OS catalogue."""
    if kind in (InstallerKind.BOOTABLE, InstallerKind.RECOVERY) and not bootable:
        raise InstallationError(f"{kind.value} installer must be marked bootable")
    if bootable and kind == InstallerKind.PACKAGE:
        raise InstallationError("package installer cannot be bootable; use bootable kind")
    if kind == InstallerKind.BOOTABLE and not filesystem:
        raise InstallationError("bootable installer requires a filesystem")
    return InstallationPlan(target, kind, artifact_format, bootable, filesystem, artifacts, metadata or {})
