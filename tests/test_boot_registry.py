import pytest

from omni.boot_backend import ContainerBootBackend
from omni.boot_contract import BootContract
from omni.boot_registry import BootBackendRegistry
from omni.os_image import OSImageError, build_os_image
from omni.targets import TargetDescriptor


def target():
    return TargetDescriptor(
        "linux", "x86_64", "sysv",
        {"boot_protocol": "uefi", "firmware": "uefi", "filesystem": "ext4"},
    )


def test_registry_has_neutral_backend():
    registry = BootBackendRegistry([ContainerBootBackend()])
    assert registry.names() == (ContainerBootBackend.name,)


def test_registry_builds_using_preferred_backend():
    t = target()
    contract = BootContract(t, "uefi", "uefi", "ext4", "boot/kernel")
    image = build_os_image(t, {"boot/kernel": b"k"}, boot_contract=contract)
    registry = BootBackendRegistry([ContainerBootBackend()])
    result = registry.build(image, contract, ContainerBootBackend.name)
    assert result.digest == image.digest


def test_registry_rejects_unknown_backend():
    t = target()
    contract = BootContract(t, "uefi", "uefi", "ext4", "boot/kernel")
    image = build_os_image(t, {"boot/kernel": b"k"})
    registry = BootBackendRegistry([ContainerBootBackend()])
    with pytest.raises(OSImageError):
        registry.build(image, contract, "future-native-backend")
