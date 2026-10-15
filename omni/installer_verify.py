"""Verify Omni installer bundles before installation or distribution."""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
import zlib
from typing import Any


class InstallerVerificationError(ValueError):
    """Raised when an installer bundle is malformed or fails integrity checks."""


def verify_installer(payload: bytes) -> dict[str, Any]:
    if not isinstance(payload, bytes):
        raise TypeError("installer payload must be bytes")
    try:
        with zipfile.ZipFile(io.BytesIO(payload), "r") as archive:
            names = archive.namelist()
            if "install.json" not in names:
                raise InstallerVerificationError("installer is missing install.json")
            manifest = json.loads(archive.read("install.json").decode("utf-8"))
            if not isinstance(manifest, dict):
                raise InstallerVerificationError("installer manifest must be an object")
            package_name = next((name for name in names if name != "install.json"), None)
            if package_name is None:
                raise InstallerVerificationError("installer contains no package payload")
            package = archive.read(package_name)
            expected_digest = manifest.get("package_digest")
            expected_size = manifest.get("package_size")
            if expected_digest != hashlib.sha256(package).hexdigest():
                raise InstallerVerificationError("installer package digest mismatch")
            if expected_size != len(package):
                raise InstallerVerificationError("installer package size mismatch")
            return {"manifest": manifest, "package_name": package_name, "package_size": len(package)}
    except (zipfile.BadZipFile, OSError, EOFError, zlib.error, RuntimeError) as exc:
        raise InstallerVerificationError("invalid or corrupted installer archive") from exc
