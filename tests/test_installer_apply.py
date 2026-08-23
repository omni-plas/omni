import pytest

from omni.installer import InstallerKind, plan_installation
from omni.installer_apply import apply_installer
from omni.installer_builder import build_installer


def _bundle():
    plan = plan_installation(
        __import__("omni").TargetDescriptor("linux", "x86_64", "sysv"),
        kind=InstallerKind.PACKAGE,
        artifact_format="omni-package",
        artifacts=("hello.omni",),
    )
    return build_installer(plan, b"payload", filename="hello.omni")


def test_apply_installer_writes_package(tmp_path):
    bundle = _bundle()
    path = apply_installer(bundle.payload, tmp_path)
    assert path.read_bytes() == b"payload"


def test_apply_installer_does_not_overwrite_by_default(tmp_path):
    bundle = _bundle()
    apply_installer(bundle.payload, tmp_path)
    with pytest.raises(ValueError, match="already exists"):
        apply_installer(bundle.payload, tmp_path)
