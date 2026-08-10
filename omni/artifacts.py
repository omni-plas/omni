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


def manifest(payload: bytes, target: TargetDescriptor, format: str) -> ArtifactManifest:
    if not isinstance(payload, bytes):
        raise TypeError("artifact payload must be bytes")
    if not format.strip():
        raise ValueError("artifact format must not be empty")
    return ArtifactManifest(
        target=target,
        format=format,
        digest=hashlib.sha256(payload).hexdigest(),
        size=len(payload),
    )
