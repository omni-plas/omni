"""Target-aware installer planning without assuming a host OS installer tool."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .targets import TargetDescriptor


class InstallerFormat(str, Enum):
    PORTABLE = "portable"
    WINDOWS = "windows-installer"
    LINUX = "linux-package"
    MACOS = "macos-installer"
    ANDROID = "android-package"
    BOOTABLE = "bootable-image"
    CUSTOM = "custom"


@dataclass(frozen=True)
class InstallerTarget:
    target: TargetDescriptor
    format: InstallerFormat
    install_root: str = ""
    bootable: bool = False


def resolve_installer_target(target: TargetDescriptor) -> InstallerTarget:
    platform = (target.platform or "").lower()
    if platform in {"windows", "win32"}:
        return InstallerTarget(target, InstallerFormat.WINDOWS)
    if platform in {"linux", "gnu-linux"}:
        return InstallerTarget(target, InstallerFormat.LINUX)
    if platform in {"macos", "darwin"}:
        return InstallerTarget(target, InstallerFormat.MACOS)
    if platform in {"android"}:
        return InstallerTarget(target, InstallerFormat.ANDROID)
    if platform in {"os-image", "operating-system", "bootable"}:
        return InstallerTarget(target, InstallerFormat.BOOTABLE, bootable=True)
    if platform in {"portable", "semantic-artifact"}:
        return InstallerTarget(target, InstallerFormat.PORTABLE)
    return InstallerTarget(target, InstallerFormat.CUSTOM)
