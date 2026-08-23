"""Deterministic target-neutral OS image construction primitives."""

from __future__ import annotations

import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import PurePosixPath

from .targets import TargetDescriptor


class OSImageError(ValueError):
    pass


@dataclass(frozen=True)
class OSImage:
    target: TargetDescriptor
    payload: bytes
    digest: str
    format: str = "omni-os-image-v1"


def _safe_path(path: str) -> str:
    p = PurePosixPath(path)
    if p.is_absolute() or ".." in p.parts or not path or path.endswith("/"):
        raise OSImageError(f"unsafe image path: {path!r}")
    return str(p)


def build_os_image(target: TargetDescriptor, files: dict[str, bytes], *, boot_contract=None) -> OSImage:
    """Build a deterministic Omni OS image container.

    A target-neutral image is not claimed to be bootable by itself. When a
    BootContract is supplied, its target and required boot capabilities are
    validated before image creation.
    """
    if not files:
        raise OSImageError("OS image must contain at least one file")
    if boot_contract is not None:
        from .boot_contract import require_boot_capabilities
        require_boot_capabilities(target, boot_contract)
    entries: list[tuple[str, bytes]] = []
    for name, data in files.items():
        safe = _safe_path(name)
        if not isinstance(data, bytes):
            raise TypeError("image file payloads must be bytes")
        entries.append((safe, data))
    entries.sort(key=lambda item: item[0])
    header = {
        "format": "omni-os-image-v1",
        "target": target.to_document(),
        "file_count": len(entries),
        "boot_contract": None if boot_contract is None else {
            "boot_protocol": boot_contract.boot_protocol,
            "firmware": boot_contract.firmware,
            "filesystem": boot_contract.filesystem,
            "entrypoint": boot_contract.entrypoint,
        },
    }
    out = bytearray(b"OMNIOS1\0")
    encoded = json.dumps(header, sort_keys=True, separators=(",", ":")).encode()
    out += struct.pack("<I", len(encoded)) + encoded
    for name, data in entries:
        name_bytes = name.encode("utf-8")
        out += struct.pack("<IQ", len(name_bytes), len(data))
        out += name_bytes + data
    payload = bytes(out)
    return OSImage(target, payload, hashlib.sha256(payload).hexdigest())
