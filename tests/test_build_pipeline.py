import pytest

from omni.build_pipeline import BuildPipelineError, create_os_build_plan
from omni.installer import InstallerKind
from omni.os_model import OperatingSystemSpec
from omni.targets import TargetDescriptor


def test_build_pipeline_connects_os_package_and_installer():
    os = OperatingSystemSpec(
        "future-os",
        TargetDescriptor("future-os", "future-cpu"),
        kernel="kernel.omni",
        filesystem="future-fs",
    )
    plan = create_os_build_plan(os, version="1.0", artifact_format="future-image")
    assert plan.package.target == os.target
    assert plan.installer.target == os.target
    assert plan.installer.kind is InstallerKind.BOOTABLE


def test_build_pipeline_rejects_non_os_input():
    with pytest.raises(TypeError, match="OperatingSystemSpec"):
        create_os_build_plan(None, version="1", artifact_format="image")


def test_build_plan_requires_matching_targets():
    os = OperatingSystemSpec("os", TargetDescriptor("future-os"), kernel="kernel")
    from omni.installer import InstallationPlan
    from omni.packaging import PackageManifest
    bad_package = PackageManifest("os", "1", TargetDescriptor("other-os"))
    installer = InstallationPlan(TargetDescriptor("future-os"), InstallerKind.PACKAGE, "pkg")
    with pytest.raises(BuildPipelineError, match="package target"):
        from omni.build_pipeline import OSBuildPlan
        OSBuildPlan(os, bad_package, installer)


def test_build_metadata_remains_open_world():
    os = OperatingSystemSpec("os", TargetDescriptor("historical-os"), kernel="kernel")
    plan = create_os_build_plan(
        os,
        version="1",
        artifact_format="historical-package",
        installer_kind=InstallerKind.PACKAGE,
        bootable=False,
        metadata={"era": "1990s", "custom-step": "legacy-loader"},
    )
    assert plan.metadata["custom-step"] == "legacy-loader"
