"""Runtime registration for language frontends and target backends."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class PluginRegistry:
    frontends: dict[str, Any]
    backends: dict[str, Any]

    def __init__(self) -> None:
        self.frontends = {}
        self.backends = {}

    def register_frontend(self, language: str, frontend: Any) -> None:
        key = language.strip()
        if not key:
            raise ValueError("frontend language must be non-empty")
        if key in self.frontends:
            raise ValueError(f"frontend already registered: {key}")
        self.frontends[key] = frontend

    def register_backend(self, target: str, backend: Any) -> None:
        key = target.strip()
        if not key:
            raise ValueError("backend target must be non-empty")
        if key in self.backends:
            raise ValueError(f"backend already registered: {key}")
        self.backends[key] = backend

    def frontend(self, language: str) -> Any:
        try:
            return self.frontends[language]
        except KeyError as exc:
            raise LookupError(f"no frontend registered for {language}") from exc

    def backend(self, target: str) -> Any:
        try:
            return self.backends[target]
        except KeyError as exc:
            raise LookupError(f"no backend registered for {target}") from exc
