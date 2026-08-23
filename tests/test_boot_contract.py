import pytest

from omni.boot_contract import BootContract, require_boot_capabilities
from omni.os_image import OSImageError
from omni.targets import TargetDescriptor


def test_boot_contract_requires_target_capabilities():
    target = TargetDescriptor(
        "linux", "x86_64", "sysv",
        {"boot_protocol": "uefi", "firmware": "uefi", "filesystem": "ext4"},
    )
    contract = BootContract(target, "uefi", "uefi", "ext4", "boot/kernel")
    require_boot_capabilities(target, contract)


def test_boot_contract_rejects_missing_capability():
    target = TargetDescriptor("future-os", "future-cpu", "future-abi")
    contract = BootContract(target, "future-boot", "future-fw", "future-fs", "kernel")
    with pytest.raises(OSImageError):
        require_boot_capabilities(target, contract)
