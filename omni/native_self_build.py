"""Self-build planning primitives.

The bootstrap implementation may execute with the current host toolchain, while
its target is Omni-native compilation of the compiler itself.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SelfBuildTarget:
    compiler_source: str
    target_os: str
    target_arch: str
    bootstrap: bool = True

def self_build_target(source='compiler.omni', target_os='linux', target_arch='x86_64'):
    if not source: raise ValueError('compiler source is required')
    return SelfBuildTarget(source,target_os,target_arch,True)
