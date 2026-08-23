"""Validate that an OS image is compatible with its declared target."""
from __future__ import annotations

from .os_image_parse import ParsedOSImage
from .os_image import OSImageError
from .targets import TargetDescriptor


def validate_os_image_target(image: ParsedOSImage, expected: TargetDescriptor) -> None:
    if image.target != expected:
        raise OSImageError(
            "OS image target mismatch: "
            f"expected {expected.identity()}, got {image.target.identity()}"
        )
