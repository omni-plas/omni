"""Compose OS image, boot artifact, manifest and verification into one operation."""
from __future__ import annotations

from dataclasses import dataclass

from .boot_backend import BootArtifact, BootBackend, build_boot_artifact
from .boot_contract import BootContract
from .boot_manifest import BootManifest, create_boot_manifest
from .boot_manifest_verify import verify_boot_manifest
from .os_image import OSImage


@dataclass(frozen=True)
class VerifiedBootResult:
    image: OSImage
    artifact: BootArtifact
    manifest: BootManifest


def build_verified_boot(
    image: OSImage,
    contract: BootContract,
    *,
    backend: BootBackend | None = None,
) -> VerifiedBootResult:
    artifact = build_boot_artifact(image, contract, backend)
    manifest = create_boot_manifest(artifact, contract)
    verify_boot_manifest(artifact, manifest)
    return VerifiedBootResult(image, artifact, manifest)
