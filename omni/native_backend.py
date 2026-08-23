"""Deterministic executable-shaped backend for the native Omni bootstrap.

This backend deliberately emits a self-describing portable artifact rather than
pretending that a semantic JSON document is a native executable.  The container
is stable and can later be consumed by a true machine-code backend without
changing the frontend or compilation contracts.
"""

from __future__ import annotations

import hashlib
import json
import struct

from .artifacts import Artifact
from .backend import BackendError
from .compiler import CompilationPlan
from .targets import TargetDescriptor
from .uir import UIR

_MAGIC = b"OMNIART1"


class NativeArtifactBackend:
    name = "omni-portable-artifact"

    def supports(self, target: TargetDescriptor) -> bool:
        return target.supports("portable-artifact", True) or target.platform == "semantic-artifact"

    def compile(self, uir: UIR, plan: CompilationPlan) -> Artifact:
        if not self.supports(plan.target):
            raise BackendError(f"backend does not support {plan.target.identity()}")
        document = json.dumps(
            uir.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        digest = hashlib.sha256(document).digest()
        header = _MAGIC + struct.pack(">I", len(document)) + digest
        payload = header + document
        return Artifact("portable-entity", uir.entity_kind, plan.target, "omni-artifact", payload=payload)


def read_artifact(payload: bytes) -> dict:
    if not isinstance(payload, bytes) or len(payload) < len(_MAGIC) + 4 + 32:
        raise ValueError("invalid Omni artifact")
    if payload[: len(_MAGIC)] != _MAGIC:
        raise ValueError("invalid Omni artifact magic")
    offset = len(_MAGIC)
    size = struct.unpack(">I", payload[offset:offset + 4])[0]
    offset += 4
    digest = payload[offset:offset + 32]
    document = payload[offset + 32:]
    if len(document) != size or hashlib.sha256(document).digest() != digest:
        raise ValueError("corrupt Omni artifact payload")
    value = json.loads(document.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("artifact document must be an object")
    return value
