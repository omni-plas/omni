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
        self._frontends: list[Frontend] = []
        for frontend in frontends:
            self.register(frontend)

    def register(self, frontend: Frontend) -> None:
        if not isinstance(frontend.language, str) or not frontend.language.strip():
            raise ValueError("frontend language must be a non-empty string")
        if not callable(getattr(frontend, "supports", None)) or not callable(getattr(frontend, "parse", None)):
            raise TypeError("frontend must provide supports() and parse()")
        if any(existing.language == frontend.language for existing in self._frontends):
            raise ValueError(f"frontend already registered: {frontend.language}")
        self._frontends.append(frontend)

    def unregister(self, language: str) -> None:
        for index, frontend in enumerate(self._frontends):
            if frontend.language == language:
                del self._frontends[index]
                return
        raise LookupError(f"no frontend registered for language {language!r}")

    def resolve(self, language: str) -> Frontend:
        if not isinstance(language, str) or not language.strip():
            raise ValueError("language must be a non-empty string")
        for frontend in self._frontends:
            if frontend.supports(language):
                return frontend
        raise LookupError(f"no frontend supports language {language!r}")

    def languages(self) -> tuple[str, ...]:
        return tuple(frontend.language for frontend in self._frontends)

    def __len__(self) -> int:
        return len(self._frontends)
