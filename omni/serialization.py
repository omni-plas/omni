"""Deterministic JSON serialization for UIR exchange boundaries."""

from __future__ import annotations

import json
from typing import Any, Mapping


class SerializationError(ValueError):
    """Raised when a UIR payload cannot be represented safely as JSON."""


def dumps_uir(document: Mapping[str, Any]) -> str:
    """Serialize UIR deterministically without losing extension fields."""
    if not isinstance(document, Mapping):
        raise SerializationError("UIR document must be an object")
    try:
        return json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise SerializationError(f"UIR is not JSON-serializable: {exc}") from exc


def loads_uir(payload: str) -> dict[str, Any]:
    """Parse JSON UIR while rejecting non-object roots and non-standard constants."""
    if not isinstance(payload, str):
        raise SerializationError("UIR payload must be text")

    def reject_constant(value: str) -> None:
        raise SerializationError(f"non-standard JSON constant: {value}")

    try:
        value = json.loads(payload, parse_constant=reject_constant)
    except json.JSONDecodeError as exc:
        raise SerializationError(f"invalid UIR JSON: {exc.msg} at line {exc.lineno} column {exc.colno}") from exc
    if not isinstance(value, dict):
        raise SerializationError("UIR JSON root must be an object")
    return value
