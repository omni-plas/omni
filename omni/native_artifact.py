"""Stable artifact contract for the native Omni bootstrap pipeline."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .backend import BackendRegistry, GenericArtifactBackend
from .compiler import CompilationPlan
from .native_frontend import OmniNativeFrontend
from .source_pipeline import compile_source
from .targets import TargetDescriptor
from .uir import UIR
from .frontend import FrontendRegistry


@dataclass(frozen=True)
class NativeArtifact:
    """A reproducible semantic artifact produced from native Omni source."""

    target: TargetDescriptor
    payload: bytes
    digest: str

    @classmethod
    def from_uir(cls, uir: UIR, target: TargetDescriptor) -> "NativeArtifact":
        payload = (
            json.dumps(uir.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
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
    if not result.ok or result.uir is None:
        raise ValueError("native Omni source did not produce a valid UIR")
    target = result.plan.target
    return NativeArtifact.from_uir(result.uir, target)
