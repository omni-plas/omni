"""Target-neutral packaging model for Omni artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Mapping, Tuple

from .targets import TargetDescriptor


class PackageError(ValueError):
    """Raised when a package manifest is invalid."""


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
                raise PackageError(f"package {label} cannot be empty")
        if not isinstance(self.target, TargetDescriptor):
            raise TypeError("package target must be a TargetDescriptor")
        for label, values in (("artifacts", self.artifacts), ("dependencies", self.dependencies)):
            if not isinstance(values, tuple) or any(not isinstance(v, str) or not v.strip() for v in values):
                raise PackageError(f"package {label} must contain non-empty strings")
        if len(set(self.artifacts)) != len(self.artifacts):
            raise PackageError("package artifacts must be unique")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise PackageError("package dependencies must be unique")
        if not isinstance(self.metadata, Mapping):
            raise TypeError("package metadata must be a mapping")
        if any(not isinstance(k, str) or not k.strip() for k in self.metadata):
            raise PackageError("package metadata keys must be non-empty strings")
        if any(not isinstance(v, str) for v in self.metadata.values()):
            raise PackageError("package metadata values must be strings")

    def with_artifact(self, artifact: str) -> "PackageManifest":
        if not isinstance(artifact, str) or not artifact.strip():
            raise PackageError("artifact cannot be empty")
        artifact = artifact.strip()
        if artifact in self.artifacts:
            raise PackageError("package artifact must be unique")
        return PackageManifest(self.name, self.version, self.target, self.artifacts + (artifact,), self.dependencies, self.metadata)

    def with_dependency(self, dependency: str) -> "PackageManifest":
        if not isinstance(dependency, str) or not dependency.strip():
            raise PackageError("dependency cannot be empty")
        dependency = dependency.strip()
        if dependency in self.dependencies:
            raise PackageError("package dependency must be unique")
        return PackageManifest(self.name, self.version, self.target, self.artifacts, self.dependencies + (dependency,), self.metadata)

    def manifest_document(self) -> dict[str, Any]:
        return {
            "schema": "omni.package.v1",
            "name": self.name.strip(),
            "version": self.version.strip(),
            "target": self.target.serialize(),
            "artifacts": list(self.artifacts),
            "dependencies": list(self.dependencies),
            "metadata": dict(self.metadata),
        }

    def manifest(self) -> bytes:
        return (json.dumps(self.manifest_document(), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

    def render_manifest(self) -> str:
        return json.dumps(self.manifest_document(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
