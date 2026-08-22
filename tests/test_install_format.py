import pytest

from omni.install_format import InstallFormat, InstallFormatError
from omni.targets import TargetDescriptor


def test_install_format_supports_future_targets():
    target = TargetDescriptor("future-os", "future-cpu", "future-abi")
    fmt = InstallFormat("future-installer", "1", target, bootable=True, filesystem="future-fs")
    assert fmt.identity() == "future-installer:1:future-os-future-cpu-future-abi"


def test_bootable_format_requires_filesystem():
    with pytest.raises(InstallFormatError, match="filesystem"):
        InstallFormat("installer", "1", TargetDescriptor("future-os"), bootable=True)


def test_install_format_rejects_empty_version():
    with pytest.raises(InstallFormatError, match="version"):
        InstallFormat("installer", "", TargetDescriptor("future-os"))


def test_install_format_metadata_is_open_world():
    fmt = InstallFormat("installer", "1", TargetDescriptor("historical-os"), metadata={"legacy": True})
    assert fmt.metadata["legacy"] is True
