"""Apply validated Omni installer payloads to a destination safely.

This layer deliberately installs package payloads only. OS-specific registration,
boot integration, service creation, and privileged operations belong to target
backends and are not guessed here.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from .installer_runtime import InstallerRuntimeError, inspect_installer


def apply_installer(payload: bytes, destination: str | Path, *, overwrite: bool = False) -> Path:
    """Validate an installer and atomically place its package in *destination*."""
    info = inspect_installer(payload)
    root = Path(destination)
    root.mkdir(parents=True, exist_ok=True)
    package_name = Path(info["package_name"]).name
    if not package_name or package_name in {".", ".."}:
        raise InstallerRuntimeError("invalid installer package name")
    target = root / package_name
    if target.exists() and not overwrite:
        raise InstallerRuntimeError(f"installation target already exists: {target}")
    temporary = target.with_name(target.name + ".omni-install-tmp")
    from io import BytesIO
    import zipfile
    try:
        with zipfile.ZipFile(BytesIO(payload), "r") as archive:
            data = archive.read(info["package_name"])
        temporary.write_bytes(data)
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    return target
