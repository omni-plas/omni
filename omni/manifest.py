"""Deterministic compilation manifests for reproducible builds."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

from .ir import ModuleIR
from .targets import TargetDescriptor


@dataclass(frozen=True)
class BuildManifest:
    compiler: str
    target: TargetDescriptor
    ir_sha256: str
    metadata: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "compiler": self.compiler,
            "target": {
                "platform": self.target.platform,
                "architecture": self.target.architecture,
                "abi": self.target.abi,
                "capabilities": dict(self.target.capabilities),
            },
            "ir_sha256": self.ir_sha256,
            "metadata": dict(self.metadata),
        }


def manifest_for(module: ModuleIR, target: TargetDescriptor, metadata: Mapping[str, Any] | None = None) -> BuildManifest:
    """Create a stable manifest fingerprint for a semantic IR build."""
    module.validate()
    canonical = json.dumps(module.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return BuildManifest(
        compiler="omni-semantic",
        target=target,
        ir_sha256=hashlib.sha256(canonical).hexdigest(),
        metadata=dict(metadata or {}),
    )
