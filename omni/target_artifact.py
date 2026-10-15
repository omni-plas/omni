"""Validation helpers for materialized Omni artifacts."""

from __future__ import annotations

from .native_backend import read_artifact
from .targets import TargetDescriptor, resolve_target


def validate_artifact_for_target(payload: bytes, target: TargetDescriptor) -> dict:
    document = read_artifact(payload)
    target_document = document.get("target")
    if not isinstance(target_document, dict):
        raise ValueError("artifact does not contain a target document")
    artifact_target = resolve_target(target_document)
    if artifact_target != target:
        raise ValueError(
            f"artifact target {artifact_target.identity()} does not match requested target {target.identity()}"
        )
    return document
