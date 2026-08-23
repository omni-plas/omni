import pytest

from omni.os_image import OSImageError, build_os_image
from omni.targets import TargetDescriptor


def test_os_image_is_deterministic():
    target = TargetDescriptor("omni-os", "x86_64", "omni-abi")
    first = build_os_image(target, {"boot/kernel": b"kernel", "etc/omni": b"config"})
    second = build_os_image(target, {"etc/omni": b"config", "boot/kernel": b"kernel"})
    assert first.payload == second.payload
    assert first.digest == second.digest
    assert first.payload.startswith(b"OMNIOS1\0")


def test_os_image_rejects_path_traversal():
    with pytest.raises(OSImageError):
        build_os_image(TargetDescriptor("omni-os"), {"../kernel": b"bad"})


def test_os_image_requires_files():
    with pytest.raises(OSImageError):
        build_os_image(TargetDescriptor("omni-os"), {})
