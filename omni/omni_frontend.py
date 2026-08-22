"""Minimal Omni-language frontend boundary for the universal pipeline.

This frontend deliberately keeps parsing independent from Python/C/C++ compiler
infrastructure. The concrete Omni grammar can grow without changing the
frontend registry or backend contracts.
"""

from __future__ import annotations

import json
from typing import Any

from .uir import UIR, validate_uir


class OmniFrontend:
    language = "omni"

    def supports(self, language: str) -> bool:
        return isinstance(language, str) and language.strip().lower() == self.language

    def parse(self, source: str, *, filename: str = "<source>") -> UIR:
        if not isinstance(source, str) or not source.strip():
            raise ValueError("Omni source cannot be empty")
        # Canonical UIR documents can be used as a bootstrap representation.
        # This makes the frontend independently testable while the native grammar
        # expands toward full self-hosting.
        try:
            document: Any = json.loads(source)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Omni bootstrap source must be valid UIR JSON: {exc}") from exc
        return validate_uir(document)
