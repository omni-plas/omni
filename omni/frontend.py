"""Source frontend contracts for translating languages into Omni UIR."""

from __future__ import annotations

from typing import Protocol

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


class FrontendRegistry:
    """Deterministic registry for source-language frontends."""

    def __init__(self, frontends: tuple[Frontend, ...] = ()) -> None:
        self._frontends = list(frontends)

    def register(self, frontend: Frontend) -> None:
        if not isinstance(frontend.language, str) or not frontend.language.strip():
            raise ValueError("frontend language must be a non-empty string")
        self._frontends.append(frontend)

    def resolve(self, language: str) -> Frontend:
        for frontend in self._frontends:
            if frontend.supports(language):
                return frontend
        raise LookupError(f"no frontend supports language {language!r}")

    def languages(self) -> tuple[str, ...]:
        return tuple(frontend.language for frontend in self._frontends)
