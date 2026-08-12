"""Canonical semantic IR serialization for hashing and reproducible builds."""

from __future__ import annotations

import json
from typing import Any

from .ir import ModuleIR


def canonicalize(value: Any) -> Any:
    """Return JSON-compatible deterministic data for supported IR values."""
    if hasattr(value, "to_dict") and callable(value.to_dict):
        return canonicalize(value.to_dict())
    if isinstance(value, dict):
        return {str(k): canonicalize(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (list, tuple)):
        return [canonicalize(item) for item in value]
    if hasattr(value, "__dict__") and value.__class__.__module__.startswith("omni"):
        return canonicalize(vars(value))
    return value


def canonical_ir_bytes(module: ModuleIR) -> bytes:
    """Serialize validated IR without incidental dictionary ordering."""
    module.validate()
    return json.dumps(canonicalize(module), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
