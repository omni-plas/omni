"""Target-neutral orchestration for Omni OS builds and installers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from .installer import InstallationPlan, InstallerKind, plan_installation
from .os_model import OperatingSystemSpec
from .packaging import PackageManifest


class BuildPipelineError(ValueError):
    """Raised when an OS build pipeline is incomplete."""


@dataclass(frozen=True)
class OSBuildPlan:
    os: OperatingSystemSpec
    package: PackageManifest
    installer: InstallationPlan
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.package.target != self.os.target:
            raise BuildPipelineError("package target must match operating-system target")
        if self.installer.target != self.os.target:
            raise BuildPipelineError("installer target must match operating-system target")
        if not isinstance(self.metadata, Mapping):
            raise TypeError("build metadata must be a mapping")

    def artifacts(self) -> tuple[str, ...]:
        return self.package.artifacts + self.installer.artifacts

    def manifest(self) -> bytes:
        """Return the canonical installer manifest for the build's target."""
        return self.installer.manifest()


def create_os_build_plan(
    os: OperatingSystemSpec,
    *,
    version: str,
    artifact_format: str,
    installer_kind: InstallerKind = InstallerKind.BOOTABLE,
    bootable: bool = True,
    metadata: Mapping[str, object] | None = None,
) -> OSBuildPlan:
    """Connect OS definition, package manifest, and installer into one validated plan."""
    if not isinstance(os, OperatingSystemSpec):
        raise TypeError("os must be an OperatingSystemSpec")
    package = PackageManifest(os.name, version, os.target)
    filesystem = os.filesystem if bootable else None
    installer_metadata = {"os": os.name, "version": version}
    for key, value in os.installation_capabilities.items():
        installer_metadata[f"capability:{key}"] = str(value)
    installer = plan_installation(
        os.target,
        kind=installer_kind,
        artifact_format=artifact_format,
        bootable=bootable,
        filesystem=filesystem,
        metadata=installer_metadata,
    )
    return OSBuildPlan(os, package, installer, metadata or {})
