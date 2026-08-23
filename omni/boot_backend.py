"""Pluggable boot backends for converting Omni images into target artifacts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .boot_contract import BootContract, require_boot_capabilities
from .os_image import OSImage, OSImageError
from .os_image_parse import parse_os_image
from .targets import TargetDescriptor


@dataclass(frozen=True)
class BootArtifact:
    target: TargetDescriptor
    payload: bytes
    format: str
    digest: str


class BootBackend(Protocol):
    name: str

    def build(self, image: OSImage, contract: BootContract) -> BootArtifact: ...


class ContainerBootBackend:
    """Target-neutral validated boot container.

    Platform-specific firmware and bootloader backends can implement the same
    protocol without changing the upstream Omni image pipeline.
    """

    name = "omni-boot-container-v1"

    def build(self, image: OSImage, contract: BootContract) -> BootArtifact:
        parsed = parse_os_image(image.payload)
        if parsed.target != image.target:
            raise OSImageError("image target changed during parsing")
        require_boot_capabilities(image.target, contract)
        if parsed.digest != image.digest:
            raise OSImageError("OS image digest mismatch")
        return BootArtifact(image.target, image.payload, self.name, image.digest)


def build_boot_artifact(image: OSImage, contract: BootContract, backend: BootBackend | None = None) -> BootArtifact:
    return (backend or ContainerBootBackend()).build(image, contract)
