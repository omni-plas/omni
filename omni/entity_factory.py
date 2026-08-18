"""Generic digital-entity construction independent of a closed type catalog."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .digital import DigitalSpec
from .entities import EntitySpec


@dataclass(frozen=True)
class DigitalBlueprint:
    """A complete, open-world description of a digital thing to materialize."""

    kind: str
    name: str
    structure: Mapping[str, Any]
    behavior: Mapping[str, Any]
    interfaces: tuple[str, ...] = ()
    constraints: Mapping[str, Any] = ()
    metadata: Mapping[str, Any] = ()

    def __post_init__(self) -> None:
        if not self.kind.strip() or not self.name.strip():
            raise ValueError("blueprint kind and name must be non-empty")


def digital_spec_from_blueprint(blueprint: DigitalBlueprint) -> DigitalSpec:
    """Convert any blueprint into Omni's language-neutral digital specification."""
    return DigitalSpec(
        name=blueprint.name,
        kind=blueprint.kind,
        structure=dict(blueprint.structure),
        behavior=dict(blueprint.behavior),
        interfaces=tuple(blueprint.interfaces),
        constraints=dict(blueprint.constraints),
        metadata=dict(blueprint.metadata),
    )


def entity_from_blueprint(blueprint: DigitalBlueprint) -> EntitySpec:
    """Create an entity specification without requiring a predefined entity kind."""
    return EntitySpec(
        kind=blueprint.kind,
        name=blueprint.name,
        structure=dict(blueprint.structure),
        behavior=dict(blueprint.behavior),
        constraints=dict(blueprint.constraints),
        inputs=tuple(blueprint.interfaces),
        outputs=(),
        execution={},
    )
