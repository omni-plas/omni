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
    """Resolve the first backend that declares support for a target.

    Resolution is intentionally open-world: no operating-system, CPU, ABI, or
    backend list is hard-coded. Backends may inspect arbitrary target
    capabilities through ``supports_target``.
    """
    if not isinstance(target, TargetDescriptor):
        raise TypeError("target must be a TargetDescriptor")
    if backends is None:
        raise TypeError("backends cannot be None")
    for backend in backends:
        supports = getattr(backend, "supports_target", None)
        if not callable(supports):
            continue
        try:
            supported = bool(supports(target))
        except Exception as exc:
            raise TargetResolutionError(
                f"backend {type(backend).__name__} failed while checking target {target.identity()}: {exc}"
            ) from exc
        if supported:
            return TargetMatch(target=target, backend=backend)
    raise TargetResolutionError(f"no backend supports target {target.identity()}")
