"""Generate OS-native registration metadata for Omni ``.oi`` files.

The source extension and artwork remain platform-independent.  This module
turns the canonical Omni icon policy into deterministic registration records
that an installer can apply on the host operating system.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from .oi_file_icon import OI_ICON_ASSET, OI_MIME_TYPE, oi_file_icon_policy


@dataclass(frozen=True)
class OIRegistration:
    platform: str
    extension: str
    mime_type: str
    icon_asset: str
    icon_color: str
    native_icon_format: str
    association_name: str = "Omni Source File"


def registration_for(platform_name: str) -> OIRegistration:
    """Return the deterministic native registration contract for a platform."""
    policy = oi_file_icon_policy()
    registration = policy.platform_registration(platform_name)
    return OIRegistration(
        platform=registration["platform"],
        extension=policy.extension,
        mime_type=OI_MIME_TYPE,
        icon_asset=str(OI_ICON_ASSET),
        icon_color=registration["icon_color"],
        native_icon_format=registration["native_icon_format"],
    )


def render_registration_manifest() -> str:
    """Render all currently-known platform registrations as stable JSON."""
    platforms = ("Windows", "Darwin", "Linux", "FutureOS")
    payload = {
        "format": "omni-oi-registration",
        "version": 1,
        "extension": ".oi",
        "icon": {"asset": str(OI_ICON_ASSET), "color": "color"},
        "registrations": [asdict(registration_for(name)) for name in platforms],
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
