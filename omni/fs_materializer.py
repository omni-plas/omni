"""Concrete filesystem materialization for Omni digital artifacts.

This layer deliberately materializes into a caller-selected staging directory. It
never executes generated content and never writes outside the requested root.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .artifacts import ArtifactManifest
from .materialize import MaterializedArtifact, validate_materialized_artifact


class FilesystemMaterializationError(ValueError):
    """Raised when an artifact cannot be safely materialized."""


@dataclass(frozen=True)
class MaterializedFile:
    path: Path
    manifest: ArtifactManifest



def _safe_relative_path(name: str) -> PurePosixPath:
    if not isinstance(name, str) or not name.strip():
        raise FilesystemMaterializationError("artifact name must be non-empty")
    candidate = PurePosixPath(name.strip())
    if candidate.is_absolute() or ".." in candidate.parts:
        raise FilesystemMaterializationError("artifact name must remain inside the staging root")
    if candidate == PurePosixPath("."):
        raise FilesystemMaterializationError("artifact name must identify a file")
    return candidate


def materialize_to_directory(artifact: MaterializedArtifact, root: str | os.PathLike[str]) -> MaterializedFile:
    """Write one validated artifact beneath *root* and return its content manifest."""
    validate_materialized_artifact(artifact)
    root_path = Path(root).resolve()
    root_path.mkdir(parents=True, exist_ok=True)
    name = artifact.entity.name.strip()
    relative = _safe_relative_path(name)
    destination = (root_path / Path(*relative.parts)).resolve()
    if os.path.commonpath((str(root_path), str(destination))) != str(root_path):
        raise FilesystemMaterializationError("resolved artifact path escaped staging root")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".omni-tmp")
    payload = artifact.payload
    digest = hashlib.sha256(payload).hexdigest()
    try:
        temporary.write_bytes(payload)
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    manifest = ArtifactManifest(
        target=artifact.entity.execution.get("target") if False else _target_from_entity(artifact),
        format=artifact.format.strip(),
        digest=digest,
        size=len(payload),
        name=name,
        kind=artifact.entity.kind.strip(),
    )
    return MaterializedFile(destination, manifest)


def _target_from_entity(artifact: MaterializedArtifact):
    """Resolve the target descriptor carried by an entity execution contract."""
    from .targets import TargetDescriptor

    target = artifact.entity.execution.get("target")
    if isinstance(target, TargetDescriptor):
        return target
    if isinstance(target, dict):
        return TargetDescriptor.from_document(target)
    raise FilesystemMaterializationError("entity execution contract must contain a target descriptor")
