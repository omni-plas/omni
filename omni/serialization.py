"""Deterministic JSON serialization for UIR exchange boundaries."""

from __future__ import annotations

import json
from typing import Any, Mapping


def dumps_uir(document: Mapping[str, Any]) -> str:
    """Serialize UIR without losing unknown extension fields."""
    return json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def loads_uir(payload: str) -> dict[str, Any]:
    """Parse a JSON UIR document while rejecting non-object roots."""
    value = json.loads(payload)
    if not isinstance(value, dict):
        raise ValueError("UIR JSON root must be an object")
    return value
