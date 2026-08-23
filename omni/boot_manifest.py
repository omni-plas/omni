"""Canonical metadata for boot artifacts."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .boot_backend import BootArtifact
from .boot_contract import BootContract


@dataclass(frozen=True)
class BootManifest:
    format: str
    target: dict
    boot_protocol: str
    firmware: str
    filesystem: str
    entrypoint: str
    artifact_format: str
    artifact_digest: str

    def to_bytes(self) -> bytes:
        doc = {
            "format": self.format,
            "target": self.target,
            "boot_protocol": self.boot_protocol,
            "firmware": self.firmware,
            "filesystem": self.filesystem,
            "entrypoint": self.entrypoint,
            "artifact_format": self.artifact_format,
            "artifact_digest": self.artifact_digest,
        }
        return json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8")


def create_boot_manifest(artifact: BootArtifact, contract: BootContract) -> BootManifest:
    if contract.target != artifact.target:
        raise ValueError("boot manifest target mismatch")
    digest = hashlib.sha256(artifact.payload).hexdigest()
    if digest != artifact.digest:
        raise ValueError("boot artifact digest mismatch")
    return BootManifest(
        "omni-boot-manifest-v1",
        artifact.target.document(),
        contract.boot_protocol,
        contract.firmware,
        contract.filesystem,
        contract.entrypoint,
        artifact.format,
        artifact.digest,
    )
