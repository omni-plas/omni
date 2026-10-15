"""Open-world backend contracts for Omni target generation."""

from __future__ import annotations

from dataclasses import dataclass

from .artifacts import Artifact
from .compiler import CompilationPlan
from .targets import TargetDescriptor
from .uir import UIR


class BackendError(ValueError):
    """Raised when a backend cannot satisfy a compilation request."""


class TargetBackend:
    """Protocol-like base contract implemented by target code generators."""

    name: str

    def supports(self, target: TargetDescriptor) -> bool:
        raise NotImplementedError

    def compile(self, uir: UIR, plan: CompilationPlan) -> Artifact:
        raise NotImplementedError


@dataclass(frozen=True)
class BackendSelection:
    backend: TargetBackend
    target: TargetDescriptor


class BackendRegistry:
    """Explicit, extensible registry; no fixed OS/CPU enumeration."""

    def __init__(self, backends: tuple[TargetBackend, ...] = ()) -> None:
        self._backends = tuple(backends)

    def register(self, backend: TargetBackend) -> "BackendRegistry":
        if not isinstance(getattr(backend, "name", None), str) or not backend.name.strip():
            raise BackendError("backend name must be a non-empty string")
        if not callable(getattr(backend, "supports", None)) or not callable(getattr(backend, "compile", None)):
            raise BackendError("backend must provide supports() and compile()")
        if any(existing.name == backend.name for existing in self._backends):
            raise BackendError(f"backend already registered: {backend.name}")
        return BackendRegistry(self._backends + (backend,))

    def select(self, target: TargetDescriptor) -> BackendSelection:
        if not isinstance(target, TargetDescriptor):
            raise TypeError("target must be a TargetDescriptor")
        matches = [backend for backend in self._backends if backend.supports(target)]
        if not matches:
            raise BackendError(f"no backend supports target {target.identity()}")
        if len(matches) > 1:
            raise BackendError(f"multiple backends support target {target.identity()}: {', '.join(b.name for b in matches)}")
        return BackendSelection(matches[0], target)

    def names(self) -> tuple[str, ...]:
        return tuple(backend.name for backend in self._backends)


class GenericArtifactBackend:
    """Backend that materializes validated UIR as a deterministic semantic artifact."""

    name = "generic-semantic-artifact"

    def supports(self, target: TargetDescriptor) -> bool:
        return target.supports("semantic-artifact", True)

    def compile(self, uir: UIR, plan: CompilationPlan) -> Artifact:
        if not self.supports(plan.target):
            raise BackendError(f"backend does not support {plan.target.identity()}")
        import json
        payload = (json.dumps(uir.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        return Artifact(plan.target, payload, "json", name=uir.entity_name, kind=uir.entity_kind)
