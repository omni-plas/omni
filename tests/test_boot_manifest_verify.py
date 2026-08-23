import dataclasses

import pytest

from omni.boot_backend import build_boot_artifact
from omni.boot_contract import BootContract
from omni.boot_manifest import create_boot_manifest
from omni.boot_manifest_verify import verify_boot_manifest
from omni.os_image import OSImageError, build_os_image
from omni.targets import TargetDescriptor


def make_artifact():
    target = TargetDescriptor("linux", "x86_64", "sysv", {"boot_protocol": "uefi", "firmware": "uefi", "filesystem": "ext4"})
    contract = BootContract(target, "uefi", "uefi", "ext4", "boot/kernel")
    image = build_os_image(target, {"boot/kernel": b"kernel"}, boot_contract=contract)
    artifact = build_boot_artifact(image, contract)
    return artifact, contract


def test_manifest_verifies_artifact():
    artifact, contract = make_artifact()
    verify_boot_manifest(artifact, create_boot_manifest(artifact, contract))


def test_manifest_rejects_tampered_artifact():
    artifact, contract = make_artifact()
    manifest = create_boot_manifest(artifact, contract)
    tampered = dataclasses.replace(artifact, payload=artifact.payload + b"x")
    with pytest.raises(OSImageError):
        verify_boot_manifest(tampered, manifest)
