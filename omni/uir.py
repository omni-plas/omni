"""Universal Intermediate Representation (UIR) and strict validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


class UIRValidationError(ValueError):
    """Raised when a UIR document violates the Omni contract."""


@dataclass(frozen=True)
class UIR:
    """A language- and target-neutral semantic program description.

    The representation deliberately models open-ended concepts instead of a
    closed list of languages or targets. Unknown language/target definitions
    can therefore be represented without changing the UIR schema.
    """

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
    """Validate and materialize a UIR document.

    Validation checks the semantic contract needed by the first vertical
    slice while preserving extensibility through arbitrary object fields.
    """
    root = _require_mapping(document, "UIR")
    version = _require_nonempty_string(root.get("version"), "version")
    entity = _require_mapping(root.get("entity"), "entity")
    source = _require_mapping(root.get("source"), "source")
    target = _require_mapping(root.get("target"), "target")
    semantics = _require_mapping(root.get("semantics"), "semantics")
    constraints = _require_mapping(root.get("constraints", {}), "constraints")

    _require_nonempty_string(entity.get("kind"), "entity.kind")
    _require_nonempty_string(source.get("language"), "source.language")
    _require_nonempty_string(target.get("platform"), "target.platform")

    if "program" not in semantics and "behavior" not in semantics:
        raise UIRValidationError("semantics must define program or behavior")

    return UIR(version, entity, source, target, semantics, constraints)
