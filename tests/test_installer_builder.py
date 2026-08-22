import io
import zipfile

import pytest

from omni.installer import InstallerKind, plan_installation
from omni.installer_builder import InstallerBuildError, build_installer
from omni.targets import TargetDescriptor


def _plan():
    return plan_installation(
        TargetDescriptor("future-os", "future-cpu"),
        kind=InstallerKind.BOOTABLE,
        artifact_format="future-image",
        bootable=True,
        filesystem="future-fs",
    )


def test_build_installer_contains_install_manifest_and_package():
    bundle = build_installer(_plan(), b"package")
    with zipfile.ZipFile(io.BytesIO(bundle.payload)) as archive:
        assert archive.namelist() == ["install.json", "package.omni"]
        assert archive.read("package.omni") == b"package"
        assert b"omni.installation.v1" in archive.read("install.json")


def test_build_installer_is_deterministic():
    assert build_installer(_plan(), b"package").payload == build_installer(_plan(), b"package").payload


def test_build_installer_records_package_digest():
    bundle = build_installer(_plan(), b"package")
    with zipfile.ZipFile(io.BytesIO(bundle.payload)) as archive:
        text = archive.read("install.json")
        assert b"package_digest" in text
        assert b"package_size" in text


def test_build_installer_rejects_invalid_filename():
    with pytest.raises(InstallerBuildError, match="filename"):
        build_installer(_plan(), b"package", filename="../package.omni")
