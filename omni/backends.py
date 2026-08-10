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
    """Lowers semantic UIR into a concrete artifact for a target."""

    def emit(self, program: UIR, target: TargetDescriptor) -> Artifact:
        ...
