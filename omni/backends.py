"""Target backend contracts."""

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


class Backend(Protocol):
    """Backend capability for turning validated Omni programs into artifacts."""

    def supports_target(self, target: TargetDescriptor) -> bool:
        """Return whether this backend can emit the requested target."""
        ...

    def emit(self, program: UIR, target: TargetDescriptor) -> Artifact:
        """Emit an artifact after target compatibility has been established."""
        ...
