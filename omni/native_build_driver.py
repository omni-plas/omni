"""Orchestrate target validation, native compilation, identity and verification."""
from __future__ import annotations
from dataclasses import dataclass
from .native_build_gate import preflight
from .native_build_identity import BuildIdentity
from .native_artifact_verify import verify_artifact
from .native_target import NativeTarget

@dataclass(frozen=True)
class NativeBuildResult:
    artifact: bytes
    identity: BuildIdentity
    target: NativeTarget
    manifest: dict

def build_artifact(build_fn, target:NativeTarget, manifest:dict)->NativeBuildResult:
    preflight(target, manifest)
    artifact=bytes(build_fn())
    entry=manifest['entry']
    symbols=dict(manifest.get('symbols',{}))
    entry_offset=int(manifest.get('entry_offset',symbols.get(entry,0)))
    verify_artifact(artifact,entry_offset,symbols,entry)
    identity=BuildIdentity.create(target.triple(),manifest,artifact)
    return NativeBuildResult(artifact,identity,target,dict(manifest))
