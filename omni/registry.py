"""Runtime registries for pluggable Omni languages, frontends and backends."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock

from .backends import Backend
from .frontends import Frontend
from .language_definition import LanguageDefinition


class RegistryError(ValueError):
    """Raised when an extension cannot be registered or resolved deterministically."""


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
            matches = [definition for definition in self._languages.values() if definition.matches(language, version)]
        if not matches:
            requested = language if version is None else f"{language}@{version}"
            raise RegistryError(f"no language definition registered for: {requested}")
        if len(matches) > 1:
            identities = ", ".join(sorted(definition.identity for definition in matches))
            raise RegistryError(f"ambiguous language definition: {language} ({identities})")
        return matches[0]

    def language_definition_for_extension(self, extension: str) -> LanguageDefinition:
        """Resolve a source language from a file suffix without a closed catalog."""
        suffix = extension.strip().lower()
        if not suffix:
            raise RegistryError("source extension must not be empty")
        if not suffix.startswith("."):
            suffix = "." + suffix
        with self._lock:
            matches = [definition for definition in self._languages.values() if definition.matches_extension(suffix)]
        if not matches:
            raise RegistryError(f"no language definition registered for extension: {suffix}")
        if len(matches) > 1:
            identities = ", ".join(sorted(definition.identity for definition in matches))
            raise RegistryError(f"ambiguous source extension {suffix}: {identities}")
        return matches[0]

    def register_frontend(self, language: str, frontend: Frontend) -> None:
        key = language.strip()
        if not key:
            raise RegistryError("frontend language must not be empty")
        if not callable(getattr(frontend, "lower", None)):
            raise RegistryError("frontend must provide lower(source)")
        with self._lock:
            if key in self._frontends:
                raise RegistryError(f"frontend already registered: {key}")
            self._frontends[key] = frontend

    def register_backend(self, target: str, backend: Backend) -> None:
        key = target.strip()
        if not key:
            raise RegistryError("backend target must not be empty")
        if not callable(getattr(backend, "emit", None)) or not callable(getattr(backend, "supports_target", None)):
            raise RegistryError("backend must provide supports_target() and emit()")
        with self._lock:
            if key in self._backends:
                raise RegistryError(f"backend already registered: {key}")
            self._backends[key] = backend

    def frontend(self, language: str) -> Frontend:
        key = language.strip()
        with self._lock:
            try:
                return self._frontends[key]
            except KeyError as exc:
                raise RegistryError(f"no frontend registered for: {key}") from exc

    def frontend_for_language(self, language: str, version: str | None = None) -> Frontend:
        """Resolve an executable frontend by language name or declared alias.

        Versioned definitions remain the authority for aliases. A direct frontend
        lookup is retained for legacy extensions that have not registered a
        LanguageDefinition yet.
        """
        key = language.strip()
        if not key:
            raise RegistryError("frontend language must not be empty")
        try:
            definition = self.language_definition(key, version)
        except RegistryError as exc:
            # Only fall back when there is no definition. Ambiguous aliases must
            # remain an error rather than silently selecting an arbitrary plugin.
            if not str(exc).startswith("no language definition registered for:"):
                raise
            if version is not None:
                raise
            return self.frontend(key)
        return self.frontend(definition.name)

    def frontend_for_extension(self, extension: str) -> Frontend:
        """Resolve the executable frontend through the registered language contract."""
        definition = self.language_definition_for_extension(extension)
        try:
            return self.frontend(definition.name)
        except RegistryError as exc:
            raise RegistryError(
                f"language {definition.identity} has a definition but no executable frontend"
            ) from exc

    def languages(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._languages))

    def frontends(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._frontends))

    def backends(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._backends))

    def backend(self, target: str) -> Backend:
        key = target.strip()
        with self._lock:
            try:
                return self._backends[key]
            except KeyError as exc:
                raise RegistryError(f"no backend registered for: {key}") from exc
