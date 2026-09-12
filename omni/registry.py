"""Runtime registries for pluggable Omni languages, frontends and backends."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Any

from .backends import Backend
from .frontends import Frontend
from .language_definition import LanguageDefinition


class RegistryError(ValueError):
    pass


@dataclass
class CompilerRegistry:
    """Thread-safe extension registry for the open-world compiler architecture."""

    _frontends: dict[str, Frontend]
    _backends: dict[str, Backend]
    _languages: dict[str, LanguageDefinition]

    def __init__(self) -> None:
        self._frontends = {}
        self._backends = {}
        self._languages = {}
        self._lock = RLock()

    def register_language_definition(self, definition: LanguageDefinition) -> None:
        """Register an authoritative language definition by its versioned identity."""
        if not isinstance(definition, LanguageDefinition):
            raise RegistryError("language definition must be a LanguageDefinition")
        with self._lock:
            if definition.identity in self._languages:
                raise RegistryError(f"language already registered: {definition.identity}")
            self._languages[definition.identity] = definition

    def language_definition(self, language: str, version: str | None = None) -> LanguageDefinition:
        """Resolve a language by canonical name/alias and optional version."""
        with self._lock:
            matches = [
                definition
                for definition in self._languages.values()
                if definition.matches(language, version)
            ]
        if not matches:
            requested = language if version is None else f"{language}@{version}"
            raise RegistryError(f"no language definition registered for: {requested}")
        if len(matches) > 1:
            identities = ", ".join(sorted(definition.identity for definition in matches))
            raise RegistryError(f"ambiguous language definition: {language} ({identities})")
        return matches[0]

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
