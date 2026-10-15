"""Validation bridge from open-world entity specifications into Omni APIs."""

from __future__ import annotations

from typing import Any, Mapping

from .entities import EntitySpec
from .uir import UIRValidationError


def entity_from_mapping(document: Mapping[str, Any]) -> EntitySpec:
    """Build and validate an EntitySpec without restricting its kind."""
    if not isinstance(document, Mapping):
        raise UIRValidationError("entity specification must be an object")
    inputs = tuple(document.get("inputs", ()))
    outputs = tuple(document.get("outputs", ()))
    entity = EntitySpec(
        kind=document.get("kind", ""),
        name=document.get("name", ""),
        structure=document.get("structure", {}),
        behavior=document.get("behavior", {}),
        constraints=document.get("constraints", {}),
        inputs=inputs,
        outputs=outputs,
        execution=document.get("execution", {}),
    )
    try:
        entity.validate()
    except (TypeError, ValueError) as exc:
        raise UIRValidationError(str(exc)) from exc
    return entity
