"""Cross-platform identity and registration policy for Omni ``.oi`` files.

The .oi format itself is OS-neutral; an operating system cannot infer a file
manager icon from a filename extension alone. This module is the single Omni
source of truth consumed by platform installers. It keeps the canonical
colored logo and extension together and exposes platform-neutral registration
metadata for Windows, macOS, freedesktop/Linux, and future platforms.

Platform installers should convert the canonical JPEG into the native icon
container required by the target OS (ICO, ICNS, SVG/PNG, or a future format)
and register the resulting icon with the OS. The source logo is never
re-colored or replaced.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
import platform


OI_EXTENSION = ".oi"
OI_MIME_TYPE = "text/x-omni"
OI_ICON_ASSET = PurePosixPath("assets/branding/omni-logo.jpg")
OI_ICON_COLOR_MODE = "color"
OI_ICON_POLICY_VERSION = 1


@dataclass(frozen=True)
class OIFileIconPolicy:
    extension: str = OI_EXTENSION
    mime_type: str = OI_MIME_TYPE
    icon_asset: str = str(OI_ICON_ASSET)
    color_mode: str = OI_ICON_COLOR_MODE
    policy_version: int = OI_ICON_POLICY_VERSION

    def platform_registration(self, system: str | None = None) -> dict[str, str]:
        """Return native-registration identifiers for a target OS.

        Unknown systems intentionally receive a generic registration contract;
        Omni can add a native backend later without changing the .oi identity.
        """
        name = (system or platform.system()).lower()
        if name == "windows":
            return {
                "platform": "windows",
                "file_extension": self.extension,
                "content_type": self.mime_type,
                "native_icon_format": "ico",
                "icon_asset": self.icon_asset,
                "icon_color": self.color_mode,
            }
        if name == "darwin":
            return {
                "platform": "macos",
                "file_extension": self.extension,
                "content_type": self.mime_type,
                "native_icon_format": "icns",
                "icon_asset": self.icon_asset,
                "icon_color": self.color_mode,
            }
        if name == "linux" or "bsd" in name:
            return {
                "platform": "freedesktop",
                "file_extension": self.extension,
                "content_type": self.mime_type,
                "native_icon_format": "svg-or-png",
                "icon_asset": self.icon_asset,
                "icon_color": self.color_mode,
            }
        return {
            "platform": "generic",
            "file_extension": self.extension,
            "content_type": self.mime_type,
            "native_icon_format": "native",
            "icon_asset": self.icon_asset,
            "icon_color": self.color_mode,
        }

    def file_icon_manifest(self) -> dict[str, object]:
        """Return the OS-neutral contract used by Omni installers."""
        return {
            "extension": self.extension,
            "mime_type": self.mime_type,
            "icon_asset": self.icon_asset,
            "color_mode": self.color_mode,
            "policy_version": self.policy_version,
            "apply_to": "every .oi file created or registered by Omni",
            "native_conversion_required": True,
        }


OFFICIAL_OI_FILE_ICON_POLICY = OIFileIconPolicy()


def oi_file_icon_policy() -> OIFileIconPolicy:
    """Return the canonical policy for Omni ``.oi`` files."""
    return OFFICIAL_OI_FILE_ICON_POLICY


def native_registration_for_current_os() -> dict[str, str]:
    """Return the registration contract for the current operating system."""
    return OFFICIAL_OI_FILE_ICON_POLICY.platform_registration()
