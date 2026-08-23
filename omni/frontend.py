"""Source frontend contracts and discovery for translating languages into Omni UIR."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .frontend_metadata import FrontendMetadata
from .uir import UIR


class Frontend(Protocol):
    """Capability boundary for a source-language frontend."""

    language: str

    def supports(self, language: str) -> bool:
        """Return whether this frontend recognizes the source language."""
        ...

    def parse(self, source: str, *, filename: str = "<source>") -> UIR:
        """Translate source text into validated UIR."""
        ...


@dataclass(frozen=True)
class FrontendCandidate:
    frontend: Frontend
    priority: int
    reason: str


class FrontendRegistry:
    """Deterministic registry for source-language frontends."""

    def __init__(self, frontends: tuple[Frontend, ...] = ()) -> None:
        self._frontends: list[Frontend] = []
        for frontend in frontends:
            self.register(frontend)

    def register(self, frontend: Frontend) -> None:
        if not isinstance(frontend.language, str) or not frontend.language.strip():
            raise ValueError("frontend language must be a non-empty string")
        if not callable(getattr(frontend, "supports", None)) or not callable(getattr(frontend, "parse", None)):
            raise TypeError("frontend must provide supports() and parse()")
        if any(existing.language.lower() == frontend.language.lower() for existing in self._frontends):
            raise ValueError(f"frontend already registered: {frontend.language}")
        self._frontends.append(frontend)

    def unregister(self, language: str) -> None:
        for index, frontend in enumerate(self._frontends):
            if frontend.language.lower() == language.lower():
                del self._frontends[index]
                return
        raise LookupError(f"no frontend registered for language {language!r}")

    def candidates(self, language: str, *, version: str | None = None, extension: str | None = None) -> tuple[FrontendCandidate, ...]:
        if not isinstance(language, str) or not language.strip():
            raise ValueError("language must be a non-empty string")
        candidates: list[FrontendCandidate] = []
        for frontend in self._frontends:
            metadata = getattr(frontend, "metadata", None)
            if isinstance(metadata, FrontendMetadata):
                if not metadata.matches_language(language):
                    continue
                if not metadata.matches_version(version) or not metadata.matches_extension(extension):
                    continue
                candidates.append(FrontendCandidate(frontend, metadata.priority, "metadata match"))
            elif frontend.supports(language):
                candidates.append(FrontendCandidate(frontend, 0, "legacy supports() match"))
        return tuple(sorted(candidates, key=lambda item: (-item.priority, item.frontend.language.lower())))

    def resolve(self, language: str, *, version: str | None = None, extension: str | None = None) -> Frontend:
        candidates = self.candidates(language, version=version, extension=extension)
        if not candidates:
            raise LookupError(f"no frontend supports language {language!r}")
        return candidates[0].frontend

    def discover(self, language: str, *, version: str | None = None, extension: str | None = None) -> FrontendCandidate:
        """Return the selected frontend and the deterministic reason for selection."""
        candidates = self.candidates(language, version=version, extension=extension)
        if not candidates:
            raise LookupError(f"no frontend supports language {language!r}")
        return candidates[0]

    def languages(self) -> tuple[str, ...]:
        return tuple(frontend.language for frontend in self._frontends)

    def __len__(self) -> int:
        return len(self._frontends)
