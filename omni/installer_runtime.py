"""Safe runtime operations for Omni installer bundles."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

from .installer import InstallationPlan


class InstallerRuntimeError(ValueError):
    pass


def inspect_installer(payload: bytes) -> dict:
    if not isinstance(payload, bytes):
        raise TypeError("installer payload must be bytes")
    try:
        from io import BytesIO
        with zipfile.ZipFile(BytesIO(payload), "r") as archive:
            names = archive.namelist()
            if "install.json" not in names:
                raise InstallerRuntimeError("installer is missing install.json")
            manifest = json.loads(archive.read("install.json").decode("utf-8"))
            if not isinstance(manifest, dict):
                raise InstallerRuntimeError("installer manifest must be an object")
            package_names = [n for n in names if n != "install.json"]
            if len(package_names) != 1:
                raise InstallerRuntimeError("installer must contain exactly one package payload")
            package_name = package_names[0]
            package = archive.read(package_name)
            expected_size = manifest.get("package_size")
            expected_digest = manifest.get("package_digest")
            if expected_size != len(package):
                raise InstallerRuntimeError("installer package size mismatch")
            if expected_digest != hashlib.sha256(package).hexdigest():
                raise InstallerRuntimeError("installer package digest mismatch")
            return {"manifest": manifest, "package_name": package_name, "package_size": len(package), "package_digest": expected_digest}
    except zipfile.BadZipFile as exc:
        raise InstallerRuntimeError("invalid installer archive") from exc


def extract_installer(payload: bytes, destination: str | Path, *, plan: InstallationPlan | None = None) -> Path:
    info = inspect_installer(payload)
    manifest = info["manifest"]
    if plan is not None and manifest.get("target") != plan.target.identity():
        raise InstallerRuntimeError("installer target does not match requested installation plan")
    root = Path(destination)
    root.mkdir(parents=True, exist_ok=True)
    package_path = root / Path(info["package_name"]).name
    from io import BytesIO
    with zipfile.ZipFile(BytesIO(payload), "r") as archive:
        package_path.write_bytes(archive.read(info["package_name"]))
    return package_path
