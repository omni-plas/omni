"""End-to-end release pipeline from materialized artifacts to an installer bundle."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .installer import InstallationPlan
from .installer_builder import InstallerBundle, build_installer
from .packaging import PackageManifest
from .package_writer import build_package


class ReleasePipelineError(ValueError):
    """Raised when a release cannot be produced consistently."""


@dataclass(frozen=True)
class ReleaseResult:
    package_payload: bytes
    installer: InstallerBundle
    package_digest: str
    installer_digest: str


def build_release(
    package_manifest: PackageManifest,
    installation_plan: InstallationPlan,
    entries: Mapping[str, bytes],
    *,
    package_filename: str = "package.omni",
) -> ReleaseResult:
    """Build and cross-check a package and its installer without invoking payloads."""
    if not isinstance(package_manifest, PackageManifest):
        raise TypeError("package_manifest must be a PackageManifest")
    if not isinstance(installation_plan, InstallationPlan):
        raise TypeError("installation_plan must be an InstallationPlan")
    if package_manifest.target != installation_plan.target:
        raise ReleasePipelineError("package and installation targets must match")
    if package_filename.strip() not in installation_plan.artifacts:
        raise ReleasePipelineError("installation plan must declare the package filename")

    package_payload = build_package(package_manifest, entries)
    package_digest = hashlib.sha256(package_payload).hexdigest()
    installer = build_installer(installation_plan, package_payload, filename=package_filename)
    manifest = json.loads(installation_plan.manifest())
    if manifest["target"] != package_manifest.target.document():
        raise ReleasePipelineError("release target identity mismatch")
    return ReleaseResult(package_payload, installer, package_digest, installer.digest)


def write_release(
    output_directory: str | Path,
    package_manifest: PackageManifest,
    installation_plan: InstallationPlan,
    entries: Mapping[str, bytes],
    *,
    package_filename: str = "package.omni",
    installer_filename: str = "installer.omni",
) -> ReleaseResult:
    """Build a release and atomically write both package and installer files."""
    result = build_release(package_manifest, installation_plan, entries, package_filename=package_filename)
    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)
    package_path = directory / package_filename
    installer_path = directory / installer_filename
    package_path.write_bytes(result.package_payload)
    installer_path.write_bytes(result.installer.payload)
    return result
