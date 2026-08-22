"""Open-world installation planning and deterministic installer manifests for Omni."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

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
    """A validated, target-neutral description of how a completed artifact is installed."""

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
        object.__setattr__(self, "artifacts", tuple(a.strip() for a in self.artifacts))
        object.__setattr__(self, "metadata", dict(self.metadata))

    def identity(self) -> str:
        return f"{self.kind.value}:{self.target.identity()}:{self.artifact_format.strip()}"

    def with_artifact(self, artifact: str) -> "InstallationPlan":
        if not isinstance(artifact, str) or not artifact.strip():
            raise ValueError("installer artifact cannot be empty")
        return InstallationPlan(
            self.target, self.kind, self.artifact_format, self.bootable,
            self.filesystem, self.artifacts + (artifact.strip(),), self.metadata
        )

    def manifest_document(self) -> dict[str, Any]:
        """Return the canonical manifest structure consumed by materializers."""
        return {
            "schema": "omni.installation.v1",
            "identity": self.identity(),
            "target": {
                "platform": self.target.platform.strip(),
                "architecture": self.target.architecture.strip() if self.target.architecture else None,
                "abi": self.target.abi.strip() if self.target.abi else None,
                "capabilities": dict(self.target.capabilities),
            },
            "kind": self.kind.value,
            "artifact_format": self.artifact_format.strip(),
            "bootable": self.bootable,
            "filesystem": self.filesystem.strip() if self.filesystem else None,
            "artifacts": list(self.artifacts),
            "metadata": dict(self.metadata),
        }

    def manifest(self) -> bytes:
        """Serialize a deterministic installation manifest for downstream materializers."""
        return (json.dumps(
            self.manifest_document(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ) + "\n").encode("utf-8")

    def render_manifest(self) -> str:
        """Render the canonical manifest as human-readable JSON."""
        return json.dumps(self.manifest_document(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "InstallationPlan":
        """Reconstruct and strictly validate a plan produced by ``manifest_document``."""
        if not isinstance(document, Mapping):
            raise InstallationError("installation manifest must be an object")
        if document.get("schema") != "omni.installation.v1":
            raise InstallationError("unsupported installation manifest schema")
        target_data = document.get("target")
        if not isinstance(target_data, Mapping):
            raise InstallationError("installation manifest target must be an object")
        try:
            target = TargetDescriptor(
                target_data["platform"],
                target_data.get("architecture"),
                target_data.get("abi"),
                target_data.get("capabilities", {}),
            )
            plan = plan_installation(
                target,
                kind=InstallerKind(document["kind"]),
                artifact_format=document["artifact_format"],
                bootable=document["bootable"],
                filesystem=document.get("filesystem"),
                artifacts=tuple(document.get("artifacts", ())),
                metadata=document.get("metadata", {}),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise InstallationError(f"invalid installation manifest: {exc}") from exc
        if document.get("identity") != plan.identity():
            raise InstallationError("installation manifest identity does not match its contents")
        return plan

    @classmethod
    def from_manifest(cls, payload: bytes | str) -> "InstallationPlan":
        """Parse a canonical manifest and validate every field before reconstruction."""
        try:
            document = json.loads(payload.decode("utf-8") if isinstance(payload, bytes) else payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise InstallationError(f"invalid installation manifest JSON: {exc}") from exc
        return cls.from_document(document)


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
    if kind in (InstallerKind.BOOTABLE, InstallerKind.RECOVERY) and not filesystem:
        raise InstallationError(f"{kind.value} installer requires a filesystem")
    return InstallationPlan(target, kind, artifact_format, bootable, filesystem, artifacts, metadata or {})
