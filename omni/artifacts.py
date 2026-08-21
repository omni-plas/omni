"""Content-addressed artifact metadata for deterministic Omni outputs."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .targets import TargetDescriptor


class ArtifactError(ValueError):
    """Raised when an artifact descriptor is invalid."""


@dataclass(frozen=True)
class ArtifactManifest:
    target: TargetDescriptor
    format: str
    digest: str
    size: int
    name: str | None = None
    kind: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.target, TargetDescriptor):
            raise TypeError("artifact target must be a TargetDescriptor")
        if not isinstance(self.format, str) or not self.format.strip():
            raise ArtifactError("artifact format must not be empty")
        if not isinstance(self.digest, str) or len(self.digest) != 64:
            raise ArtifactError("artifact digest must be a SHA-256 hex digest")
        try:
            int(self.digest, 16)
        except ValueError as exc:
            raise ArtifactError("artifact digest must be hexadecimal") from exc
        if not isinstance(self.size, int) or isinstance(self.size, bool) or self.size < 0:
            raise ArtifactError("artifact size cannot be negative")
        for label, value in (("name", self.name), ("kind", self.kind)):
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ArtifactError(f"artifact {label} cannot be empty")

    def key(self) -> str:
        return f"sha256:{self.digest}"

    def identity(self) -> str:
        prefix = self.kind or "artifact"
        name = self.name or self.key()
        return f"{prefix}:{name}:{self.target.identity()}:{self.format.strip()}"


def manifest(
    payload: bytes,
    target: TargetDescriptor,
    format: str,
    *,
    name: str | None = None,
    kind: str | None = None,
) -> ArtifactManifest:
    if not isinstance(payload, bytes):
        raise TypeError("artifact payload must be bytes")
    if not isinstance(target, TargetDescriptor):
        raise TypeError("artifact target must be a TargetDescriptor")
    if not isinstance(format, str) or not format.strip():
        raise ArtifactError("artifact format must not be empty")
    return ArtifactManifest(
        target=target,
        format=format.strip(),
        digest=hashlib.sha256(payload).hexdigest(),
        size=len(payload),
        name=name,
        kind=kind,
    )
