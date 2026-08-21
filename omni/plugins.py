"""Runtime registration for language frontends and target backends."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PluginRegistry:
    """Deterministic open-world registry for pluggable compilation capabilities."""

    frontends: dict[str, Any] = field(default_factory=dict)
    backends: dict[str, Any] = field(default_factory=dict)

    def register_frontend(self, language: str, frontend: Any) -> None:
        key = self._key(language, "frontend language")
        if frontend is None:
            raise TypeError("frontend cannot be None")
        if key in self.frontends:
            raise ValueError(f"frontend already registered: {key}")
        self.frontends[key] = frontend

    def register_backend(self, target: str, backend: Any) -> None:
        key = self._key(target, "backend target")
        if backend is None:
            raise TypeError("backend cannot be None")
        if key in self.backends:
            raise ValueError(f"backend already registered: {key}")
        self.backends[key] = backend

    @staticmethod
    def _key(value: str, label: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{label} must be a string")
        key = value.strip()
        if not key:
            raise ValueError(f"{label} must be non-empty")
        return key

    def frontend(self, language: str) -> Any:
        key = self._key(language, "frontend language")
        try:
            return self.frontends[key]
        except KeyError as exc:
            raise LookupError(f"no frontend registered for {key}") from exc

    def backend(self, target: str) -> Any:
        key = self._key(target, "backend target")
        try:
            return self.backends[key]
        except KeyError as exc:
            raise LookupError(f"no backend registered for {key}") from exc

    def unregister_frontend(self, language: str) -> Any:
        key = self._key(language, "frontend language")
        try:
            return self.frontends.pop(key)
        except KeyError as exc:
            raise LookupError(f"no frontend registered for {key}") from exc

    def unregister_backend(self, target: str) -> Any:
        key = self._key(target, "backend target")
        try:
            return self.backends.pop(key)
        except KeyError as exc:
            raise LookupError(f"no backend registered for {key}") from exc

    def languages(self) -> tuple[str, ...]:
        return tuple(self.frontends)

    def targets(self) -> tuple[str, ...]:
        return tuple(self.backends)
