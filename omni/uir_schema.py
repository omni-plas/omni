"""Reusable UIR schema checks for source and target descriptors."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .uir import UIRValidationError


def validate_descriptor(value: Any, path: str, required: tuple[str, ...]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise UIRValidationError(f"{path} must be an object")
    for key in required:
        item = value.get(key)
        if not isinstance(item, str) or not item.strip():
            raise UIRValidationError(f"{path}.{key} must be a non-empty string")
    return value


def validate_source_descriptor(source: Any) -> Mapping[str, Any]:
    return validate_descriptor(source, "source", ("language",))


def validate_target_descriptor(target: Any) -> Mapping[str, Any]:
    return validate_descriptor(target, "target", ("platform",))
