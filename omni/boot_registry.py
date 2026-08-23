"""Registry for target boot backends without a closed platform list."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .boot_backend import BootArtifact, BootBackend, ContainerBootBackend
from .boot_contract import BootContract
from .os_image import OSImage, OSImageError


@dataclass(frozen=True)
class BootBackendMatch:
    backend: BootBackend
    score: int


class BootBackendRegistry:
    def __init__(self, backends: Iterable[BootBackend] = ()) -> None:
        self._backends: dict[str, BootBackend] = {}
        for backend in backends:
            self.register(backend)

    def register(self, backend: BootBackend) -> None:
        name = getattr(backend, "name", None)
        if not isinstance(name, str) or not name.strip():
            raise TypeError("boot backend must expose a non-empty name")
        if name in self._backends:
            raise ValueError(f"boot backend already registered: {name}")
        self._backends[name] = backend

    def get(self, name: str) -> BootBackend:
        try:
            return self._backends[name]
        except KeyError as exc:
            raise OSImageError(f"unknown boot backend: {name}") from exc

    def select(self, image: OSImage, contract: BootContract, preferred: str | None = None) -> BootBackend:
        if preferred:
            return self.get(preferred)
        # The neutral backend is always available as a safe baseline. Native
        # backends can be registered by target-specific packages.
        return self.get(ContainerBootBackend.name)

    def build(self, image: OSImage, contract: BootContract, preferred: str | None = None) -> BootArtifact:
        backend = self.select(image, contract, preferred)
        return backend.build(image, contract)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._backends))
