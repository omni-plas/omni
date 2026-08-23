import struct

from omni.os_image import build_os_image
from omni.targets import TargetDescriptor


def test_os_image_header_contains_target_and_file_count():
    target = TargetDescriptor("future-os", "future-cpu", "future-abi")
    image = build_os_image(target, {"kernel": b"K", "etc/config": b"C"})
    assert image.payload[:8] == b"OMNIOS1\0"
    header_size = struct.unpack_from("<I", image.payload, 8)[0]
    header = image.payload[12 : 12 + header_size].decode()
    assert '"file_count":2' in header
    assert '"platform":"future-os"' in header
