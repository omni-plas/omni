import hashlib
import json

import pytest

from omni.installer import InstallerKind, plan_installation
from omni.packaging import PackageManifest
from omni.release_pipeline import ReleasePipelineError, build_release, write_release
from omni.targets import TargetDescriptor


def make_release():
    target = TargetDescriptor("future-os", "future-cpu", "future-abi")
    package = PackageManifest("future-os", "1.0", target, artifacts=("system.img",))
    plan = plan_installation(
        target,
        kind=InstallerKind.BOOTABLE,
        artifact_format="omni-package",
        bootable=True,
        filesystem="future-fs",
        artifacts=("package.omni",),
    )
    return build_release(package, plan, {"system.img": b"kernel-and-rootfs"})


def test_release_builds_package_and_installer():
    result = make_release()
    assert result.package_payload.startswith(b"PK")
    assert result.installer.payload.startswith(b"PK")
    assert result.package_digest == hashlib.sha256(result.package_payload).hexdigest()
    assert result.installer_digest == hashlib.sha256(result.installer.payload).hexdigest()


def test_release_installer_manifest_contains_package_digest():
    result = make_release()
    import zipfile
    from io import BytesIO
    with zipfile.ZipFile(BytesIO(result.installer.payload)) as archive:
        manifest = json.loads(archive.read("install.json"))
    assert manifest["package_digest"] == result.package_digest
    assert manifest["package_size"] == len(result.package_payload)


def test_release_rejects_target_mismatch():
    target = TargetDescriptor("os-a")
    other = TargetDescriptor("os-b")
    package = PackageManifest("os", "1", target, artifacts=("image",))
    plan = plan_installation(other, artifact_format="pkg", artifacts=("package.omni",))
    with pytest.raises(ReleasePipelineError, match="targets"):
        build_release(package, plan, {"image": b"x"}, package_filename="package.omni")


def test_release_requires_declared_package_filename():
    target = TargetDescriptor("os")
    package = PackageManifest("os", "1", target, artifacts=("image",))
    plan = plan_installation(target, artifact_format="pkg", artifacts=("other.omni",))
    with pytest.raises(ReleasePipelineError, match="filename"):
        build_release(package, plan, {"image": b"x"})


def test_write_release_rejects_path_traversal(tmp_path):
    target = TargetDescriptor("os")
    package = PackageManifest("os", "1", target, artifacts=("image",))
    plan = plan_installation(target, artifact_format="pkg", artifacts=("package.omni",))
    with pytest.raises(ReleasePipelineError, match="plain filename"):
        write_release(tmp_path, package, plan, {"image": b"x"}, package_filename="../package.omni")


def test_write_release_rejects_same_output_name(tmp_path):
    target = TargetDescriptor("os")
    package = PackageManifest("os", "1", target, artifacts=("package.omni",))
    plan = plan_installation(target, artifact_format="pkg", artifacts=("package.omni",))
    with pytest.raises(ReleasePipelineError, match="filenames must differ"):
        write_release(tmp_path, package, plan, {"package.omni": b"x"}, installer_filename="package.omni")
