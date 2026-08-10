"""Source-language frontend contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .uir import UIR


@dataclass(frozen=True)
class SourceUnit:
    language: str
    text: str
    origin: str | None = None


class Frontend(Protocol):
    """Converts a source unit into validated semantic UIR."""

    language: str

    def lower(self, source: SourceUnit) -> UIR:
        ...
