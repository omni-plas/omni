import pytest

from omni.installer import InstallerKind, plan_installation
from omni.installer_builder import build_installer
from omni.installer_verify import InstallerVerificationError, verify_installer
from omni.targets import TargetDescriptor


def _bundle():
    target = TargetDescriptor("linux", "x86_64", "sysv")
    plan = plan_installation(
        target,
        kind=InstallerKind.PACKAGE,
        artifact_format="omni-package",
        artifacts=("app.omni",),
    )
    return build_installer(plan, b"payload", filename="app.omni")


def test_installer_verifies_package_digest():
    bundle = _bundle()
    result = verify_installer(bundle.payload)
    assert result["package_name"] == "app.omni"
    assert result["package_size"] == 7


def test_installer_rejects_corruption():
    bundle = _bundle()
    corrupted = bytearray(bundle.payload)
    corrupted[-1] ^= 0x01
    with pytest.raises(InstallerVerificationError):
        verify_installer(bytes(corrupted))
