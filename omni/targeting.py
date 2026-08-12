"""Target capability resolution and backend selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .backends import Backend
from .targets import TargetDescriptor


@dataclass(frozen=True)
class TargetMatch:
    target: TargetDescriptor
    backend: Backend


class TargetResolutionError(LookupError):
    """Raised when no registered backend can satisfy a target."""


def resolve_target(target: TargetDescriptor, backends: Iterable[Backend]) -> TargetMatch:
    """Resolve a backend using its declared target capability.

    Backends may expose ``supports_target``; absence means the backend is not
    considered compatible. No operating-system or CPU list is hard-coded here.
    """
    for backend in backends:
        supports = getattr(backend, "supports_target", None)
        if callable(supports) and bool(supports(target)):
            return TargetMatch(target=target, backend=backend)
    raise TargetResolutionError(f"no backend supports target {target.identity()}")
