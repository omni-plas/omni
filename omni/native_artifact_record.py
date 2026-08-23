"""Immutable build record tying an artifact to its identity and target."""
from __future__ import annotations
from dataclasses import dataclass
from .native_artifact_identity import sha256

@dataclass(frozen=True)
class ArtifactRecord:
    target_os:str
    target_arch:str
    entry:str
    digest:str
    size:int

    @classmethod
    def create(cls,data:bytes,target_os:str,target_arch:str,entry:str):
        payload=bytes(data)
        return cls(target_os,target_arch,entry,sha256(payload),len(payload))
