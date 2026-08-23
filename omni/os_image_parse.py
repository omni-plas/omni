"""Parser and verifier for the Omni OS image container."""
from __future__ import annotations

import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import PurePosixPath

from .os_image import OSImageError
from .targets import TargetDescriptor


@dataclass(frozen=True)
class OSImageFile:
    path: str
    payload: bytes


@dataclass(frozen=True)
class ParsedOSImage:
    target: TargetDescriptor
    files: tuple[OSImageFile, ...]
    digest: str


def _validate_path(path: str) -> str:
    parsed = PurePosixPath(path)
    if not path or parsed.is_absolute() or ".." in parsed.parts or path.endswith("/"):
        raise OSImageError(f"unsafe OS image path: {path!r}")
    return path


def parse_os_image(payload: bytes) -> ParsedOSImage:
    if not isinstance(payload, bytes):
        raise TypeError("OS image payload must be bytes")
    if not payload.startswith(b"OMNIOS1\0"):
        raise OSImageError("invalid Omni OS image magic")
    offset = 8
    if len(payload) < offset + 4:
        raise OSImageError("truncated OS image header")
    header_len = struct.unpack_from("<I", payload, offset)[0]
    offset += 4
    if header_len > len(payload) - offset:
        raise OSImageError("truncated OS image metadata")
    try:
        header = json.loads(payload[offset:offset + header_len].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OSImageError("invalid OS image metadata") from exc
    offset += header_len
    if not isinstance(header, dict) or header.get("format") != "omni-os-image-v1":
        raise OSImageError("unsupported OS image format")
    target_doc = header.get("target")
    if not isinstance(target_doc, dict):
        raise OSImageError("OS image target is missing")
    try:
        target = TargetDescriptor.from_document(target_doc)
    except Exception as exc:
        raise OSImageError("invalid OS image target") from exc
    count = header.get("file_count")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise OSImageError("OS image file_count must be a positive integer")
    files: list[OSImageFile] = []
    seen: set[str] = set()
    for _ in range(count):
        if len(payload) < offset + 12:
            raise OSImageError("truncated OS image entry")
        name_len, data_len = struct.unpack_from("<IQ", payload, offset)
        offset += 12
        if name_len == 0 or name_len > len(payload) - offset:
            raise OSImageError("truncated OS image path")
        try:
            name = payload[offset:offset + name_len].decode("utf-8")
        except UnicodeDecodeError as exc:
            raise OSImageError("invalid OS image path") from exc
        offset += name_len
        _validate_path(name)
        if name in seen:
            raise OSImageError(f"duplicate OS image path: {name!r}")
        seen.add(name)
        if data_len > len(payload) - offset:
            raise OSImageError("truncated OS image payload")
        data = payload[offset:offset + data_len]
        offset += data_len
        files.append(OSImageFile(name, data))
    if offset != len(payload):
        raise OSImageError("unexpected trailing bytes in OS image")
    return ParsedOSImage(target, tuple(files), hashlib.sha256(payload).hexdigest())
