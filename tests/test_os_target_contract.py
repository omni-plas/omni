import pytest

from omni.os_image import OSImageError, build_os_image
from omni.os_image_parse import parse_os_image
from omni.os_target_contract import validate_os_image_target
from omni.targets import TargetDescriptor


def test_os_image_target_matches():
    target = TargetDescriptor("linux", "x86_64", "sysv")
    image = parse_os_image(build_os_image(target, {"kernel": b"k"}).payload)
    validate_os_image_target(image, target)


def test_os_image_target_mismatch_is_rejected():
    image = parse_os_image(build_os_image(TargetDescriptor("linux", "x86_64", "sysv"), {"kernel": b"k"}).payload)
    with pytest.raises(OSImageError):
        validate_os_image_target(image, TargetDescriptor("windows", "x86_64", "msvc"))
