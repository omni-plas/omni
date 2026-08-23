"""Construct deterministic build manifests from native module metadata."""
from __future__ import annotations
from .native_build_manifest import NativeBuildManifest

def manifest_for_functions(functions, target_os='linux', target_arch='x86_64', entry=None):
    names=tuple(fn.name for fn in functions)
    if not names:
        raise ValueError('no functions')
    chosen=entry or names[0]
    if chosen not in names:
        raise KeyError(chosen)
    return NativeBuildManifest(target_os,target_arch,chosen,names,names)
