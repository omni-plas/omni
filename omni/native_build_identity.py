"""Combine target, manifest and artifact digest into one build identity."""
from __future__ import annotations
from dataclasses import dataclass
from .native_artifact_identity import sha256
from .native_reproducibility import manifest_digest

@dataclass(frozen=True)
class BuildIdentity:
    target:str
    manifest:str
    artifact:str

    @classmethod
    def create(cls,target:str,manifest:dict,artifact:bytes):
        return cls(target,manifest_digest(manifest),sha256(artifact))
