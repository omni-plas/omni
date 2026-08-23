from omni.target_installers import InstallerFormat, resolve_installer_target
from omni.targets import TargetDescriptor


def test_windows_target_selects_windows_installer():
    result = resolve_installer_target(TargetDescriptor("windows", "x86_64", "msvc"))
    assert result.format is InstallerFormat.WINDOWS


def test_linux_target_selects_linux_package():
    result = resolve_installer_target(TargetDescriptor("linux", "x86_64", "sysv"))
    assert result.format is InstallerFormat.LINUX


def test_unknown_future_target_remains_open_world():
    target = TargetDescriptor("future-os", "future-cpu", "future-abi")
    result = resolve_installer_target(target)
    assert result.format is InstallerFormat.CUSTOM
    assert result.target == target


def test_bootable_target_is_marked_bootable():
    result = resolve_installer_target(TargetDescriptor("bootable"))
    assert result.format is InstallerFormat.BOOTABLE
    assert result.bootable is True
