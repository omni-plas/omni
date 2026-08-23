"""Stable artifact contract for the native Omni bootstrap pipeline."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .backend import BackendRegistry, GenericArtifactBackend
from .frontend import FrontendRegistry
from .native_frontend import OmniNativeFrontend
from .source_pipeline import compile_source
from .targets import TargetDescriptor


@dataclass(frozen=True)
class NativeArtifact:
    """A reproducible semantic artifact produced from native Omni source."""

    target: TargetDescriptor
    payload: bytes
    digest: str

    @classmethod
    def from_payload(cls, payload: bytes, target: TargetDescriptor) -> "NativeArtifact":
        return cls(target=target, payload=payload, digest=hashlib.sha256(payload).hexdigest())


def compile_native_artifact(source: str, *, filename: str = "<source>") -> NativeArtifact:
    """Parse and validate native Omni source and return a reproducible artifact."""
    result = compile_source(
        source,
        language="omni",
        frontends=FrontendRegistry((OmniNativeFrontend(),)),
        backends=BackendRegistry().register(GenericArtifactBackend()),
        filename=filename,
    )
    artifact = result.compilation.artifact
    target = result.compilation.plan.target
    payload = getattr(artifact, "payload", None)
    if not isinstance(payload, bytes):
        raise ValueError("native Omni backend did not produce a byte payload")
    return NativeArtifact.from_payload(payload, target)
