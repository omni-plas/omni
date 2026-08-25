"""Canonical Omni source-file association metadata."""
from __future__ import annotations

from .oi_file_icon import OI_ICON_ASSET, OI_EXTENSION, OI_MIME_TYPE

OMNI_SOURCE_EXTENSION = OI_EXTENSION
OMNI_LOGO_ASSET = OI_ICON_ASSET


def source_file_association():
    return {
        "extension": OMNI_SOURCE_EXTENSION,
        "language": "Omni",
        "mime": OI_MIME_TYPE,
        "icon": str(OMNI_LOGO_ASSET),
        "icon_color": "color",
        "open_command": "omni",
    }
