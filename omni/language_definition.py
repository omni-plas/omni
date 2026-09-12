"""Open-world language definitions used by Omni frontend discovery.

A language is data at the resolution boundary: syntax, semantics, type rules,
execution model and dependencies are described explicitly instead of being a
closed list baked into the compiler. Concrete frontends can attach executable
implementations to these definitions through the registry.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


class LanguageDefinitionError(ValueError):
    """Raised when a language definition is incomplete or inconsistent."""


@dataclass(frozen=True)
class LanguageDefinition:
    """Authoritative description of a source language or dialect."""

    name: str
    version: str
    source_extensions: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    syntax: Mapping[str, object] = field(default_factory=dict)
    semantics: Mapping[str, object] = field(default_factory=dict)
    type_rules: Mapping[str, object] = field(default_factory=dict)
    execution_model: Mapping[str, object] = field(default_factory=dict)
    memory_model: Mapping[str, object] = field(default_factory=dict)
    abi_expectations: Mapping[str, object] = field(default_factory=dict)
    dependency_rules: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        name = self.name.strip()
        version = self.version.strip()
        if not name:
            raise LanguageDefinitionError("language name must not be empty")
        if not version:
            raise LanguageDefinitionError("language version must not be empty")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "version", version)
        extensions = tuple(ext.lower() if ext.startswith(".") else "." + ext.lower() for ext in self.source_extensions)
        if any(ext == "." for ext in extensions):
            raise LanguageDefinitionError("source extension must contain a suffix")
        object.__setattr__(self, "source_extensions", extensions)
        object.__setattr__(self, "aliases", tuple(alias.strip() for alias in self.aliases if alias.strip()))

    @property
    def identity(self) -> str:
        return f"{self.name}@{self.version}"

    def matches(self, language_or_alias: str, version: str | None = None) -> bool:
        candidate = language_or_alias.strip().casefold()
        names = {self.name.casefold(), *(alias.casefold() for alias in self.aliases)}
        return candidate in names and (version is None or version.strip() == self.version)

    def matches_extension(self, extension: str) -> bool:
        suffix = extension.lower()
        if not suffix.startswith("."):
            suffix = "." + suffix
        return suffix in self.source_extensions

    def manifest(self) -> dict[str, object]:
        return {
            "name": self.name,
            "version": self.version,
            "identity": self.identity,
            "aliases": list(self.aliases),
            "source_extensions": list(self.source_extensions),
            "syntax": dict(self.syntax),
            "semantics": dict(self.semantics),
            "type_rules": dict(self.type_rules),
            "execution_model": dict(self.execution_model),
            "memory_model": dict(self.memory_model),
            "abi_expectations": dict(self.abi_expectations),
            "dependency_rules": dict(self.dependency_rules),
        }
