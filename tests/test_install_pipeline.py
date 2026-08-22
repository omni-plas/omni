import pytest

from omni.install_pipeline import InstallPipelineError, create_install_pipeline
from omni.installer import InstallerKind
from omni.target_specs import TargetSpecification
from omni.targets import TargetDescriptor


def test_install_pipeline_requires_target_boot_spec_for_bootable_output():
    spec = TargetSpecification(TargetDescriptor("future-os"), package_format="pkg")
    with pytest.raises(InstallPipelineError, match="boot protocol"):
        create_install_pipeline(spec, name="installer", version="1", artifact_format="image", bootable=True, filesystem="fs", kind=InstallerKind.BOOTABLE)


def test_install_pipeline_builds_bootable_future_target():
    target = TargetDescriptor("future-os", "future-cpu")
    spec = TargetSpecification(target, boot_protocol="future-boot", package_format="future-pkg", installation_protocol="future-install")
    pipeline = create_install_pipeline(spec, name="future-installer", version="1", artifact_format="future-image", bootable=True, filesystem="future-fs", kind=InstallerKind.BOOTABLE)
    assert pipeline.plan.target == target
    assert pipeline.format.target == target


def test_install_pipeline_supports_nonbootable_historical_target():
    target = TargetDescriptor("historical-os")
    spec = TargetSpecification(target, package_format="legacy-pkg")
    pipeline = create_install_pipeline(spec, name="legacy-installer", version="1", artifact_format="legacy-pkg")
    assert pipeline.plan.kind is InstallerKind.PACKAGE
