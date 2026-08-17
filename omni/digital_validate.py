"""Strict validation helpers for open-world digital specifications."""

from __future__ import annotations

from collections.abc import Mapping

from .digital import DigitalSpec


class DigitalSpecValidationError(ValueError):
    """Raised when a digital specification violates its structural contract."""


def validate_digital_spec(spec: DigitalSpec) -> DigitalSpec:
    """Validate a digital specification and return the same immutable object."""
    try:
        spec.validate()
    except (TypeError, ValueError) as exc:
        raise DigitalSpecValidationError(str(exc)) from exc
    if not isinstance(spec.interfaces, tuple) or not all(
        isinstance(item, str) and item.strip() for item in spec.interfaces
    ):
        raise DigitalSpecValidationError("interfaces must be a tuple of non-empty strings")
    for name, value in (("extensions", spec.extensions), ("behavior", spec.behavior)):
        if not isinstance(value, Mapping):
            raise DigitalSpecValidationError(f"{name} must be an object")
    return spec
