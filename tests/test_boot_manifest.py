import hashlib

import pytest

from omni.boot_backend import build_boot_artifact
from omni.boot_contract import BootContract
from omni.boot_manifest import create_boot_manifest
from omni.os_image import build_os_image
from omni.targets import TargetDescriptor


def test_boot_manifest_is_canonical_and_integrity_checked():
    target = TargetDescriptor("linux", "x86_64", "sysv", {"boot_protocol": "uefi", "firmware": "uefi", "filesystem": "ext4"})
    contract = BootContract(target, "uefi", "uefi", "ext4", "boot/kernel")
    image = build_os_image(target, {"boot/kernel": b"k"}, boot_contract=contract)
    artifact = build_boot_artifact(image, contract)
    manifest = create_boot_manifest(artifact, contract)
    assert manifest.format == "omni-boot-manifest-v1"
    assert manifest.artifact_digest == hashlib.sha256(artifact.payload).hexdigest()
    assert manifest.to_bytes() == manifest.to_bytes()


def test_boot_manifest_rejects_wrong_target():
    target = TargetDescriptor("linux", "x86_64", "sysv", {"boot_protocol": "uefi", "firmware": "uefi", "filesystem": "ext4"})
    other = TargetDescriptor("future", "cpu", "abi")
    contract = BootContract(other, "boot", "fw", "fs", "kernel")
    image = build_os_image(target, {"kernel": b"k"})
    artifact = build_boot_artifact(image, BootContract(target, "uefi", "uefi", "ext4", "kernel"))
    with pytest.raises(ValueError):
        create_boot_manifest(artifact, contract)
