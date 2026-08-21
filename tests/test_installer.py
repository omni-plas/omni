import pytest

from omni.installer import InstallationError, InstallationPlan, InstallerKind, plan_installation
from omni.targets import TargetDescriptor


def test_future_os_installer_is_target_driven():
    target = TargetDescriptor("future-os", "future-cpu", "future-abi")
    plan = plan_installation(target, kind=InstallerKind.BOOTABLE, artifact_format="future-image", bootable=True, filesystem="future-fs")
    assert plan.target == target
    assert plan.identity() == "bootable:future-os-future-cpu-future-abi:future-image"


def test_historical_target_can_have_installation_plan():
    target = TargetDescriptor("historical-os", capabilities={"era": "1990s", "boot": "legacy"})
    plan = plan_installation(target, kind=InstallerKind.PACKAGE, artifact_format="historical-package")
    assert plan.target.capability("era") == "1990s"


def test_bootable_installers_require_filesystem():
    with pytest.raises(InstallationError, match="filesystem"):
        plan_installation(TargetDescriptor("future-os"), kind=InstallerKind.BOOTABLE, artifact_format="image", bootable=True)


def test_bootable_kind_requires_bootable_flag():
    with pytest.raises(InstallationError, match="bootable"):
        plan_installation(TargetDescriptor("future-os"), kind=InstallerKind.BOOTABLE, artifact_format="image", filesystem="fs")


def test_package_kind_cannot_be_marked_bootable():
    with pytest.raises(InstallationError, match="cannot be bootable"):
        plan_installation(TargetDescriptor("future-os"), kind=InstallerKind.PACKAGE, artifact_format="pkg", bootable=True)


def test_installer_metadata_is_optional_and_open_world():
    plan = plan_installation(TargetDescriptor("future-os"), artifact_format="pkg", metadata={"future-feature": "enabled"})
    assert plan.metadata["future-feature"] == "enabled"


def test_installation_plan_can_accumulate_build_artifacts():
    plan = plan_installation(TargetDescriptor("os"), artifact_format="image")
    enriched = plan.with_artifact("kernel.bin").with_artifact("rootfs.img")
    assert enriched.artifacts == ("kernel.bin", "rootfs.img")
    assert plan.artifacts == ()


def test_installation_plan_rejects_invalid_artifacts():
    with pytest.raises(ValueError, match="artifacts"):
        InstallationPlan(TargetDescriptor("os"), InstallerKind.PACKAGE, "pkg", artifacts=("",))
    plan = plan_installation(TargetDescriptor("os"), artifact_format="pkg")
    with pytest.raises(ValueError, match="artifact"):
        plan.with_artifact(" ")
