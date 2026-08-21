"""Target-neutral packaging model for Omni artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Tuple

from .targets import TargetDescriptor


@dataclass(frozen=True)
class PackageManifest:
    name: str
    version: str
    target: TargetDescriptor
    artifacts: Tuple[str, ...] = field(default_factory=tuple)
    dependencies: Tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for label, value in (("name", self.name), ("version", self.version)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"package {label} cannot be empty")
        if not isinstance(self.target, TargetDescriptor):
            raise TypeError("package target must be a TargetDescriptor")
        for label, values in (("artifacts", self.artifacts), ("dependencies", self.dependencies)):
            if not isinstance(values, tuple) or any(not isinstance(v, str) or not v.strip() for v in values):
                raise ValueError(f"package {label} must contain non-empty strings")
        if not isinstance(self.metadata, Mapping):
            raise TypeError("package metadata must be a mapping")

    def with_artifact(self, artifact: str) -> "PackageManifest":
        if not isinstance(artifact, str) or not artifact.strip():
            raise ValueError("artifact cannot be empty")
        return PackageManifest(self.name, self.version, self.target, self.artifacts + (artifact,), self.dependencies, self.metadata)
