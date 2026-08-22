"""Write validated Omni package manifests and artifacts into deterministic archives."""

from __future__ import annotations

import hashlib
import io
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping

from .packaging import PackageManifest


class PackageWriteError(ValueError):
    """Raised when package inputs cannot be safely archived."""


@dataclass(frozen=True)
class PackageEntry:
    name: str
    payload: bytes


def _safe_name(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise PackageWriteError("package entry name must be non-empty")
    path = PurePosixPath(name.strip())
    if path.is_absolute() or ".." in path.parts or path == PurePosixPath("."):
        raise PackageWriteError("package entry path must remain inside the archive")
    return str(path)


def build_package(manifest: PackageManifest, entries: Mapping[str, bytes]) -> bytes:
    """Build a deterministic ZIP package containing manifest.json and entries."""
    if not isinstance(manifest, PackageManifest):
        raise TypeError("manifest must be a PackageManifest")
    if not isinstance(entries, Mapping):
        raise TypeError("entries must be a mapping")
    normalized: dict[str, bytes] = {}
    for name, payload in entries.items():
        safe = _safe_name(name)
        if not isinstance(payload, bytes):
            raise TypeError(f"package entry {safe} payload must be bytes")
        if safe in normalized:
            raise PackageWriteError(f"duplicate package entry: {safe}")
        normalized[safe] = payload
    declared = set(manifest.artifacts)
    supplied = set(normalized)
    if declared != supplied:
        missing = sorted(declared - supplied)
        extra = sorted(supplied - declared)
        raise PackageWriteError(f"package entries do not match manifest; missing={missing}, extra={extra}")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        _write_entry(archive, "manifest.json", manifest.manifest())
        for name in sorted(normalized):
            _write_entry(archive, name, normalized[name])
    return output.getvalue()


def _write_entry(archive: zipfile.ZipFile, name: str, payload: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    archive.writestr(info, payload)


def write_package(path: str | Path, manifest: PackageManifest, entries: Mapping[str, bytes]) -> str:
    """Write a deterministic package atomically and return its SHA-256 digest."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = build_package(manifest, entries)
    temporary = destination.with_name(destination.name + ".omni-tmp")
    try:
        temporary.write_bytes(payload)
        temporary.replace(destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    return hashlib.sha256(payload).hexdigest()
