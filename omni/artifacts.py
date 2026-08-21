"""Content-addressed artifact metadata for deterministic Omni outputs."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .targets import TargetDescriptor


@dataclass(frozen=True)
class ArtifactManifest:
    target: TargetDescriptor
    format: str
    digest: str
    size: int

    def __post_init__(self) -> None:
        if not isinstance(self.format, str) or not self.format.strip():
            raise ValueError("artifact format must not be empty")
        if not isinstance(self.digest, str) or len(self.digest) != 64:
            raise ValueError("artifact digest must be a SHA-256 hex digest")
        try:
            int(self.digest, 16)
        except ValueError as exc:
            raise ValueError("artifact digest must be hexadecimal") from exc
        if self.size < 0:
            raise ValueError("artifact size cannot be negative")

    def key(self) -> str:
        return f"sha256:{self.digest}"


def manifest(payload: bytes, target: TargetDescriptor, format: str) -> ArtifactManifest:
    if not isinstance(payload, bytes):
        raise TypeError("artifact payload must be bytes")
    if not isinstance(format, str) or not format.strip():
        raise ValueError("artifact format must not be empty")
    return ArtifactManifest(
        target=target,
        format=format.strip(),
        digest=hashlib.sha256(payload).hexdigest(),
        size=len(payload),
    )
