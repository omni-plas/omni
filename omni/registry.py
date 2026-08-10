"""Runtime registries for pluggable Omni frontends and backends."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Any

from .backends import Backend
from .frontends import Frontend


class RegistryError(ValueError):
    pass


@dataclass
class CompilerRegistry:
    """Thread-safe extension registry; core Omni remains independent of plugins."""

    _frontends: dict[str, Frontend]
    _backends: dict[str, Backend]

    def __init__(self) -> None:
        self._frontends = {}
        self._backends = {}
        self._lock = RLock()

    def register_frontend(self, language: str, frontend: Frontend) -> None:
        key = language.strip()
        if not key:
            raise RegistryError("frontend language must not be empty")
        with self._lock:
            if key in self._frontends:
                raise RegistryError(f"frontend already registered: {key}")
            self._frontends[key] = frontend

    def register_backend(self, target: str, backend: Backend) -> None:
        key = target.strip()
        if not key:
            raise RegistryError("backend target must not be empty")
        with self._lock:
            if key in self._backends:
                raise RegistryError(f"backend already registered: {key}")
            self._backends[key] = backend

    def frontend(self, language: str) -> Frontend:
        with self._lock:
            try:
                return self._frontends[language]
            except KeyError as exc:
                raise RegistryError(f"no frontend registered for: {language}") from exc

    def backend(self, target: str) -> Backend:
        with self._lock:
            try:
                return self._backends[target]
            except KeyError as exc:
                raise RegistryError(f"no backend registered for: {target}") from exc
