"""Target backend contracts and deterministic artifact emission."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .targets import TargetDescriptor
from .uir import UIR


@dataclass(frozen=True)
class Artifact:
    target: TargetDescriptor
    payload: bytes
    format: str

    def __post_init__(self) -> None:
        if not isinstance(self.payload, bytes):
            raise TypeError("artifact payload must be bytes")
        if not isinstance(self.format, str) or not self.format.strip():
            raise ValueError("artifact format must be a non-empty string")


class Backend(Protocol):
    """Backend capability for turning validated Omni programs into artifacts."""

    def supports_target(self, target: TargetDescriptor) -> bool:
        """Return whether this backend can emit the requested target."""
        ...

    def emit(self, program: UIR, target: TargetDescriptor) -> Artifact:
        """Emit an artifact after target compatibility has been established."""
        ...


def emit_with_backend(backend: Backend, program: UIR, target: TargetDescriptor) -> Artifact:
    """Enforce declared capability and artifact invariants before materialization."""
    if not callable(getattr(backend, "supports_target", None)) or not callable(getattr(backend, "emit", None)):
        raise TypeError("backend must provide supports_target() and emit()")
    if not backend.supports_target(target):
        raise LookupError(f"backend does not support target {target.identity()}")
    artifact = backend.emit(program, target)
    if not isinstance(artifact, Artifact):
        raise TypeError("backend.emit() must return Artifact")
    if artifact.target != target:
        raise ValueError("backend returned artifact for a different target")
    return artifact
