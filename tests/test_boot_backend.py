import pytest

from omni.boot_backend import ContainerBootBackend, build_boot_artifact
from omni.boot_contract import BootContract
from omni.os_image import OSImageError, build_os_image
from omni.targets import TargetDescriptor


def test_container_boot_backend_builds_validated_artifact():
    target = TargetDescriptor(
        "linux", "x86_64", "sysv",
        {"boot_protocol": "uefi", "firmware": "uefi", "filesystem": "ext4"},
    )
    contract = BootContract(target, "uefi", "uefi", "ext4", "boot/kernel")
    image = build_os_image(target, {"boot/kernel": b"kernel"}, boot_contract=contract)
    artifact = build_boot_artifact(image, contract)
    assert artifact.target == target
    assert artifact.payload == image.payload
    assert artifact.digest == image.digest
    assert artifact.format == ContainerBootBackend.name


def test_boot_backend_rejects_invalid_contract():
    target = TargetDescriptor("future-os", "future-cpu", "future-abi")
    contract = BootContract(target, "future", "firmware", "filesystem", "kernel")
    image = build_os_image(target, {"kernel": b"k"})
    with pytest.raises(OSImageError):
        build_boot_artifact(image, contract)
