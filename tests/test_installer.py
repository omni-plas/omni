import json

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


def test_recovery_installers_require_bootable_flag_and_filesystem():
    with pytest.raises(InstallationError, match="bootable"):
        plan_installation(TargetDescriptor("future-os"), kind=InstallerKind.RECOVERY, artifact_format="image", filesystem="fs")
    with pytest.raises(InstallationError, match="filesystem"):
        plan_installation(TargetDescriptor("future-os"), kind=InstallerKind.RECOVERY, artifact_format="image", bootable=True)


def test_package_kind_cannot_be_marked_bootable():
    with pytest.raises(InstallationError, match="cannot be bootable"):
        plan_installation(TargetDescriptor("future-os"), kind=InstallerKind.PACKAGE, artifact_format="pkg", bootable=True)


def test_installer_metadata_is_optional_and_open_world():
    plan = plan_installation(TargetDescriptor("future-os"), artifact_format="pkg", metadata={"future-feature": "enabled"})
    assert plan.metadata["future-feature"] == "enabled"


def test_installation_plan_can_accumulate_and_normalize_build_artifacts():
    plan = plan_installation(TargetDescriptor("os"), artifact_format="image")
    enriched = plan.with_artifact(" kernel.bin ").with_artifact("rootfs.img")
    assert enriched.artifacts == ("kernel.bin", "rootfs.img")
    assert plan.artifacts == ()


def test_installation_plan_rejects_invalid_artifacts():
    with pytest.raises(ValueError, match="artifacts"):
        InstallationPlan(TargetDescriptor("os"), InstallerKind.PACKAGE, "pkg", artifacts=("",))
    plan = plan_installation(TargetDescriptor("os"), artifact_format="pkg")
    with pytest.raises(ValueError, match="artifact"):
        plan.with_artifact(" ")


def test_manifest_is_canonical_and_deterministic():
    target = TargetDescriptor(
        "future-os", "future-cpu", "future-abi",
        capabilities={"z": "last", "a": {"enabled": True}},
    )
    plan = plan_installation(
        target,
        kind=InstallerKind.BOOTABLE,
        artifact_format="future-image",
        bootable=True,
        filesystem=" future-fs ",
        artifacts=("kernel.bin", "rootfs.img"),
        metadata={"version": "1", "channel": "future"},
    )
    document = json.loads(plan.manifest())
    assert document["schema"] == "omni.installation.v1"
    assert document["identity"] == plan.identity()
    assert document["target"]["capabilities"]["a"] == {"enabled": True}
    assert document["filesystem"] == "future-fs"
    assert plan.manifest() == plan.manifest()


def test_render_manifest_is_human_readable_and_matches_document():
    plan = plan_installation(TargetDescriptor("historical-os"), artifact_format="legacy-package")
    assert json.loads(plan.render_manifest()) == plan.manifest_document()


def test_manifest_round_trip_preserves_plan():
    plan = plan_installation(
        TargetDescriptor("future-os", "future-cpu", capabilities={"mode": "next"}),
        kind=InstallerKind.BOOTABLE,
        artifact_format="future-image",
        bootable=True,
        filesystem="future-fs",
        artifacts=("kernel.bin",),
        metadata={"channel": "nightly"},
    )
    restored = InstallationPlan.from_manifest(plan.manifest())
    assert restored == plan


def test_manifest_rejects_unknown_schema():
    with pytest.raises(InstallationError, match="unsupported"):
        InstallationPlan.from_manifest('{"schema":"omni.installation.v999"}')


def test_manifest_rejects_tampered_identity():
    document = plan_installation(TargetDescriptor("os"), artifact_format="pkg").manifest_document()
    document["identity"] = "tampered"
    with pytest.raises(InstallationError, match="identity"):
        InstallationPlan.from_document(document)


def test_manifest_rejects_malformed_json():
    with pytest.raises(InstallationError, match="JSON"):
        InstallationPlan.from_manifest("not-json")
