"""Contracts and validation for materializing digital entity specifications."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .entities import EntitySpec


@dataclass(frozen=True)
class MaterializedArtifact:
    entity: EntitySpec
    format: str
    payload: bytes


class Materializer(Protocol):
    """Turns a validated entity model into a concrete artifact."""

    format: str

    def materialize(self, entity: EntitySpec) -> MaterializedArtifact:
        ...


def validate_materialized_artifact(artifact: MaterializedArtifact) -> None:
    artifact.entity.validate()
    if not artifact.format.strip():
        raise ValueError("artifact format must not be empty")
    if not isinstance(artifact.payload, bytes):
        raise ValueError("artifact payload must be bytes")
