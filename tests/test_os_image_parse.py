import pytest

from omni.os_image import OSImageError, build_os_image
from omni.os_image_parse import parse_os_image
from omni.targets import TargetDescriptor


def test_os_image_round_trips():
    target = TargetDescriptor("future-os", "future-cpu", "future-abi")
    image = build_os_image(target, {"boot/kernel": b"kernel", "etc/config": b"cfg"})
    parsed = parse_os_image(image.payload)
    assert parsed.target == target
    assert [(item.path, item.payload) for item in parsed.files] == [
        ("boot/kernel", b"kernel"),
        ("etc/config", b"cfg"),
    ]
    assert parsed.digest == image.digest


def test_corrupt_os_image_is_rejected():
    with pytest.raises(OSImageError):
        parse_os_image(b"OMNIOS1\0bad")
