"""Universal Intermediate Representation (UIR) and strict validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .uir_schema import validate_source_descriptor, validate_target_descriptor


class UIRValidationError(ValueError):
    """Raised when a UIR document violates the Omni contract."""


@dataclass(frozen=True)
class UIR:
    """A language- and target-neutral semantic program description."""

    version: str
    entity: Mapping[str, Any]
    source: Mapping[str, Any]
    target: Mapping[str, Any]
    semantics: Mapping[str, Any]
    constraints: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "entity": dict(self.entity),
            "source": dict(self.source),
            "target": dict(self.target),
            "semantics": dict(self.semantics),
            "constraints": dict(self.constraints),
        }


def _require_mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise UIRValidationError(f"{path} must be an object")
    return value


def _require_nonempty_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise UIRValidationError(f"{path} must be a non-empty string")
    return value


def validate_uir(document: Mapping[str, Any]) -> UIR:
    root = _require_mapping(document, "UIR")
    version = _require_nonempty_string(root.get("version"), "version")
    entity = _require_mapping(root.get("entity"), "entity")
    source = validate_source_descriptor(root.get("source"))
    target = validate_target_descriptor(root.get("target"))
    semantics = _require_mapping(root.get("semantics"), "semantics")
    constraints = _require_mapping(root.get("constraints", {}), "constraints")
    _require_nonempty_string(entity.get("kind"), "entity.kind")
    if "program" not in semantics and "behavior" not in semantics:
        raise UIRValidationError("semantics must define program or behavior")
    return UIR(version, entity, source, target, semantics, constraints)
