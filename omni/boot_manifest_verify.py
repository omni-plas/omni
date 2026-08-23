"""Verify boot artifacts against their canonical manifest."""
from __future__ import annotations

import hashlib
import json

from .boot_backend import BootArtifact
from .boot_manifest import BootManifest
from .os_image import OSImageError


def verify_boot_manifest(artifact: BootArtifact, manifest: BootManifest) -> None:
    if artifact.target.to_document() != manifest.target:
        raise OSImageError("boot artifact target does not match manifest")
    if artifact.format != manifest.artifact_format:
        raise OSImageError("boot artifact format does not match manifest")
    digest = hashlib.sha256(artifact.payload).hexdigest()
    if digest != artifact.digest or digest != manifest.artifact_digest:
        raise OSImageError("boot artifact integrity check failed")
    try:
        document = json.loads(manifest.to_bytes().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OSImageError("invalid boot manifest serialization") from exc
    if document.get("format") != "omni-boot-manifest-v1":
        raise OSImageError("unsupported boot manifest format")
