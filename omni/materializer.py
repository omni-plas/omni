"""Target-aware materialization plans for Omni build artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from .artifacts import Artifact
from .targets import TargetDescriptor


class MaterializationError(ValueError):
    """Raised when a materialization plan cannot be represented safely."""


@dataclass(frozen=True)
class MaterializationPlan:
    target: TargetDescriptor
    artifacts: tuple[Artifact, ...] = field(default_factory=tuple)
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.target, TargetDescriptor):
            raise TypeError("materialization target must be a TargetDescriptor")
        if not isinstance(self.artifacts, tuple) or any(not isinstance(a, Artifact) for a in self.artifacts):
            raise TypeError("materialization artifacts must contain Artifact values")
        if any(a.target != self.target for a in self.artifacts):
            raise MaterializationError("all artifacts must use the materialization target")
        if not isinstance(self.metadata, Mapping):
            raise TypeError("materialization metadata must be a mapping")

    def add(self, artifact: Artifact) -> "MaterializationPlan":
        if not isinstance(artifact, Artifact):
            raise TypeError("artifact must be an Artifact")
        if artifact.target != self.target:
            raise MaterializationError("artifact target must match materialization target")
        return MaterializationPlan(self.target, self.artifacts + (artifact,), self.metadata)

    def identities(self) -> tuple[str, ...]:
        return tuple(a.identity() for a in self.artifacts)


def create_materialization_plan(target: TargetDescriptor, *, metadata: Mapping[str, object] | None = None) -> MaterializationPlan:
    """Create an empty, target-neutral materialization plan."""
    return MaterializationPlan(target, (), metadata or {})
