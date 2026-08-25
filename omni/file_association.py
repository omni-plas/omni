"""Canonical Omni source-file association metadata."""
from __future__ import annotations
from pathlib import PurePosixPath

OMNI_SOURCE_EXTENSION = ".oi"
OMNI_LOGO_ASSET = PurePosixPath("assets/branding/omni-logo.jpg")

def source_file_association():
    return {
        "extension": OMNI_SOURCE_EXTENSION,
        "language": "Omni",
        "mime": "text/x-omni",
        "icon": str(OMNI_LOGO_ASSET),
        "open_command": "omni",
    }
