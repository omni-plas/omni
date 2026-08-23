from omni.boot_contract import BootContract
from omni.boot_pipeline import build_verified_boot
from omni.os_image import build_os_image
from omni.targets import TargetDescriptor


def test_verified_boot_pipeline_produces_consistent_outputs():
    target = TargetDescriptor(
        "linux", "x86_64", "sysv",
        {"boot_protocol": "uefi", "firmware": "uefi", "filesystem": "ext4"},
    )
    contract = BootContract(target, "uefi", "uefi", "ext4", "boot/kernel")
    image = build_os_image(target, {"boot/kernel": b"kernel"}, boot_contract=contract)
    result = build_verified_boot(image, contract)
    assert result.image.digest == result.artifact.digest == result.manifest.artifact_digest
    assert result.manifest.target == target.document()
