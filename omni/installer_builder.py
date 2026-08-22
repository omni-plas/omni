"""Build deterministic installer bundles from validated installation plans."""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from dataclasses import dataclass
from pathlib import Path

from .installer import InstallationPlan


class InstallerBuildError(ValueError):
    """Raised when an installer bundle cannot be constructed safely."""


@dataclass(frozen=True)
class InstallerBundle:
    payload: bytes
    digest: str


def build_installer(plan: InstallationPlan, package_payload: bytes, *, filename: str = "package.omni") -> InstallerBundle:
    """Wrap a package artifact in a deterministic Omni installer bundle."""
    if not isinstance(plan, InstallationPlan):
        raise TypeError("plan must be an InstallationPlan")
    if not isinstance(package_payload, bytes):
        raise TypeError("package payload must be bytes")
    if not isinstance(filename, str) or not filename.strip() or "/" in filename or "\\" in filename or filename in {".", ".."}:
        raise InstallerBuildError("installer package filename must be a simple file name")
    document = plan.manifest_document()
    document["package_digest"] = hashlib.sha256(package_payload).hexdigest()
    document["package_size"] = len(package_payload)
    manifest = (json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        _entry(archive, "install.json", manifest)
        _entry(archive, filename.strip(), package_payload)
    payload = output.getvalue()
    return InstallerBundle(payload, hashlib.sha256(payload).hexdigest())


def write_installer(path: str | Path, plan: InstallationPlan, package_payload: bytes, *, filename: str = "package.omni") -> str:
    """Atomically write an installer bundle and return its SHA-256 digest."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    bundle = build_installer(plan, package_payload, filename=filename)
    temporary = destination.with_name(destination.name + ".omni-tmp")
    try:
        temporary.write_bytes(bundle.payload)
        temporary.replace(destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    return bundle.digest


def _entry(archive: zipfile.ZipFile, name: str, payload: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    archive.writestr(info, payload)
