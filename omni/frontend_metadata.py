"""Metadata and deterministic resolution rules for source frontends."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True)
class FrontendMetadata:
    """Describes a frontend's language family and supported language variants."""

    language: str
    aliases: FrozenSet[str] = field(default_factory=frozenset)
    versions: FrozenSet[str] = field(default_factory=frozenset)
    source_extensions: FrozenSet[str] = field(default_factory=frozenset)
    priority: int = 0

    def __post_init__(self) -> None:
        if not self.language.strip():
            raise ValueError("language must be non-empty")
        if any(not value.strip() for value in self.aliases):
            raise ValueError("frontend aliases must be non-empty")
        if any(not value.strip() for value in self.versions):
            raise ValueError("frontend versions must be non-empty")
        if any(not value.startswith(".") or len(value) == 1 for value in self.source_extensions):
            raise ValueError("source extensions must begin with '.'")

    def matches_language(self, language: str) -> bool:
        normalized = language.strip().lower()
        return normalized == self.language.lower() or normalized in {a.lower() for a in self.aliases}

    def matches_version(self, version: str | None) -> bool:
        return version is None or not self.versions or version in self.versions

    def matches_extension(self, extension: str | None) -> bool:
        return extension is None or not self.source_extensions or extension.lower() in {e.lower() for e in self.source_extensions}
